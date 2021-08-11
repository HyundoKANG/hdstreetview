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
import os

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
 
    print("CSV파일의 좌표로부터 최근접 파노라마 ID를 조회합니다")
    for lat, lng in tqdm(coordlist):
        
        panoid = sv.nearby(lat, lng)
        panoids.append(panoid)
        time.sleep(random()/10)        

    if year is not None:
        print("설정한 연도에 해당하는 파노라마가 존재하는지 확인합니다")
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

    print("파노라마 ID로부터 2x2x3개의 타일을 다운로드합니다")
    for panoid in tqdm(panoids):

        tiles.download(panoid, path)

    print("타일을 이어붙여서 하나의 사진으로 저장합니다")
    for panoid in tqdm(panoids):
        if year is not None:
            tiles.stitch(panoid, path, final, timeline=pair2)
        else:
            tiles.stitch(panoid, path, final)

    print("타일을 삭제합니다")
    for panoid in tqdm(panoids):

        try:
            tiles.delete(panoid, path)
        except:
            pass      
