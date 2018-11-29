# -*- coding: utf-8 -*
from __future__ import division
from math import *
RADIAN_DE_LA_TERRE=6371

def dst(latitude,longitude,azimut,distance):
    #transformation des valeurs de degré en radian
    rLat=radians(latitude)
    rLong=radians(longitude)
    rAzimut=radians(azimut)
    quotient=distance/RADIAN_DE_LA_TERRE

    #calcul de la latitude et de la longitude du second point
    rLat2=asin(sin(rLat)*cos(quotient)+cos(rLat)*sin(quotient)*cos(rAzimut))
    param1=cos(quotient)-sin(rLat)*sin(rLat2)
    param2=sin(rAzimut)*sin(quotient)*cos(rLat)
    rLong2=rLong+atan2(param2,param1)

    #transformation des valeurs de radian en degré
    return degrees(rLat2),degrees(rLong2)
    
