from dataclasses import dataclass


@dataclass
class State:
    name: str

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class Event:
    name: str

    def __hash__(self) -> int:
        return hash(self.name)
