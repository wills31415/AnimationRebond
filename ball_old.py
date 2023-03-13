# coding: utf-8


from mat2d import *
from math import *

dt = 0.01       # en secondes
g = 9.807

coeffRestitutionBord = 19/20
coeffRestitutionBalle = 19/20
viscositeDynamiqueAir = 18.5e-6       # Viscosité dynamique de l'air



class Point:

    def __init__(self, position = [0, 0], rayon = 0):
        self.position = mat2d(position)
        self.rayon = rayon

    @staticmethod
    def dist(point1, point2):
        return point1.position % point2.position



class Ball(Point):

    def __init__(self, position = [0, 0], vitesse = [0, 0], rayon = 10, masse = 1):
        Point.__init__(self, position, rayon)
        self.vitesse = mat2d(vitesse)
        self.masse = masse                                  # en kg
        self.coeffFrottements = 6 * pi * self.rayon         # Coefficient lié à la géométrie de l'objet



class Bond:

    def __init__(self, point1, point2, epaisseur = 1):
        assert issubclass(type(point1), Point) and issubclass(type(point2), Point), "On ne peut relier autre chose que des points. "
        self.point1 = point1
        self.point2 = point2
        self.epaisseur = epaisseur

    @property
    def l(self):
        return Point.dist(self.point1, self.point2)



class Rod(Bond):

    def __init__(self, point1, point2, epaisseur = 1):
        Bond.__init__(self, point1, point2, epaisseur)
        self.l0 = Point.dist(point1, point2)



class String(Rod):

    def __init__(self, point1, point2, epaisseur = 1):
        Rod.__init__(self, point1, point2, epaisseur)



class Elastic(String):

    def __init__(self, point1, point2, **kwargs):
        String.__init__(self, point1, point2)
        if "epaisseur" in kwargs:
            self.epaisseur = kwargs["epaisseur"]
        if "l0" in kwargs:
            self.l0 = kwargs["l0"]
        self.k = 1
        if "k" in kwargs:
            self.k = kwargs["k"]



class Spring(Elastic):

    def __init__(self, point1, point2, **kwargs):
        Elastic.__init__(self, point1, point2, **kwargs)
        self.lMin = 0
        self.lMax = self.l0
        if "lRange" in kwargs:
            (self.lMin, self.lMax) = kwargs["lRange"]
        else:
            if "lMin" in kwargs:
                self.lMin = kwargs["lMin"]
            if "lMax" in kwargs:
                self.lMax = kwargs["lMax"]



class repere2d:

    def __init__(self, origine = (0, 0), unitX = 1, unitY = 1):
        self.O = mat2d(list(origine))
        self.e = mat2d([[unitX, 0], [0, unitY]])



