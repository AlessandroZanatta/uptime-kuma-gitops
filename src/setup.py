import httpx
from pydantic import BaseModel

from config import get_config
from logger import log
from util import get_socketio_connection


class SetupDatabaseInfo(BaseModel):
    runningSetup: bool
    needSetup: bool


class SetupDatabase(BaseModel):
    ok: bool


def is_setup_needed():
    config = get_config()
    r = httpx.get(
        f"{config.server.url}/setup-database-info",
    )
    r.raise_for_status()
    info = SetupDatabaseInfo.model_validate(r.json())
    return info.needSetup


def setup():
    log.info("Setting up database")
    config = get_config()
    r = httpx.post(
        f"{config.server.url}/setup-database",
        json={"dbConfig": config.setup.model_dump()},
    )
    r.raise_for_status()

    log.info("Setting up admin user")
    sio = get_socketio_connection()
    sio.call("setup", data=(config.auth.username, config.auth.password))
    sio.disconnect()

    log.info("Setup done!")
