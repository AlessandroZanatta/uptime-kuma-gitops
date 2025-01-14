from typing import Any

import socketio
from pydantic import BaseModel, ConfigDict, TypeAdapter


class MonitorList(BaseModel):
    pass


class UptimeNotification(BaseModel):
    id: int
    name: str
    active: bool
    userId: int
    isDefault: bool
    config: str


UptimeNotificationList = TypeAdapter(list[UptimeNotification])


class UptimeMonitor(BaseModel):
    id: int
    name: str
    type: str

    model_config = ConfigDict(extra="allow")


class UptimeStatusPage(BaseModel):
    id: int
    slug: str
    title: str
    description: str | None
    icon: str
    theme: str
    autoRefreshInterval: int
    published: bool
    showTags: bool
    domainNameList: list[Any]
    customCSS: str | None
    footerText: str | None
    showPoweredBy: bool
    googleAnalyticsId: str | None
    showCertificateExpiry: bool


class UptimeData(BaseModel):
    monitors: list[UptimeMonitor] = []
    notifications: list[UptimeNotification] = []
    status_pages: list[UptimeStatusPage] = []


def get_lists(sio: socketio.SimpleClient):
    data = UptimeData()

    while True:
        try:
            msg = sio.receive(timeout=1)

        except socketio.exceptions.TimeoutError:
            break
        match msg[0]:
            case "monitorList":
                data.monitors = [
                    UptimeMonitor.model_validate(m) for m in msg[1].values()
                ]
            case "notificationList":
                data.notifications = [
                    UptimeNotification.model_validate(n)
                    for n in msg[1]
                    if isinstance(n, dict)
                ]
            case "statusPageList":
                data.status_pages = [
                    UptimeStatusPage.model_validate(sp) for sp in msg[1].values()
                ]
    return data
