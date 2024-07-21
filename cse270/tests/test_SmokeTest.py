import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class TestSmokeTetonTest:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        options = Options()
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        self.vars = {}
        yield
        self.driver.quit()

    def wait_for_element(self, by, value, timeout=30):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))

    def test_homePage(self):
        self.driver.get("http://127.0.0.1:5500/teton/1.6/index.html")
        self.driver.set_window_size(1920, 1032)
        assert self.driver.find_elements(By.CSS_SELECTOR, ".header-logo img")
        assert self.driver.find_element(By.CSS_SELECTOR, ".header-title > h1").text == "Teton Idaho"
        assert self.driver.find_element(By.CSS_SELECTOR, ".header-title > h2").text == "Chamber of Commerce"
        assert self.driver.title == "Teton Idaho CoC"
        assert self.driver.find_elements(By.CSS_SELECTOR, ".main-spotlight")
        self.wait_for_element(By.CSS_SELECTOR, ".spotlight1 img")
        self.wait_for_element(By.CSS_SELECTOR, ".spotlight2 img")
        assert self.driver.find_elements(By.LINK_TEXT, "Join Us")
        self.driver.find_element(By.LINK_TEXT, "Join Us").click()

    def test_directoryPage(self):
        self.driver.get("http://127.0.0.1:5500/teton/1.6/directory.html")
        self.driver.set_window_size(1920, 1032)
        self.driver.find_element(By.ID, "directory-grid").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".gold-member:nth-child(9) > p:nth-child(2)").text == "Teton Turf and Tree"
        self.driver.find_element(By.ID, "directory-list").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".gold-member:nth-child(9) > p:nth-child(2)").text == "Teton Turf and Tree"

    def test_adminPage(self):
        self.driver.get("http://127.0.0.1:5500/teton/1.6/admin.html")
        self.driver.set_window_size(1920, 1032)
        self.driver.find_element(By.CSS_SELECTOR, ".myinput:nth-child(2)").click()
        username_field = self.driver.find_element(By.ID, "username")
        assert username_field
        username_field.send_keys("admin")
        self.driver.find_element(By.ID, "password").send_keys("admin")
        self.driver.find_element(By.CSS_SELECTOR, ".mysubmit:nth-child(4)").click()
        self.wait_for_element(By.CSS_SELECTOR, ".errorMessage")

    def test_joinPage(self):
        self.driver.get("http://127.0.0.1:5500/teton/1.6/join.html")
        self.driver.set_window_size(1920, 1032)

        # Explicitly wait for the first name field to be present
        fname_field = self.wait_for_element(By.NAME, "fname")
        assert fname_field is not None
        fname_field.send_keys("Testing Name")

        # Explicitly wait for the last name field to be present
        lname_field = self.wait_for_element(By.NAME, "lname")
        lname_field.send_keys("Smith")

        # Explicitly wait for the business name field to be present
        bizname_field = self.wait_for_element(By.NAME, "bizname")
        bizname_field.send_keys("Enterprice")

        # Explicitly wait for the business title field to be present
        biztitle_field = self.wait_for_element(By.NAME, "biztitle")
        biztitle_field.send_keys("Test")

        self.driver.find_element(By.CSS_SELECTOR, "fieldset").click()
        self.driver.find_element(By.NAME, "submit").click()

        # Explicitly wait for the email field to be present
        email_field = self.wait_for_element(By.NAME, "email")
        email_field.send_keys("test@mail.com")
        assert email_field is not None
