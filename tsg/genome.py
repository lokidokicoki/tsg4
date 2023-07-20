"""
Genome and Genes
"""
import random
from enum import Enum
from typing import List, Optional

SENSOR = 1
NEURON = 0
ACTION = 1

MAX_GENE_WEIGHT = 0xFF
WEIGHT_DIVIDER = 0xFF
WEIGHT_SHIFT = 0

# weight shift is more important for neural weights


class GeneType(Enum):
    SPEED = 1
    HUNGER = 2
    SPAWN = 3
    SPIN_RATE = 4
    SPIN_CW = 5
    SPIN_CCW = 6


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
        weight: int = MAX_GENE_WEIGHT,
    ):
        self.gene_type = gene_type
        self.source_type = source_type
        self.source_id = source_id
        self.sink_type = sink_type
        self.sink_id = sink_id
        self.weight = weight

    def get_weight_as_float(self) -> float:
        return self.weight / WEIGHT_DIVIDER

    @staticmethod
    def get_random_weight() -> int:
        return random.randint(0, MAX_GENE_WEIGHT) - WEIGHT_SHIFT

    def __str__(self):
        return f"{self.gene_type}:{self.weight}:{self.get_weight_as_float()}"


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
        self.genes.append(Gene(GeneType.SPIN_RATE))
        self.genes.append(Gene(GeneType.SPIN_CW))
        self.genes.append(Gene(GeneType.SPIN_CCW))

    def get_gene_by_type(self, gene_type: GeneType) -> Optional[Gene]:
        return next((x for x in self.genes if x.gene_type == gene_type), None)

    @staticmethod
    def get_value(a, b):
        return ((a.weight + b.weight) / (2 * MAX_GENE_WEIGHT)) * MAX_GENE_WEIGHT

    def get_genotype(self):
        return (
            int(self.get_value(self.genes[0], self.genes[1])),
            int(self.get_value(self.genes[2], self.genes[3])),
            int(self.get_value(self.genes[4], self.genes[5])),
        )


class NeuralNetwork:
    def __init__(self):
        print("new nnet")
