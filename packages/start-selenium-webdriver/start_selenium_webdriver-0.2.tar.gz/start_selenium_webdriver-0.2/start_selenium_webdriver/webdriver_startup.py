import platform
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

from subprocess import getoutput
from pathlib import Path


def start_web_driver(endpoint, num_sec_implicit_wait=3, gui=True, options=Options(),
                     firefox_bin_path="C:/Program Files/Mozilla Firefox/firefox.exe"):

    """Starts a selenium webdriver, while taking care of dependencies.
        num_sec_implicit_wait:  How many seconds the selenium driver should wait before failing (See selenium docs.)
        gui: False tells selenium to run headless
        options: Gives the possibility to add additional parameters for the driver startup
        firefox_bin_path: for windows finding the firefox binary path only works automatically if firefox is installed without the microsoft store, otherwise it has the binary path has to be provided
    """

    _linux = "Linux"
    _windows = "Windows"
    _path_windows_mozilla_bin_location = Path(firefox_bin_path)

    active_system = platform.system()
    options.headless = not gui
    exec_path = GeckoDriverManager().install()

    if active_system == _linux:
        snap_firefox_binary_location = getoutput("find /snap/firefox -name firefox")
        if "No such file or directory" in snap_firefox_binary_location:
            options.binary_location = "/usr/bin/firefox"  # non snap version
        else:
            options.binary_location = snap_firefox_binary_location.split("\n")[-1]  # snap installed firefox version

    elif active_system == _windows:
        options.binary_location = str(_path_windows_mozilla_bin_location.resolve())
    else:
        raise ValueError("You are running on a non-supported platform.")

    driver = webdriver.Firefox(options=options, executable_path=exec_path)

    driver.get(endpoint)
    driver.implicitly_wait(num_sec_implicit_wait)

    return driver
