
'''Linear regression is a statistical method used to model the relationship between a dependent variable 
and one or more independent variables by fitting a linear equation to the observed data. In simple linear regression, 
there is only one independent variable and the relationship between the two variables is represented by a line. 
In multiple linear regression, there are two or more independent variables.

'''

from typing import List, Tuple

class LinearRegressionModel:
    def __init__(self, x: List[float], y: List[float]):
        self.x = x
        self.y = y
        self.x_mean = sum(x) / len(x)
        self.y_mean = sum(y) / len(y)
        self.x_value = list(map(lambda value: value - self.x_mean, x))
        self.y_value = list(map(lambda value: value - self.y_mean, y))
        self.x_value_square = list(map(lambda value: value**2, self.x_value))
        self.x_value_square_total = sum(self.x_value_square)
        self.x_y_value_square = list(map(lambda xv, yv: xv * yv, self.x_value, self.y_value))
        self.x_y_value_square_total = sum(self.x_y_value_square)
        self.b1 = self.x_y_value_square_total / self.x_value_square_total
        self.bo = self.y_mean - (self.b1 * self.x_mean)
    
    def predict(self, x: List[float]) -> List[float]:
        return list(map(lambda xi: self.bo + self.b1 * xi, x))


# regression = LinearRegressionModel(x, y)
# pred_y = regression.predict(x)
# pred_y

