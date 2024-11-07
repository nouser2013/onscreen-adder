import os
import sys
import logging
import argparse
import subprocess
import shutil
import datetime

# Config Section for your environment
MONITOR = "27GN950_12345-67890"
PROFILE = "Game 1"
PROFILE_NUMBER = 45

# Configure logging and make it pretty
logging.basicConfig(level=logging.DEBUG, encoding='utf-8', format="[%(asctime)s] [%(levelname)s] %(message)s")
logging.addLevelName(logging.DEBUG, "\x1b[30;20mDBG\x1b[0m")
logging.addLevelName(logging.INFO, "\x1b[32;20mINF\x1b[0m")
logging.addLevelName(logging.WARNING, "\x1b[33;20mWRN\x1b[0m")
logging.addLevelName(logging.ERROR, "\x1b[31;20mERR\x1b[0m")

# OK, let's start...
print()
print("  OnScreen [Control] Adder")
print("  ========================")
print()

# Some basic checks. First, if running on windows...
if not os.name == "nt":
    logging.error("Script can only run on Windows, as OnScreen Control is a Windows program.")
    sys.exit(1)
# Second, if LG OSC is running
s = subprocess.check_output('tasklist', text=True)
if "OnScreen Control.exe" in s:
    logging.warning("OnScreen Control is running. Restart program to apply changes made by this script!")

# Get installed LG OnScreen folders, one for each screen
lgScreens = []
try:
    lgScreens = os.listdir(os.path.expanduser("~\\Documents\\OnScreen Control"))
except:    
    logging.error("Could not enumerate directories in '$USERHOME$\\Documents\\OnScreen Control' directory. Do you have OnScreen Control installed?")
    sys.exit(2)
try:
    lgScreens.remove("My Profiles")
except:
    logging.warning("There is no 'My Profiles' folder in OnScreen Control folder. Perhaps a newer, incompatible version, is installed?")
if len(lgScreens) == 0:
    logging.error("Could not find any folders in 'OnScreen Control' folder. Do you have LG monitors?")
    sys.exit(3)
logging.info("LG OnScreen Control folder structure seems to be in order.")

# Configure ArgParse
parser = argparse.ArgumentParser(
    "osa.py",
    description="This script adds an executable to LGs OnScreen Control. It became necessary because not every Software or Video game would show up in the built-in selector.\n\nDisclaimer: not affiliated with LG or any of its subsidiaries."
)
parser.add_argument("-m", "--monitor", type=str, help="name of the screen you want to add the program for", choices=lgScreens, default=MONITOR)
parser.add_argument("-p", "--profile", type=str, help="which profile name to add (e.g., 'Game 2')?", default=PROFILE)
parser.add_argument("-pn", "--profile-number", type=int, help="which profile number to add (e.g., 45)?", default=PROFILE_NUMBER)
parser.add_argument("EXECUTABLE", type=str, help="Which executable to add to the configuration? Either supply a binary from current working directory (e.g., helldivers2.exe) or supply the path in double quotes (e.g., \"D:\\Games\\Helldivers 2\\helldivers2.exe\").")
parser.add_argument("DISPLAY_NAME", type=str, help="what is the window title of the application (e.g., \"Helldivers 2\")? Use double-quotes where necessary.")
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(4)
args = parser.parse_args()

# Ok, got all arguments or defaults, let's check if the destination exists and is an EXE file.
if not os.path.exists(args.EXECUTABLE):
    logging.error(f"Given EXECUTABLE value \x1b[97;1;20m{args.EXECUTABLE}\x1b[0m does not point to a file.")
    sys.exit(5)
if not str(args.EXECUTABLE).lower().endswith(".exe"):
    logging.warning(f"Given EXECUTABLE value \x1b[97;1;20m{args.EXECUTABLE}\x1b[0m does not end with '.exe'. This will likely not work.")

args.EXECUTABLE = os.path.abspath(args.EXECUTABLE)
logging.info("Provided EXECUTABLE seems to point to a file.")

# Let's read the config file...
configFileName = os.path.expanduser("~\\Documents\\OnScreen Control\\") + args.monitor + "\\" + args.monitor + ".txt"
configFileLines = []
try:
    with open(configFileName, mode="r", encoding='utf-16') as f:
        configFileLines = f.readlines()
    configFileLines = [(x.strip() + "\n") for x in configFileLines if x.strip() != ""]
    if len(configFileLines) == 0:
        logging.warning(f"There are no configured monitor profiles in your configuration file. At least the default profile should be there. This is strange.")
except:
    logging.error(f"Could not read the monitor's configuration file '{configFileName}'. Abort.")
    sys.exit(7)

# Let's see if this binary already exists in the file...
executableTestString = os.path.basename(args.EXECUTABLE).lower()
for configFileEntry in configFileLines:
    logging.debug(f"Testing for '{executableTestString}' in '{configFileEntry.lower().strip()}'...")
    if executableTestString in configFileEntry.lower():
        logging.error(f"Given EXECUTABLE value \x1b[97;1;20m{os.path.basename(args.EXECUTABLE)}\x1b[0m is already present in the config file of the monitor.")
        sys.exit(8)

# All there, now let's add...
logging.info(f"All checks passed, adding '{args.EXECUTABLE}' to chosen monitor '{args.monitor}'.")
logging.debug(f"Executable: {args.EXECUTABLE}")
logging.debug(f"Window Title: {args.DISPLAY_NAME}")
logging.debug(f"Monitor: {args.monitor}")
logging.debug(f"Profile: {args.profile}")
logging.debug(f"Number: {args.profile_number}")
configLineToAdd = f"{args.DISPLAY_NAME};{args.profile};{os.path.basename(args.EXECUTABLE)};{args.EXECUTABLE};{args.profile_number}\n"
logging.debug(f"Compiled CSV line: '''{configLineToAdd.strip()}'''")

# Create backup of current file...
logging.info(f"Creating backup of current config file '{configFileName}'...")
try:
    shutil.copyfile(configFileName, os.path.expanduser("~\\Documents\\OnScreen Control\\") + args.monitor + "\\" + datetime.date.strftime(datetime.datetime.now(), "%Y%m%dT%H%M%S") + " - " + args.monitor + ".txt")
except:
    logging.error(f"Could not backup the current config file. Abort.")
    sys.exit(8)

# Append Entry
logging.info(f"Adding new line to the config file...")
configFileLines.append(configLineToAdd)
try:
    with open(configFileName, mode="w", encoding='utf-16') as f:
        f.writelines(configFileLines)
except:
    logging.error(f"Could not add the config line to the monitor's configuration file '{configFileName}'. Abort.")
    sys.exit(9)

# Ok, all done
logging.info(f"Successfully added \x1b[97;1;20m{args.EXECUTABLE}\x1b[0m to \x1b[97;1;20m{configFileName}\x1b[0m.")