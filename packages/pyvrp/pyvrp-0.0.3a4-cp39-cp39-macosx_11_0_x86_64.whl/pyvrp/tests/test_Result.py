from numpy.testing import (
    assert_,
    assert_almost_equal,
    assert_equal,
    assert_raises,
)
from pytest import mark

from pyvrp import Individual, PenaltyManager, Population, XorShift128
from pyvrp.Result import Result
from pyvrp.Statistics import Statistics
from pyvrp.diversity import broken_pairs_distance
from pyvrp.tests.helpers import read


@mark.parametrize(
    "routes, num_iterations, runtime",
    [([[1, 2], [3], [4]], 1, 1.5), ([[1, 2, 3, 4]], 100, 54.2)],
)
def test_fields_are_correctly_set(routes, num_iterations, runtime):
    data = read("data/OkSmall.txt")
    pm = PenaltyManager(data.vehicle_capacity)
    indiv = Individual(data, pm, routes)

    res = Result(indiv, Statistics(), num_iterations, runtime)

    assert_equal(res.is_feasible(), indiv.is_feasible())
    assert_equal(res.num_iterations, num_iterations)
    assert_almost_equal(res.cost(), indiv.cost())
    assert_almost_equal(res.runtime, runtime)


@mark.parametrize(
    "num_iterations, runtime",
    [
        (-1, 0.0),  # num_iterations < 0
        (0, -1.0),  # runtime < 0
    ],
)
def test_init_raises_invalid_arguments(num_iterations, runtime):
    data = read("data/OkSmall.txt")
    pm = PenaltyManager(data.vehicle_capacity)
    indiv = Individual(data, pm, [[1, 2, 3, 4], [], []])

    with assert_raises(ValueError):
        Result(indiv, Statistics(), num_iterations, runtime)


@mark.parametrize(
    "num_iterations, has_statistics", [(0, False), (1, True), (10, True)]
)
def test_has_statistics(num_iterations: int, has_statistics: bool):
    data = read("data/OkSmall.txt")
    pm = PenaltyManager(data.vehicle_capacity)
    rng = XorShift128(seed=42)
    pop = Population(data, pm, rng, broken_pairs_distance)
    stats = Statistics()

    for _ in range(num_iterations):
        stats.collect_from(pop)

    res = Result(Individual(data, pm, rng), stats, num_iterations, 0.0)
    assert_equal(res.has_statistics(), has_statistics)
    assert_equal(res.num_iterations, num_iterations)


def test_str_contains_essential_information():
    data = read("data/OkSmall.txt")
    pm = PenaltyManager(data.vehicle_capacity)
    rng = XorShift128(seed=42)

    for _ in range(5):  # let's do this a few times to really make sure
        individual = Individual(data, pm, rng)
        res = Result(individual, Statistics(), 0, 0.0)
        str_representation = str(res)

        # Test that feasibility status and solution cost are presented.
        assert_(str(individual.cost()) in str_representation)
        assert_(str(individual.is_feasible()) in str_representation)

        # And make sure that all non-empty routes are printed as well.
        for route in individual.get_routes():
            if route:
                assert_(str(route) in str_representation)
