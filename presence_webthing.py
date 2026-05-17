import tornado.ioloop
from webthing import (Property, Thing, Value)
from presence import Presence
from redzoo.math.display import duration


class PresenceThing(Thing):

    # regarding capabilities refer https://iot.mozilla.org/schemas
    # there is also another schema registry http://iotschema.org/docs/full.html not used by webthing

    def __init__(self, description: str, presence: Presence):
        Thing.__init__(
            self,
            'urn:dev:ops:presence-1',
            'presence_' + presence.name,
            ['MultiLevelSensor'],
            description
        )
        self.ioloop = tornado.ioloop.IOLoop.current()
        self.presence = presence
        self.presence.add_listener(self.on_value_changed)

        self.name = Value(presence.name)
        self.add_property(
            Property(self,
                     'name',
                     self.name,
                     metadata={
                         'title': 'name',
                         "type": "string",
                         'description': 'the device name',
                         'readOnly': True,
                     }))

        self.addr = Value(presence.addr)
        self.add_property(
            Property(self,
                     'addr',
                     self.addr,
                     metadata={
                         'title': 'addr',
                         "type": "string",
                         'description': 'the device address',
                         'readOnly': True,
                     }))

        self.is_presence = Value(presence.is_presence)
        self.add_property(
            Property(self,
                     'is_presence',
                     self.is_presence,
                     metadata={
                         'title': 'is_presence',
                         "type": "boolean",
                         'description': 'true, if presence',
                         'readOnly': True,
                     }))

        self.last_time_presence = Value(presence.last_time_presence.strftime("%Y-%m-%dT%H:%M"))
        self.add_property(
            Property(self,
                     'last_time_presence_utc',
                     self.last_time_presence,
                     metadata={
                         'title': 'last_time_presence_utc',
                         "type": "string",
                         'description': 'the last time presence ISO8601 string (UTC)',
                         'readOnly': True,
                     }))

        self.elapsed_since_last_seen = Value(duration(presence.age_sec, 1))
        self.add_property(
            Property(self,
                     'elapsed_since_last_seen',
                     self.elapsed_since_last_seen,
                     metadata={
                         'title': 'elapsed_since_last_seen',
                         "type": "string",
                         'description': 'elapsed time since last seen',
                         'readOnly': True,
                     }))


    def on_value_changed(self, name: str):
        self.ioloop.add_callback(self._on_value_changed)

    def _on_value_changed(self):
        self.last_time_presence.notify_of_external_update(self.presence.last_time_presence.strftime("%Y-%m-%dT%H:%M"))
        self.elapsed_since_last_seen.notify_of_external_update(duration(self.presence.age_sec, 1))
        self.is_presence.notify_of_external_update(self.presence.is_presence)

