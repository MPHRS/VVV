from bondset import DENDRON
from mol import Dendron


def test_dendron():
    dendron = Dendron(n=2, g=2)
    assert dendron.bonds == DENDRON
