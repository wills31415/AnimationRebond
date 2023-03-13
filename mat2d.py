# coding: utf-8

from math import *



class Mat2d:

    def __init__(self, val = []):

        if isinstance(val, Mat2d):
            val = val.data

        self.dim = [0, 0]
        self.data = []

        if isinstance(val, tuple):
            val = list(val)

        if val == []:
            pass

        elif not isinstance(val, list):
            self.dim = [1, 1]
            self.data.append([val])

        elif not isinstance(val[0], list):
            self.dim = [len(val), 1]
            for elem in val:
                assert not isinstance(elem, list), "Erreur de typage lors de l'instanciation d'un vecteur. "
                self.data.append([elem])

        else:
            self.dim = [len(val), len(val[0])]
            for row in val:
                assert isinstance(row, list), "Erreur de typage lors de l'instanciation d'une matrice. "
                assert len(row) == self.dim[1], "Erreur de dimensions lors de l'instanciation d'une matrice. "
                self.data.append(row)


    def get_dim(self):
        if self.data == []:
            return (0, 0)
        return (len(self.data), len(self.data[0]))


    def __len__(self):
        if self.data == []:
            return 0
        return len(self.data) * len(self.data[0])



    def __getitem__(self, index):
        I = [None, None]
        if not isinstance(index, tuple):
            tmpList = [self.data[i][j] for i in range(self.dim[0]) for j in range(self.dim[1])]
            if isinstance(index, slice):
                if len(tmpList[index]) == 1:
                    return tmpList[index][0]
                return Mat2d(tmpList[index])
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
        return Mat2d(subMat)


    def __setitem__(self, index, value):
        assert self.get_dim() != [0, 0], "Erreur : assignement à une matrice nulle. "
        assert value != [], "Erreur : assignement vide. "

        indexMat = Mat2d([[(i, j) for j in range(self.dim[1])] for i in range(self.dim[0])])

        if isinstance(value, Mat2d) and value.get_dim() == [1, 1]:
            value = value.data[0][0]

        if not isinstance(value, list) and not isinstance(value, Mat2d):
            if isinstance(indexMat[index], tuple):
                (i, j) = indexMat[index]
                self.data[i][j] = value
            else:
                for indexRow in indexMat[index].data:
                    for (i, j) in indexRow:
                        self.data[i][j] = value
        elif isinstance(value, list):
            assert len(value) == self[index].dim[0] * self[index].dim[1], "Erreur de dimensions lors de l'assignation d'une liste à une matrice. "
            for iValue, elem in enumerate(value):
                (i, j) = indexMat[index][iValue].data[0][0]
                self.data[i][j] = elem
        else:
            assert indexMat[index].get_dim() == value.get_dim(), "Erreur de dimensions lors de l'assignation d'une matrice à une matrice. "
            for i, indexRow in enumerate(indexMat[index].data):
                for j, (iSubMat, jSubMat) in enumerate(indexRow):
                    self.data[iSubMat][jSubMat] = value[i, j]




    def __str__(self):
        return "\n[" + ", \n ".join(["[" + ", ".join(map(str, self.data[i])) + "]" for i in range(self.dim[0])]) + "]\n"


    def transpose(self):
        if self.data == []:
            return Mat2d();
        return Mat2d([[self.data[i][j] for i in range(len(self.data))] for j in range(len(self.data[0]))])


    def submat(self, *index):
        assert isinstance(index, tuple), "Il faut deux arguments pour calculer une sous-matrice. "
        [l, c] = self.get_dim()
        return Mat2d([[self[i, j] for j in range(c) if j != index[1]] for i in range(l) if i != index[0]])


    def det(self):
        [l, c] = self.get_dim()
        assert l == c, "Erreur : seule une matrice carrée possède un déterminant. "
        if [l, c] == [0, 0]:
            return 0
        elif [l, c] == [1, 1]:
            return self.data[0][0]
        elif [l, c] == [2, 2]:
            return self[0,0] * self[1,1] - self[1,0] * self[0,1]
        else:
            return sum([(-1) ** (i % 2) * self[i, 0] * self.submat(i, 0).det() for i in range(l)])


    def inv(self):
        [l, c] = self.get_dim()
        assert l == c, "Erreur : seule une matrice carrée est inversible. "
        detMat = self.det()
        assert detMat != 0, "Erreur : la matrice n'est pas inversible. "
        invMat = Mat2d([[(-1) ** ((i + j) % 2) * self.submat(i, j).det() for j in range(c)] for i in range(l)])
        return invMat.transpose() / detMat


    def __add__(self, other):
        (l, c) = self.get_dim()
        assert self.get_dim() == other.get_dim(), "Les deux matrices doivent être de même dimensions. "
        if self.data == []:
            return Mat2d()
        return Mat2d([[self.data[i][j] + other.data[i][j] for j in range(c)] for i in range(l)])


    def __iadd__(self, other):
        (l, c) = self.get_dim()
        assert self.get_dim() == other.get_dim(), "Les deux matrices doivent être de même dimensions. "
        if self.data == []:
            return Mat2d()
        return Mat2d([[self.data[i][j] + other.data[i][j] for j in range(c)] for i in range(l)])


    def __sub__(self, other):
        (l, c) = self.get_dim()
        assert self.get_dim() == other.get_dim(), "Les deux matrices doivent être de mêmes dimensions. "
        if self.data == []:
            return Mat2d()
        return Mat2d([[self.data[i][j] - other.data[i][j] for j in range(c)] for i in range(l)])


    def __isub__(self, other):
        (l, c) = self.get_dim()
        assert self.get_dim() == other.get_dim(), "Les deux matrices doivent être de mêmes dimensions. "
        if self.data == []:
            return Mat2d()
        return Mat2d([[self.data[i][j] - other.data[i][j] for j in range(c)] for i in range(l)])


    def __neg__(self):
        (l, c) = self.get_dim()
        if self.data == []:
            return Mat2d()
        return Mat2d([[-self.data[i][j] for j in range(c)] for i in range(l)])


    def __pos__(self):
        (l, c) = self.get_dim()
        if self.data == []:
            return Mat2d()
        return Mat2d([[self.data[i][j] for j in range(c)] for i in range(l)])


    def __mul__(self, other):
        if type(self) == type(Mat2d()) and type(other) == type(Mat2d()):
            (l1, c1) = self.get_dim()
            (l2, c2) = other.get_dim()
            assert c1 == l2, "Les deux matrices doivent avoir respectivement autant de colonnes que de lignes. "
            if l1 == 0 or l2 == 0:
                return Mat2d()
            result = Mat2d([[sum([self.data[i][k] * other.data[k][j] for k in range(c1)]) for j in range(c2)] for i in range(l1)])
        else:
            result = Mat2d([[other * self.data[i][j] for j in range(self.get_dim()[1])] for i in range(self.get_dim()[0])])
        if result.get_dim == [1, 1]:
            return result.data[0][0]
        else:
            return result


    def __imul__(self, other):
        if type(self) == type(Mat2d()) and type(other) == type(Mat2d()):
            (l1, c1) = other.get_dim()
            (l2, c2) = self.get_dim()
            assert c1 == l2, "Les deux matrices doivent avoir respectivement autant de colonnes que de lignes. "
            if l1 == 0 or l2 == 0:
                return Mat2d()
            result = Mat2d([[sum([other.data[i][k] * self.data[k][j] for k in range(c1)]) for j in range(c2)] for i in range(l1)])
        else:
            result = Mat2d([[other * self.data[i][j] for j in range(self.get_dim()[1])] for i in range(self.get_dim()[0])])
        if result.get_dim() == [1, 1]:
            return result.data[0][0]
        else:
            return result


    def __rmul__(self, other):
        if type(self) == type(Mat2d()) and type(other) == type(Mat2d()):
            (l1, c1) = self.get_dim()
            (l2, c2) = other.get_dim()
            assert c1 == l2, "Les deux matrices doivent avoir respectivement autant de colonnes que de lignes. "
            if l1 == 0 or l2 == 0:
                return Mat2d()
            result = Mat2d([[sum([self.data[i][k] * other.data[k][j] for k in range(l1)]) for j in range(c2)] for i in range(l1)])
        else:
            result = Mat2d([[other * self.data[i][j] for j in range(self.get_dim()[1])] for i in range(self.get_dim()[0])])
        if result.get_dim() == [1, 1]:
            return result.data[0][0]
        else:
            return result


    def __truediv__(self, other):
        assert other != 0, "Tentative de division par 0 : attention c'est pas bien ! "
        (l, c) = self.get_dim()
        if l == 0:
            return Mat2d()
        return Mat2d([[self[i,j] / other for j in range(c)] for i in range(l)])


    def __itruediv__(self, other):
        assert other != 0, "Tentative de division par 0 : attention c'est pas bien ! "
        (l, c) = self.get_dim()
        if l == 0:
            return Mat2d()
        return Mat2d([[self[i,j] / other for j in range(c)] for i in range(l)])


    def __matmul__(self, other):
        (l1, c1) = self.get_dim()
        (l2, c2) = other.get_dim()
        assert c1 == 1 and c2 == 1, "Un produit scalaire ne peut se faire qu'entre deux vecteurs. "
        assert l1 == l2, "Un produit scalaire ne peut se faire qu'entre deux vecteurs de mêmes dimensions. "
        return sum([self[i] * other[i] for i in range(l1)])


    def __floordiv__(self, other):
        (l1, c1) = self.get_dim()
        (l2, c2) = other.get_dim()
        assert c2 == 1, "Erreur : le second membre doit être un vecteur. "
        return self.inv() * other


    def __mod__(self, other):
        return (other - self).norm()


    def norm(self):
        (l, c) = self.get_dim()
        assert l != 0 and c == 1, "Seul un vecteur possède une norme. "
        return sqrt(self @ self)


    @classmethod
    def zeros(cls, *dim):
        assert len(dim) < 3, "La fonction 'zeros' ne prend qu'au plus 2 arguments. "
        if len(dim) == 0:
            return cls()
        if len(dim) == 1:
            return cls([[0] * dim[0]] * dim[0])
        return cls([[0] * dim[1]] * dim[0])


    @classmethod
    def ones(cls, *dim):
        assert len(dim) < 3, "La fonction 'ones' ne prend qu'au plus 2 arguments. "
        if len(dim) == 0:
            return cls()
        if len(dim) == 1:
            return cls([[1] * dim[0]] * dim[0])
        return cls([[1] * dim[1]] * dim[0])


    @classmethod
    def Id(cls, dim):
        assert isinstance(dim, int) and dim >= 0, "La dimension doit être un entier positif. "
        return cls([[int(i == j) for j in range(dim)] for i in range(dim)])


    @classmethod
    def rot2d(cls, vecteur):
        assert vecteur.get_dim() == (2, 1), "La fonction 'rot2d' ne prend qu'un vecteur de taille 2 en argument. "
        return cls([[vecteur[0], -vecteur[1]], [vecteur[1], vecteur[0]]]) / vecteur.norm()
