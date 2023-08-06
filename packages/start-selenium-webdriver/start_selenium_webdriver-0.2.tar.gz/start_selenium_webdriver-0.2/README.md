# start_selenium_webdriver

One simple selenium webdriver start script that (tries to) take care of binary locations and dependendencies in a platform independent manner.

Example:

```python

from start_selenium_webdriver.webdriver_startup import start_web_driver

end_point = "https://www.google.com/"
driver = start_web_driver(end_point, num_sec_implicit_wait=0)

```


## Note

Only works with firefox atm. and therefore needs a valid firefox installation.

## Roadmap

* Support Chrome webdriver

## Contributions & Improvments

Be encouraged to send pull-requests for any kind of improvment.