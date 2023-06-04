import random
from abc import ABC, abstractmethod
from typing import Iterable

import numpy as np
import scipy.stats as st


class PercentageChangeDistribution(ABC):
    """Probability distribution with the ability to generate random values."""

    @abstractmethod
    def rvs(self, n_observations: int) -> np.ndarray:
        ...


class DistributionFromObservations(PercentageChangeDistribution):
    """Probability distribution that uses a set of values as possible outcomes."""

    def __init__(self, values: Iterable) -> None:
        self.values = values

    def rvs(self, n_observations: int) -> np.ndarray:
        return np.random.choice(self.values, n_observations)


class NctDistribution(PercentageChangeDistribution):
    def __init__(self, *nct_params) -> None:
        self.nct = st.nct(*nct_params)

    def rvs(self, n_observations: int) -> np.ndarray:
        return self.nct.rvs(n_observations)


def simulate_share_price(
    starting_value: float,
    distribution: PercentageChangeDistribution,
    n_observations: int,
    min_val: float = -0.25,
    max_val: float = 0.25,
) -> list[float]:
    """Apply n - 1 variations to a stock price to simulate its value over n periods.

    It is assumed that distribution returns variations expressed as base 100,
    so that 50% variation is 50.
    """
    variations_sequence = distribution.rvs(n_observations - 1) / 100
    output = [starting_value]
    for index, variation in enumerate(variations_sequence):
        variation = min(max(variation, min_val), max_val)
        new_value = output[index] * (1 + variation)
        output.append(new_value)
    return output


def infer_nct_parameters(data: Iterable) -> list[float]:
    return list(st.nct.fit(data))


def get_best_distribution(data):
    dist_names = [
        "norm",
        "exponweib",
        "weibull_max",
        "weibull_min",
        "pareto",
        "genextreme",
        "nct",
    ]
    dist_results = []
    params = {}
    for dist_name in dist_names:
        dist = getattr(st, dist_name)
        param = dist.fit(data)

        params[dist_name] = param
        # Applying the Kolmogorov-Smirnov test
        _, p = st.kstest(data, dist_name, args=param)
        print(f"p value for {dist_name} = {p:.3f}")
        dist_results.append((dist_name, p))

    # select the best fitted distribution
    best_dist, best_p = max(dist_results, key=lambda item: item[1])
    # store the name of the best fit and its p value

    print("Best fitting distribution: " + str(best_dist))
    print("Best p value: " + str(best_p))
    print("Parameters for the best fit: " + str(params[best_dist]))

    return best_dist, best_p, list(params[best_dist])


class CrisisCounter:
    MIN_DAYS_CRISIS_STARTS = 120
    MIN_DAYS_IN_CRISIS = 180
    MAX_DAYS_IN_CRISIS = 540
    DAILY_PROBABILITY_CRISIS_STARTS = 0.01
    DAILY_PROBABILITY_CRISIS_ENDS = 0.01

    def __init__(self) -> None:
        self.in_crisis = False
        self.days_in_crisis = 0

    def update(self, day_index: int) -> None:
        if self.in_crisis:
            if self.crisis_is_over():
                self.in_crisis = False
                return
            self.days_in_crisis += 1
            return

        # if crisis already over then no new crisis can start
        if self.days_in_crisis > 0:
            return
        if self.crisis_starts(day_index):
            self.in_crisis = True

    def crisis_is_over(self):
        if self.days_in_crisis < self.MIN_DAYS_IN_CRISIS:
            return False
        return (random.random() <= self.DAILY_PROBABILITY_CRISIS_ENDS) or (
            self.days_in_crisis >= self.MAX_DAYS_IN_CRISIS
        )

    def crisis_starts(self, day_index):
        return (day_index >= self.MIN_DAYS_CRISIS_STARTS) and (
            random.random() <= self.DAILY_PROBABILITY_CRISIS_STARTS
        )
