from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random


class CartPage:
    SEARCH_BAR_XPATH = (By.XPATH, "//input[@name='filter_keyword']")
    SEARCH_BUTTON_XPATH = (By.XPATH, "//div[@class='button-in-search']")
    ALL_CARDS = (By.CSS_SELECTOR, ".thumbnails .col-md-3.col-sm-6.col-xs-12")
    QTY_FIELD = (By.ID, 'product_quantity')
    ADD_TO_CARD_BTN = (By.CSS_SELECTOR, 'a.cart')
    ALL_ROWS_IN_CART = (By.CSS_SELECTOR, '.cart-info.product-list table tr:not(:first-child)')
    UPDATE_CART_BUTTON = (By.CSS_SELECTOR, '[id=cart_update]')
    TOTAL_IN_CART = (By.XPATH, "//table[@id='totals_table']//tr[1]//td[2]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def find_shirts(self):
        type_shirt = self.wait.until(EC.element_to_be_clickable(self.SEARCH_BAR_XPATH))
        type_shirt.send_keys("shirt")

        search_button = self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON_XPATH))
        search_button.click()

    def add_second_and_third_to_cart(self):
        shirts_cards = self.wait.until(EC.presence_of_all_elements_located(self.ALL_CARDS))
        assert len(shirts_cards) >= 3, "Меньше 3-х товаров при поиске"
        search_result_url = self.driver.current_url
        indexes = [1, 2]
        added_products_to_cart = []

        for index in indexes:
            self.driver.get(search_result_url)
            shirts_cards = self.wait.until(EC.presence_of_all_elements_located(self.ALL_CARDS))
            card = shirts_cards[index]
            name_el = card.find_element(By.CSS_SELECTOR, ".prdocutname")
            name = name_el.get_attribute("textContent").strip()

            try:
                price_el = card.find_element(By.CSS_SELECTOR, ".oneprice")
            except:
                price_el = card.find_element(By.CSS_SELECTOR, ".pricenew")

            price = float(price_el.text.replace("$", ""))

            add_to_cart = card.find_element(By.CSS_SELECTOR, 'a.productcart')
            add_to_cart.click()

            type_qty = self.wait.until(EC.element_to_be_clickable(self.QTY_FIELD))
            quantity = random.randint(1, 10)
            type_qty.clear()
            type_qty.send_keys(str(quantity))
            self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CARD_BTN)).click()

            added_products_to_cart.append({
                "name": name,
                "price": price,
                "quantity": quantity
            })

            if index != indexes[-1]:
                self.driver.get(search_result_url)

        return added_products_to_cart


    def get_data_from_cart(self):
        rows = self.wait.until(EC.presence_of_all_elements_located(self.ALL_ROWS_IN_CART))

        actual_products_in_cart = []

        for row in rows:
            try:
                name_el = row.find_element(By.CSS_SELECTOR,'td:nth-child(2) a')
                name = name_el.text.strip()
            except:
                continue
            unit_price = row.find_element(By.CSS_SELECTOR, 'td:nth-child(4)').text
            quantity = row.find_element(By.CSS_SELECTOR, 'td:nth-child(5) input').get_attribute('value')

            actual_products_in_cart.append({
                "name": name,
                "price": float(unit_price.replace("$", "")),
                "quantity": int(quantity)
            })

        return actual_products_in_cart


    def double_cheapest_price(self):
        rows = self.wait.until(EC.presence_of_all_elements_located(self.ALL_ROWS_IN_CART))
        cheapest_row = None
        min_price = float("inf")
        for row in rows:
            try:
                price_text = row.find_element(By.CSS_SELECTOR,
                        'td:nth-child(4)').text.replace("$", "").strip()
                unit_price = float(price_text)

                if unit_price <= min_price:
                    min_price = unit_price
                    cheapest_row = row
            except:
                continue

        assert cheapest_row is not None, "Не найден самый дешевый товар"

        qty_input = cheapest_row.find_element(By.CSS_SELECTOR, "td:nth-child(5) input")
        qty = int(qty_input.get_attribute("value"))

        qty_input.clear()
        qty_input.send_keys(str(qty * 2))

        self.wait.until(EC.element_to_be_clickable(self.UPDATE_CART_BUTTON)).click()
        self.wait.until(EC.presence_of_all_elements_located(self.ALL_ROWS_IN_CART))


    def calculate_expected_price(self):
        rows = self.wait.until(EC.presence_of_all_elements_located(self.ALL_ROWS_IN_CART))
        calc_total = 0.0
        for row in rows:
            price = row.find_element(By.CSS_SELECTOR, 'td:nth-child(4)')
            taking_price = float(price.text.replace("$", ""))
            qty = int(row.find_element(By.CSS_SELECTOR, "td:nth-child(5) input").get_attribute("value"))
            calc_total += (taking_price * qty)
        return calc_total

    def get_ui_total(self):
        self.wait.until(EC.text_to_be_present_in_element(self.TOTAL_IN_CART, "$"))
        ui_total = self.wait.until(EC.presence_of_element_located(self.TOTAL_IN_CART))
        ui_total_price = float(ui_total.text.replace("$", ""))
        return round(ui_total_price, 2)