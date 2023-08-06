from typing import List

from pyvrp._Individual import Individual
from pyvrp._PenaltyManager import PenaltyManager
from pyvrp._ProblemData import ProblemData
from pyvrp._XorShift128 import XorShift128

Neighbours = List[List[int]]

class LocalSearch:
    def __init__(
        self,
        data: ProblemData,
        penalty_manager: PenaltyManager,
        rng: XorShift128,
        neighbours: Neighbours,
    ) -> None: ...
    def add_node_operator(self, op) -> None: ...
    def add_route_operator(self, op) -> None: ...
    def set_neighbours(self, neighbours: Neighbours) -> None: ...
    def get_neighbours(self) -> Neighbours: ...
    def intensify(
        self, individual: Individual, overlap_tolerance_degrees: int = 0
    ) -> Individual: ...
    def search(self, individual: Individual) -> Individual: ...
