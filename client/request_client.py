from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep

# disable the UI
opts = Options()
# opts.set_headless()
# assert opts.headless is True, "headless has not been set yet"# Operating in headless mode
browser = Chrome(options=opts)
browser.get('https://bandcamp.com')
browser.close()

