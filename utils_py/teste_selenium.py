print('aq')
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome()
driver.get("https://google.com")

print("Funcionou!")
driver.quit()