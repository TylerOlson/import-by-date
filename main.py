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
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description='Move files in order of date taken.')
    parser.add_argument('-adb', help='use adb transfer', action='store_true')
    parser.add_argument('-ftp', help='use ftp transfer', action='store_true')
    parser.add_argument(
        '--ip', type=str, help='ip to use for ftp transfer', default='192.168.1.107')
    parser.add_argument('--port', type=int,
                        help='port to use for ftp transfer', default=2221)

    args = parser.parse_args()
    server = None
    destination_folder = None

    Path('wrote_files.txt').touch(exist_ok=True)

    print("Select source folder")
    originfolder = draw_file_dialog()
    # originfolder = 'C:/Users/tolso/Documents/Coding/python/import-by-date/pictures'
    print(originfolder)

    all_files = get_all_files(originfolder)

    if args.ftp:
        server = ftplib.FTP()
        server.connect(args.ip, args.port)
        server.login('android', 'android')
        server.dir()
        copy_files_ftp(all_files, server)
    elif args.adb:
        copy_files_adb(all_files)
    else:
        print("Select destination folder")
        destination_folder = draw_file_dialog()
        # destination_folder = 'C:/Users/tolso/Documents/Coding/python/import-by-date/destination'
        print(destination_folder)
        copy_files(all_files, destination_folder)

    os.remove("wrote_files.txt")

    if args.ftp:
        server.close()


def get_all_files(picture_path):
    all_files = []

    for (dirpath, dirnames, filenames) in os.walk(picture_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)

            searchfile = open("wrote_files.txt", "r")
            found = False
            for line in searchfile:
                if "searchphrase" in line:
                    found = True
            if not found:
                all_files.append(
                    {'filename': filename, 'full_path': full_path, 'timestamp': os.path.getmtime(full_path)})

    all_files.sort(key=sort_func)  # sort files oldest first
    return all_files


def copy_files(all_files, destination_folder):
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


def copy_files_ftp(all_files, server):
    for file_to_move in all_files:
        final_path = os.path.join(
            'DCIM', 'Restored', file_to_move['filename'])
        print("Copying " + final_path + " to FTP server (" +
              str(all_files.index(file_to_move)) + " of " + str(len(all_files)))
        binary = open(file_to_move['full_path'], 'rb')
        print(server.storbinary("STOR " + final_path, binary))
        binary.close()
        print("Copied " + final_path + " to FTP server (" +
              str(all_files.index(file_to_move)) + " of " + str(len(all_files)))
        time.sleep(1)


def copy_files_adb(all_files):
    for file_to_move in all_files:
        final_path = os.path.join(
            'storage', 'emulated', '0', 'Pictures', 'Restored', file_to_move['filename'])
        print("Copying " + file_to_move['filename'] + " to phone (" +
              str(all_files.index(file_to_move)+1) + " of " + str(len(all_files)))
        subprocess.call(
            'adb push "' + file_to_move['full_path'] + '" "' + final_path + '"', shell=True)
        print("Copied " + file_to_move['filename'] + " to phone (" +
              str(all_files.index(file_to_move)+1) + " of " + str(len(all_files)))

        f = open("wrote_files.txt", "a")
        f.write(file_to_move['full_path']+"\n")
        f.close()
        time.sleep(0.5)


def draw_file_dialog():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askdirectory()
    return file_path


def sort_func(e):
    return e['timestamp']


if __name__ == "__main__":
    main()
