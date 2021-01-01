import xml.etree.ElementTree as ET
# tkinter solution

def get_playlist():
   filename = ""
   try:
      from tkinter import Tk     # from tkinter import Tk for Python 3.x
      from tkinter.filedialog import askopenfilename

      Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
      filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
   #print(filename)
   except Exception as msg:
      print(msg)
   return filename
   
def get_stations():
   items = []
   playlistfile = get_playlist()
   #print(playlistfile)

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

   return items

# database = [] 
# database= get_stations()
# print(database[0])






