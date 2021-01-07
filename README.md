# Radio-Qt5
This is an Internet Radio player built on PyQt5/tkinter and Python.

![Image](https://imgur.com/KbxW9Qt.png)

## Requirements
- Python <= 3.8.7 (3.9.1 in testing. Working nice so far)
- PyQt5
- python-mpd2
- mpd
- tkinter

## Installation
``` 
git clone https://github.com/aptrinh/Radio-Qt5
cd Radio-Qt5 
python pyqtradio.py
```
### **Windows**
Much more of a pain to set up than Linux, but doable. Follow the guide [(Part 1)](https://www.daangemist.nl/2012/11/16/installing-mpd-on-windows) & [(Part 2)](https://www.daangemist.nl/2012/11/26/run-mpd-as-windows-service) to set up mpd as a Windows service. The ```mpd.exe``` is in the same dir as ```mpd.db```

For reference, my Windows mpd.conf looks like this 
```
music_directory "C:/Users/honeypot/Music"
log_file "C:/Users/honeypot/mpd.log"
db_file "C:/Users/honeypot/mpd.db"
playlist_directory "C:/Users/honeypot/playlists"
audio_output {
    type "winmm"
    name "Speakers"
    device "Speakers (High Definition Audio Device)"
}
```

### **Linux**  
Double check to make sure mpd is running before starting up player. Then choose from below:
- Option 1:  
Just git clone, cd to dir and run as python. Install prereqs as needed. Tested on **Arch** and **Manjaro**. Smaller folder size.

- Option 2:  
Download the .zip, go to the extracted folder and ```./pyqtradio``` to save time. Bigger folder size.

My Linux mpd.conf looks like this. ```mixer_type "software"``` is there for the volume slider to work.

```
pid_file "~/.mpd/mpd.pid"
playlist_directory "~/.mpd/playlists"
db_file "~/.mpd/mpd.db"
state_file "~/.mpd/mpdstate"

audio_output {
    type "pulse"
    name "Pulse Audio"
    mixer_type "software"
}
```

### **MacOS**
I don't have a Mac. Feel free to test and let me know if there are problems

----

## Usage  
**Again, make sure mpd is running somewhere, otherwise player won't start.**

Click on the station name to choose from a list of stations. If the program doesn't crash and you can't hear anything, that station just might not be broadcasting at the moment. Pick another one!

Included are TuneIn, SomaFM and Pinguin options for easy navigation. You can also upload your own URLs under **playlist** format (currently only .xspf is supported). Other playlist types can work too, but you need to convert them to .xspf with VLC first.

## TODO
- Pack everything into binary for early release candidates ❌
- Parser for other playlist types (.m3u, .m3u8, .pls) ❌
- Get rid of tkinter file browser for pure PyQt5 widgets ❌
- Audio slider ✅


### This Project is licensed under GNU General Public License 3 (GPL-3.0)

