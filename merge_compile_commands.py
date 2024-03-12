import json

def merge_compile_commands(file1, file2, output_file):
    with open(file1, 'r') as f:
        data1 = json.load(f)
    with open(file2, 'r') as f:
        data2 = json.load(f)

    merged_data = data1 + data2

    with open(output_file, 'w') as f:
        json.dump(merged_data, f, indent=4)

# Usage
merge_compile_commands('hostapd/compile_commands.json', 
                       'wpa_supplicant/compile_commands.json', 
                       'cc.json')
