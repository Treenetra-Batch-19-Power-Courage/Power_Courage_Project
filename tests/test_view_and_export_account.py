import csv
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def login_to_suitecrm(driver):
    driver.get("https://demo.suiteondemand.com/index.php?action=Login&module=Users&login_module=Users&login_action=Logout")
    time.sleep(3)
    driver.find_element(By.NAME, 'user_name').send_keys('will')
    driver.find_element(By.NAME, 'username_password').send_keys('will' + Keys.RETURN)
    time.sleep(5)

def get_account_data_from_ui(driver):
    all_data = []

    while True:
        table = driver.find_element(By.XPATH, "//table[contains(@class, 'list view table-responsive')]/tbody")
        rows = table.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 6:
                data = {
                    "Name": cols[0].text.strip(),
                    "City": cols[1].text.strip(),
                    "Billing Country": cols[2].text.strip(),
                    "Phone": cols[3].text.strip(),
                    "User": cols[4].text.strip(),
                    "Email": cols[5].text.strip()
                }
                all_data.append(data)

        # Pagination: break if next button is disabled
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "button[name='listView_nextButton']")
            if not next_button.is_enabled():
                break
            next_button.click()
            time.sleep(2)
        except:
            break

    return all_data

def save_data_to_csv(data, filename="accounts_data.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Name", "City", "Billing Country", "Phone", "User", "Email"])
        writer.writeheader()
        writer.writerows(data)

def load_data_from_csv(filename="accounts_data.csv"):
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def test_validate_accounts_data(driver):
    login_to_suitecrm(driver)
    driver.get("https://demo.suiteondemand.com/index.php?module=Accounts&action=index")
    time.sleep(5)

    ui_data = get_account_data_from_ui(driver)
    save_data_to_csv(ui_data)
    csv_data = load_data_from_csv()

    assert len(ui_data) == len(csv_data), f"Mismatch in number of rows: UI={len(ui_data)}, CSV={len(csv_data)}"

    # Validate each row
    for i in range(len(ui_data)):
        for key in ui_data[i]:
            assert ui_data[i][key] == csv_data[i][key], f"Data mismatch at row {i+1}, column '{key}'"

    print(f"\n✅ Validation passed! All {len(ui_data)} rows match the CSV.")
