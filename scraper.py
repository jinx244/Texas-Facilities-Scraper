from selenium.common import exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://www.txssa.org/Online/Facility_Locator/Facility_Locator.aspx'
driver = webdriver.Chrome('C:/Users/admin/Downloads/chromedriver.exe')
driver.get(url)

texas_zip_codes = pd.read_csv('C:/Users/admin/Desktop/Social Explorer/MultiplePagesZIP.csv')

for zip_code in texas_zip_codes.zip:
    driver.refresh()
    search_input = driver.find_element(
        value='ctl01_TemplateBody_WebPartManager1_gwpcisearch_cisearch_zipsearch_ResultsGrid_Sheet0_Input0_TextBox1')
    search_input_submit_button = driver.find_element(
        value='ctl01_TemplateBody_WebPartManager1_gwpcisearch_cisearch_zipsearch_ResultsGrid_Sheet0_SubmitButton')
    search_input.clear()
    search_input.send_keys(zip_code)
    search_input_submit_button.click()
    el = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                         '//*[@id="ctl01_TemplateBody_WebPartManager1_gwpcisearch_cisearch_zipsearch_ResultsGrid_Grid1_ctl00"]/tbody/tr')))
    # try:
    #
    #     # show_all_results_button = driver.find_element(by=By.PARTIAL_LINK_TEXT, value='show all')
    #     # show_all_results_button.click()
    #
    #     page_button = driver.find_element(by=By.CLASS_NAME, value='rgPageFirst')
    #     with open(r'C:/Users/admin/Desktop/Social Explorer/MultiplePagesZIP.csv', 'a', newline='') as f3:
    #         writer = csv.writer(f3)
    #         writer.writerow([zip_code])
    #     f3.close()
    #     continue

    # except exceptions.NoSuchElementException as e:
    #     # with open(r'C:/Users/admin/Desktop/Social Explorer/SinglePagesZIP.csv', 'a', newline='') as f3:
    #     #     writer = csv.writer(f3)
    #     #     writer.writerow([zip_code])
    #     # f3.close()
    #     pass

    try:
        table_data = driver.find_elements(by=By.XPATH, value='//*[@id="ctl01_TemplateBody_WebPartManager1_gwpcisearch_cisearch_zipsearch_ResultsGrid_Grid1_ctl00"]/tbody/tr')
        for row in table_data:
            table_row = []
            columns = row.find_elements(by=By.XPATH, value='./td')
            for col in columns:
                table_row.append(col.text)
            table_row.append(zip_code)
            # print(table_row)

            with open(r'C:/Users/admin/Desktop/Social Explorer/TexasFacilities.csv', 'a', newline='') as f1:
                writer = csv.writer(f1)
                writer.writerow(table_row)
            f1.close()

        with open(r'C:/Users/admin/Desktop/Social Explorer/FinishedZIP.csv', 'a', newline='') as f2:
            writer = csv.writer(f2)
            writer.writerow([zip_code])
        f2.close()

    except exceptions.StaleElementReferenceException as e:
        with open(r'C:/Users/admin/Desktop/Social Explorer/StaleElementZIP.csv', 'a', newline='') as f4:
            writer = csv.writer(f4)
            writer.writerow([zip_code])
        f4.close()
        continue