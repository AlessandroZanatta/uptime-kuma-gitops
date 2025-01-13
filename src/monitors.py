import socketio
from data import UptimeMonitor, UptimeNotification
from config import get_config
from logger import log


def sync_monitors(
    sio: socketio.SimpleClient,
    monitors: list[UptimeMonitor],
    notifications: list[UptimeNotification],
):
    config = get_config()

    for monitor in config.monitors:
        m = next((x for x in monitors if x.name == monitor.name), None)

        log.info("Setting up monitor %s", monitor.name)

        notifiers = [
            n for n in notifications if any(n.name == x for x in monitor.notifications)
        ]

        monitor_data = monitor.model_dump()
        if m is not None:
            monitor_data["id"] = m.id
        monitor_data["notificationIDList"] = {n.id: True for n in notifiers}
        monitor_data["proxyId"] = None  # Currently not supported
        r = sio.call("editMonitor" if m is not None else "add", data=monitor_data)
        if not r["ok"]:
            log.error("Error while syncing monitor %s: %s", monitor.name, r["msg"])
            continue
