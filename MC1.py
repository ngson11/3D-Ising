Python 3.6.4 (v3.6.4:d48ecebad5, Dec 18 2017, 21:07:28) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "copyright", "credits" or "license()" for more information.
>>> WARNING: The version of Tcl/Tk (8.5.9) in use may be unstable.
Visit http://www.python.org/download/mac/tcltk/ for current information.
import numpy as np

def spin_configuration(n):          #create initial spin configuration
    s = np.random.randint(0, 2, size=(n,n,n))
    s[s == 0] = -1
    return s

def find_neighbors(n, x, y, z):     #find 6 nearest neighbours (periodic boundary condition)
    front   = ((x-1)%n, y      , z)
    back    = ((x+1)%n, y      , z)
    left    = (x      , (y-1)%n, z)
    right   = (x      , (y+1)%n, z)
    top     = (x      , y      , (z+1)%n)
    bottom  = (x      , y      , (z-1)%n)
    return [[front[0], front[1], front[2]], [back[0]  , back[1]  , back[2]  ],
            [left[0] , left[1] , left[2] ], [right[0] , right[1] , right[2] ],
            [top[0]  , top[1]  , top[2]  ], [bottom[0], bottom[1], bottom[2]]]
L  = 40           #int(input("L = "))
Bc = 0.2216544          #Critical value
B  = 1.1*Bc
p  = 1 - np.exp(-2 * B) #Probabiliy to put a bond & flipping spin
MC = 1000
trial = 1000
output = []
chi = []
spins = spin_configuration(L)
#Wolff's single cluster

a = 1
while a <= 20:
    for t in range(trial):
        spin = 0
        spins = spin_configuration(L)
        for sweep in range(MC):
            Q = np.random.randint(0, L, 3)
            S = spins[tuple(Q)]
            spins[tuple(Q)] *= -1
            count = 1
            cluster = [Q]
            for i in cluster:
                X = find_neighbors(L, i[0], i[1], i[2])
                for j in X:
                    k = spins[tuple(j)]
                    if k == S and np.random.random_sample() <= p:
                        cluster.append(np.array(j))
                        spins[tuple(j)] *= -1
                        count += 1
            output.append(count)
        chi.append(np.average(output))
        print(np.average(output))
    m = np.std(chi)/np.sqrt(trial)
    if m <= 0.02:
        print("%d %s %.15f %s %.15f" % (L, 5 * ' ', np.average(chi), 5 * ' ', m))
        break
    else:
        print("%s %d %s %.15f %s %.15f" % (20*' ',L, 5 * ' ', np.average(chi), 5 * ' ', m))
        trial += 100
        a += 1

