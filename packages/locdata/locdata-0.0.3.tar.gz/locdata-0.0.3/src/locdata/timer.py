from __future__ import print_function
import time
import json
import datetime
import sys
import win32gui
import uiautomation as auto
from locdata.activity import AcitivyList, TimeEntry, Activity
from locdata.custom_exception import InvalidOSException
activeList = AcitivyList([])

try:
    if sys.platform in ["Mac", "darwin", "os2", "os2emx"]:
        raise InvalidOSException
    elif sys.platform in ["linux", "linux2"]:
        raise InvalidOSException
except InvalidOSException:
    print("This package is not build for MACOS or Linux.\nIf you want to use it for macos you can use locadataMAC ")

try:
    activeList.initialize_me()
except Exception:
    print("No json")

def get_active_window():
    _active_window_name = None
    if sys.platform in ["Windows", "win32", "cygwin"]:
        window = win32gui.GetForegroundWindow()
        _active_window_name = win32gui.GetWindowText(window)
    else:
        print("sys.platform={platform} is not supported.".format(platform=sys.platform))
        print(sys.version)
    return _active_window_name


def get_chrome_url():
    _active_window_name = None
    if sys.platform in ["Windows", "win32", "cygwin"]:
        window = win32gui.GetForegroundWindow()
        chromeControl = auto.ControlFromHandle(window)
        edit = chromeControl.EditControl()
        web = edit.GetValuePattern().Value
        return web.split('/')[0]
    else:
        print("sys.platform={platform} is not supported.".format(platform=sys.platform))
        print(sys.version)
    return _active_window_name


def start():
    global active_window_name
    active_window_name = ""

    global first_time
    first_time = True

    global start_time
    start_time = datetime.datetime.now()

    global activity_name
    activity_name = ""

    try:
        while True:
            if sys.platform not in ["linux", "linux2"]:
                new_window_name = get_active_window()
                if "Google Chrome" in new_window_name:
                    new_window_name = get_chrome_url()

            if active_window_name != new_window_name:
                print(active_window_name)
                activity_name = active_window_name

                if not first_time:
                    end_time = datetime.datetime.now()
                    time_entry = TimeEntry(start_time, end_time, 0, 0, 0, 0)
                    time_entry._get_specific_times()

                    exists = False
                    for activity in activeList.activities:
                        if activity.name == activity_name:
                            exists = True
                            activity.time_entries.append(time_entry)

                    if not exists:
                        activity = Activity(activity_name, [time_entry])
                        activeList.activities.append(activity)
                    with open("activities.json", "w") as json_file:
                        json.dump(
                            activeList.serialize(), json_file, indent=4, sort_keys=True
                        )
                        start_time = datetime.datetime.now()
                first_time = False
                active_window_name = new_window_name

            time.sleep(1)

    except KeyboardInterrupt:
        with open("activities.json", "w") as json_file:
            json.dump(activeList.serialize(), json_file, indent=4, sort_keys=True)
