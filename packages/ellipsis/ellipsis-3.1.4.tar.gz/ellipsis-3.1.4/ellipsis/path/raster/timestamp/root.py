from ellipsis import sanitize
from ellipsis.util.root import getActualExtent
from ellipsis import apiManager
from ellipsis.util import loadingBar
from ellipsis.util import chunks
from ellipsis.util.root import reprojectRaster
from rasterio.io import MemoryFile

import json
import numpy as np
from io import BytesIO
import rasterio
import math
import tifffile
import threading
from PIL import Image
import geopandas as gpd
import datetime


def getDownsampledRaster(pathId, timestampId, extent, width, height, epsg=3857, style = None, token = None):
    return getSampledRaster(pathId, timestampId, extent, width, height, epsg, style, token)

def getSampledRaster(pathId, timestampId, extent, width, height, epsg=3857, style = None, token = None):
    bounds = extent
    token = sanitize.validString('token', token, False)
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    bounds = sanitize.validBounds('bounds', bounds, True)
    style = sanitize.validObject('style', style, False)
    epsg = sanitize.validInt('epsg', epsg, True)
    body = {'pathId':pathId, 'timestampId':timestampId, 'extent':bounds, 'width':width, 'height':height, 'style':style, 'epsg':epsg}
    r = apiManager.get('/path/' + pathId + '/raster/timestamp/' + timestampId + '/rasterByExtent', body, token, crash = False)
    if r.status_code != 200:
        raise ValueError(r.message)


    if type(style) == type(None):
        r = tifffile.imread(BytesIO(r.content))
    else:
        r = np.array(Image.open(BytesIO(r.content)))
    #tif also has bands in last channel
    r = np.transpose(r, [2,0,1])

    xMin = bounds['xMin']
    yMin = bounds['yMin']
    xMax = bounds['xMax']
    yMax = bounds['yMax']



    trans = rasterio.transform.from_bounds(xMin, yMin, xMax, yMax, r.shape[2], r.shape[1])

    return {'raster': r, 'transform':trans, 'extent': {'xMin' : xMin, 'yMin': yMin, 'xMax': xMax, 'yMax': yMax}, 'crs':"EPSG:" + str(epsg) }


def getValuesAlongLine(pathId, timestampId, line, token = None, epsg = 4326):
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    token = sanitize.validString('token', token, False)
    line = sanitize.validShapely('line', line, True)

    if line.type != 'LineString':
        raise ValueError('line must be a shapely lineString')

    temp = gpd.GeoDataFrame({'geometry':[line]})
    temp.crs = 'EPSG:' + str(epsg)
    temp = temp.to_crs('EPSG:4326')
    line = temp['geometry'].values[0]
    line = list(line.coords)
        
    x_of_line = [p[0] for p in line]
    y_of_line = [p[1] for p in line]

    #the first action is to cacluate a bounding box for the raster we need to retrieve
    xMin = min(x_of_line)
    xMax = max(x_of_line)
    yMin = min(y_of_line)
    yMax = max(y_of_line)

    #now we retrieve the needed raster we use epsg = 4326 but we can use other coordinates as well
    extent = {'xMin': xMin, 'xMax':xMax, 'yMin':yMin, 'yMax':yMax}

    size = 1000
    r = getSampledRaster(pathId = pathId, timestampId = timestampId, extent = extent, width = size, height = size, epsg=4326)
    raster = r['raster']

    memfile =  MemoryFile()
    dataset = memfile.open( driver='GTiff', dtype='float32', height=size, width=size, count = raster.shape[0], crs= r['crs'], transform=r['transform'])
    dataset.write(raster)

    values = list(dataset.sample(line))

    return values

    
    

