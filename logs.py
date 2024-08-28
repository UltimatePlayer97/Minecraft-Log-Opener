import os
import platform
import requests
import json
import subprocess

os_system = platform.system()

os.system('COLOR A0')
print(r"""    __                   ____                            
   / /   ____  ____ _   / __ \____  ___  ____  ___  _____
  / /   / __ \/ __ `/  / / / / __ \/ _ \/ __ \/ _ \/ ___/
 / /___/ /_/ / /_/ /  / /_/ / /_/ /  __/ / / /  __/ /    
/_____/\____/\__, /   \____/ .___/\___/_/ /_/\___/_(_)   
            /____/        /_/                            """)

# Ask user for custom logs directory or use default directory
custom_directory = input("Enter the path to the directory where latest.log is located (press Enter to use default directory): ")

if custom_directory.strip() == "":
    if os_system == "Windows":  # Windows
        appdata = os.getenv("APPDATA")
        logs_directory = os.path.join(appdata, r".minecraft\logs")
    elif os_system == "Linux":  # Linux
        logs_directory = os.path.expanduser("~/.minecraft/logs")
    elif os_system == "Darwin":  # MacOS
        logs_directory = os.path.expanduser("~/.minecraft/logs")
    else:
        print("Unsupported Operating System")
        exit()
else:
    logs_directory = custom_directory

latest_logs_path = os.path.join(logs_directory, "latest.log")

api_input = input("Do you wish to create a link for your log file? [Y/N]: ")

if api_input.lower() == "y" | api_input.lower() == "yes":

    if os.path.exists(latest_logs_path):
        # Read the content of the latest.log file
        with open(latest_logs_path, 'r', encoding='utf-8') as log_file:
            log_content = log_file.read()

        URL = "https://api.mclo.gs/1/log"
        # Prepare the PAYLOAD for POST request using 'content' as the key
        PAYLOAD = {
            "content": log_content  # Use the actual log content
        }

        # Post the log content to the API
        response = requests.post(url=URL, data=PAYLOAD) 
        
        # Directly get the JSON response
        data = response.json()

        # Check if the response contains the 'url' key
        if 'url' in data:
            print("URL:", data['url'])
            
            # Copy the URL to the clipboard based on the operating system
            if os_system == "Windows":
                # Use 'clip' command for Windows
                subprocess.run("echo " + data['url'] + "| clip", shell=True)
                print("URL copied to clipboard.")
            elif os_system == "Linux":
                # Use 'xclip' or 'xsel' command for Linux (ensure one of these is installed)
                subprocess.run("echo " + data['url'] + " | xclip -selection clipboard", shell=True)
                print("URL copied to clipboard.")
            elif os_system == "Darwin":
                # Use 'pbcopy' command for macOS
                subprocess.run("echo " + data['url'] + " | pbcopy", shell=True)
                print("URL copied to clipboard.")
            else:
                print("Unsupported Operating System for clipboard operation.")
        else:
            print("No 'url' key found in the response.")
    else:
        print("latest.log was not found in the specified directory")
    

notepad_input = input("Do you wish to open the specified log in Notepad? [Y/N]: ")

if notepad_input.lower() == "y" | notepad_input.lower() == "yes":

    if os_system == "Windows":
            print(f"Opening file in: {latest_logs_path}")
            os.system(f"notepad.exe {latest_logs_path}")
    elif os_system in ["Linux", "Darwin"]:  # Linux or MacOS
            print(f"Opening file in: {latest_logs_path}")
            os.system(f"open -e {latest_logs_path}")
    else:
        print("latest.log was not found in the specified directory")
else:
    print("Log file not opened.")

input()