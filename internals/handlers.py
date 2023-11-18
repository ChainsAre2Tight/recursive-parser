from dataclasses import dataclass
from datetime import datetime


@dataclass
class _Event:
    timestamp: str
    name: str
    description: str

    def __str__(self):
        return f'> {self.timestamp} {self.name}: {self.description}'


@dataclass
class _EventHandler:
    printout: bool  # Whether to print events or not
    events: list[_Event]  # list of all events

    def __init__(self, printout: bool = True):
        self.printout = printout
        self.events = list()

    def _add_event(self, event_name: str, description: str):
        timestamp = datetime.time(datetime.now())
        event = _Event(name=event_name, description=description, timestamp=timestamp)
        self.events.append(event)

        if self.printout:
            print(event)

    def new_status(self, description: str):
        self._add_event("> Status", description=description)

    def new_event(self, description: str):
        self._add_event("> Event", description=description)

    def new_error(self, description: str):
        self._add_event("!!! Error", description=description)

    def new_info(self, description: str):
        self._add_event("> Info", description=description)


eventhandler = _EventHandler(printout=True)
