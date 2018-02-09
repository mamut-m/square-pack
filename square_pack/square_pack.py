'''
Created on Feb 2, 2018

@author: murschitzm
'''

import cv2
import numpy as np
from math import sqrt, ceil, floor
import doctest
frame =0

def _visualize(nx,ny,ns,a,w,h,save =False):
    """
    @param nx: number of columns
    @param ny: number of rows
    @param ns: number of squares
    @param a: lenght of one side of the square in pixels
    @param h: the height of the available space in pixels
    @param w: the width of the square in pixels
    """
    global frame
    img = np.zeros((h,w,3),dtype=np.uint8)
    #hue in  [0,179] sat in [0,255], value in [0,255]
    max_hue = 179
    min_hue = 0;
    hue_step = max(max_hue/ns,1);
    hue=min_hue;
    cnt=0
    for iy in range(ny+1):
        for ix in range(nx+1):# we draw one grey rect more to easily see errors
            if iy < ny and ix < nx and  cnt < ns:
                hue = (hue + hue_step) % (max_hue-1)
                color = cv2.cvtColor(np.array([[(hue,255,255)]],dtype=np.uint8),cv2.COLOR_HSV2BGR)
                color = color[0,0].astype("int")
                cv2.rectangle(img, (ix*a,iy*a), ((ix+1)*a-1,(iy+1)*a-1), color, cv2.cv.CV_FILLED )
                cv2.putText(img, str(cnt), org=(ix*a,(iy+1)*a-1) ,fontFace= cv2.FONT_HERSHEY_PLAIN, fontScale=0.75, color=(0,0,0))
                cnt = cnt +1
            cv2.rectangle(img, (ix*a,iy*a), ((ix+1)*a-1,(iy+1)*a-1), (128,128,128) ) 
    if save: 
        cv2.imwrite("data/out_%05i.png" % (frame ),img)#_%ix%i_a%d_r%i#,nx,ny,a, _calc_rest_area(a,ns,h,w)
    frame = frame +1
    cv2.imshow("res", img)
    cv2.waitKey(1)
    
def _calc_rest_area(a,ns,h,w):
    """ Calculates the rest area which is to be minimized
    @param a: the length of one square side
    @param ns: the number of squares
    @param h: the height of the available space in pixels
    @param w: the width of the square in pixels
    @return The rest area in pixels^2 
    """
    return h*w - a**2*ns 

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


    

def _calc_brute_force(ns,w,h):
    """
    function to check that all is correct. not good at all but definitley correct
    """
    best = [float("inf"),None,None,None]
    for nr in range(0,ns):
        for rx in range(0,w):
            for ry in range(0,h):
                nxo = sqrt((ns+nr) * (w - rx)/float(h - ry))   
                ny = int(ceil((ns + nr)/nxo))
                nx = int(ceil(nxo))
                a  = int(floor((w -  rx)/nx))
                cost = _calc_rest_area(a,ns,h,w)
                if cost < best[0]:
                    best = (cost, a, nx, ny, nxo)
    cost, a, nx, ny, nxo = best
    print nxo
    return a, nx, ny 


def test2():
    for h,w  in [(480, 640)]:
        for ns in range(1,h*w/20**2):
            f=w/float(h)
            a, nx, ny = calc(ns,w,h)
            print "a", a, "(" , nx, "x", ny, ") rects", " with ", nx*ny-ns," that are not used" 
            _visualize(nx,ny,ns,a,w,h,save=True)

def test_vis():
    ns=45; 
    nx= 10; ny=5; a=50; 
    _visualize(nx,ny,ns,a)

if __name__ == '__main__':
    doctest.testmod() #runs a simple doctest
    test2()
    
    
