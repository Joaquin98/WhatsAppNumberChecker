import undetected_chromedriver as uc
from fp.fp import FreeProxy
from selenium import webdriver

HEADLESS = True
HEADLESS = False


def set_proxy(options):
    proxy_server_url = FreeProxy(timeout=1).get()
    options.add_argument(f"--proxy-server={proxy_server_url}")


def get_driver(proxy=False):
    options = uc.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless")
    if proxy:
        set_proxy(options)
    driver = uc.Chrome(options=options)
    return driver


def get_driver2():

    # Define las opciones del navegador
    options = webdriver.ChromeOptions()

    # Adding argument to disable the AutomationControlled flag
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--log-level=3')
    if HEADLESS:
        options.add_argument("--headless")
    set_proxy(options)
    # Exclude the collection of enable-automation switches
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Turn-off userAutomationExtension
    options.add_experimental_option("useAutomationExtension", False)

    # Setting the driver path and requesting a page
    driver = webdriver.Chrome(options=options)

    return driver
