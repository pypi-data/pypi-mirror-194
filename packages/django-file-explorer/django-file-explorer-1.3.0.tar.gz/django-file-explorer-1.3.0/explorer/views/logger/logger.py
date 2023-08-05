""" 
Author:		 Muhammad Tahir Rafique
Date:		 2023-02-25 11:21:59
Project:	 Explorer
Description: Provide function to write the log file. 
"""

import os
import datetime

from django.conf import settings

from ..extractor.request import RequestDataExtractor

class ExplorerLogger():
    def __init__(self) -> None:
        # GETTING LOG PATH
        try:
            self.log_dir = settings.EXPLORER.get('log_dir')
            self.log_file = settings.EXPLORER.get('log_file')
            self.disable = True
            if self.log_dir:
                self.log_dir = str(self.log_dir)
                self.disable = False
                os.makedirs(self.log_dir, exist_ok=True)
            if self.log_file:
                self.log_file = str(self.log_file)
                self.disable = False
                os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        except:
            self.disable = True
        return None
    
    def _getInfo(self, request, response):
        """Making information string."""
        info = {}
        # GETTING TIME INFORMATION
        now = datetime.datetime.now()
        info['time'] = now.strftime("[%d/%b/%Y %I:%M:%S:%p]")
        
        # GETTING OTHER INFO
        info['request_method'] = request.method
        info['status_code'] = response.status_code
        info['username'] = request.user.username
        
        # GETTING APPLICATION RELATED INFOMTAION
        extractor = RequestDataExtractor(request)
        info['action'] = extractor.getAction()
        info['volume'] = extractor.getVolume()
        info['page_number'] = extractor.getPageNumber()
        info['location'] = extractor.getLocation()
        info['check_box'] = extractor.getCheckboxIdx()
        return info
    
    def _infoToSingleLine(self, info):
        """Convert the information dict to single line of string."""
        line_info = ""
        line_info += f"{info['time']}"
        line_info += f" {info['request_method']}"
        line_info += f" | {info['status_code']}"
        line_info += f" | {info['username']}"
        line_info += f" | {info['action']}"
        line_info += f" | {info['volume']}"
        line_info += f" | {info['page_number']}"
        line_info += f" | {info['location']}"
        line_info += f" | {info['check_box']} |"
        line_info += "\n"
        return line_info
    
    def _writeLogFile(self, file_path, log_line):
        """Writing single line to log file."""
        with open(file_path, 'a') as f:
            f.writelines([log_line])
        return None
        
    def _writeToDir(self, info):
        """Writing log on the base of username."""
        # GETTING SINGLE LINE INFORMATION
        line_info = self._infoToSingleLine(info)
        
        # GETTING FILE PATH
        username = info.get('username')
        file_path = os.path.join(self.log_dir, f'{username}.log')
        
        # WRITING FILE INFOMTATION
        self._writeLogFile(file_path, line_info)
        return None
    
    def _writeToFile(self, info):
        """Writing log information to a single file."""
        # GETTING SINGLE LINE INFORMATION
        line_info = self._infoToSingleLine(info)
        
        # WRITING FILE INFOMTATION
        self._writeLogFile(self.log_file, line_info)
        return None
        
    def log(self, request, response):
        """Log the information to desire location."""
        # IF LOGGING IS DISABLED
        if self.disable:
            return None
        
        # GETTING INFORMATION
        info = self._getInfo(request, response)
        
        # LOGGING IN DIRECTORY
        if self.log_dir:
            self._writeToDir(info)
        
        # LOGGINF IN FILE
        if self.log_file:
            self._writeToFile(info)
        return None