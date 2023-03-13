# coding: utf-8



from mat2d import *


array = [
[707, 615, 806, 704, 765, 852],
[980, 124, 820, 581, 263, 752],
[379, 587, 794, 288, 485, 890],
[848, 717, 104, 351, 641, 109],
[468, 615, 729, 306, 851, 265],
[730, 579, 216, 449, 460, 895],
[361, 173, 741, 400, 298, 698],
[147, 477, 438, 161, 457, 591]
]

v1 = 1
v2 = -1

Id2 = Mat2d.Id(2)
e1 = Id2[:,0]
e2 = Id2[:,1]

v = v1 * e1 + v2 * e2

F = Mat2d.rot2d(v)
B = F.transpose()
f1 = F[:,0]
f2 = F[:,1]

w = B * v

print("F :", F)
print("B :", B)

print("e1 :", e1)
print("e2 :", e2)

print("f1 :", f1)
print("f2 :", f2)

print("v :", v)
print("B * v :", B * v)

print("w :", w)
print("F * w :", F * w)


def number_of_occurences(l):
    occ = {key : 0 for key in l}
    for key in l:
        occ[key] += 1
    return occ


l_array = [array[i][j] for i in range(len(array)) for j in range(len(array[i]))]
print(l_array)
print(number_of_occurences(l_array))
