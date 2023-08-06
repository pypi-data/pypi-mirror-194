import logging
import pickle
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, cast

import httpx
from httpx import AsyncClient

from ._cache import getCacheDir
from ._constants import DEVICE_NAME
from ._keystore import KeyStore
from ._unit import Group, Scene, Unit, UnitControl, UnitControlType, UnitType
from .errors import AuthenticationError, NetworkNotFoundError, NetworkUpdateError


@dataclass()
class _NetworkSession:
    session: str
    network: str
    manager: bool
    keyID: int
    expires: datetime

    role: int = 3  # TODO: Support other role types?

    def expired(self) -> bool:
        return datetime.utcnow() > self.expires


class Network:
    _session: Optional[_NetworkSession] = None

    _networkName: Optional[str] = None
    _networkRevision: Optional[int] = None

    _unitTypes: dict[int, UnitType] = {}
    units: list[Unit] = []
    groups: list[Group] = []
    scenes: list[Scene] = []

    def __init__(self, uuid: str, httpClient: AsyncClient) -> None:
        self._logger = logging.getLogger(__name__)

        self._uuid = uuid
        self._httpClient = httpClient

        self._cachePath = getCacheDir(uuid)
        self._keystore = KeyStore(self._cachePath)

        self._sessionPath = self._cachePath / "session.pck"
        if self._sessionPath.exists():
            self._loadSession()

        self._typeCachePath = self._cachePath / "types.pck"
        if self._typeCachePath.exists():
            self._loadTypeCache()

    def _loadSession(self) -> None:
        self._logger.info("Loading session...")
        self._session = pickle.load(self._sessionPath.open("rb"))

    def _saveSesion(self) -> None:
        self._logger.info("Saving session...")
        pickle.dump(self._session, self._sessionPath.open("wb"))

    def _loadTypeCache(self) -> None:
        self._logger.info("Loading unit type cache...")
        self._unitTypes = pickle.load(self._typeCachePath.open("rb"))

    def _saveTypeCache(self) -> None:
        self._logger.info("Saving type cache...")
        pickle.dump(self._unitTypes, self._typeCachePath.open("wb"))

    async def getNetworkId(self) -> None:
        _logger = logging.getLogger(__name__)
        _logger.info(f"Getting network id...")

        # TODO: Use cache

        getNetworkIdUrl = f"https://api.casambi.com/network/uuid/{self._uuid}"
        res = await self._httpClient.get(getNetworkIdUrl)

        if res.status_code == httpx.codes.NOT_FOUND:
            raise NetworkNotFoundError(
                "API failed to find network. Is your network configured correctly?"
            )
        if res.status_code != httpx.codes.OK:
            raise NetworkNotFoundError(
                f"Getting network id returned unexpected status {res.status_code}"
            )

        self._id = cast(str, res.json()["id"])
        _logger.info(f"Got network id {self._id}.")

    def authenticated(self) -> bool:
        if not self._session:
            return False
        return not self._session.expired()

    def getKeyStore(self) -> KeyStore:
        return self._keystore

    async def logIn(self, password: str) -> None:
        await self.getNetworkId()

        if self.authenticated():
            return

        self._logger.info(f"Logging in to network...")
        getSessionUrl = f"https://api.casambi.com/network/{self._id}/session"

        res = await self._httpClient.post(
            getSessionUrl, json={"password": password, "deviceName": DEVICE_NAME}
        )
        if res.status_code == httpx.codes.OK:
            # Parse session
            sessionJson = res.json()
            sessionJson["expires"] = datetime.utcfromtimestamp(
                sessionJson["expires"] / 1000
            )
            self._session = _NetworkSession(**sessionJson)
            self._logger.info("Login sucessful.")
            self._saveSesion()
        else:
            raise AuthenticationError(f"Login failed: {res.status_code}\n{res.text}")

    async def update(self) -> None:
        self._logger.info(f"Updating network...")
        if not self.authenticated():
            raise AuthenticationError("Not authenticated!")

        # TODO: Save and send revision to receive actual updates?

        getNetworkUrl = f"https://api.casambi.com/network/{self._id}/"

        # **SECURITY**: Do not set session header for client! This could leak the session with external clients.
        res = await self._httpClient.put(
            getNetworkUrl,
            json={"formatVersion": 1, "deviceName": DEVICE_NAME},
            headers={"X-Casambi-Session": self._session.session},  # type: ignore[union-attr]
        )

        if res.status_code != httpx.codes.OK:
            self._logger.error(f"Update failed: {res.status_code}\n{res.text}")
            raise NetworkUpdateError("Could not update network!")

        self._logger.debug(f"Network: {res.text}")

        resJson = res.json()

        # Prase general information
        self._networkName = resJson["network"]["name"]
        self._networkRevision = resJson["network"]["revision"]

        # Parse keys if there are any. Otherwise the network is probably set up for keyless auth.
        if "keyStore" in resJson["network"]:
            keys = resJson["network"]["keyStore"]["keys"]
            for k in keys:
                self._keystore.addKey(k)

        # Parse units
        self.units = []
        units = resJson["network"]["units"]
        for u in units:
            uType = await self._fetchUnitInfo(u["type"])
            uObj = Unit(
                u["type"],
                u["deviceID"],
                u["uuid"],
                u["address"],
                u["name"],
                str(u["firmware"]),
                uType,
            )
            self.units.append(uObj)

        # Parse cells
        self.groups = []
        cells = resJson["network"]["grid"]["cells"]
        for c in cells:
            # Only one type at top level is currently supported
            if c["type"] != 2:
                continue

            # Parse group members
            group_units = []
            # We assume no nested groups here
            for subC in c["cells"]:
                # Ignore everyting that isn't a unit
                if subC["type"] != 1:
                    continue

                unitMatch = list(
                    filter(lambda u: u.deviceId == subC["unit"], self.units)
                )
                if len(unitMatch) != 1:
                    self._logger.warning(
                        f"Incositent unit reference to {subC['unit']} in group {c['groupID']}. Got {len(unitMatch)} matches."
                    )
                    continue
                group_units.append(unitMatch[0])

            gObj = Group(c["groupID"], c["name"], group_units)
            self.groups.append(gObj)

        # Parse scenes
        self.scenes = []
        scenes = resJson["network"]["scenes"]
        for s in scenes:
            sObj = Scene(s["sceneID"], s["name"])
            self.scenes.append(sObj)

        # TODO: Parse more stuff

        self._saveTypeCache()

        self._logger.info("Network updated.")

    async def _fetchUnitInfo(self, id: int) -> UnitType:
        self._logger.info(f"Fetching unit type for id {id}...")

        # Check whether unit type is already cached
        cachedType = self._unitTypes.get(id)
        if cachedType:
            self._logger.info("Using cached type.")
            return cachedType

        getUnitInfoUrl = f"https://api.casambi.com/fixture/{id}"
        async with AsyncClient() as request:
            res = await request.get(getUnitInfoUrl)

        if res.status_code != httpx.codes.OK:
            self._logger.error(f"Getting unit info returned {res.status_code}")

        unitTypeJson = res.json()

        # Parse UnitControls
        controls = []
        for controlJson in unitTypeJson["controls"]:
            typeStr = controlJson["type"].upper()
            try:
                type = UnitControlType[typeStr]
            except KeyError:
                self._logger.warning(
                    f"Unsupported control mode {typeStr} in fixture {id}."
                )
                type = UnitControlType.UNKOWN

            controlObj = UnitControl(
                type,
                controlJson["offset"],
                controlJson["length"],
                controlJson["default"],
                controlJson["readonly"],
                controlJson["min"] if "min" in controlJson else None,
                controlJson["max"] if "max" in controlJson else None,
            )

            controls.append(controlObj)

        # Parse UnitType
        unitTypeObj = UnitType(
            unitTypeJson["id"],
            unitTypeJson["model"],
            unitTypeJson["vendor"],
            unitTypeJson["mode"],
            unitTypeJson["stateLength"],
            controls,
        )

        # Chache unit type
        self._unitTypes[unitTypeObj.id] = unitTypeObj

        self._logger.info("Sucessfully fetched unit type.")
        return unitTypeObj

    async def disconnect(self) -> None:
        return None