def getRaster(pathId, timestampId, extent, style = None, threads = 1, token = None, showProgress = True, epsg = 3857):
    bounds = extent
    threads = sanitize.validInt('threads', threads, True)
    token = sanitize.validString('token', token, False)
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    bounds = sanitize.validBounds('bounds', bounds, True)
    style = sanitize.validObject('style', style, False)
    showProgress = sanitize.validBool('showProgress', showProgress, True)

        
    xMin = bounds['xMin']
    yMin = bounds['yMin']
    xMax = bounds['xMax']
    yMax = bounds['yMax']

    res = getActualExtent(xMin, xMax, yMin, yMax, 'EPSG:' + str(epsg))
    if res['status'] == '400':
        raise ValueError('Invalid epsg and extent combination')
        
    bounds = res['message']

    xMinWeb = bounds['xMin']
    yMinWeb = bounds['yMin']
    xMaxWeb = bounds['xMax']
    yMaxWeb = bounds['yMax']
    
    info = apiManager.get('/path/' + pathId, None, token)
    bands =  info['raster']['bands']
    if type(style) == type(None):
        num_bands = len(bands)
        dtype = info['raster']['format']
    else:
        num_bands = 4
        dtype = 'uint8'

    timestamps =  info['raster']['timestamps']
    all_timestamps = [item['id'] for item in timestamps]
    if not timestampId in all_timestamps:
        raise ValueError('given timestamp does not exist')
    
    zoom = next(item for item in timestamps if item["id"] == timestampId)['zoom']

    body = {'style':style}

    LEN = 2.003751e+07

    x_start = 2**zoom * (xMinWeb + LEN) / (2* LEN)
    x_end = 2**zoom * (xMaxWeb + LEN) / (2* LEN)
    y_end = 2**zoom * (LEN - yMinWeb) / (2* LEN)
    y_start = 2**zoom * (LEN - yMaxWeb) / (2* LEN)

    x1_osm = math.floor(x_start)
    x2_osm = math.floor(x_end)
    y1_osm = math.floor(y_start)
    y2_osm = math.floor(y_end)
    
    x_tiles = np.arange(x1_osm, x2_osm+1)
    y_tiles = np.arange(y1_osm, y2_osm +1)
    
    r_total = np.zeros((num_bands, 256*(y2_osm - y1_osm + 1) ,256*(x2_osm - x1_osm + 1)), dtype = dtype)
    
    tiles = []            
    for tileY in y_tiles:
        for tileX in x_tiles:
            tiles = tiles + [(tileX, tileY)]
    def subTiles(tiles):
            N = 0
            for tile in tiles:
                tileX = tile[0]
                tileY = tile[1]
                x_index = tileX - x1_osm
                y_index = tileY - y1_osm
                
                r = apiManager.get('/path/' + pathId + '/raster/timestamp/' + timestampId + '/tile/' + str(zoom) + '/' + str(tileX) + '/' + str(tileY), body, token, False)

                if r.status_code == 403:
                        raise ValueError('insufficient access')
                if r.status_code != 200:
                        r = np.zeros((num_bands,256,256))
                else:
                    if type(style) == type(None):
                        r = tifffile.imread(BytesIO(r.content))
                    else:
                        r = np.array(Image.open(BytesIO(r.content)))
                        r = np.transpose(r, [2,0,1])

                r = r.astype(dtype)
                r_total[:,y_index*256:(y_index+1)*256,x_index*256:(x_index+1)*256] = r
                if showProgress:
                    loadingBar(N, len(tiles))
                N = N + 1
            

    size = math.floor(len(tiles)/threads) + 1
    tiles_chunks = chunks(tiles, size)
    prs = []
    for tiles in tiles_chunks:
        pr = threading.Thread(target = subTiles, args =(tiles,), daemon=True)
        pr.start()
        prs = prs + [pr]
    for pr in prs:
        pr.join()
        
    min_x_index = int(math.floor((x_start - x1_osm)*256))
    max_x_index = max(int(math.floor((x_end- x1_osm)*256 + 1 )), min_x_index + 1 )
    min_y_index = int(math.floor((y_start - y1_osm)*256))
    max_y_index = max(int(math.floor((y_end- y1_osm)*256 +1)), min_y_index + 1)

    r_total = r_total[:,min_y_index:max_y_index,min_x_index:max_x_index]

    mercatorExtent =  {'xMin' : xMinWeb, 'yMin': yMinWeb, 'xMax': xMaxWeb, 'yMax': yMaxWeb}
    if epsg == 3857:
        trans = rasterio.transform.from_bounds(xMinWeb, yMinWeb, xMaxWeb, yMaxWeb, r_total.shape[2], r_total.shape[1])
    
        return {'raster': r_total, 'transform':trans, 'extent':mercatorExtent, 'epsg':3857}
    else:
        return reprojectRaster(r = r_total, sourceExtent = mercatorExtent, targetExtent = extent, targetWidth=r_total.shape[2], targetHeight=r_total.shape[1], sourceEpsg = 3857, targetEpsg= epsg, interpolation = 'nearest')


