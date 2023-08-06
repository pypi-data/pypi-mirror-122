# -*- coding: utf-8 -*-
from .config import load_cima_h
CIMA_H = load_cima_h()
# Taux d'intérêt
i = 0.035
# Facteur d'actualisation
v = 1/(1+i)

def lx(x):
    """Nombre de survivants  à l'âge x dans la TM.

    Args:
        x: l'âge.
    Returns:
        Nombre de survivants à l'âge x.
    """
    rec = next((item for item in CIMA_H if item['age']==x), None)
    return 0 if rec is None else rec['lx']


def dx(x):
    """Nombre de décès é à l'âge x dans la TM.

    Args:
        x: l'âge.
    Returns:
        Nombre de décès à l'âge x.
    """
    rec = next((item for item in CIMA_H if item['age']==x), None)
    return 0 if rec is None else rec['dx']


def W():
    """L'âge où il n'y a plus de survivant dans la table de mortalité

    Returns:
        L'âge où il n'y a plus de survivant dans la table de mortalité.
    """
    rec = next((item for item in CIMA_H if item['lx']==0), None)
    return 0 if rec is None else rec['age']


def qx(x):
    """Probabilité de décès entre les âges x et x+1.

    Args:
        x: l'âge.
    Returns:
        Probabilité de décès entre les âges x et x+1.
    """
    return dx(x)/lx(x)


def Cx(x):
    """Nombre de décès actualisé à l'âge x.

    Args:
        x: l'âge.
    Returns:
        Le nomre de décès actualisé à l'âge x.
    """
    return dx(x)*v**(x+0.5)

"""
Nombre de survivants actualisés
"""
def Dx(x):
    """Nombre de survivants actualisés.

    Args:
        x: l'âge.
    Returns:
        Nombre de survivants actualisés.
    """
    return lx(x)*v**x

def Mx(x):
    return sum([Cx(x) for x in range(x, W())])

def Rx(x):
    return sum([Mx(x) for x in range(x, W())])

def Sx(x): 
    return sum([Nx(x) for x in range(x, W())])

def Nx(x):
    return sum([Dx(x) for x in range(x, W())])

"""
Valeur actuelle certaine pour une rente certaine de 1F payable d'avance sur k années
"""
def A_k(k):
    return v*(1-v**k)/(1-v)

"""
Valeur actuelle probable à l'âge x sur n années
"""
def A_xn(x,n):
    return (Nx(x)-Nx(x+n))/Dx(x)

"""
Capital différé à l'âge x sur n années
"""
def nEx(x):
    return Dx(x+n)/Dx(x)




if __name__ == '__main__':
    pass