class environnement:

    def __init__(self, res = (800, 400), origine = (0, 0), pixelsPerUnit = 1, coeffRestitutionBord = 1, coeffRestitutionBalle = 1, viscositeDynamique = 0):
        self.R = repere2d(origine, pixelsPerUnit, -pixelsPerUnit)
        self.limX = (-origine[0] / pixelsPerUnit, (res[0] - origine[0]) / pixelsPerUnit)
        self.limY = ((origine[1] - res[1]) / pixelsPerUnit, origine[1] / pixelsPerUnit)
        self.pixelsPerUnit = pixelsPerUnit

        self.viscositeDynamique = viscositeDynamique
        self.coeffRestitutionBord = coeffRestitutionBord
        self.coeffRestitutionBalle = coeffRestitutionBalle

        self.movables = []
        self.fixedPoints = []
        self.bonds = []


    def locate(self, position):
        assert isinstance(self.R, repere2d), "L'environnement doit être muni d'un repère. "
        assert isinstance(position, mat2d) and position.get_dim() == (2, 1), "L'objet à localiser doit être de dimensions (2, 1). "
        coord = self.R.O + self.R.e * position
        return (coord[0], coord[1])


    def unlocate(self, coord):
        assert isinstance(self.R, repere2d), "L'environnement doit être muni d'un repère. "
        assert isinstance(coord, tuple) and len(coord) == 2, "L'objet à délocaliser doit être un tuple de taille 2. "
        return self.R.e.inv() * (mat2d(list(coord)) - self.R.O)


    def add_movable(self, movable):
        assert movable not in self.movables and movable not in self.fixedPoints, "L'objet mobile est déjà dans l'environnement. "
        if movable.position[0] - movable.rayon <= self.limX[0]:
            movable.position[0] = self.limX[0] + movable.rayon
        elif movable.position[0] + movable.rayon >= self.limX[1]:
            movable.position[0] = self.limX[1] - movable.rayon
        if movable.position[1] - movable.rayon <= self.limY[0]:
            movable.position[1] = self.limY[0] + movable.rayon
        elif movable.position[1] + movable.rayon >= self.limY[1]:
            movable.position[1] = self.limY[1] - movable.rayon
        self.movables.append(movable)
        return self.movables[-1]


    def add_fixedPoint(self, point):
        assert point not in self.movables and point not in self.fixedPoints, "L'objet fixe est déjà dans l'environnement. "
        if point.position[0] - point.rayon <= self.limX[0]:
            point.position[0] = self.limX[0] + point.rayon
        elif point.position[0] + point.rayon >= self.limX[1]:
            point.position[0] = self.limX[1] - point.rayon
        if point.position[1] - point.rayon <= self.limY[0]:
            point.position[1] = self.limY[0] + point.rayon
        elif point.position[1] + point.rayon >= self.limY[1]:
            point.position[1] = self.limY[1] - point.rayon
        self.fixedPoints.append(point)
        return self.fixedPoints[-1]


    def add_bond(self, bond):
        assert issubclass(type(bond), Bond), "Erreur de type dans la fonction 'add_bond'. "
        assert bond.point1 in self.movables or bond.point1 in self.fixedPoints, "L'objet 1 doit être dans l'environnement. "
        assert bond.point2 in self.movables or bond.point2 in self.fixedPoints, "L'objet 2 doit être dans l'environnement. "
        assert bond not in self.bonds, "La liaison est déjà dans l'environnement. "
        self.bonds.append(bond)
        return self.bonds[-1]


    def collision_movable_border(self, movable):
        assert movable in self.movables, "L'objet mobile doit être dans l'environnement. "
        collision = [False, False]

        if movable.position[0] - movable.rayon <= self.limX[0] and movable.vitesse[0] <= 0:
            collision[0] = True
            movable.position[0] = self.limX[0] + movable.rayon

        elif movable.position[0] + movable.rayon >= self.limX[1] and movable.vitesse[0] >= 0:
            collision[0] = True
            movable.position[0] = self.limX[1] - movable.rayon


        if movable.position[1] - movable.rayon <= self.limY[0] and movable.vitesse[1] <= 0:
            collision[1] = True
            movable.position[1] = self.limY[0] + movable.rayon

        elif movable.position[1] + movable.rayon >= self.limY[1] and movable.vitesse[1] >= 0:
            collision[1] = True
            movable.position[1] = self.limY[1] - movable.rayon

        return collision


    def distance_movable_movable(self, movable1, movable2):
        assert movable1 in self.movables, "L'objet mobile 1 doit être dans l'environnement. "
        assert movable2 in self.movables, "L'objet mobile 2 doit être dans l'environnement. "
        # assert self.movables.index(movable1) != self.movables.index(movable2), "Les objets mobiles 1 et 2 doivent être différents. "

        distance = (movable1.position[0] - movable2.position[0]) ** 2 + (movable1.position[1] - movable2.position[1]) ** 2

        return sqrt(distance) - movable1.rayon - movable2.rayon


    def collision_movable_movable(self, movable1, movable2):
        if self.movables.index(movable1) != self.movables.index(movable2) and self.distance_movable_movable(movable1, movable2) <= 0:
            return True
        return False


    def update_env(self):
        for movable in self.movables:
            collisionMovableBorder = self.collision_movable_border(movable)
            if collisionMovableBorder != [False, False]:
                if collisionMovableBorder[0]:
                    movable.vitesse[0] *= -self.coeffRestitutionBord
                if collisionMovableBorder[1]:
                    movable.vitesse[1] *= -self.coeffRestitutionBord
            else:
                listMovablesCollision = [movable2 for movable2 in self.movables[:self.movables.index(movable)] if self.collision_movable_movable(movable, movable2)]
                if len(listMovablesCollision) != 0:
                    for movable2 in listMovablesCollision:
                        position = movable2.position - movable.position
                        rotation = mat2d([[position[0], position[1]], [-position[1], position[0]]]) / position.norm()
                        v1 = rotation * movable.vitesse
                        v2 = rotation * movable2.vitesse
                        vn = mat2d([v1[0], v2[0]])
                        vn *= mat2d([[movable.masse - self.coeffRestitutionBalle * movable2.masse, (1 + self.coeffRestitutionBalle) * movable2.masse], [(1 + self.coeffRestitutionBalle) * movable.masse, movable2.masse - self.coeffRestitutionBalle * movable.masse]]) / (movable.masse + movable2.masse)
                        v1[0] = vn[0]
                        v2[0] = vn[1]
                        movable.vitesse = rotation.transpose() * v1
                        movable2.vitesse = rotation.transpose() * v2

                        distance = -self.distance_movable_movable(movable, movable2)
                        xn = rotation.transpose() * mat2d([distance, 0]) / (movable.rayon * movable.masse + movable2.rayon * movable2.masse)
                        movable.position -= xn * movable2.rayon * movable2.masse
                        movable2.position += xn * movable.rayon * movable.masse
                else:
                    a = -self.viscositeDynamique * movable.coeffFrottements / movable.masse * movable.vitesse - g * mat2d([0, 1])
                    movable.vitesse += dt * a
        for movable in self.movables:
            movable.position += dt * movable.vitesse




#y' = f(t, y)

#y(t0) = y0
#y(t + dt) = y(t) + dt * y'(t)
# il va subir -m g u_y h

#   v_x(t + dt) = v_x(t)
#   v_y(t + dt) = -e * v_y(t)

# calculer a
# calculer v(t + dt) = v(t) + a * dt
# calculer x(t + dt) = x(t) + v(t + dt) * dt

# -1 * v(t_coll) * coeff