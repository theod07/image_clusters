from bs4 import BeautifulSoup
import selenium.webdriver as webdriver

url = 'http://instagram.com/'
driver = webdriver.Firefox()
driver.get(url)

soup = BeautifulSoup(driver.page_source)

for x in soup.findAll('li', {'class':'photo'}):
    print x
