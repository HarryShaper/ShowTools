'''*************************************************
content     FileSplitter

version     0.0.1
date        16-02-2026

author      Harry Shaper <harryshaper@gmail.com>

*************************************************'''
import os
import shutil

#*********************************************************************
# Folder to sort: dynamically set by your BAT via reg
import sys
if len(sys.argv) < 2:
    print("Usage: file_splitter.py <folder_path>")
    sys.exit(1)

folder_path = sys.argv[1]

if not os.path.isdir(folder_path):
    print(f"Error: '{folder_path}' is not a valid folder.")
    sys.exit(1)

#********************************************************************
# Variables
image_types = set()

#********************************************************************
# Functions
def get_image_paths():
    return [
        os.path.join(folder_path, image)
        for image in os.listdir(folder_path)
        if not os.path.isdir(os.path.join(folder_path, image))
    ]

def get_type(image):
    file_type = os.path.splitext(image)[-1]
    return file_type[1:].lower()

def update_types_list():
    for image in os.listdir(folder_path):
        image_ext = get_type(image)
        image_types.add(image_ext)

def make_image_folders():
    for ext in image_types:
        new_folder = os.path.join(folder_path, ext.upper())
        os.makedirs(new_folder, exist_ok=True)  # safer than mkdir

def move_images():
    for image in os.listdir(folder_path):
        source_path = os.path.join(folder_path, image)
        if not os.path.isdir(source_path):
            extension = get_type(image)
            destination_path = os.path.join(folder_path, extension.upper(), image)
            shutil.move(source_path, destination_path)

def file_split(shoot_path=None):
    """
    Main entry point. 
    shoot_path: folder to split. If None, uses sys.argv[1] (for right-click standalone use)
    """
    global folder_path

    if shoot_path:
        folder_path = shoot_path
    elif len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        print("Usage: file_splitter.py <folder_path>")
        return

    print(f"FileSplitter running on folder: {folder_path}")
    update_types_list()
    make_image_folders()
    move_images()

#*********************************************************************
# EXECUTION
file_split()
