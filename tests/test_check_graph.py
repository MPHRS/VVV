import bondset
import pytest
from check_graph import CheckGraph


class TestCheckGraph:
    @pytest.mark.parametrize("bonds, expected_result", [(bondset.EMPTY, True),
                                                        (bondset.LINEAR, True),
                                                        (bondset.GAP_ENUM, False)])
    def test_is_not_gaps(self, bonds: bondset.Bondtype, expected_result: bool):
        assert CheckGraph.is_not_gaps(bonds) == expected_result

    @pytest.mark.parametrize("bonds", [(bondset.NEGATIVE),])
    def test_is_not_gaps_raises(self,  bonds: bondset.Bondtype):
        with pytest.raises(Exception) as err:
            CheckGraph.is_not_gaps(bonds)
        assert "Some node in grpah is negative" in str(err.value)

    @pytest.mark.parametrize("bonds, expected_result", [(bondset.EMPTY, True),
                                                        (bondset.LINEAR, True),
                                                        (bondset.NEGATIVE, True),
                                                        (bondset.DOUBLE_BOND, False),
                                                        (bondset.CYCLIC_EDGE, False),])
    def test_is_simple(self, bonds: bondset.Bondtype, expected_result: bool):
        assert CheckGraph.is_simple(bonds) == expected_result