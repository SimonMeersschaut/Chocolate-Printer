from dataclasses import dataclass

# Base Event class (optional, but good for type hinting)
@dataclass(frozen=True) # frozen=True makes them immutable and hashable
class Event:
    pass

@dataclass(frozen=True)
class UpdateNozzleTemperature(Event):
    temperature: int # This makes 'temperature' an attribute of the event

@dataclass(frozen=True)
class UpdateTargetTemperature(Event):
    temperature: int
