from numpy.testing import assert_, assert_equal

from pyvrp import PenaltyManager, Population, Statistics, XorShift128
from pyvrp.diversity import broken_pairs_distance
from pyvrp.tests.helpers import read


def test_csv_serialises_correctly(tmp_path):
    data = read("data/OkSmall.txt")
    pm = PenaltyManager(data.vehicle_capacity)
    rng = XorShift128(seed=42)
    pop = Population(data, pm, rng, broken_pairs_distance)

    collected_stats = Statistics()

    for _ in range(10):  # populate the statistics object
        collected_stats.collect_from(pop)

    csv_path = tmp_path / "test.csv"
    assert_(not csv_path.exists())

    # Write the collected statistcs to the CSV file location, and check that
    # the file now does exist.
    collected_stats.to_csv(csv_path)
    assert_(csv_path.exists())

    # Now read them back in, and check that the newly read object is the same
    # as the previously written object.
    read_stats = Statistics.from_csv(csv_path)
    assert_equal(collected_stats, read_stats)
