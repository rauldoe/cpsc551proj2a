from enum import Enum

class Constants(Enum):
    MessageEntity = 'entity',
    MessageEvent = 'event',
    MessageData = 'data',

    EventStart = 'start',
    EventWrite = 'write',
    EventTake = 'take',
    EventRead = 'read',

    ServerMessage = 'message',
    ServerInstance = 'instance',

    NotifyNList = 'notificationlist',
    NotifyMList = 'messagelist'