# Inline SCTime

This plugin is designed to detect and automatically inject estimated supercruise travel times. Whenever a distance
such as "30 kls" or "30000ls" is printed in chat, this plugin will estimate the supercruise travel time calculated
with the same equations that Mecha/SwiftSqueak uses. It is designed with dispatchers in mind, though all are welcome
to use it.

![Inline-sctime example](/Images/example.png)

# Installation:

## AdiIRC:

1. Open AdiIRC
2. Go to Tools > Edit Scripts
3. Create a new script (file > new)
4. Copy the contents of [AdiIRC/inline-sctime.ini](AdiIRC/inline-sctime.ini) into the new file
5. Save the file with the name inline-sctime.ini (file > save)

## mIRC:

1. Open AdiIRC
2. Go to Tools > Scripts Editor
3. Copy the contents of [mIRC/remote.ini](mIRC/remote.ini) into the Remote tab
4. Copy the contents of [mIRC/aliases.ini](mIRC/aliases.ini) into the Aliases tab
5. Save the files (file > save all)

## HexChat:

Close HexChat. Open a file browser and go to the folder for your OS:

    - Windows: %APPDATA%\HexChat\addons
    - Microsoft Store: %LOCALAPPDATA%\Packages\39215TingPing.HexChat_fqe8h3fzrj50c\LocalCache\Roaming\HexChat\addons
    - Unix: ~/.config/hexchat/addons
    - Flatpak: ~/.var/app/io.github.Hexchat/config/hexchat/addons
    - Snap: ~/snap/hexchat/current/.config/hexchat/addons

Download [HexChat/inline_sctime.py](HexChat/inline_sctime.py) and save the file to the above directory.

## Features:

- Injects estimated supercruise travel time next to detected distances
- AdiIRC only, injected text color will match the whois color, gravwell detection with -g or 'gravwell'
- Toggle the plugin with the command "/togglesctime" (case insensitive)
- /sctime alias for silent one-off calculation
- All messages, or just case callouts
  - Case callouts are prefixed with the case number (ex: #69 bc+ 20kls)
  - Choose the desired regular expression at the top of the plugin file


# TODO:

- Color formatting for HexChat, mIRC
- Configurable options
  - Color options
  - Channel limit options
  - Callout limit options
- Calculate multiple sctimes in a single line
- Organize Adi into separate functions

# Limitations:

Purposeful:  
Mecha is ignored  
Distances in light years are ignored over 0.5ly  

Unintentional:  
Historic logs when launching a client might print incorrect (now) timestamps for lines with distances in them  

Adi:  
Only calculates right-most distance in a message   
Does not support DMs  

HexChat:  
Only calculates left-most distance in a message  
Does not support DMs  
