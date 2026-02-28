'''*************************************************
content     Slate Sorter

version     0.0.2
date        02-04-2025

author      Harry Shaper <harryshaper@gmail.com>

*************************************************'''

import os
import sys
import shutil
import yaml
import time

from functools import wraps

import generate_report

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(SCRIPT_DIR, "FileSplitter"))

# Import the function from file_splitter.py
from file_splitter import file_split

#*********************************************************************
# DYNAMICALLY FETCH SELECTED FOLDER - For Right-Click / Send To
if len(sys.argv) < 2:
    print("Usage: python sort_shoot.py <shoot_folder_path>")
    sys.exit(1)

SHOOT_FOLDER = sys.argv[1]

if not os.path.isdir(SHOOT_FOLDER):
    print(f"Error: '{SHOOT_FOLDER}' is not a valid folder.")
    sys.exit(1)

#*********************************************************************    
# CONSTANTS
SLATE_LIST = []

#*********************************************************************
# User settings / Config file
with open ("user_settings.yaml","r") as f:
    config = yaml.safe_load(f) or {}

rename_shoot_folder = config.get("RENAME_SHOOT_FOLDER", True) 
rename_suffix = config.get("RENAME_SUFFIX", "_sorted")
rename_prefix = config.get("RENAME_PREFIX", "")

subfolder_check = config.get("SUBFOLDER_BY_FORMAT", False)

#*********************************************************************   
# FUNCTIONS       
def timer_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds.")
        return result
    return wrapper

def define_shoot_data():
    """Creates a list of paths to main data types (Example - HDRI path, PANO path, etc)"""
    return [
        os.path.join(SHOOT_FOLDER, folder)
        for folder in os.listdir(SHOOT_FOLDER)
        if os.path.isdir(os.path.join(SHOOT_FOLDER, folder))
    ]

def update_slate_list(folder):
    """Adds all unique slate ID's to a list """
    data_set_folder = os.listdir(folder)

    for item in data_set_folder:
        unique_slate = item.split("_")

        if unique_slate[0] not in SLATE_LIST:
            SLATE_LIST.append(unique_slate[0])
    
def get_slates():
    """Walks through all shoot data folders"""
    for folder in define_shoot_data():
        update_slate_list(folder)

def make_slate_folders():
    """Creates all slate folders """
    for slate in SLATE_LIST:
        slate_path = os.path.join(SHOOT_FOLDER, slate.upper())
        os.mkdir(slate_path)    #Makes a slate folder 

@timer_function
def sort_data():
    """Moves data to new file path SLATE>DATATYPE/DATA """
    moves = []
    source_folders = set(define_shoot_data())

    # Scan through each shoot data type (HDRI / PANO / TEXTURE / etc)
    for data_type_folder in define_shoot_data():
        data_type = os.path.basename(data_type_folder)

        # Creates source path
        for item in os.listdir(data_type_folder):
            src_path = os.path.join(data_type_folder, item)

            # Only allows folders
            if not os.path.isdir(src_path):
                continue

            slate = item.split("_")[0].upper()

            # Creates destination path and structure
            dst_path = os.path.join(
                SHOOT_FOLDER,
                slate,
                data_type,
                item  
            )

            moves.append((src_path, dst_path))

    # Move folders from source to destination
    for src, dst in moves:
        # CHANGE: only create parent directories
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(src, dst)

    # Clear original folders
    for folder in source_folders:
        if os.path.exists(folder) and not os.listdir(folder):
            os.rmdir(folder)

    if subfolder_check:
        import subprocess

        for _, dst in moves:
            if os.path.isdir(dst):
                # Only run if folder contains files
                if any(os.path.isfile(os.path.join(dst, f)) for f in os.listdir(dst)):
                    subprocess.run([
                        "python",
                        os.path.join(os.path.dirname(__file__), "FileSplitter", "file_splitter.py"),
                        dst
                    ])

        
#*********************************************************************#
# EXECUTE
get_slates() # Identify all slates
make_slate_folders() # Create all slates
sort_data() # Move data to new path

#*********************************************************************#
# Create report file ?
answer = input("Would you like to generate a YAML report (Y/N): ").strip().lower()

if answer == "y":
    print("Generating report...")
    generate_report.generate_report(SHOOT_FOLDER)
    print("Report generation finished.")

#*********************************************************************#
# Rename folder to "_sorted", marking it ready for ingestion

if rename_shoot_folder:
    parent_folder = os.path.dirname(SHOOT_FOLDER)
    original_name = os.path.basename(SHOOT_FOLDER)

    # Build new name using prefix + original + suffix
    new_shoot_name = f"{rename_prefix}{original_name}{rename_suffix}"
    new_shoot_path = os.path.join(parent_folder, new_shoot_name)

    # Prevent renaming if already renamed
    if original_name == new_shoot_name:
        print("Folder name unchanged (prefix/suffix result identical).")

    elif not os.path.exists(new_shoot_path):
        os.rename(SHOOT_FOLDER, new_shoot_path)
        print(f"Folder renamed to: {new_shoot_path}")

    else:
        print(f"Cannot rename. Destination already exists: {new_shoot_path}")

print("\nProcessing complete. Press Enter to exit.")
#input()  # Keeps terminal open until user presses Enter