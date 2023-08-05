# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 12:52:31 2022

@author: mwodring
"""

import logging 
import sys
import os
import functools
import pathlib

#This is just magpied from the 'net. Decorators are magic. https://realpython.com/primer-on-python-decorators/
def count_calls(func):
    @functools.wraps(func)
    def wrapper_count_calls(*args, **kwargs):
        wrapper_count_calls.num_calls += 1
        return func(*args, **kwargs)
    wrapper_count_calls.num_calls = 0
    return wrapper_count_calls

def new_logger(name = __name__):
    logger = logging.getLogger(name)
    
    #If I don't do this, it repeats itself for some reason.
    if not logger.handlers:
        logger.propagate = False
        logger.setLevel(logging.DEBUG)
        
        console_handler = logging.StreamHandler(sys.stdout)
        current_dir = os.getcwd()
        file_handler = logging.FileHandler(f"{current_dir}/logs.log")
        
        msg = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        console_format = logging.Formatter(msg)
        file_format = logging.Formatter(msg)
        
        console_handler.setFormatter(console_format)
        file_handler.setFormatter(file_format)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger

def Cleanup(folders: list, filetypes: list):
    for folder in folders:
        for file in os.scandir(folder):
            last_suffix = (lambda suffixes : suffixes[-1] if len(suffixes) > 0 else "None")(pathlib.Path(file.name).suffixes)
            if last_suffix in filetypes:
                os.remove(file)