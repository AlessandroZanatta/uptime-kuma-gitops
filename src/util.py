import time

import socketio

from config import get_config
from logger import log


def get_socketio_connection(tries: int = 5, sleep_time: int = 5):
    config = get_config()

    attempts = 0
    sio = socketio.SimpleClient()
    while attempts < tries:
        try:
            print(attempts)
            sio.connect(config.server.url)
            return sio
        except Exception as e:
            log.debug(e)
            attempts += 1
            time.sleep(sleep_time)
    else:
        raise ConnectionError("Could not connect to socket!")


def get_logged_socket():
    config = get_config()

    sio = get_socketio_connection()
    sio.call(
        "login",
        data={
            "username": config.auth.username,
            "password": config.auth.password,
            "token": False,
        },
    )
    return sio
