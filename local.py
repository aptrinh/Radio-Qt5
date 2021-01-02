import xml.etree.ElementTree as ET
import json
# tkinter solution

def get_playlist():
   filename = ""
   try:
      from tkinter import Tk     # from tkinter import Tk for Python 3.x
      from tkinter.filedialog import askopenfilename

      Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
      filename = askopenfilename(initialdir = "$HOME",title = "Select file",filetypes = (("playlist files","*.xspf"),("all files","*.*"))) # show an "Open" dialog box and return the path to the selected file
      if not filename:
         return None
      elif type(filename) == tuple:
         return None
      else:
         return filename
   #print(filename)
   except Exception as msg:
      print(msg)
   
def get_stations():
   items = []
   playlistfile = get_playlist()
   print("Playlist name is ", playlistfile)

   if playlistfile != None:
      root = ET.parse(playlistfile).getroot()
      # Iterate through trackList, find locations and titles
      for track in root[1].iter('{http://xspf.org/ns/0/}track'):
         location = track.find('{http://xspf.org/ns/0/}location')
         title = track.find('{http://xspf.org/ns/0/}title')
      # If track.find() can't find a title tag or finds a null one, print N/A
         if (title is None or type(title.text) == type(None)):
            print("N/A", location.text)
         else:
            #print(title.text, location.text)
            items.append({"name":title.text,"url":location.text, "image": "https://i.imgur.com/1zsbpOD.jpg", "type":"audio"})
      # Static file for later use
      with open('savedLocal.json', 'w') as f:
         json.dump(items, f)
      return items
   else:
      return None
   

# database = [] 
# database= get_stations()
# print(database[0])






