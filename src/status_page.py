import socketio

from config import get_config
from data import UptimeMonitor, UptimeStatusPage
from logger import log


def sync_status_pages(
    sio: socketio.SimpleClient,
    monitors: list[UptimeMonitor],
    status_pages: list[UptimeStatusPage],
):
    config = get_config()

    for status_page in config.status_pages:
        sp = next((x for x in status_pages if x.title == status_page.title), None)

        log.info("Syncing status page %s", status_page.title)

        if sp is None:
            r = sio.call("addStatusPage", data=(status_page.title, status_page.slug))
            if not r["ok"]:
                log.error(
                    "Skipping syncing of status page '%s' due to errors: '%s'",
                    status_page.title,
                    r["msg"],
                )
                continue
            log.info("Created status page %s", status_page.title)

            r = sio.call("getStatusPage", data=status_page.slug)
            if not r["ok"]:
                log.error(
                    "Could not retrieve data for status page '%s', skipping",
                    status_page.title,
                )
            sp = UptimeStatusPage.model_validate(r["config"])

        groups = []
        for group in status_page.groups:
            group_monitors = []
            for monitor in group.monitors:
                m = next((x for x in monitors if x.name == monitor), None)
                if m is None:
                    log.error(
                        "Skipping missing monitor '%s' in status page '%s'",
                        monitor,
                        status_page.title,
                    )
                    continue
                group_monitors.append(m.model_dump())
            groups.append({"name": group.name, "monitorList": group_monitors})

        r = sio.call(
            "saveStatusPage",
            data=(status_page.slug, sp.model_dump(), "/icon.svg", groups),
        )
        if not r["ok"]:
            log.error(
                "Error while syncing status page '%s': %s", status_page.title, r["msg"]
            )
            continue
        log.info("Status page '%s' synced!", status_page.title)
