#!/usr/bin/env python3

from config import get_config
from data import get_lists
from logger import log
from monitors import sync_monitors
from notifications import sync_notifications
from setup import is_setup_needed, setup
from status_page import sync_status_pages
from util import get_logged_socket


def main():
    config = get_config()
    log.debug("Parsed configuration: %s", config.model_dump_json())

    if is_setup_needed():
        log.info("Setup required")
        setup()
    else:
        log.info("Setup already run, skipping")

    sio = get_logged_socket()
    lists = get_lists(sio)
    sync_notifications(sio, lists.notifications)

    # Refresh lists, notifications may have changed
    sio = get_logged_socket()
    lists = get_lists(sio)
    sync_monitors(sio, lists.monitors, lists.notifications)

    # Refresh lists one more time!
    sio = get_logged_socket()
    lists = get_lists(sio)
    sync_status_pages(sio, lists.monitors, lists.status_pages)


if __name__ == "__main__":
    main()
