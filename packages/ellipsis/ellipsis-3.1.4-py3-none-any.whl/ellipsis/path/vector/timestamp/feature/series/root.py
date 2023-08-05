from ellipsis import apiManager
from ellipsis import sanitize
from ellipsis.util.root import recurse
from ellipsis.util.root import chunks
from ellipsis.util.root import loadingBar
from ellipsis.util.root import stringToDate


import numpy as np
import pandas as pd

def get(pathId, timestampId, featureId, pageStart = None, dateTo = None, userId = None, seriesProperty = None, deleted = False, listAll= True,  token = None ):    
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    featureId = sanitize.validUuid('featureId', featureId, True) 
    pageStart = sanitize.validUuid('pageStart', pageStart, False)
    dateTo = sanitize.validDate('dateTo', dateTo, False)
    userId = sanitize.validUuid('userId', userId, False)
    seriesProperty = sanitize.validString('seriesProperty', seriesProperty, False)
    deleted = sanitize.validBool('deleted', deleted, True)
    listAll = sanitize.validBool('listAll', listAll, True)
    token = sanitize.validString('token', token, False)

    body = {'pageStart' : pageStart, 'dateTo' : dateTo, 'userId' : userId, 'seriesProperty': seriesProperty, 'deleted': deleted, 'listAll': listAll}
    
    def f(body):
        r = apiManager.get('/path/' + pathId + '/vector/timestamp/' + timestampId + '/feature/' + featureId + '/series/element', body, token)
        return r
    
    r = recurse(f, body, listAll)
    series = r['result']
    series = [ { 'id':k['id'], 'property': k['property'], 'value': k['value'], 'date': stringToDate(k['date']) } for k in series]
    series = pd.DataFrame(series)
    r['result'] = series

    return r
    

def info(pathId, timestampId, featureId, token = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    featureId = sanitize.validUuid('featureId', featureId, True) 
    token = sanitize.validString('token', token, False)
    
    r = apiManager.get('/path/' + pathId + '/vector/timestamp/' + timestampId + '/feature/' + featureId + '/series/info', None, token)
    r['dateFrom'] = stringToDate(r['dateFrom'])
    r['dateTo'] = stringToDate(r['dateTo'])
    return r


def add(pathId, timestampId, featureId, seriesData, token, showProgress = True):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    featureId = sanitize.validUuid('featureId', featureId, True) 
    token = sanitize.validString('token', token, True)
    seriesData = sanitize.validDataframe('seriesData', seriesData, True)
    showProgress = sanitize.validBool('showProgress', showProgress, True)

    if 'date' in seriesData.columns:
        if str(seriesData['date'].dtypes) == 'datetime64[ns]':
            seriesData['date'] = seriesData['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
            dates = list(seriesData['date'])
            del seriesData['date']
        else:
           raise  ValueError('datetime column must be of type datetime')
    else:
           raise  ValueError('seriesData must have a column datetime of type datetime')


    for c in seriesData.columns:
            seriesData[c] = seriesData[c].astype(float)
        
    values = []
    for i in np.arange(seriesData.shape[0]):
        for c in seriesData.columns:
                value = seriesData[c].values[i]
                if not np.isnan(value):
                    values = values + [{'property':c, 'value':seriesData[c].values[i], 'date':dates[i]}]


    chunks_values = chunks(values)
    N = 0
    r_total = []
    for values_sub in chunks_values:
        body = { "values":values_sub}
        r = apiManager.post("/path/" + pathId + "/vector/timestamp/" + timestampId  + '/feature/' + featureId + '/series/element', body, token)
        
        r_total = r_total + r
        if len(chunks_values) >1 and showProgress:
            loadingBar(N*3000 + len(values_sub), len(values))
        N = N+1
    return r_total




def trash(pathId, timestampId, featureId, seriesIds, token, showProgress = True):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    featureId = sanitize.validUuid('featureId', featureId, True) 
    token = sanitize.validString('token', token, True)
    seriesIds = sanitize.validUuidArray('seriesIds', seriesIds, True)
    showProgress = sanitize.validBool('showProgress', showProgress, True)

    chunks_values = chunks(seriesIds)
    N = 0
    for seriesIds_sub in chunks_values:
        body = { "seriesIds":seriesIds_sub, "trashed": True}
        r = apiManager.put("/path/" + pathId + "/vector/timestamp/" + timestampId  + '/feature/' + featureId + '/series/element/trashed', body, token)
        if showProgress:
            loadingBar(N*3000 + len(seriesIds_sub), len(seriesIds))
        N = N+1
    return r

def recover(pathId, timestampId, featureId, seriesIds, token, showProgress = True):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    featureId = sanitize.validUuid('featureId', featureId, True) 
    token = sanitize.validString('token', token, True)
    seriesIds = sanitize.validUuidArray('seriesIds', seriesIds, True)
    showProgress = sanitize.validBool('showProgress', showProgress, True)

    chunks_values = chunks(seriesIds)
    N = 0

    for seriesIds_sub in chunks_values:
        body = { "seriesIds":seriesIds_sub, "trashed": False}
        r = apiManager.put("/path/" + pathId + "/vector/timestamp/" + timestampId  + '/feature/' + featureId + '/series/element/trashed', body, token)
        if showProgress:           
            loadingBar(N*3000 + len(seriesIds_sub), len(seriesIds))
        N = N+1
    return r


def changelog(pathId, timestampId, featureId, listAll = False, actions = None, userId = None, pageStart = None, token = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    featureId = sanitize.validUuid('featureId', featureId, True) 
    listAll = sanitize.validBool('listAll', listAll, True) 
    actions = sanitize.validStringArray('actions', actions, False) 
    userId = sanitize.validUuid('userId', userId, False) 
    pageStart = sanitize.validUuid('pageStart', pageStart, False) 
    token = sanitize.validString('token', token, False)

    body = {'userId': userId, 'actions':actions, 'pageStart':pageStart}

    def f(body):
        r = apiManager.get('/path/' + pathId + '/vector/timestamp/' + timestampId + '/feature/' + featureId + '/series/changelog', body, token)
        return r
        
    r = recurse(f, body, listAll)

    r['result'] = [{**x, 'date':stringToDate(x['date'])} for x in r['result']]
    return r

    
    
