"""Data design (Phase 1): what a parcel and a road network look like."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Parcel:
    id: int
    dest: int        # graph node where the parcel must be delivered (0 is the depot)
    weight: int      # kg, integer so the knapsack table can be indexed by weight
    priority: int    # 1 (low) .. 5 (express); used as the knapsack "value"
    deadline: int    # hours from now; smaller = more urgent

    @property
    def value(self):
        # Higher priority and tighter deadlines are worth more when space is scarce.
        return self.priority * 10 + max(0, 24 - self.deadline)
