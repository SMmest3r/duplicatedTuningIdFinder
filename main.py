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
    meta_files = {
        "carcols": [],
        "vehicles": {},
        "handling": []
    }
    for root, dirs, files in os.walk(folder_selected):
        for file in files:
            if file.endswith("carcols.meta"):
                meta_files["carcols"].append(os.path.join(root, file))
            elif file.endswith("vehicles.meta"):
                meta_files["vehicles"][os.path.join(root, file)] = None
            elif file.endswith("handling.meta"):
                meta_files["handling"].append(os.path.join(root, file))
    return meta_files

def get_model_name(vehicles_meta_file):
    with open(vehicles_meta_file, "r", encoding="utf-8") as file:
        content = file.read()
    model_names = re.findall(r'<modelName>(.*?)</modelName>', content)
    return model_names[0] if model_names else "Unknown"

def rebuild_handling_ids(handling_files, start_id=2000):
    handling_id_map = {}
    new_id = start_id

    for file_path in handling_files:
        with open(file_path, "r+", encoding="utf-8") as file:
            content = file.read()
            handling_names = re.findall(r'<handlingName>(.*?)</handlingName>', content)

            for name in handling_names:
                if name not in handling_id_map:
                    handling_id_map[name] = f"handling_{new_id}"
                    new_id += 1
                content = content.replace(f'<handlingName>{name}</handlingName>', f'<handlingName>{handling_id_map[name]}</handlingName>')

            file.seek(0)
            file.write(content)
            file.truncate()

    return new_id  # Returning the next starting ID for car mod kits

def rebuild_car_mod_kit_ids(meta_files, start_id=2000):
    new_id = rebuild_handling_ids(meta_files["handling"], start_id)  # Start car mod kit IDs after handling IDs
    summary = {"count": 0, "cars": {}, "handlingDuplicates": {}}

    for file_path in meta_files["carcols"]:
        directory = os.path.dirname(file_path)
        vehicle_meta_file_path = next((f for f in meta_files["vehicles"] if f.startswith(directory)), None)
        model_name = get_model_name(vehicle_meta_file_path) if vehicle_meta_file_path else "Unknown"

        with open(file_path, "r+", encoding="utf-8") as file:
            content = file.read()

            ids_found = set(re.findall(r'<id value="(\d+)"', content))
            kit_names_found = set(re.findall(r'<kitName>(\d+)(_[\w]+)</kitName>', content))

            for id_val in ids_found.union(kit_names_found):
                original_id = id_val[0] if isinstance(id_val, tuple) else id_val
                suffix = id_val[1] if isinstance(id_val, tuple) else "_default_modkit"
                new_kit_name = f"{new_id}{suffix}"
                content = content.replace(f'<id value="{original_id}"', f'<id value="{new_id}"')
                content = content.replace(f'<kitName>{original_id}{suffix}</kitName>', f'<kitName>{new_kit_name}</kitName>')
                summary["cars"][new_id] = {"file_path": file_path, "model_name": model_name, "original_id": original_id, "new_id": new_id, "kitName": new_kit_name}
                new_id += 1

            file.seek(0)
            file.write(content)
            file.truncate()

    summary["count"] = len(summary["cars"])

    with open('car_mods_summary.json', 'w', encoding='utf-8') as json_file:
        json.dump(summary, json_file, indent=4, ensure_ascii=False)

def main():
    folder_selected = select_directory()
    if not folder_selected:
        print("No folder selected! Exiting...")
        return

    meta_files = find_meta_files(folder_selected)
    rebuild_car_mod_kit_ids(meta_files)
    print("Processing complete. Summary saved to 'car_mods_summary.json'.")

if __name__ == "__main__":
    main()