def analyse(pathId, timestampIds, geometry, returnType= 'all', approximate=True, token = None, epsg = 4326):
    token = sanitize.validString('token', token, False)
    pathId = sanitize.validUuid('pathId', pathId, True)    
    timestampIds = sanitize.validUuidArray('timestampIds', timestampIds, True)    
    approximate = sanitize.validBool(approximate, approximate, True)    
    geometry = sanitize.validShapely('geometry', geometry, True)
    returnType = sanitize.validString('returnType', returnType, True)

    temp = gpd.GeoDataFrame({'geometry':[geometry]})
    temp.crs = 'EPSG:' + str(epsg)
    temp = temp.to_crs('EPSG:4326')
    geometry = temp['geometry'].values[0]

    try:
        sh = gpd.GeoDataFrame({'geometry':[geometry]})
        geometry =sh.to_json(na='drop')
        geometry = json.loads(geometry)
        geometry = geometry['features'][0]['geometry']
    except:
        raise ValueError('geometry must be a shapely geometry')


    body = {'timestampIds':timestampIds, 'geometry':geometry, 'approximate':approximate, returnType:returnType}
    r = apiManager.get('/path/' + pathId + '/raster/timestamp/analyse', body, token)
    return r


def add(pathId, token, description= None, date ={'from': datetime.datetime.now(), 'to': datetime.datetime.now()}):
    

    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    date = sanitize.validDateRange('date', date, True)    
    description = sanitize.validString('description', description, False)    

    body = { 'date': date, 'description': description}    
    r = apiManager.post('/path/' + pathId + '/raster/timestamp'  , body, token)
    return r
    
def edit(pathId, timestampId, token, date=None, description= None):

    
    
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    description = sanitize.validString('description', description, False)    
    date = sanitize.validDateRange('date', date, False)    

    body = {'date':date, 'description': description}    
    r = apiManager.patch('/path/' + pathId + '/raster/timestamp/' + timestampId  , body, token)
    return r

def getBounds(pathId, timestampId, token = None):
    token = sanitize.validString('token', token, False)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    r = apiManager.get('/path/' + pathId + '/raster/timestamp/' + timestampId + '/bounds'  , None, token)
    r = {'id': 0, 'properties':{}, 'geometry':r}

    r  = gpd.GeoDataFrame.from_features([r])
    r = r.unary_union
    return r

def activate(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    r = apiManager.post('/path/' + pathId + '/raster/timestamp/' + timestampId + '/activate'  , None, token)
    return r

def deactivate(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    r = apiManager.post('/path/' + pathId + '/raster/timestamp/' + timestampId + '/deactivate'  , None, token)
    return r


def delete(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  

    r = apiManager.delete('/path/' + pathId + '/raster/timestamp/' + timestampId  , None, token)
    return r


def trash(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    body = {'trashed' : True}
    r = apiManager.put('/path/' + pathId + '/raster/timestamp/' + timestampId + '/trashed'  , body, token)
    return r

    
def recover(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    body = {'trashed' : False}
    r = apiManager.put('/path/' + pathId + '/raster/timestamp/' + timestampId + '/trashed'  , body, token)
    return r
