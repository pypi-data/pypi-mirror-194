""" 
Author:		 Muhammad Tahir Rafique
Date:		 2023-01-03 12:19:29
Project:	 File Explorer
Description: Provide path related functions.
"""

import os

def is_path_exists(*args):
    """Check weather the path exists or not."""
    # MAKING PATH
    for idx, arg in enumerate(args):
        if idx == 0:
            path = arg
            continue
        path = os.path.join(path, arg)
    return os.path.exists(path)

def is_path_contain_reverse(path):
    """Checking weather the path contain ../"""
    split_path = path.split(os.path.sep)
    if '..' in split_path:
        return False
    return True