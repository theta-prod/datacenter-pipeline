# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.set_capability("browserVersion", "107.0")
chrome_options.set_capability("platformName", "LINUX")

# create web driver with chrome
# chrome_options = Options()
# chrome_options.set_capability("browserVersion", "100")
# chrome_options.set_capability("platformName", "Windows XP")
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# browser = webdriver.Chrome(options=chrome_options)
browser = webdriver.Remote(command_executor='http://127.0.0.1:4444',
                           options=chrome_options)

# navigate to news list page
browser.get('https://36kr.com/information/web_news/')
browser.quit()
