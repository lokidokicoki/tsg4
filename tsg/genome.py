"""
Genome and Genes
"""
import random
from enum import Enum
from typing import List, Optional

SENSOR = 1
NEURON = 0
ACTION = 1


class GeneType(Enum):
    SPEED = 1
    HUNGER = 2
    SPAWN = 3
    SPIN = 4


class Gene:
    """
    Defines neural network connections and weighting
    """

    def __init__(
        self,
        gene_type: GeneType,
        source_type: int = 0,
        source_id: int = 0,
        sink_type: int = 0,
        sink_id: int = 0,
        weight: int = 0xFFFF,
    ):
        self.gene_type = gene_type
        self.source_type = source_type
        self.source_id = source_id
        self.sink_type = sink_type
        self.sink_id = sink_id
        self.weight = weight

    def get_weight_as_float(self) -> float:
        return self.weight / 8192.0

    @staticmethod
    def get_random_weight() -> int:
        return random.randint(0, 0xFFFF) - 0x8000


class Genome:
    """
    A collection of Gene instances
    """

    def __init__(self, genes: Optional[List[Gene]] = None):
        self.genes: List[Gene] = []
        if genes:
            self.genes = genes
        else:
            self.stock_genome()

    def stock_genome(self):
        """
        Default genome - good for testing
        """
        self.genes.append(Gene(GeneType.SPEED))
        self.genes.append(Gene(GeneType.HUNGER))
        self.genes.append(Gene(GeneType.SPAWN))
        self.genes.append(Gene(GeneType.SPIN))

    def get_gene_by_type(self, gene_type: GeneType) -> Optional[Gene]:
        return next((x for x in self.genes if x.gene_type == gene_type), None)


class NeuralNetwork:
    def __init__(self):
        print("new nnet")
