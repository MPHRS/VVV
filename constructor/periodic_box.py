import numpy as np
from exceptions import OutBoxError
from typing import Tuple


def periodic(coord: float, box: float) -> float:
    """ 
    Returns the coordinate to the box if it goes out of it

    Args:
        coord (float): coordinate
        box (float): box size along some axis

    Returns:
        float: changed (or old) coordinate
    """
    if abs(coord) > 1.5 * box:
        raise OutBoxError
    elif abs(coord) > 0.5 * box:
        return coord - np.sign(coord) * box
    else:
        return coord


class Box():
    """ 
    Sets up a 3D-box for simulation of a molecular system
    Its center has coordinates (0.0, 0.0, 0.0)
    Edge sizes: self.x, self.y, self.z 
    """

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def periodic_correct(self, xb: float, yb: float, zb: float) -> Tuple[float, float, float]:
        """
        Returns the coordinates to the box if they go out of it

        Args:
            xb (float), yb (float), zb (float): the beads coordinates

        Returns:
            Tuple[float, float, float]: changed (or old) coordinates
        """
        xb = periodic(xb, self.x)
        yb = periodic(yb, self.y)
        zb = periodic(zb, self.z)
        return xb, yb, zb


if __name__ == '__main__':
    box = Box(x=10., y=20., z=30.)
    x, y, z = box.periodic_correct(2., 12., -16.)
    print(x, y, z)
    print(periodic(coord=11, box=0))
