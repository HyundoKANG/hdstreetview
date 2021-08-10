# -*- coding: utf-8 -*-

"""
Module : naversv
Author : Hyundo Kang

This is a module for downloading images from Naver Map Street View.
It's still being tested, so Its functions are incomplete and may have some errors.

"""

import os
import time
import itertools
from random import random
import pandas as pd
import requests
from PIL import Image
import shutil


def roadxy(directory, column_lat, column_lng):
    """
    DESCRIPTION
    Get the latitude and longitude data from CSV table.
    Only the WGS 1984 coordinate system(EPSG:4326) is available.

    VARIABLES
    - directory  : Path of the CSV file.
    - column_lat : Name of a column includes latitude values.
    - column_lng : Name of a column includes longitude values.

    """

    table  = pd.read_csv(
        directory, 
        header  = 0, 
        usecols = [column_lat, column_lng]
    )
    
    lat    = table[column_lat].values.tolist()
    lng    = table[column_lng].values.tolist()
    
    coords = list(zip(lat, lng))
    
    return coords



def nearby(lat, lng):
    """
    DESCRIPTION
    Get the nearest panorama's id from each of coordinates.

    VARIABLES
    - lat        : latitude.
    - lng        : longitude.

    """
    
    url    = "https://map.naver.com/v5/api/v2/nearby/{1:}/{0:}/3".format(lat, lng)

    resp   = requests.get(url, proxies=None)
    data   = resp.json()
    
    panoid = data['features'][0]['properties']['id']
    juso   = data['features'][0]['properties']['title']
    
    return panoid
    
    
    
def timeline(panoid):
    """
    DESCRIPTION
    This returns data about a bunch of panoramas
    taken in the similar location from one panorama.
    It's based on the timeline data from Naver Maps.

    VARIABLES
    - panoid     : The id of a reference panorama to find the timeline.

    """    


    url    = "https://panorama.map.naver.com/metadata/timeline/{0:}".format(panoid)
    resp   = requests.get(url, proxies=None)
    data   = resp.json()
    
    timeline = pd.DataFrame(data['timeline']['panoramas'][1:], columns=['panoid','lng','lat','date'])
    timeline['date']   = pd.to_datetime(timeline['date'])
    timeline['year']   = timeline['date'].dt.year
    timeline['month']  = timeline['date'].dt.month
    timeline['timeid'] = panoid
    
    del resp
    return timeline



    
def comparison(panoid, year1, year2, tolerance=1):
    """
    DESCRIPTION
    This returns information about panoramas taken in both years.
    If the panorama's timeline has no data for a specific year,
    This looks up the data for an year ago or an year later.

    VARIABLES
    - panoid     : THe id of a reference panorama to find the timeline.
    - year1      : The first year to compare.
    - year2      : The Second year to compare.
    
    """

    timelist = timeline(panoid)
    pair     = pd.DataFrame(columns=list(timelist.columns))
    years    = list(timelist['year'])
    firstyear  = year1
    secondyear = year2
    for i in range(tolerance+1):
        
        if year1 - i in years:
            firstyear = year1 - i
            break
        elif year1 + i in years:
            firstyear = year1 + i
            break
    
    for i in range(tolerance+1):

        if year2 - i in years:
            secondyear= year2 - i
            break
        elif year2 + i in years:
            secondyear= year2 + i
            break

    pair = pair.append(timelist[timelist['year'] == firstyear])
    pair = pair.append(timelist[timelist['year'] == secondyear])
    
    return pair

    
       
class tiles:
    
    
    def info(self, panoid):

        tiles_url = "https://panorama.pstatic.net/image/{0}/512/M/{1}/{2}/{3}"
        direction = ['l', 'f', 'r']
        grids     = list(itertools.product(direction, range(1,3), range(1,3)))

        tiles     = [(d, y, x, "%s_%s%d%d.jpg" % (panoid, d, x, y), tiles_url.format(panoid, d, y, x)) for d, y, x in grids]

        return tiles

    
    def download(self, panoid, directory):
        
        tiles = self.info(panoid)

        for i, (d, x, y, fname, url) in enumerate(tiles):

            while True:
                try:
                    resp = requests.get(url, stream=True)
                    break
                except requests.ConnectionError:
                    print("ConnectionError. Trying again in 5 seconds.")
                    time.sleep(5)

            with open(directory + fname, 'wb') as out_file:
                shutil.copyfileobj(resp.raw, out_file)
            del resp

            time.sleep(random()/10)


    def stitch(self, panoid, directory, final_directory, timeline=None):
        
        tiles = self.info(panoid)

        tile_width  = 512
        tile_height = 512

        left  = Image.new('RGB', (2*tile_width, 2*tile_height))
        front = Image.new('RGB', (2*tile_width, 2*tile_height))
        right = Image.new('RGB', (2*tile_width, 2*tile_height))

        panorama = Image.new('RGB', (6*tile_width, 2*tile_height))

        for d, x, y, fname, url in tiles:

            x = x - 1
            y = y - 1

            if d == 'l':

                fname = directory + fname
                tile  = Image.open(fname)

                left.paste(im=tile, box=(x*tile_width, y*tile_height))

            elif d == 'f':

                fname = directory + fname
                tile  = Image.open(fname)

                front.paste(im=tile, box=(x*tile_width, y*tile_height))

            elif d == 'r':

                fname = directory + fname
                tile  = Image.open(fname)

                right.paste(im=tile, box=(x*tile_width, y*tile_height))

        panorama.paste(im=left, box=(0, 0))
        panorama.paste(im=front, box=(2*tile_width, 0))
        panorama.paste(im=right, box=(4*tile_width, 0))

        
        if timeline is None:
            
            panorama.save(final_directory + ("%s.jpg" % panoid))
            
        else:
            
            timeid = timeline['timeid'].values[timeline['panoid'] == panoid][0]
            year   = timeline['year'].values[timeline['panoid'] == panoid][0]
            panorama.save(final_directory + ("[%s][%s]%s.jpg" % (timeid, year, panoid)))

        del panorama


    def delete(self, panoid, directory):
        
        tiles = self.info(panoid)
        
        for d, x, y, fname, url in tiles:
            os.remove(directory + fname)
