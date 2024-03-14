import platform
import time
import sys
import tkinter
from tkinter import filedialog
import os

def main():
    print("Welcome to the tuning kit ID checker from https://mest3rdevelopment.com/ !\n\n")
    if platform.system() == "Windows":
        main_win()
    elif platform.system() == "Linux":
        main_linux()
    else:
        print("Please use Windows or Linux")
        time.sleep(5)
        sys.exit()

def main_win():
    print("Select the folder where all the vehicles are located")
    root = tkinter.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    if folder_selected == "":
        print("No folder selected! Exiting...")
        time.sleep(5)
        sys.exit()
    print(f"Searching for vehicles in {folder_selected}...")
    carcols_files = []
    for root, dirs, files in os.walk(folder_selected):
        for file in files:
            if file.endswith("carcols.meta"):
                carcols_files.append(os.path.join(root, file))
    print(f"Found {len(carcols_files)} carcols.meta files")
    print("Checking tuning kit IDs...")
    tuning_kits = []
    for file in carcols_files:
        with open(file, "r") as f:
            lines = f.readlines()
            for i in range(len(lines)):
                if "<id value=" in lines[i]:
                    id = lines[i].split('"')[1]
                    tuning_kits.append(id)
                    break
    print(f"Found {len(tuning_kits)} tuning kit IDs")
    duplicates = []
    for kit in tuning_kits:
        if tuning_kits.count(kit) > 1:
            duplicates.append(kit)
    if len(duplicates) > 0:
        printed_kits = []
        printed_files = []
        print("!!! Duplicates found:")
        for kit in duplicates:
            if kit in printed_kits:
                continue
            printed_kits.append(kit)
            print(f"Duplicated ID: {kit}")
            for file in carcols_files:
                with open(file, "r") as f:
                    for line in f:
                        if f'<id value="{kit}"' in line:
                            if file in printed_files:
                                continue
                            printed_files.append(file)
                            print(f"Location: {file}")
    else:
        print("No duplicates found! :) Exiting...")
    time.sleep(5)
    sys.exit()

def main_linux():
    print("Select the folder where all the vehicles are located")
    folder_selected = input("Folder: ")
    if folder_selected == "":
        print("No folder selected! Exiting...")
        time.sleep(5)
        sys.exit()
    print(f"Searching for vehicles in {folder_selected}...")
    carcols_files = []
    for root, dirs, files in os.walk(folder_selected):
        for file in files:
            if file.endswith("carcols.meta"):
                carcols_files.append(os.path.join(root, file))
    print(f"Found {len(carcols_files)} carcols.meta files")
    print("Checking tuning kit IDs...")
    tuning_kits = []
    for file in carcols_files:
        with open(file, "r") as f:
            lines = f.readlines()
            for i in range(len(lines)):
                if "<id value=" in lines[i]:
                    id = lines[i].split('"')[1]
                    tuning_kits.append(id)
                    break
    print(f"Found {len(tuning_kits)} tuning kit IDs")
    duplicates = []
    for kit in tuning_kits:
        if tuning_kits.count(kit) > 1:
            duplicates.append(kit)
    if len(duplicates) > 0:
        printed_kits = []
        printed_files = []
        print("!!! Duplicates found:")
        for kit in duplicates:
            if kit in printed_kits:
                continue
            printed_kits.append(kit)
            print(f"Duplicated ID: {kit}")
            for file in carcols_files:
                with open(file, "r") as f:
                    for line in f:
                        if f'<id value="{kit}"' in line:
                            if file in printed_files:
                                continue
                            printed_files.append(file)
                            print(f"Location: {file}")
    else:
        print("No duplicates found! :) Exiting...")
    time.sleep(5)
    sys.exit()

if __name__ == "__main__":
    main()
