'''*************************************************
content     Tool Demo

version     0.0.2
date        25-12-2025

author      Harry Shaper <harryshaper@gmail.com>

*************************************************'''

# IMPORTS

import os
import shutil
import sys
import generate_report

#*********************************************************************#
#DYNAMICALLY FETCH SELECTED FOLDER - For Right-Click / Send To
#*********************************************************************#

if len(sys.argv) < 2:
    print("Usage: python sort_shoot.py <shoot_folder_path>")
    sys.exit(1)

SHOOT_FOLDER = sys.argv[1]

if not os.path.isdir(SHOOT_FOLDER):
    print(f"Error: '{SHOOT_FOLDER}' is not a valid folder.")
    sys.exit(1)

#*********************************************************************#    
#CONSTANTS
#*********************************************************************#

SLATE_LIST = []

#*********************************************************************#    
#FUNCTIONS
#*********************************************************************#           

def define_shoot_data():
    """Creates a list of paths to main data types
       (Example - HDRI path, PANO path, etc)"""
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
        slate_path = SHOOT_FOLDER + "\\" + slate.upper() 
        os.mkdir(slate_path)    #Makes a slate folder 

        
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
        # --- CHANGE: only create parent directories ---
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(src, dst)

    # Clear original folders
    for folder in source_folders:
        if os.path.exists(folder) and not os.listdir(folder):
            os.rmdir(folder)

        
#*********************************************************************#
# EXECUTE
#*********************************************************************#

get_slates() # Identify all slates
make_slate_folders() # Create all slates
sort_data() # Move data to new path

#*********************************************************************#
#Create report file ?
#*********************************************************************#

answer = input("Would you like to generate a YAML report (Y/N): ").strip().lower()

if answer == "y":
    try:
        generate_report.generate_report(SHOOT_FOLDER)
    except ModuleNotFoundError:
        print("Error: generate_report.py not found or PyYAML not installed.")

#*********************************************************************#
#Rename folder to "_sorted", marking it ready for ingestion
#*********************************************************************#

rename = True #Users can set this to False if they don't want renaming to happen
suffix = "_sorted"

if rename:
    parent_folder = os.path.dirname(SHOOT_FOLDER)
    new_shoot_name = os.path.basename(SHOOT_FOLDER) + suffix
    new_shoot_path = os.path.join(parent_folder, new_shoot_name)

    if not os.path.exists(new_shoot_path):
        os.rename(SHOOT_FOLDER, new_shoot_path)
        print(f"Folder renamed to: {new_shoot_path}")
    else:
        print(f"Folder already has _sorted: {new_shoot_path}")

print("\nProcessing complete. Press Enter to exit.")
input()  #Keeps terminal open until user presses Enter