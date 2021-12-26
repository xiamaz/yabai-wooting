#!/usr/bin/env python3
"""Show the currently active desktop with a red key on the number row.
"""
import sys
from wooting_rgb import wooting_rgb_wrapper
from yabai_client import YabaiClient

ACTIVE_COLOR = (255, 199, 0)

active_id = int(sys.argv[1])
last_id = int(sys.argv[2])

yc = YabaiClient()
spaces_info = yc.send_message("query --spaces")

active_index = 0
last_index = 0
for space_info in spaces_info:
    if space_info["id"] == active_id:
        active_index = space_info["index"]
    elif space_info["id"] == last_id:
        last_index = space_info["index"]

if active_index == 0 or last_index == 0:
    raise RuntimeError("Could not find index")

wooting_rgb_wrapper.wooting_rgb_kbd_connected()
wooting_rgb_wrapper.wooting_rgb_direct_reset_key(1, last_index)
wooting_rgb_wrapper.wooting_rgb_direct_set_key(1, active_index, *ACTIVE_COLOR)
