# -*- coding: utf-8 -*-

"""
Module : csv2naver
Author : Hyundo Kang

This is a batch tool for downloading street view images from Naver Map.

"""

from . import naversv as sv
from tqdm import tqdm
from random import random
import pandas as pd
import time

def csv2naver(csv, path, column, year=None):

    final = path + "final/"
 
    if not os.path.isdir(final):
        os.mkdir(final)
   
    col_lat   = column[0]
    col_lng   = column[1]
    year1     = year[0]
    year2     = year[1]
    
    coordlist = sv.roadxy(csv, col_lat, col_lng)
    
    panoids   = []
 

    for lat, lng in tqdm(coordlist):
        
        panoid = sv.nearby(lat, lng)
        panoids.append(panoid)
        time.sleep(random()/10)        

    if year is not None:
        for i, panoid in tqdm(enumerate(panoids)):

            if i == 0:
                pair = sv.comparison(panoid, year1, year2)
            else:
                temp = sv.comparison(panoid, year1, year2)
                pair = pd.concat([pair, temp])

            time.sleep(random()/10)        
        
        pair['counts'] = pair.groupby(['timeid'])['panoid'].transform('count')
        pair2 = pair[pair['counts']>1]

        panoids = pair2['panoid'].values.tolist()

    tiles = sv.tiles()        

    
    for panoid in tqdm(panoids):

        tiles.download(panoid, path)

    for panoid in tqdm(panoids):
        if year is not None:
            tiles.stitch(panoid, path, final, timeline=pair2)
        else:
            tiles.stitch(panoid, path, final)

    for panoid in tqdm(panoids):

        try:
            tiles.delete(panoid, path)
        except:
            pass      
