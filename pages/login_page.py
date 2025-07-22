import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import time
import json


driver = webdriver.Chrome()
    # ''''''
driver.get('https://demo.suiteondemand.com/index.php?action=Login&module=Users&login_module=Users&login_action=Logout')
time.sleep(2)
driver.maximize_window()

driver.find_element(By.ID,"user_name").send_keys('will')
time.sleep(2)

driver.find_element(By.ID,"username_password").send_keys('will')
time.sleep(2)

driver.find_element(By.NAME,'Login').click()
time.sleep(5)


acc_hover = driver.find_element(By.LINK_TEXT, 'CREATE')
action = ActionChains(driver)
action.move_to_element(acc_hover).perform()
time.sleep(5)

creat_acc = driver.find_elements(By.XPATH, "//ul/li/a[text()='Create Accounts']")
for i in creat_acc:
    if i.text == 'Create Accounts':
        i.click()
        break
time.sleep(3)

driver.find_element(By.ID,'name').send_keys("Courage & Power")
time.sleep(2)
driver.find_element(By.XPATH,"//input[@id='phone_office']").send_keys("8978375284")
time.sleep(2)
driver.find_element(By.XPATH,"//input[@id='website']").send_keys("www.youtube.com/")
time.sleep(2)
driver.find_element(By.ID,"phone_fax").send_keys("don't know")
time.sleep(2)
driver.find_element(By.XPATH,"//button[@title='Add Email Address ']").click()
driver.find_element(By.XPATH,"//input[@id='Accounts0emailAddress0']").send_keys("chinu@gmail.com")


#billing address

driver.find_element(By.XPATH,"//textarea[@id='billing_address_street']").send_keys("ODISHA")
time.sleep(2)
driver.find_element(By.XPATH,"//input[@id='billing_address_city']").send_keys("BHUBANESWAR")
time.sleep(2)
driver.find_element(By.XPATH,"//input[@id='billing_address_state']").send_keys("INDIAN")
time.sleep(2)
driver.find_element(By.XPATH,"//input[@id='billing_address_postalcode']").send_keys("467500")
time.sleep(2)
driver.find_element(By.XPATH,"//input[@id='billing_address_country']").send_keys("INDIA")
time.sleep(2)

#Shipping Address

driver.find_element(By.XPATH,"//textarea[@id='shipping_address_street']").send_keys("Odisha")
time.sleep(2)
driver.find_element(By.XPATH,"//input[@id='shipping_address_city']").send_keys("BHUBANESWAR")
time.sleep(2)
driver.find_element(By.XPATH,"//input[@id='shipping_address_state']").send_keys("INDIAN")
time.sleep(2)
driver.find_element(By.XPATH,"//input[@id='shipping_address_postalcode']").send_keys("467500")
time.sleep(2)
driver.find_element(By.XPATH,"//input[@id='shipping_address_country']").send_keys("INDIA")
time.sleep(2)
driver.find_element(By.XPATH,"//textarea[@id='description']").send_keys("This project is all about team work")

#more information

select_type= Select(driver.find_element(By.XPATH,"//select[@id='account_type']"))
select_type.select_by_visible_text("Investor")
time.sleep(2)
select_type= Select(driver.find_element(By.XPATH,"//select[@id='industry']"))
select_type.select_by_visible_text("Banking")
time.sleep(2)
driver.find_element(By.XPATH,"//input[@id='annual_revenue']").send_keys("20cr")
time.sleep(2)
driver.find_element(By.XPATH,"//input[@id='employees']").send_keys("18")
time.sleep(2)
driver.find_element(By.XPATH,"//input[@id='parent_name']").send_keys("Cardiology")
time.sleep(2)
driver.find_element(By.XPATH,"//input[@id='campaign_name']").send_keys("Medical")
time.sleep(2)
driver.find_element(By.XPATH,"//div[@id='EditView_tabs']/following-sibling::*[2]/input[@id='SAVE']").click()
time.sleep(3)

driver.find_element(By.XPATH,"//div[text()='View Accounts']").click()

headers = driver.find_elements(By.XPATH, "//table[contains(@class,'list')]//thead//th")
header_names = [h.text.strip() for h in headers if h.text.strip() != '']
print(" Headers:", header_names)

rows = driver.find_elements(By.XPATH, "//table[contains(@class,'list')]/tbody/tr")
all_data = []

for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    row_data = [cell.text.strip() for cell in cells]
    if row_data and len(row_data) >= len(header_names):
        data_dict = dict(zip(header_names, row_data[:len(header_names)]))
        all_data.append(data_dict)

json_file = "suitecrm_accounts.json"
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=4)

print(f" Data saved to {json_file}")
time.sleep(8)

# --- Step 4: Connect to MySQL ---
conn = mysql.connector.connect(
    host='127.0.0.1',
    port='3306',
    user='root',
    password='Jeeban9439@',
    database='sweetdata'
)

if conn.is_connected():
    print(" Connected to MySQL")
else:
    print(" Connection failed")

cursor = conn.cursor()

# --- Step 5: Create Table if not exists ---
cursor.execute('''
    CREATE TABLE IF NOT EXISTS crm_table (
        Name VARCHAR(50),
        City VARCHAR(50),
        Billing_country VARCHAR(20),
        Phone VARCHAR(20),
        User VARCHAR(50),
        Email VARCHAR(50),
        Date_create VARCHAR(50)
    )
''')

# --- Step 6: Extract and Insert Table Data ---
rows = driver.find_elements(By.XPATH, "//table[@class='list view table-responsive']/tbody/tr")

for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) >= 7:
        Name = cols[1].text.strip()
        City = cols[2].text.strip()
        Billing_country = cols[3].text.strip()
        Phone = cols[4].text.strip()
        User = cols[5].text.strip()
        Email = cols[6].text.strip()
        Date_create = cols[7].text.strip()

        # Insert into MySQL
        cursor.execute('''
            INSERT INTO crm_table (Name, City, Billing_country, Phone, User, Email, Date_create)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (Name, City, Billing_country, Phone, User, Email, Date_create))

conn.commit()
print("Data inserted into MySQL")
conn.close()
driver.quit()