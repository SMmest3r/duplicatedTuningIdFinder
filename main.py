import os
import re
import tkinter
from tkinter import filedialog
import platform
import json

def select_directory():
    if platform.system() == "Windows":
        root = tkinter.Tk()
        root.withdraw()
        folder_selected = filedialog.askdirectory()
    else:
        folder_selected = input("Folder: ")
    return folder_selected

def find_meta_files(folder_selected):
    carcols_files = []
    vehicles_meta_files = {}
    for root, dirs, files in os.walk(folder_selected):
        for file in files:
            if file.endswith("carcols.meta"):
                carcols_files.append(os.path.join(root, file))
            elif file.endswith("vehicles.meta"):
                vehicles_meta_files[os.path.join(root, file)] = None
    return carcols_files, vehicles_meta_files

def get_model_name(vehicles_meta_file):
    with open(vehicles_meta_file, "r", encoding="utf-8") as file:
        content = file.read()
    model_names = re.findall(r'<modelName>(.*?)</modelName>', content)
    return model_names[0] if model_names else "Unknown"


def rebuild_car_mod_kit_ids(carcols_files, vehicles_meta_files):
    new_id = 2000
    car_summary = {"count": 0, "cars": {}}

    for file_path in carcols_files:
        directory = os.path.dirname(file_path)
        vehicle_meta_file_path = next((f for f in vehicles_meta_files if f.startswith(directory)), None)
        model_name = get_model_name(vehicle_meta_file_path) if vehicle_meta_file_path else "Unknown"

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        ids_found = set(re.findall(r'<id value="(\d+)"', content))
        kit_names_found = set(re.findall(r'<kitName>(\d+)(_[\w]+)</kitName>', content))

       
        for id_val in ids_found:
            content = re.sub(rf'<id value="{id_val}"', f'<id value="{new_id}"', content)
            car_summary["cars"][new_id] = {"file_path": file_path, "model_name": model_name, "original_id": id_val, "new_id": new_id, "kitName": f"{new_id}_default_modkit"}  # Assume a default kitName structure
            new_id += 1

        
        for _, suffix in kit_names_found:
            if new_id not in car_summary["cars"]:  
                car_summary["cars"][new_id] = {"file_path": file_path, "model_name": model_name, "new_id": new_id}
            car_summary["cars"][new_id]["kitName"] = f"{new_id}{suffix}"
            content = re.sub(rf'<kitName>\d+{suffix}</kitName>', f'<kitName>{new_id}{suffix}</kitName>', content, 1)
            new_id += 1

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

    car_summary["count"] = len(car_summary["cars"])

    with open('car_mods_summary.json', 'w', encoding='utf-8') as json_file:
        json.dump(car_summary, json_file, indent=4, ensure_ascii=False)


def main():
    folder_selected = select_directory()
    if not folder_selected:
        print("No folder selected! Exiting...")
        return

    carcols_files, vehicles_meta_files = find_meta_files(folder_selected)
    if not carcols_files:
        print("No 'carcols.meta' files found in the selected directory.")
        return

    rebuild_car_mod_kit_ids(carcols_files, vehicles_meta_files)
    print("All car mod kit IDs have been rebuilt starting from 2000, including model names. A summary has been saved to 'car_mods_summary.json'.")

if __name__ == "__main__":
    main()
