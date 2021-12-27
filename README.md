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

Add the following signales to your `.yabairc`:

```
yabai -m signal --add event=space_changed action='echo "space $YABAI_SPACE_ID" | nc -U /tmp/yabai-wooting.socket' label=wootserv
yabai -m signal --add event=display_changed action='echo "refresh $YABAI_DISPLAY_ID" | nc -U /tmp/yabai-wooting.socket' label=wootservdisplay
yabai -m signal --add event=mission_control_exit action='echo "refresh $YABAI_DISPLAY_ID" | nc -U /tmp/yabai-wooting.socket' label=wootservmc
yabai -m signal --add event=display_added action='echo "refresh $YABAI_DISPLAY_ID" | nc -U /tmp/yabai-wooting.socket' label=wootservda
yabai -m signal --add event=display_removed action='echo "refresh $YABAI_DISPLAY_ID" | nc -U /tmp/yabai-wooting.socket' label=wootservdr
```

In order for the space type indicator to work properly any keybinds that modify
the space type will need to have the following command as a part:

```
echo "refresh" | nc -U /tmp/yabai-wooting.socket
```
