from typing import Final

import pytest
from exceptions import OutBoxError
from periodic_box import Box

EPS: Final = 1e-8


def test_periodic():
    assert abs(Box.periodic(coord=11, box=20) - (-9)) < EPS
    assert abs(Box.periodic(coord=-11, box=20) - (9)) < EPS


def test_periodic_raises():
    with pytest.raises(OutBoxError) as err:
        Box.periodic(coord=11, box=1)
    assert "Some bead occure out of box > 1.5 box" in str(err.value)
    with pytest.raises(OutBoxError) as err:
        Box.periodic(coord=11, box=0)
    assert "Some bead occure out of box > 1.5 box" in str(err.value)
