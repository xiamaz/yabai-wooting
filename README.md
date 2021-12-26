# Yabai Wooting scripts

## Installation requirements

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
