import time

from selenium.webdriver.common.by import By


class HomePage:
    def __init__(self, driver):
        self.driver = driver

    SEARCH_PRODUCT = (By.CSS_SELECTOR, "input.search-keyword")
    PRODUCTS_COUNT = (By.XPATH, "//div[@class='products']/div")
    ADD_TO_CARD_BUTTON = (By.XPATH, "//div[@class='product-action']/button")
    PRODUCT_NAME = (By.XPATH, "parent::div/parent::div/h4")

    def search_product(self, product_name):
        self.driver.find_element(*HomePage.SEARCH_PRODUCT).send_keys(product_name)
        time.sleep(4)

    def get_products_count(self):
        return len(self.driver.find_elements(*HomePage.PRODUCTS_COUNT))

    def get_add_to_card_buttons(self):
        return self.driver.find_elements(*HomePage.ADD_TO_CARD_BUTTON)

    def get_product_names_and_add_to_card(self):
        list = []
        buttons = self.get_add_to_card_buttons()
        for button in buttons:
            list.append(button.find_element(*HomePage.PRODUCT_NAME).text)
            button.click()
        return list

    def verify_product_count(self, actual_count: int, expected_count: int):
        if actual_count != expected_count:
            raise Exception(f"Product actual count ({actual_count}) does not match expected count ({expected_count})")
        else:
            return actual_count == expected_count


