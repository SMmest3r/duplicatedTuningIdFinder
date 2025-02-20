import os
import re
import tkinter
from tkinter import filedialog
import platform
import json
from typing import Dict, List, Generator
import tqdm

def select_directory() -> str:
    """Select directory using GUI on Windows or CLI on other platforms."""
    if platform.system() == "Windows":
        root = tkinter.Tk()
        root.withdraw()
        folder_selected = filedialog.askdirectory()
    else:
        folder_selected = input("Folder: ")
    return folder_selected

def read_file_in_chunks(file_path: str, chunk_size: int = 8192) -> Generator[str, None, None]:
    """Read file in chunks to manage memory usage."""
    with open(file_path, "r", encoding="utf-8") as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk

def find_meta_files(folder_selected: str) -> Dict[str, List[str]]:
    """Find all relevant meta files with progress indication."""
    meta_files = {
        "carcols": [],
        "vehicles": {},
        "handling": []
    }
    total_files = sum([len(files) for _, _, files in os.walk(folder_selected)])
    
    with tqdm.tqdm(total=total_files, desc="Finding meta files") as pbar:
        for root, _, files in os.walk(folder_selected):
            for file in files:
                if file.endswith("carcols.meta"):
                    meta_files["carcols"].append(os.path.join(root, file))
                elif file.endswith("vehicles.meta"):
                    meta_files["vehicles"][os.path.join(root, file)] = None
                elif file.endswith("handling.meta"):
                    meta_files["handling"].append(os.path.join(root, file))
                pbar.update(1)
    
    return meta_files

def get_model_name(vehicles_meta_file: str) -> str:
    """Extract model name from vehicles meta file."""
    try:
        content = ""
        for chunk in read_file_in_chunks(vehicles_meta_file):
            content += chunk
        model_names = re.findall(r'<modelName>(.*?)</modelName>', content)
        return model_names[0] if model_names else "Unknown"
    except Exception as e:
        print(f"Error reading model name from {vehicles_meta_file}: {str(e)}")
        return "Unknown"

def safe_file_update(file_path: str, transform_function) -> None:
    """Safely update file contents using a temporary file."""
    temp_path = file_path + ".tmp"
    try:
        content = ""
        for chunk in read_file_in_chunks(file_path):
            content += chunk
            
        new_content = transform_function(content)
        
        with open(temp_path, "w", encoding="utf-8") as temp_file:
            temp_file.write(new_content)
            
        os.replace(temp_path, file_path)
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        if os.path.exists(temp_path):
            os.remove(temp_path)

def rebuild_handling_ids(handling_files: List[str], start_id: int = 2000) -> int:
    """Rebuild handling IDs with progress bar."""
    handling_id_map = {}
    new_id = start_id

    with tqdm.tqdm(handling_files, desc="Processing handling files") as pbar:
        for file_path in pbar:
            def transform_content(content: str) -> str:
                nonlocal new_id
                handling_names = re.findall(r'<handlingName>(.*?)</handlingName>', content)
                
                for name in handling_names:
                    if name not in handling_id_map:
                        handling_id_map[name] = f"handling_{new_id}"
                        new_id += 1
                    content = content.replace(
                        f'<handlingName>{name}</handlingName>',
                        f'<handlingName>{handling_id_map[name]}</handlingName>'
                    )
                return content

            safe_file_update(file_path, transform_content)
            pbar.set_postfix({"current_id": new_id})

    return new_id

def rebuild_car_mod_kit_ids(meta_files: Dict[str, List[str]], start_id: int = 2000) -> None:
    """Rebuild car mod kit IDs with progress tracking."""
    new_id = rebuild_handling_ids(meta_files["handling"], start_id)
    summary = {"count": 0, "cars": {}, "handlingDuplicates": {}}

    with tqdm.tqdm(meta_files["carcols"], desc="Processing vehicle files") as pbar:
        for file_path in pbar:
            try:
                directory = os.path.dirname(file_path)
                vehicle_meta_file_path = next(
                    (f for f in meta_files["vehicles"] if f.startswith(directory)),
                    None
                )
                model_name = get_model_name(vehicle_meta_file_path) if vehicle_meta_file_path else "Unknown"

                def transform_content(content: str) -> str:
                    nonlocal new_id
                    ids_found = set(re.findall(r'<id value="(\d+)"', content))
                    kit_names_found = set(re.findall(r'<kitName>(\d+)(_[\w]+)</kitName>', content))

                    for id_val in ids_found.union(kit_names_found):
                        original_id = id_val[0] if isinstance(id_val, tuple) else id_val
                        suffix = id_val[1] if isinstance(id_val, tuple) else "_default_modkit"
                        new_kit_name = f"{new_id}{suffix}"
                        content = content.replace(
                            f'<id value="{original_id}"',
                            f'<id value="{new_id}"'
                        )
                        content = content.replace(
                            f'<kitName>{original_id}{suffix}</kitName>',
                            f'<kitName>{new_kit_name}</kitName>'
                        )
                        summary["cars"][new_id] = {
                            "file_path": file_path,
                            "model_name": model_name,
                            "original_id": original_id,
                            "new_id": new_id,
                            "kitName": new_kit_name
                        }
                        new_id += 1
                    return content

                safe_file_update(file_path, transform_content)
                pbar.set_postfix({"current_id": new_id})

            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                continue

    summary["count"] = len(summary["cars"])

    with open('car_mods_summary.json', 'w', encoding='utf-8') as json_file:
        json.dump(summary, json_file, indent=4, ensure_ascii=False)

def main():
    """Main entry point with error handling."""
    try:
        folder_selected = select_directory()
        if not folder_selected:
            print("No folder selected! Exiting...")
            return

        print("Starting processing...")
        meta_files = find_meta_files(folder_selected)
        rebuild_car_mod_kit_ids(meta_files)
        print("\nProcessing complete. Summary saved to 'car_mods_summary.json'.")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())
