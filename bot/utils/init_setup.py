import os
from pathlib import Path

def init_directories():
    """Creates necessary directories if they don't exist"""
    directories = ['logs', 'data']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

if __name__ == "__main__":
    init_directories() 