import random
from abc import ABC, abstractmethod
from typing import Union


class RoadGenerator(ABC):
    """
    Generates new roads
    """

    @abstractmethod
    def generate(self, *args, **kwargs) -> Union[str, None]:
        """
        Generates a new road and returns it as string representation. Example road is `1.0,1.0,1.0@2.0,2.0,2.0@3.0,3.0,2.0`.

        kwargs needs to contain the initial staring pos as arg `starting_pos`
        """
        pass
