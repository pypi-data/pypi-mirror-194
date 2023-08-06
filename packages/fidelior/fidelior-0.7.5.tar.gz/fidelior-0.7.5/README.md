FIDELIOR
=======

**FIDELIOR** (_latin_: more reliable) stands for **FInite-Difference-Equation LInear OperatoR package**.

The purpose of _FIDELIOR_ is to help with numerical solution of **partial differential equations (PDE)**. In order to obtain a numerical solution, continuous functions and differential operators that enter a PDE are discretized. There are two main approaches to such discretization: the **finite-difference (FD) method** and the **finite-element method (FEM)**. The main idea of the FD approach is to represent various differential operators entering the PDE as _finite differences_. A linear PDE is represented as a linear system L**u** = **f**, where matrix L represents the action of a differential operator, vector **u** is the discretized unknown function, and **f** is the discretized inhomogeneous part. In FEM, the differential operators do not have to be supplied by the user; the FD equations emerge by writing the PDE in the _weak form_. Obtaining the discretized equation in FEM may be cumbersome. To help with discretization, there is an excellent Python package [FEniCS](https://fenicsproject.org) which allows the user to automate the generation of linear systems (such as one given above) from the weak forms. FEniCS provides much flexibility with finite element choice, and thus is a rather large project. The present package, _FIDELIOR_, strives to do for the FD method the same that FEniCS does for FEM, namely to provide flexibility and convenience in setting up the FD schemes. The user must have the knowledge of how the differential operators are discretized. Some help, however, is provided with [automatic](https://gitlab.com/nleht/fidelior/-/tree/master/old/src/fidelior/autoschemes.py) generation of FD schemes _(**NOTE**: this was done for the old interface, and I am in the process of rewriting it!)_. In case of a time-dependent PDE, the user must also provide the time-stepping scheme. We should point out that the **stability** of a time-stepping scheme is not guaranteed even in the FEM method, and this process is not automated even in FEniCS.

The _FIDELIOR_ package has undergone some changes from the [previous version](https://gitlab.com/nleht/fidelior/-/releases/v0.6). The most important change was to introduce a better and simpler interface, which allows much more flexibility in setting up complicated boundary conditions and other constraints. Some of the new interface, e.g., the use of `==` operator for setting up equations, was inspired by FEniCS. At the same time, the code became shorter, as some non-essential features were dropped. However, the functionality of the package did not suffer.

A good introduction to FD methods may be found, e.g., in
* Randall J. LeVeque (2007), _Finite Difference Methods for Ordinary and Partial Differential Equations_, SIAM, Philadelphia.

_FIDELIOR_ requires Python3, NumPy and SciPy to run and Matplotlib if you would like to plot the results. Plotting, in particular, is used in the [examples](https://gitlab.com/nleht/fidelior/-/tree/master/examples/).

Here is a quick demo of what _FIDELIOR_ can do. The following is a [complete program](https://gitlab.com/nleht/fidelior/-/tree/master/examples/quick_test.py) that sets up and solves a Poisson equation in 2D on a 100x100 cell grid and plots and checks the result:
```python
import numpy as np
from matplotlib import pyplot as  plt
import fidelior as fdo
from fidelior import end, half

# Set up the simple geometry
N = 100
x1 = np.arange(N+1)-N/2; y1 = x1
box = fdo.Box((N, N))
x, y = box.ndgrid(x1, y1)[0:end, 0:end]

# Charge density
x0 = 25; y0 = -25; w = 10;
rho = fdo.exp(-((x-x0)**2+(y-y0)**2)/(2*w**2))

# Unknown electrostatic potential
phi = box.sym('phi')[0:end, 0:end]

# These functions use 'fdo.diff(u, axis)' which is itself defined as
# def diff(u, axis): u.shift(half, axis) - u.shift(-half, axis)
def grad(u):
    return (fdo.diff(u, axis=0), fdo.diff(u, axis=1))
def div(A):
    return fdo.diff(A[0], axis=0) + fdo.diff(A[1], axis=1)

# Unknown electric field
E = grad(-phi)

# Boundary conditions (constraints with which the equation will be solved)
(phi[[0, end], :] == 0).constraint('Dirichlet') # on left and right edges
(E[1][1:end-1, [half, end-half]] == 1).constraint('Neumann') # Ey = 1 on top and bottom

# Set up and solve the equation
phiv = (div(E) == rho).solve()

# Plot and check the error
plt.pcolor(x1, y1, phiv[:,:].T, shading='auto')
plt.gca().set_aspect('equal')
print('Error =', fdo.max(fdo.abs(div(grad(-phiv))-rho)))
```
Notice that this script does not use any pre-defined finite-difference approximations to differential operators or boundary conditions. Operators `grad`, `div` and custom boundary conditions are _defined_ by the user within these few lines.

In summary, _FIDELIOR_ allows the user
1. to represent known and unknown functions as discretized values on a rectangular grid;
2. to specify custom finite-difference operators which represent approximations to differential operators;
3. to specify constraints (boundary conditions) on unknown discretized functions;
4. to set up and solve linear PDE which take into account the given constraints.

# Installation

_FIDELIOR_ is now available at Python Package Index [PyPI](https://pypi.org/project/fidelior/). You can install it by typing the following at the command prompt:
```
pip install fidelior
```
Use `pip3` if you still have Python2 on your system. Or, if you prefer to use the absolutely latest version, download `fidelior` folder from [`src/`](https://gitlab.com/nleht/fidelior/-/tree/master/src) directory and put it in the path where Python looks for packages (`sys.path`).

After you have installed _FIDELIOR_, you can try running the above script to make sure it works.

# Start using _FIDELIOR_

Capabilites of _FIDELIOR_ are described in the [manual](https://gitlab.com/nleht/fidelior/-/tree/master/doc/) and their usage is demonstrated by the included [examples](https://gitlab.com/nleht/fidelior/-/tree/master/examples/).

# License

[![License: CC BY-ND 4.0](https://img.shields.io/badge/License-CC_BY--ND_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nd/4.0/)

The project is free to use, however, it is protected by copyright. If you would like to use it in your publication, please cite the project webpage (https://gitlab.com/nleht/fidelior). A journal article is in preparation, and when it is available, it will have to be cited. If you have any suggestions for improvement (new features, bug fixes, etc.) please contact the the author, [Nikolai G. Lehtinen](https://gitlab.com/nleht), at ![his email address](https://gitlab.com/nleht/fidelior/-/raw/master/email.png).

The [examples](https://gitlab.com/nleht/fidelior/-/tree/master/examples/) are distributed under a less restrictive [CC BY 4.0 License](https://creativecommons.org/licenses/by/4.0/) ![License: CC BY 4.0](https://licensebuttons.net/l/by/4.0/80x15.png).

# Acknowledgements

This study was supported by the European Research Council under the European Union's Seventh Framework Programme (FP7/2007-2013)/ERC grant agreement number 320839 and the Research Council of Norway under contracts 208028/F50, 216872/F50 and 223252/F50 (CoE). 

# Older versions

See also the [previous interface version](https://gitlab.com/nleht/fidelior/-/tree/master/old/src/fidelior) and the [demonstration of some of its capabilities](https://gitlab.com/nleht/fidelior/-/tree/master/old/examples). Some of the examples [were converted to the new interface](https://gitlab.com/nleht/fidelior/-/tree/master/examples), others are in the process of such conversion.

The former location of the project was [here](https://gitlab.uib.no/BCSS-Q4/TRUMP) and then [here](https://git.app.uib.no/Nikolai.Lehtinen/TRUMP).

