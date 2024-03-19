import platform
import time
import sys
import tkinter
from tkinter import filedialog
import os

def select_directory():
    """Selects a directory based on the operating system."""
    if platform.system() == "Windows":
        root = tkinter.Tk()
        root.withdraw()
        folder_selected = filedialog.askdirectory()
    else:
        folder_selected = input("Folder: ")
    return folder_selected

def find_carcols_files(folder_selected):
    """Finds all 'carcols.meta' files within the selected directory."""
    carcols_files = []
    for root, dirs, files in os.walk(folder_selected):
        for file in files:
            if file.endswith("carcols.meta"):
                carcols_files.append(os.path.join(root, file))
    return carcols_files

import json  # Import the json module

def check_tuning_kit_ids(carcols_files):
    """Checks and reports duplicate tuning kit IDs and writes a summary to a JSON file."""
    tuning_kits = {}
    for file in carcols_files:
        with open(file, "r", encoding='utf-8', errors='ignore') as f:
            for line in f:
                if "<id value=" in line:
                    id = line.split('"')[1]
                    if id not in tuning_kits:
                        tuning_kits[id] = [file]
                    else:
                        tuning_kits[id].append(file)
    
    duplicates = {id: files for id, files in tuning_kits.items() if len(files) > 1}
    
    if duplicates:
        print("!!! Duplicates found:")
        for id, files in duplicates.items():
            print(f"Duplicated ID: {id} in {len(files)} locations.")
    else:
        print("No duplicates found! :)")

    # Writing the summary to a JSON file
    summary = {
        "total_duplicate_ids": len(duplicates),
        "duplicates": duplicates
    }

    with open("duplicates_summary.json", "w", encoding='utf-8') as jsonfile:
        json.dump(summary, jsonfile, indent=4, ensure_ascii=False)

    print("Summary of duplicates has been written to 'duplicates_summary.json'.")

    
def main():
    print("Welcome to the tuning kit ID checker from https://mest3rdevelopment.com/ !\n")
    folder_selected = select_directory()
    if not folder_selected:
        print("No folder selected! Exiting...")
        time.sleep(5)
        sys.exit()
    
    print(f"Searching for vehicles in {folder_selected}...")
    carcols_files = find_carcols_files(folder_selected)
    print(f"Found {len(carcols_files)} 'carcols.meta' files")
    print("Checking tuning kit IDs...")
    check_tuning_kit_ids(carcols_files)
    time.sleep(5)
    sys.exit()

if __name__ == "__main__":
    main()
