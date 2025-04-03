from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
# 혹은 options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)
driver.get('http://naver.com')
driver.implicitly_wait(3)
driver.get_screenshot_as_file('naver_main_headless.png')

driver.quit()