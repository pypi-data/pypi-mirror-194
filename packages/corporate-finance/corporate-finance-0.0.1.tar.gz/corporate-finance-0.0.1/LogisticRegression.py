from typing import List, Tuple
import math

class LogisticRegressionModel:
    def __init__(self, x: List[List[float]], y: List[int], learning_rate: float = 0.01, num_iterations: int = 1000):
        self.x = x
        self.y = y
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations
        self.theta = [0.0] * (len(x[0]) + 1)

    def sigmoid(self, z: float) -> float:
        return 1 / (1 + math.exp(-z))
    
    def predict_probability(self, x: List[float]) -> float:
        z = self.theta[0]
        for i in range(len(x)):
            z += self.theta[i + 1] * x[i]
        return self.sigmoid(z)
    
    def fit(self):
        for _ in range(self.num_iterations):
            z = [0.0] * len(self.y)
            for i in range(len(self.x)):
                z[i] = self.predict_probability(self.x[i])
                error = [0.0] * len(self.y)
                for i in range(len(self.y)):
                    error[i] = (z[i] - self.y[i])
                self.theta[0] = self.theta[0] - self.learning_rate * sum(error) / len(self.y)
                for i in range(len(self.x[0])):
                    gradient = [0.0] * len(self.y)
                    for j in range(len(self.y)):
                        gradient[j] = (z[j] - self.y[j]) * self.x[j][i]
                    self.theta[i + 1] = self.theta[i + 1] - self.learning_rate * sum(gradient) / len(self.y)
    
    def predict(self, x: List[List[float]]) -> List[int]:
        predictions = []
        for i in range(len(x)):
            probability = self.predict_probability(x[i])
            if probability >= 0.5:
                predictions.append(1)
            else:
                predictions.append(0)
        return predictions

# x = [[1, 2], [2, 4], [3, 6], [4, 8], [5, 10]]
# y = [0, 0, 1, 1, 1]

# regression = LogisticRegressionModel(x, y)
# regression.fit()

# x_test = [[1, 2], [3, 4], [5, 6]]
# predictions = regression.predict(x_test)

# print("Predictions:", predictions)