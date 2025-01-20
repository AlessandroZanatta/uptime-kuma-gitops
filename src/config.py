import os
from enum import StrEnum
from functools import lru_cache
from pathlib import Path
from typing import Annotated, Any

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from logger import log


class Server(BaseSettings):
    url: str = "http://localhost:3001"


class DatabaseType(StrEnum):
    SQLITE = "sqlite"
    MARIADB = "mariadb"


class Setup(BaseSettings):
    type: DatabaseType = DatabaseType.SQLITE
    port: int = 3306
    hostname: str = "mariadb"
    username: str = "mariadb"
    password: str = "mariadb"
    dbName: str = "mariadb"


class Auth(BaseSettings):
    username: str
    password: str


class Notification(BaseSettings):
    name: str
    type: str
    isDefault: bool = False
    applyExisting: bool = False

    model_config = SettingsConfigDict(extra="allow")


class Monitor(BaseSettings):
    notifications: Annotated[list[str], Field(exclude=True)] = []
    proxy: Annotated[str | None, Field(exclude=True)] = None  # Currently not supported

    type: str
    name: str
    parent: str | None = None
    url: str = "https://"
    method: str = "GET"
    interval: int = 60
    resendInterval: int = 0
    maxretries: int = 0
    ignoreTls: bool = False
    upsideDown: bool = False
    packetSize: int = 56
    expiryNotification: bool = False
    maxredirects: int = 10
    accepted_statuscodes: list[str] = ["200-299"]
    dns_resolve_type: str = "A"
    dns_resolve_server: str = "1.1.1.1"
    docker_container: str = ""
    docker_host: Any | None = None
    mqttUsername: str = ""
    mqttPassword: str = ""
    mqttTopic: str = ""
    mqttSuccessMessage: str = ""
    mqttCheckType: str = "keyword"
    authMethod: Any | None = None
    oauth_auth_method: str = "client_secret_basic"
    httpBodyEncoding: str = "json"
    kafkaProducerBrokers: list[Any] = []
    kafkaProducerSaslOptions: dict[str, str] = {}
    cacheBust: bool = False
    kafkaProducerSsl: bool = False
    kafkaProducerAllowAutoTopicCreation: bool = False
    gamedigGivenPortOnly: bool = True
    remote_browser: Any | None = None
    rabbitmqNodes: list[Any] = []
    rabbitmqUsername: str = ""
    rabbitmqPassword: str = ""
    conditions: list[Any] = []
    timeout: int = 48
    snmpVersion: str = "2c"
    jsonPathOperator: str = "=="

    model_config = SettingsConfigDict(extra="allow")


class Group(BaseSettings):
    name: str
    monitors: list[str] = Field(exclude=True)


class StatusPage(BaseSettings):
    title: str
    slug: str
    description: str = ""
    groups: list[Group]


# ["add",{"type":"http","name":"asdf","parent":null,"url":"https://aaa","method":"GET","interval":60,"retryInterval":60,"resendInterval":0,"maxretries":0,"notificationIDList":{"1":true},"ignoreTls":false,"upsideDown":false,"packetSize":56,"expiryNotification":false,"maxredirects":10,"accepted_statuscodes":["200-299"],"dns_resolve_type":"A","dns_resolve_server":"1.1.1.1","docker_container":"","docker_host":null,"proxyId":null,"mqttUsername":"","mqttPassword":"","mqttTopic":"","mqttSuccessMessage":"","mqttCheckType":"keyword","authMethod":null,"oauth_auth_method":"client_secret_basic","httpBodyEncoding":"json","kafkaProducerBrokers":[],"kafkaProducerSaslOptions":{"mechanism":"None"},"cacheBust":false,"kafkaProducerSsl":false,"kafkaProducerAllowAutoTopicCreation":false,"gamedigGivenPortOnly":true,"remote_browser":null,"rabbitmqNodes":[],"rabbitmqUsername":"","rabbitmqPassword":"","conditions":[],"timeout":48,"snmpVersion":"2c","jsonPath":"$","jsonPathOperator":"=="}]
class Config(BaseSettings):
    server: Server = Server()
    setup: Setup = Setup()
    auth: Auth
    notifications: list[Notification] = []
    monitors: list[Monitor] = []
    status_pages: list[StatusPage] = []

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
    )


@lru_cache
def get_config():
    config_path = Path(os.getenv("CONFIG_PATH", "/config.yaml"))
    log.info("Loading configuration from %s", config_path)

    config_yaml = yaml.safe_load(config_path.read_text())

    return Config(**config_yaml)
