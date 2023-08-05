from enum import Enum


class PulsarConfigKeys(str, Enum):
    HOST = 'host'
    PORT = 'port'
    PERSISTENT = 'persistent'
    TENANT = 'tenant'
    NAMESPACE = 'namespace'
    TOPIC = 'topic'


class PropertyKeys(str, Enum):
    REQUEST_CONTEXT = "requestContext"
    RESPONSE_TOPIC = "response_topic"
    REQUEST_MESSAGEID = "requestMessageId"
    MESSAGE_TYPE = "messageType"
    MODULE_TYPE = "module"


class MessageType(str, Enum):
    PING = 'ping'
    PONG = 'pong'
    REQUEST = 'request'
    RESPONSE = 'response'
    LOG = 'log'
    INFO = 'info'
    PROGRESS = 'progress'
