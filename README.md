# OnScreen Control Adder

This script written for Python 3 can be used to automatically add a new program to your LG monitor's control software named **OnScreen Control**. Using the built-in function is a hassle, and it by far does not show all installed programs on your computer.

I use it to enable the monitor to switch between a 100% brightness `Game 1` HDR profile for gaming, and a much lower brightness profile `Game 2` for standard desktop applications.

> [!IMPORTANT]
> Please consider the following caveats:
> * This version supports the Windows version only. I don't own a Mac to test.
> * I tested the script with OnScreen Control `v9.28`.
> * The script will create a backup of the configuration file before changing it.

> [!NOTE]  
> **Disclaimer:** Neither I nor this program are in any way affiliated with LG or its subsidaries. Use at your own risk.

# Installation and Prerequisites

For it to work you need a recent Python 3 version. Anything above Python 3.9 should work. Also, we assume that your `py` command is working.

The script does not need to be installed, just copied to a folder of your choice. Let's assume for the rest of this text that you copied it to `C:\Users\$username$\Documents\osa.py`.

> [!IMPORTANT]  
> You need to make sure that the `My Application Preset` function is enabled for your monitor:
> * Open OnScreen Control.
> * Select the desired monitor in the bottom line.
> * Press the cog-wheel in the top-right corner to open the settings.
> * Select `My Application Preset`.
> * Turn it on if it isn't already.
> * Select the desired `Default` profile, for instance, `Game 2`.

# Usage

Open a command prompt or a PowerShell console (this one shows colors :smile:) and type `py "C:\Users\$username$\Documents\osa.py"`.

> [!CAUTION]  
> After you have used this script and added a program, **do not** open `My Application Preset` again. All your entries will be deleted otherwise.


## Command Line Parameters

If you call the script without parameters, it will show you the command line arguments and where to put them. Here's what they do:

### Monitor Selection (-m)

This argument selects the monitor you want to add the program to. Note that the script enumerates the possible options by listing all directories under `C:\Users\$username$\Documents\OnScreen Control\` except `My Profiles`.

The monitor's folder name will look something like this: `27GN950_12345_67890`.

> [!NOTE]  
> * You can add this string to the `osa.py` file in the configuration section at the top of the file. Then you don't need to specify the name every time, except for when you want to add a program to a different monitor.

### Monitor Profile to activate (-p)

This is the name of your monitor's profile that you want to activate when the selected Program is shown in foreground on the monitor.

To get the profile name, open the existing config file in the folder with a text app and note down what the second field shows, e.g., `Game 1`, `Game 2`, etc.

> [!NOTE]  
> * This is dependent on your operating system's language.
> * You can add this string to the `osa.py` file in the configuration section at the top of the file. Then you don't need to specify the name every time, except for when you want to add a program to a different monitor.

### Monitor Profile Number (-pn)

The reason for this number is unknown, however, you'll find the value also in the file if you have enabled the default `My Application Profile` setting. It will be an integer number, such as `46` (in my case for `Game 1`) or `45` (in my case for `Game 2`).

> [!NOTE]  
> * You can add this string to the `osa.py` file in the configuration section at the top of the file. Then you don't need to specify the name every time, except for when you want to add a program to a different monitor.

### EXECUTABLE

Pretty much self-explanatory, this positional argument receives either an absolute path to an executable, a relative path to an executable, or a direct executable name for processing.

> [!TIP]
> The easiest method is to navigate to the directory where the executable is located, and launch the script from there like so: `py "C:\Users\$username$\Documents\osa.py" -m XXX -p YYY -pn NN "my program.exe" "Program Name"`.


> [!WARNING]  
> The script tests if the file name is already present in the chosen monitor's configuration file, and will terminate in case it is.

> [!CAUTION]
> You **must** use double-quotes (`"`) around paths with a space in them.

### DISPLAY_NAME

Also, the program seems to require a display name of some sort, which you can set with this parameter.

> [!CAUTION]
> You **must** use double-quotes (`"`) around display names with a space in them.

## Examples

Here's a full example to add Helldivers 2 to a monitor and the `Game 1` profile:

`C:\>py "C:\Users\$username$\Documents\osa.py" -m 27GN950_12345_67890 -p "Game 1" -pn 46 "d:\Programs\Steam\steamapps\common\Helldivers 2\helldivers2.exe" "Helldivers 2"`

In case you added your monitor's name and the profile parameter already to the script, and the config section looks like this:

```python
# Config Section for your environment
MONITOR = "27GN950_12345_67890"
PROFILE = "Game 1"
PROFILE_NUMBER = 45
```

you can shorten the command:

`C:\>py "C:\Users\$username$\Documents\osa.py" "d:\Programs\Steam\steamapps\common\Helldivers 2\helldivers2.exe" "Helldivers 2"`

And lastly, if your opened the command prompt in the EXECUTABLE's folder already, it becomes even shorter:

`D:\Programs\Steam\steamapps\common\Helldivers 2\>py "C:\Users\$username$\Documents\osa.py" "helldivers2.exe" "Helldivers 2"`

> [!TIP]
> Optionally, experienced users can add the `osa.py` location to their `PATH` variable to shorten the command even more:  `D:\Programs\Steam\steamapps\common\Helldivers 2\>py osa.py "helldivers2.exe" "Helldivers 2"`