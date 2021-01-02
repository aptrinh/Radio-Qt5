# Radio-Qt5
This is an Internet Radio player built on PyQt5/tkinter and Python.

![Image](https://imgur.com/KbxW9Qt.png)

## Requirements
- Python <= 3.8.7 (3.9 should work too)
- PyQt5
- python-mpd2
- mpd
- tkinter

## Usage
``` 
git clone https://github.com/aptrinh/Radio-Qt5 
python pyqtradio.py
```
Included are TuneIn, SomaFM and Pinguin options for easy navigation. You can also upload your own URLs under **playlist** form (currently .xspf is supported). Other playlist types can work too, but you need to convert them to .xspf with VLC.

## TODO
- Parser for other playlist types (.m3u, .m3u8, .pls)
- Get rid of tkinter file browser for pure PyQt5 widgets
- Pack everything into binary

### This Project is licensed under GNU General Public License 3 (GPL-3.0)

