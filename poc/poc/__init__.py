from dataclasses import dataclass
from functools import partial
from typing import Callable, Mapping, Self


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


class StateMachine:
    states: set[State]
    transitions: Mapping[tuple[State, Event], Callable[[], State]]

    current: State

    def __init__(
        self,
        initial: Callable[[], State],
        states: set[State],
        transitions: Mapping[tuple[State, Event], Callable[[], State]],
    ) -> None:
        self.current = initial()
        self.states = states
        self.transitions = transitions

    def __str__(self) -> str:
        return f"StateMachine(states={self.states}, transitions={self.transitions}, current={self.current})"

    def on(self, event: Event) -> Self:
        next = self.transitions.get((self.current, event))
        if next is not None:
            self.current = next()
        return self


On = partial(State, "On")
Off = partial(State, "Off")

Click = partial(Event, "Click")


class StateMachineBuilder:
    states: set[State]
    transitions: dict[tuple[State, Event], Callable[[], State]]
    initial: Callable[[], State]

    def __init__(self) -> None:
        self.states = set()
        self.transitions = {}

    def add_state(self, state: State) -> Self:
        self.states.add(state)
        return self

    def add_transition(
        self, previous: State, on: Event, next: Callable[[], State]
    ) -> Self:
        if previous not in self.states:
            self.add_state(previous)

        self.transitions[(previous, on)] = next
        return self

    def set_initial(self, initial: Callable[[], State]) -> Self:
        self.initial = initial
        return self

    def build(self) -> StateMachine:
        if len(self.states) == 0:
            raise Exception("states cannot be empty")
        return StateMachine(
            initial=self.initial, states=self.states, transitions=self.transitions
        )


def merge(
    initial: Callable[[], State], m1: StateMachine, m2: StateMachine
) -> StateMachine:
    if len(m1.states.intersection(m2.states)) == 0:
        raise Exception()

    m3_builder = StateMachineBuilder()

    for state in m1.states:
        m3_builder.add_state(state)

    for (previous, event), next in m1.transitions.items():
        m3_builder.add_transition(previous, Event("v1." + event.name), next)

    for state in m2.states:
        m3_builder.add_state(state)

    for (previous, event), next in m2.transitions.items():
        m3_builder.add_transition(previous, Event("v2." + event.name), next)

    m3_builder.set_initial(initial)

    return m3_builder.build()


v1_sm = (
    StateMachineBuilder()
    .add_state(On())
    .add_state(Off())
    .add_transition(On(), Click(), Off)
    .add_transition(Off(), Click(), On)
    .set_initial(Off)
    .build()
)

# print(v1_sm.current)

# v1_sm.on(Click())

# print(v1_sm.current)

Half = partial(State, "Half")

v2_sm = (
    StateMachineBuilder()
    .add_state(On())
    .add_state(Off())
    .add_state(Half())
    .add_transition(On(), Click(), Off)
    .add_transition(Off(), Click(), Half)
    .add_transition(Half(), Click(), On)
    .set_initial(Off)
    .build()
)

# print(v2_sm.current)

# v2_sm.on(Click())

# print(v2_sm.current)

v3_sm = merge(Off, v1_sm, v2_sm)

V1Click = partial(Event, "v1.Click")
V2Click = partial(Event, "v2.Click")


print(v3_sm.current)
v3_sm.on(V2Click())
print(v3_sm.current)
v3_sm.on(V2Click())
print(v3_sm.current)
v3_sm.on(V2Click())
print(v3_sm.current)
