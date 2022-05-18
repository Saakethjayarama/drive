import json
from multiprocessing.sharedctypes import Value
from selenium import webdriver
from selenium.webdriver.common.by import By
import re

driver = webdriver.Chrome()
driver.get('https://web.sensibull.com/option-chain?expiry=2022-05-19&tradingsymbol=NIFTY')
driver.maximize_window()

table = driver.find_element(by=By.ID, value="oc-table-body")
rows = len(table.find_elements(by=By.CLASS_NAME, value="rt-tr-group"))

ocData = []
for i in range(rows):

    oi_change_ce = driver.find_element(by=By.XPATH, value=f'//*[@id="oc-table-body"]/div[{i+1}]/div/div[1]').get_attribute('innerHTML')
    oi_lakh_ce = driver.find_element(by=By.XPATH, value=f'//*[@id="oc-table-body"]/div[{i+1}]/div/div[2]').text

    ltp_ce = driver.find_element(by=By.XPATH, value=f'//*[@id="oc-table-body"]/div[{i+1}]/div/div[3]/div/div/div[1]').get_attribute('innerHTML')
    ltp_ce_price = ltp_ce.split('&nbsp;')[0].strip()

    if ltp_ce_price == '-':
        ltp_ce_change_sign = ''
        ltp_ce_change_value = '0'
    else:
        ltp_ce_change_sign = driver.find_element(by=By.XPATH, value=f'//*[@id="oc-table-body"]/div[{i+1}]/div/div[3]/div/div/div/div/span[1]').text
        string =  driver.find_element(by=By.XPATH, value=f'//*[@id="oc-table-body"]/div[{i+1}]/div/div[3]/div/div/div[1]/div').get_attribute('innerHTML')
        pattern = r'<span>.?<\/span>'
        ltp_ce_change_value = re.split(pattern, string)[1]

    strike = driver.find_element(by=By.XPATH, value=f'//*[@id="oc-table-body"]/div[{i+1}]/div/div[4]').text
    iv = driver.find_element(by=By.XPATH, value=f'//*[@id="oc-table-body"]/div[{i+1}]/div/div[5]').text

    ltp_pe = driver.find_element(by=By.XPATH, value=f'//*[@id="oc-table-body"]/div[{i+1}]/div/div[6]/div/div/div[1]').get_attribute('innerHTML')
    ltp_pe_price = ltp_pe.split('&nbsp;')[0].strip()

    if ltp_pe_price == '-':
        ltp_pe_change_sign = ''
        ltp_pe_change_value = '0'
    else:
        ltp_pe_change_sign = driver.find_element(by=By.XPATH, value=f'//*[@id="oc-table-body"]/div[{i+1}]/div/div[6]/div/div/div/div/span[1]').text
        string =  driver.find_element(by=By.XPATH, value=f'//*[@id="oc-table-body"]/div[{i+1}]/div/div[6]/div/div/div[1]/div').get_attribute('innerHTML')
        pattern = r'<span>.?<\/span>'
        ltp_pe_change_value = re.split(pattern, string)[1]

    oi_change_pe = driver.find_element(by=By.XPATH, value=f'//*[@id="oc-table-body"]/div[{i+1}]/div/div[8]').get_attribute('innerHTML')
    oi_lakh_pe = driver.find_element(by=By.XPATH, value=f'//*[@id="oc-table-body"]/div[{i+1}]/div/div[7]').text

    ocData.append({
        'oi_change_ce': oi_change_ce,
        'oi_lakh_ce': oi_lakh_ce,
        'ltp_ce': {
            'price': ltp_ce_price,
            'change': ltp_ce_change_sign + str(ltp_ce_change_value)
        },
        'strike':strike,
        'iv': iv,
        'ltp_pe': {
            'price': ltp_pe_price,
            'change': ltp_pe_change_sign + str(ltp_pe_change_value)
        },
        'oi_lakh_pe': oi_lakh_pe,
        'oi_change_pe': oi_change_pe,
    })

with open('oi_nifty.json', 'w') as f:
    f.write(json.dumps(ocData))