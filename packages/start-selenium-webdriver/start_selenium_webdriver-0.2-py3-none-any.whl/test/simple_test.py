from start_selenium_webdriver.webdriver_startup import start_web_driver

end_point = "https://www.google.com/"
firefox_bin_path = "C:\Program Files\WindowsApps\Mozilla.Firefox_110.0.0.0_x64__n80bbvh6b1yt2\VFS\ProgramFiles\Firefox Package Root\\firefox.exe"
driver = start_web_driver(end_point, num_sec_implicit_wait=0, firefox_bin_path=firefox_bin_path)

print("Done")
