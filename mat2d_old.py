# coding: utf-8


from math import *



class mat2d:

    def __init__(self, val = [], *dim):
        self.data = []
        self.dim = []

        if len(dim) == 0:
            if len(val) == 0:
                self.dim.append(0)
            elif type(val[0]) != type([]):
                self.dim.extend([len(val), 1])
                self.data.extend([[elem] for elem in val])
            else:
                self.dim.append(len(val))
                self.dim.append(max([len(row) for row in val]))
                for row in val:
                    self.data.append([0] * self.dim[1])
                    self.data[-1][:len(row)] = row
        elif type(val) != type([]):
            self.dim.extend(list(dim[:2]))
            if len(dim) == 1:
                self.dim.append(dim[0])
            self.data.extend([[val] * self.dim[1]] * self.dim[0])
        else:
            self.dim.extend(list(dim[:2]))
            if len(dim) == 1:
                self.dim.append(dim[0])
            self.data = [[0] * self.dim[1]] * self.dim[0]
            for i in range(0, min(len(val), self.dim[0])):
                if type(val[i]) != type([]):
                    self.data[i][0] = val[i]
                else:
                    self.data[i][:min(len(val[i]), self.dim[1])] = val[i][min(len(val[i]), self.dim[1])]


    def get_dim(self):
        if self.data == []:
            return (0, 0)
        return (len(self.data), len(self.data[0]))


    def __getitem__(self, index):
        I = [None, None]
        if not isinstance(index, tuple):
            tmpList = [self.data[i][j] for i in range(self.dim[0]) for j in range(self.dim[1])]
            if isinstance(index, slice):
                if len(tmpList[index]) == 1:
                    return tmpList[index][0]
                return mat2d(tmpList[index])
            else:
                return tmpList[index]
        if not isinstance(index[0], slice) and not isinstance(index[1], slice):
            return self.data[index[0]][index[1]]
        for i, item in enumerate(index):
            if isinstance(item, slice):
                I[i] = item
            elif item >= 0:
                I[i] = slice(item, item + 1, None)
            else:
                I[i] = slice(item, None, None)
        subLines = range(len(self.data))[I[0]]
        subColumns = range(len(self.data[0]))[I[1]]
        subMat = [[self.data[i][j] for j in subColumns] for i in subLines]
        return mat2d(subMat)


    def __str__(self):
        return '\n'.join([' '.join(map(str, self.data[i])) for i in range(self.dim[0])])


    def transpose(self):
        if self.data == []:
            return mat2d();
        return mat2d([[self.data[i][j] for i in range(len(self.data))] for j in range(len(self.data[0]))])


    def __add__(self, other):
        (l, c) = self.get_dim()
        assert self.get_dim() == other.get_dim(), "Les deux matrices doivent être de même dimensions. "
        if self.data == []:
            return mat2d()
        return mat2d([[self.data[i][j] + other.data[i][j] for j in range(c)] for i in range(l)])


    def __iadd__(self, other):
        (l, c) = self.get_dim()
        assert self.get_dim() == other.get_dim(), "Les deux matrices doivent être de même dimensions. "
        if self.data == []:
            return mat2d()
        return mat2d([[self.data[i][j] + other.data[i][j] for j in range(c)] for i in range(l)])


    def __sub__(self, other):
        (l, c) = self.get_dim()
        print(self.get_dim())
        print(other.get_dim())
        assert self.get_dim() == other.get_dim(), "Les deux matrices doivent être de mêmes dimensions. "
        if self.data == []:
            return mat2d()
        return mat2d([[self.data[i][j] - other.data[i][j] for j in range(c)] for i in range(l)])


    def __isub__(self, other):
        (l, c) = self.get_dim()
        assert self.get_dim() == other.get_dim(), "Les deux matrices doivent être de mêmes dimensions. "
        if self.data == []:
            return mat2d()
        return mat2d([[self.data[i][j] - other.data[i][j] for j in range(c)] for i in range(l)])


    def __neg__(self):
        (l, c) = self.get_dim()
        if self.data == []:
            return mat2d()
        return mat2d([[-self.data[i][j] for j in range(c)] for i in range(l)])


    def __pos__(self):
        (l, c) = self.get_dim()
        if self.data == []:
            return mat2d()
        return mat2d([[self.data[i][j] for j in range(c)] for i in range(l)])


    def __mul__(self, other):
        if type(self) == type(mat2d()) and type(other) == type(mat2d()):
            (l1, c1) = self.get_dim()
            (l2, c2) = other.get_dim()
            assert c1 == l2, "Les deux matrices doivent avoir respectivement autant de colonnes que de lignes. "
            if l1 == 0 or l2 == 0:
                return mat2d()
            return mat2d([[sum([self.data[i][k] * other.data[k][j] for k in range(c1)]) for j in range(c2)] for i in range(l1)])
        else:
            return mat2d([[other * self.data[i][j] for i in range(self.get_dim()[0])] for j in range(self.get_dim()[1])])


    def __imul__(self, other):
        if type(self) == type(mat2d()) and type(other) == type(mat2d()):
            (l1, c1) = other.get_dim()
            (l2, c2) = self.get_dim()
            assert c1 == l2, "Les deux matrices doivent avoir respectivement autant de colonnes que de lignes. "
            if l1 == 0 or l2 == 0:
                return mat2d()
            return mat2d([[sum([other.data[i][k] * self.data[k][j] for k in range(c1)]) for j in range(c2)] for i in range(l1)])
        else:
            return mat2d([[other * self.data[i][j] for j in range(self.get_dim()[1])] for i in range(self.get_dim()[0])])


    def __rmul__(self, other):
        if type(self) == type(mat2d()) and type(other) == type(mat2d()):
            (l1, c1) = self.get_dim()
            (l2, c2) = other.get_dim()
            assert c1 == l2, "Les deux matrices doivent avoir respectivement autant de colonnes que de lignes. "
            if l1 == 0 or l2 == 0:
                return mat2d()
            return mat2d([[sum([self.data[i][k] * other.data[k][j] for k in range(l1)]) for j in range(c2)] for i in range(l1)])
        else:
            return mat2d([[other * self.data[i][j] for i in range(self.get_dim()[0])] for j in range(self.get_dim()[1])])


    def __truediv__(self, other):
        assert other != 0, "Tentative de division par 0 : attention c'est pas bien ! "
        (l, c) = self.get_dim()
        if l == 0:
            return mat2d()
        return mat2d([[self[i,j] / other for j in range(c)] for i in range(l)])


    def __itruediv__(self, other):
        assert other != 0, "Tentative de division par 0 : attention c'est pas bien ! "
        (l, c) = self.get_dim()
        if l == 0:
            return mat2d()
        return mat2d([[self[i,j] / other for j in range(c)] for i in range(l)])


    def __matmul__(self, other):
        (l1, c1) = self.get_dim()
        (l2, c2) = other.get_dim()
        assert c1 == 1 and c2 == 1, "Un produit scalaire ne peut se faire qu'entre deux vecteurs. "
        assert l1 == l2, "Un produit scalaire ne peut se faire qu'entre deux vecteurs de mêmes dimensions. "
        return sum([self[i] * other[i] for i in range(l1)])



    def norm(self):
        (l, c) = self.get_dim()
        assert l != 0 and c == 1, "Seul un vecteur possède une norme. "
        return sqrt(self @ self)
