""" 
Author:		 Muhammad Tahir Rafique
Date:		 2023-02-27 12:26:11
Project:	 Explorer
Description: Provide function to use the vscode icons.
"""

import os
import json
from django.conf import settings

class VSCodeIcons():
    def __init__(self) -> None:
        # GETTING FILE AND DIR NAME
        explorer_static = 'explorer/vs-code-icons'
        info_json = 'vsicons-icon-theme.json'
        icon_dir = 'icons'
        
        # GETTING LOCATIONS
        location = os.path.join(settings.STATIC_ROOT, explorer_static)
        
        # FINDING EXISTANCE LOCATION
        exist_info_path = None
        icon_dir_path = os.path.join(location, icon_dir)
        if os.path.exists(icon_dir_path):
            info_path = os.path.join(location, info_json)
            if os.path.exists(info_path):
                exist_info_path = info_path
                    
        # READING INFO
        self.info = None
        self.icon_root = os.path.join(explorer_static, icon_dir)
        if exist_info_path:
            with open(exist_info_path, 'rb') as f:
                self.info = json.load(f)
        else:
            self.info = None
        return None
    
    def _findDirectoryIcon(self, name):
        """Finding best possible icon for directory."""
        # FINDING ICON
        icon_name = self.info['folderNames'].get(name)
        if icon_name is None: # Default condition
            icon_name = '_folder'
        
        # FINDING ICON PATH
        icon_path = self.info['iconDefinitions'][icon_name]
        icon_name = os.path.basename(icon_path['iconPath'])
        
        # FINDING STATIC PATH
        static_path = os.path.join(self.icon_root, icon_name)
        return static_path
        
    def _findFileIcon(self, name):
        """Finding best possible icon for file."""
        # FINDING ICON
        icon_name = self.info['fileNames'].get(name)
        if icon_name is None:
            # GETTING ON THE BASE OF EXT
            ext = os.path.splitext(name)[-1][1:]
            icon_name = self.info['fileExtensions'].get(ext)
            if icon_name is None:
                icon_name = '_file' # Default Condition
        
        # FINDING ICON PATH
        icon_path = self.info['iconDefinitions'][icon_name]
        icon_name = os.path.basename(icon_path['iconPath'])
        
        # FINDING STATIC PATH
        static_path = os.path.join(self.icon_root, icon_name)
        return static_path
    
    def _updateInfo(self, data):
        """Find the corosponding icon."""
        # GETTING TYPE AND NAME
        type = data['type']
        name = data['name']
        
        # UPDATE IN CASE OF INFO AVAILABLE
        if self.info:
            if type == 'directory':
                icon_path = self._findDirectoryIcon(name)
            else:
                icon_path = self._findFileIcon(name)
            data['icon'] = icon_path
        else:
            data['icon'] = None
        return data
    
    def addIconInfo(self, data_list):
        """Getting icon paths."""
        # UPDATING LIST
        icon_data = []
        for data in data_list:
            icon_data.append(self._updateInfo(data))
        return icon_data