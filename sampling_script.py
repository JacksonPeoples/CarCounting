#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 13:38:23 2021

@author: jacksonpeoples
"""


import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

np.random.seed(42)

## First will create quadrants to weight sampling probability based on label distribution
## returns list of probabilities in top-left, top-right, bottom-left, bottom-right

def quad_prob(anno):
    '''
    

    Parameters
    ----------
    anno : array
        Array/image where nonzero elements represent car centers.

    Returns
    -------
    list
        List of portion of cars in given quadrant
        in order: top-left, top-right, bottom-left, bottom-right.

    '''
    #create quadrants
    h = anno.shape[0]
    w = anno.shape[1]
    mh = int(.5*h)
    mw = int(.5*w)
    
    q1 = anno[0:mh, 0:mw]
    q2 = anno[0:mh, mw:-1]
    q3 = anno[mh:-1, 0:mw]
    q4 = anno[mh:-1, mw:-1]
    
    # compute the probability distributions
    p1 = round((np.count_nonzero(q1)/np.count_nonzero(anno)), 2)
    p2 = round((np.count_nonzero(q2)/np.count_nonzero(anno)), 2)
    p3 = round((np.count_nonzero(q3)/np.count_nonzero(anno)), 2)
    p4 = round((np.count_nonzero(q4)/np.count_nonzero(anno)), 2)
    
    #ensure that probs add up to one
    if sum([p1,p2,p3,p4]) > 1:
        p4 -= (sum([p1,p2,p3,p4])-1)
    if sum([p1,p2,p3,p4]) < 1:
        p4 += (1 - sum([p1,p2,p3,p4]))
        
    return [p1, p2, p3, p4]

# create a list of xy coords that will represent the top left corner of 400x400 tiles for training.

def choose_xy(img, p, n):
    '''
    

    Parameters
    ----------
    img : image
        aerial image of cars.
    p : list
        list of proportions from quad_prob function. 4 floats, must add
        up to 1
    n : int
        number of coordinates to be produced.

    Returns
    -------
    coord_list : list
        List of tuples representing the upper left corner of tiles
        to be sampled from image. Drawn randomly with probabilities weighted
        based on proportions generated in quad_anno.

    '''
    h = img.shape[0]
    w = img.shape[1]
    mh = int(.5*h)
    mw = int(.5*w)
    # create list of quadrant each coordinate will be sampled from
    quad_list = list(np.random.choice([1,2,3,4], n, True, p))
    coord_list =[]
    #draw random coordinates from given list.
    for n in quad_list:
        if n == 1:
            x = np.random.randint(0,mw-400)
            y = np.random.randint(0,mh-400)
            coord_list.append((x,y))
        elif n == 2:
            x = np.random.randint(mw,w-400)
            y = np.random.randint(0,mh-400)
            coord_list.append((x,y))
        elif n ==3:
            x = np.random.randint(0,mw-400)
            y = np.random.randint(mh,h-400)
            coord_list.append((x,y))
        else:
            x = np.random.randint(mw,w-400)
            y = np.random.randint(mh,h-400)
            coord_list.append((x,y))
    return coord_list

def tiles(img, coords, tag, CWD):
    '''
    

    Parameters
    ----------
    img : image/array
        image.
    coords : list
        list of coordinates representing upper left corner of tiles to be
        sampled.

    Returns
    -------
    None.
    saves tiles to folder 'Data'

    '''
    filepath = CWD+'/Data/Images/'
    count = 1
    for x,y in coords:
        tile = img[y:y+400,x:x+400,:]
        filepath_tile = os.path.join(filepath, '{tag_no}_img_train{n}.jpg'.format(tag_no=tag, n=count))
        matplotlib.image.imsave(filepath_tile, tile)
        count += 1
    return

def annotate_text(anno, coords, tag, CWD):
    '''
    

    Parameters
    ----------
    anno : array/img
        Array where nonzero elements represent car centers.
    coords : list
        list of coordinates representing top left corner of tiles sampled.

    Returns
    Saves txt file to folder 'Data'
    -------
    None.

    '''
    count = 1 
    for x,y in coords:
        anno_tile = anno[y:y+400,x:x+400]
        yc, xc = np.nonzero(anno_tile)
        
        c_list = []
        for i in range(len(xc)):
            c_list.append((xc[i],yc[i]))
        
        with open(CWD+'/Data/Labels/{tag_no}_img_train{n}.txt'.format(tag_no=tag, n=count), 'w') as f:
            for c in c_list:
                content = '0 {x} {y} {width} {height}'.format(x=c[0]/400,
                                                                        y=c[1]/400,
                                                                        width=.05,
                                                                        height=.05)
                f.write(content + os.linesep)
        f.close()
        count+=1
    return



def main():
    n_tiles = int(input('Number of samples per image?'))
    cwd = os.getcwd()
    path = cwd+'/Raw_Image/'
    img_count = 1
    for filename in os.listdir(path):
        if filename.startswith('_'):
            img_path = path+filename
            anno_path = path+'anno'+filename
            TAG = img_count
            
            img = plt.imread(img_path)
            anno = plt.imread(anno_path)
            
            bin_anno = anno[:,:,0]
            
            p = quad_prob(bin_anno)
            coord_list = choose_xy(img, p, n_tiles)
            tiles(img, coord_list, TAG, cwd)
            annotate_text(bin_anno, coord_list, TAG, cwd)
            print(str(img_count)+' IMAGE(S) DONE')
            img_count += 1
            
        else:
            continue
    print('Completed')
        
if __name__ == "__main__":
    main()