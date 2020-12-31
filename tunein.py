#http://opml.radiotime.com/Browse.ashx?id=r0&render=json

import urllib.request
from urllib.request import Request
from urllib.request import urlopen
from urllib.error import HTTPError
import json





class openRadio(object):
    def __init__(self):
        pass
    
    
    def getOverview(self):
        result = []
        url = "http://opml.radiotime.com/Browse.ashx?render=json"
        try:
            req = urllib.request.urlopen(url)
            res = json.loads(req.read().decode('utf-8'))
            body = res.get("body")
            for item in body:
                result.append({"name":item.get("text"),"url":item.get("URL"), "type":item.get("type")})
        except Exception as msg:
            print(msg)
        return result
            
    def getNextLayer(self, url):
        result = []
        try:
            req = urllib.request.urlopen(url + "&render=json")
            res = json.loads(req.read().decode('utf-8'))
            body = res.get("body")
            if "children" in body[0]:
                body = body[0].get("children")
            #print("BODY" + str(body))
            for item in body:
                result.append({"name":item.get("text"),"url":item.get("URL"), "type":item.get("type"), "image":item.get("image")})
        except Exception as msg:
            print(msg)
        return result
            
    def getStreamUrl(self, url):
        result = []
        try:
            req = urllib.request.urlopen(url)
            res = req.read().decode('utf-8')
            print(res)
            result = res
        except Exception as msg:
            print(msg)
        return result
            
        
      

       