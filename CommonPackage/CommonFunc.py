# -*- encoding=utf8 -*-
import sys
import gzip
import io
import base64
import json
import zlib

#gzip压缩
def EncodeText(encodeContent):
    if(type(encodeContent).__name__ == 'dict'):
        encodeContent = json.dumps(encodeContent).replace(" ", "") #字典类型的需要转换成字符串
    encodeByte = bytes(encodeContent,encoding='utf-8')
    #将byte做压缩，在用base64加密
    result = base64.b64encode(gzip.compress(encodeByte))
    return str(result,'utf-8')

#解gzip压缩
def DecodeText(decodeContent):
    result = gzip.decompress(base64.b64decode(decodeContent))
    return str(result,'utf-8')

