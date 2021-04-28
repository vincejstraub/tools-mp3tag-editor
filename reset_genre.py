#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Automatically renames genre tags for .mp3 files using the eyed3 library.

The library eyed3 is used to load mp3 files, reset_genre then uses the 
eyed3.mp3.Mp3AudioFile object and replace specific characters, i.e. '/'
with ';' by default.
"""

import os   # standard library
import sys
import glob
import path

import eyed3    # 3rd party packages

__author__ = "Vince J. Straub"

def main():
    # Read file paths
    file_paths = read_mp3_file_paths()
    # Load each .mp3 file as eyed3 objects in a list and edit genre tag
    for file in file_paths:
        try: 
            # Load file
            audiofile = eyed3.load(file)
            # Declare new genre value by resetting tag values
            genre = reset_genre(audiofile)
            # Init genre tag
            audiofile.initTag()
            # Store value in tag
            audiofile.tag.genre = u'{}'.format(genre)
            # Save to file
            audiofile.tag.save()
        except:
            print("Genre tag could not be changed")

def reset_genre(audiofile, chars={'/': '; '}):
    """
    Resets genre tag for eyed3.mp3.Mp3AudioFile object by 
    replacing specific characters, '/' replaced with ';'
    by default.
    
    Args:
        audiofile (eyed3.mp3.Mp3AudioFile): mp3 audiofile.
        chars (str, default=/) character to replace.
    """
    # Remove digits in genre tag
    genre = str(audiofile.tag.genre)
    genre = ''.join([char for char in genre if not char.isdigit()])
    
    # Replace each character with new character
    for old_char, new_char in chars.items():
        genre = genre.replace(old_char, new_char)
        
    # Reset genre for single genre tags
    genre = genre.replace('()', '')
    return genre

def read_mp3_file_paths(dir_path='cwd'):
    """
    Stores paths of .mp3 files in the current directory in a list;
    asks user to provide different directory path if none are found. 
    
    Args:
        dir_path (str, default=cwd): path to directory containing 
        .mp3 files or subdirectories with .mp3 files, defaults to 
        current working directory.
    
    Returns:
        A list of file paths as strings.
    """
    # Search for .mp3 files in current directory and subdirectories 
    # if no directory path is provided
    if dir_path is 'cwd':
        mp3_file_paths = file_paths = glob.glob('**/*.mp3', recursive=True)
        num_mp3_files = len(mp3_file_paths)
        
        # Prompt user for directory path if no none found else store paths
        if num_mp3_files == 0:
            print('No .mp3 files found in current working'
                  'directory and subdirectories')

    # Check provided directory path exists and read .CSV files
    else:
        assert os.path.exists(dir_path), 'Directory path not found.'
        mp3_file_paths = glob.glob(os.path.join(dir_path, '**/*.mp3'))        
        
        # Check mp3 files exist
        if len(mp3_file_paths) == 0:
            print('No .mp3 files found in directory path.')

    return mp3_file_paths 

if __name__ == '__main__':
    main()
