#!/usr/bin/env python3
"""Show the currently active desktop with a red key on the number row.
"""
import sys
from wooting_rgb import wooting_rgb_wrapper
from yabai_client import YabaiClient

ACTIVE_COLOR = (255, 199, 0)

active_did = int(sys.argv[1])
last_did = int(sys.argv[2])

yc = YabaiClient()
display_infos = yc.send_message("query --displays")
active_dindex = 0
last_dindex = 0
for display_info in display_infos:
    if display_info["id"] == active_did:
        active_dindex = display_info["index"]
    elif display_info["id"] == last_did:
        last_dindex = display_info["index"]

if active_dindex == 0 or last_dindex == 0:
    raise RuntimeError("Could not find display index")

spaces_info = yc.send_message("query --spaces")

active_index = 0
last_index = 0
for space_info in spaces_info:
    if not space_info["visible"]:
        continue
    if space_info["display"] == active_dindex:
        active_index = space_info["index"]
    elif space_info["display"] == last_dindex:
        last_index = space_info["index"]

if active_index == 0 or last_index == 0:
    raise RuntimeError("Could not find index")

wooting_rgb_wrapper.wooting_rgb_kbd_connected()
wooting_rgb_wrapper.wooting_rgb_direct_reset_key(1, last_index)
wooting_rgb_wrapper.wooting_rgb_direct_set_key(1, active_index, *ACTIVE_COLOR)
