''' Python Playlist Parser (plparser)
    Copyright (C) 2012  Hugo Caille
    
    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
    1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer
    in the documentation and/or other materials provided with the distribution.
    3. The name of the author may not be used to endorse or promote products derived from this software without specific prior written permission.
    
    THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
    OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
    OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    '''

from xml.dom import minidom
from random import randrange
try:
    from chardet.universaldetector import UniversalDetector
    chardet = True
except:
    chardet = False

class Track:
    def __init__(self, Artist = None, Title = None, Album = None, Name = None, Duration = None, File = None):
        self.Artist = Artist
        self.Title = Title
        self.Album = Album
        self.Name = Name
        self.Duration = Duration
        self.File = File
        
        self.Inverted = False
    
    def defineArtist(self, Artist):
        self.Artist = Artist
        if self.Inverted:
            self.Title = self.Name.split(' - ' + Artist)[0]
        else:
            self.Title = self.Name.split(Artist + ' - ')[1]
        
    def nameParse(self, invert = False):
        if invert:
            self.Inverted = True
        invert = self.Inverted

        results = list()
        splitted = self.Name.split(' - ')
        if len(splitted) == 2:
            if not invert:
                self.Artist = splitted[0]
                self.Title = splitted[1]
            else:
                self.Artist = splitted[1]
                self.Title = splitted[0]
            return True
        elif len(splitted) < 2:
            return False
        else:
            probcursor = 1
            if invert:
                splitted.reverse()
            while probcursor != len(splitted):    
                artist = str()
                wordcursor = 1
                words = splitted[ 0:probcursor ]
                if invert:
                    words.reverse()
                for part in words:
                    artist = artist + part
                    if len(words) - wordcursor > 0:
                        artist = artist + ' - '
                    wordcursor = wordcursor + 1
                results.append( artist )
                probcursor = probcursor + 1
            return results
    def mustInvert(self, artist):
        if self.Name.lower().rfind(artist.lower()) > 0:
            self.Inverted = True
        else:
            self.Inverted = False
        return self.Inverted

class Playlist:
    def __init__(self, Tracks=None, Encoding=None):
        self.Tracks = Tracks
        self.Inverted = False
        self.Encoding = Encoding
    def nameParse(self, invert = False):
        for track in self.Tracks:
            track.nameParse(invert)
    def mustInvert(self, artist = None):
        if artist == None:
            self.randTracks = list()
            for i in range(0, 3, 1):
                self.randTracks.append(self.Tracks[ randrange(0, len(self.Tracks) - 1) ])
            return self.randTracks
        else:
            for track in self.randTracks:
                if track.mustInvert(artist):
                    for track in self.Tracks:
                        track.Inverted = True
                    self.Inverted = True
                    return True
        
            

def typeGuess(data):
    lines = data.split('\n')
    if '#EXTM3U' in lines[0]:
        try:
            lines.decode('utf-8')
            return '.m3u8'
        except:
            return '.m3u'
    if '[playlist]' in lines[0]:
        return '.pls'
    dom = minidom.parseString(data)
    try:
        for namespace in dom.getElementsByTagName('playlist')[0].attributes.items():
            try:
                if namespace[1] == 'http://xspf.org/ns/0/':
                    return '.xspf'
            except:
                pass
    except:
        pass
    try:
        dom.getElementsByTagName('plist')
        return '.xml'
    except:
        return None
    
def decode(filename, data):
    if '.m3u8' in filename:
        encoding = 'utf-8'
        data = data.decode(encoding)
    elif '.m3u' in filename or '.pls' in filename:
        try:
            encoding = 'ISO-8859-2'
            data = data.decode(encoding)
        except:
            if chardet:
                u = UniversalDetector()
                u.feed(data)
                u.close()
                if u.result['confidence'] > 0.5:
                    try:
                        encoding = u.result['encoding']
                        data = data.decode(encoding)
                    except:
                        encoding = 'ascii'
                else:
                    encoding = 'ascii'
            else:
                encoding = 'ascii'
    elif '.xml' in filename or '.xspf' in filename:
        encoding = 'utf-8'

    return {'data' : data, 'encoding' : encoding}

def parse(filename=None, filedata=None, trackObject=Track, playlistObject=Playlist, encoding=None):
    if filedata != None:
        file = filedata
        if filename == None:
            filename = typeGuess(filedata)
    else:
        f = open(filename, 'r')
        file = f.read()
        f.close()
    
    if encoding == None:
        decoded = decode(filename, file)
        file = decoded['data']
        encoding = decoded['encoding']
    else:
        try:
            file = file.decode(encoding)
        except:
            decoded = decode(filename, file)
            file = decoded['data']
            encoding = decoded['encoding']
            

    if '.m3u' in filename or '.m3u8' in filename:
        import m3uparser
        return m3uparser.parse(file, encoding, trackObject, playlistObject)
    if '.pls' in filename:
        import plsparser
        return plsparser.parse(file, encoding, trackObject, playlistObject)
    if '.xspf' in filename:
        import xspfparser
        return xspfparser.parse(file, trackObject, playlistObject)
    if '.xml' in filename:
        import xmlparser
        return xmlparser.parse(file, trackObject, playlistObject)

