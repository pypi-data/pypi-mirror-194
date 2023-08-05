
from ellipsis import sanitize
from ellipsis import apiManager

def get(token):
    r = apiManager.get('/path/vector/timestamp/order', None, token)
    return r

def add(pathId, timestampId, token, extent = None, uploadId = None):
    
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    extent = sanitize.validBounds('extent', extent, False)
    uploadId = sanitize.validUuid('uploadId', uploadId, False)

    body = {'uploadId': uploadId, 'extent':extent, 'format' :'geojson'}
    
    r = apiManager.post('/path/' + pathId + '/vector/timestamp/' + timestampId + '/order', body, token)    

    return r  

def download(orderId, filePath, token):
    
    token = sanitize.validString('token', token, True)
    orderId = sanitize.validUuid('orderId', orderId, True)
    filePath = sanitize.validString('filePath', filePath, True)

    if filePath[len(filePath)-4 : len(filePath) ] != '.zip':
        raise ValueError('filePath must end with .zip')

    apiManager.download('/path/vector/timestamp/order/' + orderId + '/data', filePath, token)
