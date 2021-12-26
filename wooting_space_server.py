#!/usr/bin/env python3
# pylint: skip-file
# flake8: noqa

import pathlib
import socketserver
from yabai_client import YabaiClient
from wooting_rgb import wooting_rgb_wrapper

ACTIVE_COLOR = (255, 199, 0)  # currently active space
INACTIVE_COLOR = (255, 255, 255)  # spaces not in focus
DISABLED_COLOR = (0, 0, 0)  # spaces that do not exist
MAX_KEYS = 12  # maximum number of keys to be used for rgb

# This will put a color indicator on the "`" key of the current space type.
ENABLE_SPACE_TYPE_INDICATOR = True
SPACE_TYPE_COLORS = {
    "bsp": (0, 255, 255),
    "float": (255, 255, 0),
    "stack": (255, 0, 255),
}

YC = YabaiClient()

SERVER_ADDRESS="/tmp/yabai-wooting.socket"
Colors = [ACTIVE_COLOR, INACTIVE_COLOR, DISABLED_COLOR]

class YabaiWootingServer:

    def __init__(self):
        self._activeSpace = 0
        self._spaceIdMapping = {}
        self._spacesData = None

        self._rgbStatus = [3]*MAX_KEYS
        self._initialize()

    @property
    def activeSpace(self):
        return self._activeSpace

    @property
    def rgbStatus(self):
        return self._rgbStatus

    @activeSpace.setter
    def activeSpace(self, value):
        new_status = self._rgbStatus.copy()
        new_status[self._activeSpace-1] = 1
        new_status[value-1] = 0
        self._activeSpace = value
        self.update_keyboard(new_status)

    def setSpaceById(self, space_id):
        space_index = self._spaceIdMapping.get(space_id)
        if space_index:
            self.activeSpace = space_index
        else:
            # refresh ID mappings
            pass

    def _setIndicator(self):
        for sinfo in self._spacesData:
            if sinfo["index"] == self.activeSpace:
                color = SPACE_TYPE_COLORS[sinfo["type"]]
                wooting_rgb_wrapper.wooting_rgb_direct_set_key(1, 0, *color)
                break

    def _initialize(self):
        spaces_info = YC.send_message("query --spaces")
        self._spacesData = spaces_info

        new_status = []
        for i in range(MAX_KEYS):
            if i >= len(spaces_info):
                new_status.append(2)
            else:
                sinfo = spaces_info[i]
                self._spaceIdMapping[sinfo["id"]] = sinfo["index"]
                if sinfo["has-focus"] and sinfo["is-visible"]:
                    self._activeSpace = i + 1
                    new_status.append(0)
                else:
                    new_status.append(1)
        self.update_keyboard(new_status)

    def refresh_spaces(self):
        self._initialize()

    def update_keyboard(self, new_rgb_status):
        for i, status in enumerate(new_rgb_status):
            old_status = self._rgbStatus[i]
            if old_status != status:
                wooting_rgb_wrapper.wooting_rgb_direct_set_key(1, i + 1, *Colors[status])
                self._rgbStatus[i] = status

        if ENABLE_SPACE_TYPE_INDICATOR:
            self._setIndicator()


def process_request(request_string):
    name, *params = request_string.split(" ")
    response = ""
    if name == "space":
        # switched spaces
        SERVER.setSpaceById(int(params[0]))
    elif name == "refresh":
        # if display changed we will need to get new spaces info
        SERVER.refresh_spaces()
    elif name == "info":
        response += "Info:\n"
        response += f"RGBStatus: {SERVER.rgbStatus}\n"
        response += f"ActiveSpace: {SERVER.activeSpace}\n"
        response += f"SpaceMapping: {SERVER._spaceIdMapping}\n"
        response += "\n"
    return response


class YabaiWootingHandler(socketserver.StreamRequestHandler):

    def handle(self):
        request_data = self.rfile.read()
        request_string = request_data.decode("utf-8").strip()
        response = process_request(request_string)
        self.wfile.write(response.encode("utf-8"))


if __name__ == "__main__":
    wooting_rgb_wrapper.wooting_rgb_kbd_connected()
    wooting_rgb_wrapper.wooting_rgb_direct_set_key(1, 0, *Colors[2])
    wooting_rgb_wrapper.wooting_rgb_direct_set_key(1, 13, *Colors[2])

    SERVER = YabaiWootingServer()

    pathlib.Path(SERVER_ADDRESS).unlink(missing_ok=True)

    try:
        with socketserver.UnixStreamServer(SERVER_ADDRESS, YabaiWootingHandler) as server:
            server.serve_forever()
    except Exception as e:
        print("Error:", e)
    finally:
        wooting_rgb_wrapper.wooting_rgb_reset()
