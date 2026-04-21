from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class SortedPage:
    SELECT_XPATH = (By.XPATH, "//select[@name='sort']")
    ALL_CARDS = (By.CSS_SELECTOR, ".thumbnails .thumbnail")
    ELEMENTS_PRICE = (By.CSS_SELECTOR, ".oneprice, .pricenew")
    ELEMENTS_NAME = (By.XPATH, "//div[contains(@class,'thumbnails') and contains(@class,'grid')]//a[@class='prdocutname']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def find_category(self):
        cat_skincare_xpath = (By.XPATH, "//a[contains(@href, 'path=43')]")
        subcat_face_xpath = (By.XPATH, "//a[contains(@href, 'path=43_46')]")

        cat_skincare = self.wait.until(EC.element_to_be_clickable(cat_skincare_xpath))
        actions = ActionChains(self.driver)
        actions.move_to_element(cat_skincare).perform()

        click_category_face = self.wait.until(EC.visibility_of_element_located(subcat_face_xpath))
        actions.move_to_element(click_category_face).click().perform()


    def get_prices_from_cards(self) -> list[float]:
        self.wait.until(EC.presence_of_all_elements_located(self.ALL_CARDS))
        price_elements = self.wait.until(EC.visibility_of_any_elements_located(self.ELEMENTS_PRICE))

        return [
            float(el.text.replace("$", ""))
            for el in price_elements
        ]

    def sort_by_price_ascending(self):
        select_dropdown = self.wait.until(EC.presence_of_element_located(self.SELECT_XPATH))
        select_ascending = Select(select_dropdown)
        select_ascending.select_by_value("p.price-ASC")

    def sort_by_price_descending(self):
        select_dropdown = self.wait.until(EC.presence_of_element_located(self.SELECT_XPATH))
        select_ascending = Select(select_dropdown)
        select_ascending.select_by_value("p.price-DESC")


    def get_names_from_cards(self) -> list[str]:
        self.wait.until(EC.presence_of_all_elements_located(self.ALL_CARDS))
        name_elements = self.wait.until(EC.visibility_of_any_elements_located(self.ELEMENTS_NAME))

        return [
            el.get_attribute("textContent").strip()
            for el in name_elements
        ]

    def sort_by_name_a_to_z(self):
        select_dropdown = self.wait.until(EC.presence_of_element_located(self.SELECT_XPATH))
        select_ascending = Select(select_dropdown)
        select_ascending.select_by_value("pd.name-ASC")

    def sort_by_name_z_to_a(self):
        select_dropdown = self.wait.until(EC.presence_of_element_located(self.SELECT_XPATH))
        select_ascending = Select(select_dropdown)
        select_ascending.select_by_value("pd.name-DESC")