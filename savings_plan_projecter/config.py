from dataclasses import dataclass
from typing import Any

import yaml


@dataclass
class Config:
    content: dict[str, Any]

    def get_distribution_parameters(self, ticket: str, period: str) -> list[float]:
        return self.content[ticket][period]["distribution"]["parameters"]


def load_config() -> Config:
    with open(r"config.yml") as file:
        return Config(yaml.full_load(file))
