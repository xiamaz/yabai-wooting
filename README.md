# Yabai Wooting scripts

## Installation requirements

Wooting RGB SDK needs to be installed. This can be easily done with Homebrew
using the following command:

```
brew install xiamaz/formula/wooting-rgb-sdk
```

Both https://github.com/xiamaz/python-yabai-client and
https://github.com/xiamaz/python-wooting-rgb need to be installed before these
scripts can be run.

## Spaces indicator

Use the following scripts for indicating the active space by adding the
following signals:

```
yabai -m signal --add event=space_changed action='set_space_switch.py $YABAI_SPACE_ID $YABAI_RECENT_SPACE_ID' label=wootspace
yabai -m signal --add event=display_changed action='set_space_display_switch.py $YABAI_DISPLAY_ID $YABAI_RECENT_DISPLAY_ID' label=wootdisplay
```

## Server based spaces indicator

This requires `wooting_space_server.py` to be running in the background.

The script will automatically add rules into yabai. These will also be removed
on script exit.

In order for the space type indicator to work properly any keybinds that modify
the space type will need to have the following command as a part:

```
echo "refresh" | nc -U /tmp/yabai-wooting.socket
```
