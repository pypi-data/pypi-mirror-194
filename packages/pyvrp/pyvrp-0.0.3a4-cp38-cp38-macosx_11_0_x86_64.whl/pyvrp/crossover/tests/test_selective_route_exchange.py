from numpy.testing import assert_equal

from pyvrp import Individual, PenaltyManager, XorShift128
from pyvrp.crossover import selective_route_exchange as srex
from pyvrp.tests.helpers import read


def test_srex_move_all_routes():
    """
    Tests if SREX produces an offspring that is identical to the second parent
    when all routes are replaced during crossover.
    """
    data = read("data/OkSmall.txt")
    pm = PenaltyManager(data.vehicle_capacity)

    # This RNG seed sets the internal SREX variable ``nMovedRoutes`` to 3.
    rng = XorShift128(seed=4)

    indiv1 = Individual(data, pm, [[1], [2], [3, 4]])
    indiv2 = Individual(data, pm, [[1, 2], [3], [4]])
    parents = (indiv1, indiv2)

    offspring = srex(parents, data, pm, rng)

    assert_equal(offspring.get_routes(), indiv2.get_routes())


def test_srex_greedy_repair():
    """
    Tests the case where greedy repair is used during SREX crossover.
    """
    data = read("data/OkSmallGreedyRepair.txt")
    pm = PenaltyManager(data.vehicle_capacity)

    # This RNG seed sets the internal SREX variables ``startA = 0`` and
    # ``nMovedRoutes = 1``.
    rng = XorShift128(seed=2)

    indiv1 = Individual(data, pm, [[1, 2], [3, 4], []])
    indiv2 = Individual(data, pm, [[2, 3], [4, 1], []])
    parents = (indiv1, indiv2)

    # The start indices do not change because there are no improving moves.
    # So, indiv1's route [1, 2] will be replaced by indiv2's route [2, 3].
    # This results in two incomplete offspring [[2, 3], [4]] and [[2], [3, 4]],
    # which are both repaired using greedy repair. After repair, we obtain the
    # offspring [[2, 3, 1], [4]] with cost 8735, and [[1, 2], [3, 4]] with
    # cost 9725. The first one is returned since it has the lowest cost.
    offspring = srex(parents, data, pm, rng)

    assert_equal(offspring.get_routes(), [[2, 3, 1], [4], []])


def test_srex_changed_start_indices():
    """
    Tests the case where the initial start indices are changed in SREX.
    """
    data = read("data/OkSmall.txt")
    pm = PenaltyManager(data.vehicle_capacity)

    # This RNG seed sets the internal SREX variables ``startA = 0`` and
    # ``nMovedRoutes = 1``.
    rng = XorShift128(seed=2)

    indiv1 = Individual(data, pm, [[1, 2, 3], [4], []])
    indiv2 = Individual(data, pm, [[1, 2, 4], [3], []])
    parents = (indiv1, indiv2)

    # The start indices at initialization are startA = 0 and startB = 0.
    # The difference for A to move left (= right) is -1. The difference for B
    # to move left (= right) is 1. The new indices become startA = 1 and
    # startB = 0. There are no improving moves in this position since the
    # difference for A to move is 1 and difference for B to move is 1.
    # So, indiv1's route [4] will be replaced by indiv2's route [1, 2, 4].
    # This results in two candidate offspring, [[3], [1, 2, 4]] with cost
    # 10195, and [[1, 2, 3], [4]] with cost 31029. The first candidate is
    # returned since it has the lowest cost.
    offspring = srex(parents, data, pm, rng)

    assert_equal(offspring.get_routes(), [[3], [1, 2, 4], []])


def test_srex_a_left_move():
    """
    Tests the case where the initial start indices are changed by moving the
    A index to the left.
    """
    data = read("data/OkSmall.txt")
    pm = PenaltyManager(data.vehicle_capacity)

    # This RNG seed sets the internal SREX variables ``startA = 0`` and
    # ``nMovedRoutes = 1``.
    rng = XorShift128(seed=17)

    indiv1 = Individual(data, pm, [[1, 3], [2], [4]])
    indiv2 = Individual(data, pm, [[4, 1], [2], [3]])
    parents = (indiv1, indiv2)

    # We describe the A-left case here in detail. The tests below for A-right,
    # B-left and B-right can be worked out similarly: note that we only change
    # the ordering of the routes.
    #
    # Initial start indices (indicated by **)
    # *[1, 3]* [2] [4]
    # *[4, 1]* [2] [3]
    #
    # Differences
    # A-left:   0 - 1 = -1
    # A-right:  1 - 1 =  0
    # B-left:   1 - 1 =  0
    # B-right:  1 - 0 =  1
    #
    # New start indices
    # [1, 3] [2] *[4]*
    # *[4, 1]* [2] [3]
    #
    # Differences
    # A-left:   1 - 0 = 1
    # A-right:  1 - 0 = 1
    # B-left:   1 - 0 = 1
    # B-right:  1 - 0 = 1
    #
    # No more improving moves.
    #
    # Candidate offspring
    # [1, 3] [2] [4] - cost: 24416
    # [3] [2] [4, 1] - cost: 12699 <-- selected as new offspring
    offspring = srex(parents, data, pm, rng)

    assert_equal(offspring.get_routes(), [[3], [2], [4, 1]])


def test_srex_a_right_move():
    """
    Tests the case where the initial start indices are changed by moving to
    A index to the right.
    """
    data = read("data/OkSmall.txt")
    pm = PenaltyManager(data.vehicle_capacity)

    # This RNG seed sets the internal SREX variables ``startA = 0`` and
    # ``nMovedRoutes = 1``.
    rng = XorShift128(seed=17)

    indiv1 = Individual(data, pm, [[1, 3], [4], [2]])
    indiv2 = Individual(data, pm, [[4, 1], [2], [3]])
    parents = (indiv1, indiv2)

    offspring = srex(parents, data, pm, rng)

    assert_equal(offspring.get_routes(), [[3], [4, 1], [2]])


def test_srex_b_left_move():
    """
    Tests the case where the initial start indices are changed by moving the
    B index to the left.
    """
    data = read("data/OkSmall.txt")
    pm = PenaltyManager(data.vehicle_capacity)

    # This RNG seed sets the internal SREX variables ``startA = 0`` and
    # ``nMovedRoutes = 1``.
    rng = XorShift128(seed=17)

    indiv1 = Individual(data, pm, [[4], [2], [1, 3]])
    indiv2 = Individual(data, pm, [[3], [2], [4, 1]])
    parents = (indiv1, indiv2)

    offspring = srex(parents, data, pm, rng)

    assert_equal(offspring.get_routes(), [[4, 1], [2], [3]])


def test_srex_b_right_move():
    """
    Tests the case where the initial start indices are changed by moving the
    B index to the right.
    """
    data = read("data/OkSmall.txt")
    pm = PenaltyManager(data.vehicle_capacity)

    # This RNG seed sets the internal SREX variables ``startA = 0`` and
    # ``nMovedRoutes = 1``.
    rng = XorShift128(seed=17)

    indiv1 = Individual(data, pm, [[4], [2], [1, 3]])
    indiv2 = Individual(data, pm, [[3], [4, 1], [2]])
    parents = (indiv1, indiv2)

    offspring = srex(parents, data, pm, rng)

    assert_equal(offspring.get_routes(), [[4, 1], [2], [3]])
