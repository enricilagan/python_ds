class Matrix(object):

    def __init__(self, values):
        self.values = values

    def __repr__(self):
        return f'<Matrix values="{self.values}">'

    def __matmul__(self, other):
        lst = [[self.values[x][0] * other.values[0][y] + self.values[x][1] * other.values[1][y]
                for y in range(0, len(other.values[0]))] for x in range(0, len(self.values))]
        return Matrix(lst)

    def __imatmul__(self, other):
        lst = [[self.values[x][0] * other.values[0][y] + self.values[x][1] * other.values[1][y]
                for y in range(0, len(other.values[0]))] for x in range(0, len(self.values))]
        return Matrix(lst)

    def __rmatmul__(self, other):
        lst = [[other.values[x][0] * self.values[0][y] + other.values[x][1] * self.values[1][y]
                for y in range(0, len(self.values[0]))] for x in range(0, len(other.values))]
        return Matrix(lst)
