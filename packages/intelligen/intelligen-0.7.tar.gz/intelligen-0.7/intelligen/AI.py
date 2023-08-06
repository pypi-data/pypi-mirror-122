from typing import List
Vector = List[float]

import numpy as np

def mean_squared_error(y_real: Vector, y_pred: Vector) -> float:
    """Returns the mean squared error

    Args:
        y_real (Vector): real data
        y_pred (Vector): predicted data

    Returns:
        float: mean squared error
    """
    y_real = np.array(y_real)
    y_pred = np.array(y_pred)
    
    return np.mean((y_real - y_pred)**2)

def mean_absolute_error(y_real: Vector, y_pred: Vector) -> float:
    """Returns the mean absolute error

    Args:
        y_real (Vector): real data
        y_pred (Vector): predicted data

    Returns:
        float: mean absolute error
    """
    y_real = np.array(y_real)
    y_pred = np.array(y_pred)
    
    return np.mean(np.abs(y_real - y_pred))

x = [1,2,3,4]
y = [3,3,4,5]

print(mean_absolute_error(x,y))
print(mean_squared_error(x,y))
