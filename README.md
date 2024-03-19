# Car Mod Kit and Handling ID Rebuilder

This script is designed for game modders and enthusiasts working with vehicle modifications in gaming environments. It provides an all-in-one solution to manage, update, and ensure the uniqueness of IDs in `carcols.meta`, `vehicles.meta`, and `handling.meta` files within a specified directory. Additionally, it generates a detailed summary of modifications, including model names and duplicate handling names.

## Features

- **Sequential ID Updates**: Automatically updates `<id value="...">` and `<kitName>` tags in `carcols.meta`, as well as `<handlingName>` in `handling.meta`, starting from a base ID of 2000.
- **Model Name Inclusion**: Extracts and includes `<modelName>` from `vehicles.meta` in the output summary.
- **Duplicate Handling Detection**: Identifies and lists duplicate handling names within `handling.meta` files.
- **Comprehensive Summary**: Outputs a `car_mods_summary.json` file, detailing the processed vehicles, their new IDs, model names, and any duplicate handling entries.

## Usage

1. **Environment Setup**: Ensure you have Python 3 installed on your system.
2. **Download**: Clone or download this script to your local machine.
3. **Execution**: Run the script via a command-line interface. On Windows, PowerShell or CMD can be used; on Linux or macOS, use the Terminal.
4. **Directory Selection**: When prompted, select the directory containing your `.meta` files. Windows users will see a graphical folder selection dialog, while users on other operating systems will input the directory path manually.
5. **Review Summary**: After the script completes, examine the `car_mods_summary.json` file in the script's directory for a detailed summary of all changes and noted duplicates.

## Output Details

The `car_mods_summary.json` includes:
- **Count**: The total number of processed car mod kits.
- **Cars**: Detailed entries for each vehicle, including file paths, original and new IDs, model names, and updated kit names.
- **HandlingDuplicates**: A list of duplicate handling names found, along with their file paths.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](https://github.com/Irishstevie/duplicate-Meta-Handing-system/blob/main/LICENSE) file for full details.

## Acknowledgments

This project is a fork and extension of the "Duplicated tuning kit ID finder" originally created by SM mest3r. The foundation provided by this tool has been instrumental in developing further functionalities.

- **Original Creator**: SM mest3r
- **Website**: [smmest3r.dev](https://smmest3r.dev/)
- **Development Site**: [mest3rdevelopment.com](https://mest3rdevelopment.com/)
- **Original GitHub Repository**: [SMmest3r/duplicatedTuningIdFinder](https://github.com/SMmest3r/duplicatedTuningIdFinder)

A heartfelt thank you to SM mest3r for the initial creation and to the open-source community for ongoing support and contributions.
