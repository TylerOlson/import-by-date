import argparse
import os
import sys
from datetime import datetime
import shutil
import pathlib
import tkinter as tk
from tkinter import filedialog
import ftplib


def main():
    """
    parser = argparse.ArgumentParser(
        description='Move files in order of date taken.')
    parser.add_argument('originfolder', type=str, help='folder to move from')
    parser.add_argument('destination_folder', type=str,
                        help='folder to move to')

    args = parser.parse_args()

    args.originfolder = pathlib.Path(args.originfolder)
    args.destination_folder = os.path.abspath(args.destination_folder)
    """

    server = ftplib.FTP()
    server.connect('192.168.1.107', 2221)
    server.login('android', 'android')
    server.dir()

    print("Select source folder")
    #originfolder = draw_file_dialog()
    originfolder = 'C:/Users/tolso/Documents/Coding/python/import_by_date/pictures'
    print(originfolder)

    print("Select destination folder")
    #destination_folder = draw_file_dialog()
    destination_folder = 'C:/Users/tolso/Documents/Coding/python/import_by_date/destination'
    print(destination_folder)

    all_files = get_all_files(originfolder)
    for file in all_files:
        print(file)
    copy_files(all_files, destination_folder)


def get_all_files(picture_path):
    all_files = []

    for (dirpath, dirnames, filenames) in os.walk(picture_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            all_files.append(
                {'filename': filename, 'full_path': full_path, 'timestamp': os.path.getmtime(full_path)})

    all_files.sort(key=sort_func)  # sort files oldest first
    return all_files


def copy_files(all_files, destination_folder):
    if os.path.isfile(destination_folder):
        print("Desination folder is a file")
        return
    if not os.path.isdir(destination_folder):
        os.makedirs(os.path.dirname(destination_folder), exist_ok=True)
    for file_to_move in all_files:
        full_destination_folder = os.path.join(
            destination_folder, file_to_move['filename'])
        os.makedirs(os.path.dirname(destination_folder), exist_ok=True)

        print("Copying " + file_to_move['full_path'] +
              " to " + full_destination_folder)
        shutil.copyfile(file_to_move['full_path'], full_destination_folder)
        print("Copied " + file_to_move['full_path'] +
              " to " + full_destination_folder)


def draw_file_dialog():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askdirectory()
    return file_path


def sort_func(e):
    return e['timestamp']


if __name__ == "__main__":
    main()

#            print(full_path) date = datetime.fromtimestamp(os.path.getmtime(full_path))
