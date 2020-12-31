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

Keys = ['File', 'Title', 'Length']
genKeys = dict()

def iniParse(data):
    result = dict()
    lines = data.split('\n')
    for line in lines:
        parts = line.split('=')
        if len(parts) == 2:
            result[parts[0]] = parts[1].replace('\r','')
    return result

def mkKeys(cursor):
    global genKeys
    cKeys = list()
    for key in Keys:
        cKeys.append(key + str(cursor))
        genKeys[key + str(cursor)] = key
    return cKeys

def getKeyName(genKey):
    global genKeys
    return genKeys[genKey]

def parse(data, encoding, trackObject, playlistObject):
    Track = trackObject
    Playlist = playlistObject
    playlist = list()
    data = iniParse(data)
    
    finish = False
    cursor = 1
    while finish != True:
        keys = mkKeys(cursor)
        result = dict()
        for key in keys:
            try:
                result[ getKeyName(key) ] = data[key]
            except KeyError:
                pass
        if len(result) > 0:
            try:
                playlist.append( Track(Name=result['Title'], Duration=int(result['Length']), File=result['File']) )
            except KeyError:
                pass
            cursor = cursor + 1
        else:
            finish = True
    
    return Playlist(Tracks=playlist, Encoding = encoding)