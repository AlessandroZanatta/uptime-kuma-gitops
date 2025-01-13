import socketio
from data import UptimeNotification
from config import get_config
from logger import log


def sync_notifications(
    sio: socketio.SimpleClient, notifications: list[UptimeNotification]
):
    config = get_config()

    for notification in config.notifications:
        n = next((x for x in notifications if x.name == notification.name), None)
        log.info("Syncing notification: %s", notification.name)
        r = sio.call(
            "addNotification",
            data=(notification.model_dump(), n.id if n is not None else None),
        )
        if not r["ok"]:
            log.error(
                "Error while syncing notification %s: %s", notification.name, r["msg"]
            )
        log.info("Notification synced correctly: %s", notification.name)


# ["addNotification",{"name":"kalexlab","type":"telegram","isDefault":false,"applyExisting":false,"telegramBotToken":"1234","telegramChatID":"2345"}]
# ["addNotification",{"name":"My Telegram Alert (1)","type":"telegram","isDefault":true,"telegramBotToken":"asdf","telegramChatID":"1234","applyExisting":true},null]

# ["notificationList",[{"id":1,"name":"My Telegram Alert (1)","active":true,"userId":1,"isDefault":true,"config":"{\"name\":\"My Telegram Alert (1)\",\"type\":\"telegram\",\"isDefault\":true,\"telegramBotToken\":\"asdf\",\"telegramChatID\":\"1234\",\"applyExisting\":true}"}]]
