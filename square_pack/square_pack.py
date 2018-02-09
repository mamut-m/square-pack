'''
Created on Feb 2, 2018

@author: murschitzm
'''


from math import sqrt, floor
import doctest

def calc(ns,w,h):
    """ calculate the size of squares and the grid (nx times ny cells) they can be placed in to optimaly fill a rectangle
    @param ns: number of squares
    @param w: width of the available space in pixels
    @param h: height of the available space in pixels
    @return: (square length(=height) in pixels, number of columns, and number of rows)
    Example:
    >>> calc(6, 640 ,480)
    (213, 3, 2)
     """
    if ( ns > w * h ):
        raise ValueError("can not fit " + str(ns) + " squares (of a at least 1x1 px) in an image of size " + str(w) + " x " + str(h))
    if ( ns == 0 ):
        raise ValueError("can not fit 0 squares")
    a_opt = int(floor(sqrt(float(w*h)/ns)))

    for a in range(a_opt,0,-1):
        nx = int(floor(w/a)) 
        ny = int(floor(h/a))
        if nx > 0 and ny > 0 and nx * ny >= ns: 
            break   
    return a, nx, ny 

if __name__ == '__main__':
    doctest.testmod() #runs a simple doctest
    


    
    
