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

def parse(data, trackObject, playlistObject):
    Track = trackObject
    Playlist = playlistObject
    dom = minidom.parseString(data)
    
    tracks = dom.getElementsByTagName('dict')[0].getElementsByTagName('dict')[0].getElementsByTagName('dict')
    playlist = list()
    
    for track in tracks:
        t = Track()
        items = track.getElementsByTagName('key')
        for item in items:
            key = item.childNodes[0].nodeValue
            value = item.nextSibling.childNodes[0].nodeValue
            if key == 'Artist':
                t.Artist = value
            if key == 'Name':
                t.Title = value
            if key == 'Location':
                t.File = value
            if key == 'Total Time':
                t.Duration = int(value)
            if key == 'Album':
                t.Album = value
            playlist.append(t)
    
    return Playlist(Tracks=playlist, Encoding='utf-8')