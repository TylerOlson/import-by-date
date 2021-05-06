import argparse
import os
import sys
from datetime import datetime
import shutil
import pathlib
import tkinter as tk
from tkinter import filedialog
import ftplib
import time


def main():
    parser = argparse.ArgumentParser(
        description='Move files in order of date taken.')
    parser.add_argument('-ftp',
                        help='use ftp transfer', action='store_true')
    parser.add_argument(
        '--ip', type=str, help='ip to use for ftp transfer', default='192.168.1.107')
    parser.add_argument('--port', type=int,
                        help='port to use for ftp transfer', default=2221)

    args = parser.parse_args()
    server = None
    destination_folder = None

    print("Select source folder")
    originfolder = draw_file_dialog()
    #originfolder = 'C:/Users/tolso/Documents/Coding/python/import-by-date/pictures'
    print(originfolder)

    if args.ftp:
        server = ftplib.FTP()
        server.connect(args.ip, args.port)
        server.login('android', 'android')
        server.dir()
    else:
        print("Select destination folder")
        destination_folder = draw_file_dialog()
        # destination_folder = 'C:/Users/tolso/Documents/Coding/python/import-by-date/destination'
        print(destination_folder)

    all_files = get_all_files(originfolder)
    for file in all_files:
        print(file)

    copy_files(all_files, destination_folder, server, args.ftp)

    if args.ftp:
        server.close()


def get_all_files(picture_path):
    all_files = []

    for (dirpath, dirnames, filenames) in os.walk(picture_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            all_files.append(
                {'filename': filename, 'full_path': full_path, 'timestamp': os.path.getmtime(full_path)})

    all_files.sort(key=sort_func)  # sort files oldest first
    return all_files


def copy_files(all_files, destination_folder, server, ftp):
    if not ftp:
        if os.path.isfile(destination_folder):
            print("Desination folder is a file")
            return
        if not os.path.isdir(destination_folder):
            print("Not found")
            return
        for file_to_move in all_files:
            full_destination_folder = os.path.join(
                destination_folder, file_to_move['filename'])
            os.makedirs(os.path.dirname(destination_folder), exist_ok=True)

            print("Copying " + file_to_move['full_path'] +
                  " to " + full_destination_folder)
            shutil.copyfile(file_to_move['full_path'], full_destination_folder)
            shutil.copystat(file_to_move['full_path'], full_destination_folder)
            print("Copied " +
                  file_to_move['full_path'] + " to " + full_destination_folder)
    else:
        for file_to_move in all_files:
            final_path = os.path.join(
                'DCIM', 'Restored', file_to_move['filename'])
            print("Copying " + final_path + " to FTP server")
            binary = open(file_to_move['full_path'], 'rb')
            print(server.storbinary("STOR " + final_path, binary))
            binary.close()
            print("Copied " + final_path + " to FTP server")
            time.sleep(1)


def draw_file_dialog():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askdirectory()
    return file_path


def sort_func(e):
    return e['timestamp']


if __name__ == "__main__":
    main()
