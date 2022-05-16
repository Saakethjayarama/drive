from multiprocessing.sharedctypes import Value
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get('https://web.sensibull.com/option-chain?expiry=2022-05-19&tradingsymbol=BANKNIFTY')
driver.maximize_window()

table = driver.find_element(by=By.ID, value="oc-table-body")
rows = len(table.find_elements(by=By.CLASS_NAME, value="rt-tr-group"))

ocData = []
for i in range(rows):

    oi_change_ce = driver.find_element(by=By.XPATH, value=f'//*[@id="oc-table-body"]/div[{i+1}]/div/div[1]').get_attribute('innerHTML')
    oi_lakh_ce = driver.find_element(by=By.XPATH, value=f'//*[@id="oc-table-body"]/div[{i+1}]/div/div[2]').text

    ltp_ce = driver.find_element(by=By.XPATH, value=f'//*[@id="oc-table-body"]/div[{i+1}]/div/div[3]/div/div/div[1]').get_attribute('innerHTML')
    print(ltp_ce)
    ltp_ce_price = ltp_ce.split('&nbsp;')[0]

    ltp_ce_change_sign = driver.find_element(by=By.XPATH, value='//*[@id="oc-table-body"]/div[5]/div/div[3]/div/div/div/div/span[1]').text
    ltp_ce_change_value =  driver.find_element(by=By.XPATH, value=f'//*[@id="oc-table-body"]/div[{i+1}]/div/div[3]/div/div/div[1]/div').get_attribute('innerHTML').split('<span>.?<\/span>')

    strike = driver.find_element(by=By.XPATH, value=f'//*[@id="oc-table-body"]/div[{i+1}]/div/div[4]').text
    iv = driver.find_element(by=By.XPATH, value=f'//*[@id="oc-table-body"]/div[{i+1}]/div/div[5]').text

    oi_change_pe = driver.find_element(by=By.XPATH, value=f'//*[@id="oc-table-body"]/div[{i+1}]/div/div[8]').get_attribute('innerHTML')
    oi_lakh_pe = driver.find_element(by=By.XPATH, value=f'//*[@id="oc-table-body"]/div[{i+1}]/div/div[7]').text

    # //*[@id="oc-table-body"]/div[6]/div/div[3]/div/div/div[1]/text()[1]
    # //*[@id="oc-table-body"]/div[8]/div/div[3]/div/div/div[1]/text()[1]
    
    print({
        'strike':strike,
        'iv': iv,
        'oi_change_ce': oi_change_ce,
        'oi_lakh_pe': oi_lakh_pe,
        'oi_lakh_ce': oi_lakh_ce,
        'oi_change_pe': oi_change_pe,
        'ltp_ce': {
            'price': ltp_ce_price,
            'change': ltp_ce_change_sign + str(ltp_ce_change_value)
        }
    })
    break