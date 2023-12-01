from .Segment import Segment
from abc import ABC, abstractmethod

class Node(ABC):
    @abstractmethod
    def run():
        pass