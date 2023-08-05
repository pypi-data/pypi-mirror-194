import sys, os
from asterisk.agi import AGI
from ura_agi.entities import Node


class UraAgi:
    _agi = AGI()

    class InvalidAudiosFolder(Exception):
        ...

    def __init__(self, audios_folder: str) -> None:
        self.audios_folder = audios_folder
        self._validate_audios_folder()

    def _validate_audios_folder(self) -> None:
        
        if not os.path.isdir(self.audios_folder):
            raise UraAgi.InvalidAudiosFolder()

    def goto(self, node: Node) -> None:
        self._agi.goto_on_exit(node.context, node.extension, node.priority)
        sys.exit(0)
    
    def background(self, audio: str, variable_name: str, timeout: int=3):
        timeout = timeout * 1000
        audio_file = self.audios_folder + audio
        received_digits = self._agi.stream_file(audio_file, escape_digits=[0,1,2,3,4,5,6,7,8,9])    
        digit = self._agi.wait_for_digit(timeout=timeout)
        
        while digit != '' and digit != '#':
            received_digits += digit
            digit = self._agi.wait_for_digit(timeout=timeout)
        
        self._agi.set_variable(variable_name, received_digits)       
        return received_digits
    
    def playback(self, audio: str) -> None:
        self._agi.stream_file(self.audios_folder + audio)
    
    def hangup(self) -> None:
        self._agi.hangup()
        sys.exit(0)
    
    def get_callerid(self):
        return self._agi.env['agi_callerid']

    def get_variable(self, variable_name: str) -> str:
        return self._agi.get_variable(variable_name)

    def console(self, msg: str) -> None:
        self._agi.verbose(msg)
    
