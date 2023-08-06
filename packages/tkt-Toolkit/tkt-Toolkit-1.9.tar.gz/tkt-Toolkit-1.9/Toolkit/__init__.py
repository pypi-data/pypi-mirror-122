__title__ = 'tkt-Toolkit'
__author__ = 'Suprime'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020-2021 Suprime'
__version__ = '1.9'

import time,socket,json,os,piexif.helper
from . import SpeechRecongition,translator, parse,tracking,audio
from .errors import *
from win32com.client import Dispatch

here = os.path.dirname(os.path.abspath(__file__))

Tracking = tracking
Parse = parse
AudioFormatting = audio.Format
AudioPlayer = audio.Player

class exlist:
    def __init__(self,list:list):
        """
        Some extra life improvements for list type objects.
        :param list:
        The list that is used for all operations
        """
        self._list = list
    def in_list(self,find:str,ignore_lower_and_upper:bool=False):
        c = -1
        for item in self._list:
            c += 1
            if item == find:
                return (True,c)
            if ignore_lower_and_upper:
                if item.lower() == find.lower():
                    return (True,c)
        return (False)
    def del_item(self,pos:int):
        new = []
        c = -1
        for item in self._list:
            c = c + 1
            if c == pos:
                pass
            else:
                new.append(item)
        return new
    def add_item(self,pos:int,entry:str):
        new = []
        c = -1
        for item in self._list:
            c = c + 1
            new.append(item)
            if c == pos:
                new.append(entry)
        return new
    def tuple_array(self,array2:list):
        c1 = 0
        c2 = 0
        array1 = self._list
        array3 = []
        for item1 in array1:
            c1 = c1 + 1
            for item2 in array2:
                c2 = c2 + 1
                tupled = (item1,item2)
                array3.append(tupled)
        return array3
    def __len__(self):
        return len(self._list)
    def __str__(self):
        return str(self._list)

class SpeechRecognition:
    """
    Requires Pyaudio that you have to install
    using 'pipwin install pyaudio'.
    Records or reads audio and transforms it to text.
    Can also list Microphones.
    """
    def __init__(self,show_msg:bool=True):
        self.show_msg = show_msg
    def from_Microphone(self):
        return SpeechRecongition.recon.recon_from_mic(self.show_msg)
    def from_Wav_File(self,wav_file: str, show_msg: bool = True):
        return SpeechRecongition.recon.recon_from_file(wav_file, show_msg)
    def list_Microphones(self):
        for EE in SpeechRecongition.recon.get_mics(self.show_msg): yield EE

class Toolkit:
    def __init__(self):
        """
        The main function with all sorts of things.
        """
        self.__version__ = __version__
    def __str__(self):
        return str("Version : " + self.__version__)
    def del_all(self,dir : str):
        """
        Clears out all of the files in the folder and
        then delets them.
        :param dir:
        The target folder.
        :return:
        None
        """
        parse.using.del_files(dir,False)
        parse.using.del_folders(dir,False)
        return None
    def getip(self):
        """
        Gets the users IP using the python
        built-in socket package.
        """
        return socket.gethostbyname(socket.gethostname())
    def translate(self,Text:str,Dest,From='auto'):
        """
        Translates text into another language using
        the googletrans package.
        :param Text:
        The Text that is going to be translated.
        :param Dest:
        The destination language for the text.
        :param From:
        The language of the given text.
        Use 'auto' here to automatically recognize
        the language.
        :return:
        Returns 2 values:
        1 : Translated Text
        2 : Tuple:
            1 : Text Language
            2 : Translated Language
            3 : Text
        """
        return translator.Translate(Text,Dest,From)
    def weather(self,city:str, key:str):
        """
        Gets the weather from 'openweathermap.org',
        uses the standard free to use api.
        :param city:
        The city that the weather is going
        to be from.
        :param key:
        The key for 'openweathermap.org'.
        :return:
        """
        api_key = key
        uul = ("https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + api_key)
        url = uul
        response = parse.x.get(url).text
        data = json.loads(response)
        return data
    def get_color(self,rgb : tuple = None, hex : int = None):
        """
        Gets the color-data of one 'hex'/'rgb' color.
        At least one of the two parameters has to be entered.
        :param rgb:
        The rgb color code tuple.
        :param hex:
        The hex color value. (int)
        :return:
        Returns 5 values:
        1 : The hex value.
        2 : The rgb tuple.
        3 : The hsl code.
        4 : The vsv code.
        5 : All of them.
        """
        if rgb == None and hex == None:
            raise ValueError('Not enough values.')
        elif not rgb == None and not hex == None:
            raise ValueError('Too many values.')
        elif not rgb == None and hex == None:
            R = 1
        elif rgb == None and not hex == None:
            R = 2
        else:
            raise InternalError
        if R == 1:
            req = parse.Q.build_main + parse.Q.build_rgb + str(rgb)
        elif R == 2:
            req = parse.Q.build_main + parse.Q.build_hex + str(hex.replace('#', '', 1))
        else:
            raise InternalError
        resp = (parse.x.get(req).text)
        return parse.using.pull_values(resp)
    def calc(self,calc):
        exec(f'global __COMP_CALC_END__\n__COMP_CALC_END__=({calc})')
        return __COMP_CALC_END__
    def do_for(self,n_seconds: int, func):
        """
        Runs the given function for the given amount of seconds.
        :param n_seconds:
        The seconds the function is run for.
        :param func:
        The function that is ran.
        :return:
        None
        """
        t_end = time.time() + n_seconds
        while time.time() < t_end: func()
        return None
    def read_metadata(self,filename:str):
        """
        Reads the metadata from an image file.
        :param filename:
        The file to be read.
        :return:
        The metadata in json format.
        """
        exif_dict = piexif.load(filename)
        user_comment = piexif.helper.UserComment.load(exif_dict["Exif"][piexif.ExifIFD.UserComment])
        d = json.loads(user_comment)
        return d
    def write_metadata(self,filename:str,json_data:dict):
        """
        Writes metadata into an image file.
        :param filename:
        The image to be used.
        :param json_data:
        The data to be written.
        :return:
        None
        """
        exif_dict = piexif.load(filename)
        exif_dict["Exif"][piexif.ExifIFD.UserComment] = piexif.helper.UserComment.dump(
            json.dumps(json_data),
            encoding="unicode"
        )
        piexif.insert(
            piexif.dump(exif_dict),
            filename
        )
        return None
    def create_shortcut(self,target:str,output:str):
        """
        Creates a shortcut on windows.
        :param target:
        The file that the shortcut accesses.
        :param output:
        The output file.
        :return:
        None
        """
        path = output
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = target
        shortcut.IconLocation = target
        shortcut.save()
        return None