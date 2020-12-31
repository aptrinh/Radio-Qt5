#http://api.somafm.com/channels.json
import urllib
from urllib.request import Request
from urllib.request import urlopen
import json
import plparser

url = "http://api.somafm.com/channels.json"



def get_json():
    result = {}
    try:
        req = urllib.request.urlopen(url)
        result = json.loads(req.read().decode('utf-8'))
    except Exception as msg:
        print(msg)
    return result
        
def get_stations():
    items = []
    jsonfile = get_json()
    channels = jsonfile.get("channels")
    for channel in channels:
        url = None
        playlists = channel.get("playlists")
        for playlist in playlists:
            if playlist.get("format") == "aac":
                url = playlist.get("url")
                continue
        if url == None:
            for playlist in playlists:
                if playlist.get("format") == "mp3":
                    url = playlist.get("url")
                    continue
        if url != None:        
            items.append({"name":channel.get("title"),"url":url, "image": channel.get("image"), "type":"audio"})
              
        
        #if url != None:
        #    try:
        #        req = urllib.request.urlopen(url)
        #        file = req.read()
        #        url = plparser.parse(filename=url, filedata=file).Tracks[0].File
        #        items.append({"name":channel.get("title"),"url":url, "image": channel.get("image"), "type":"audio"})
        #    except Exception as msg:
        #        print(msg)    
            
    return items    
 
 
#stations =  get_stations()
#print(stations)       
#playlist = stations[0].get("url")

#req = urllib.request.urlopen(playlist)
#file = req.read()

#print(plparser.parse(filename=playlist, filedata=file).Tracks[0].File)

   
        

    
      