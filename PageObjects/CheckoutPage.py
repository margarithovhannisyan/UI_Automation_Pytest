import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver

    PROMO_CODE_FIELD = (By.CLASS_NAME, "promoCode")
    PRODUCT_NAMES_CHECKOUT = (By.CSS_SELECTOR, "p.product-name")
    TOTAL_AMOUNT_BEFORE_DISCOUNT = (By.CLASS_NAME, "totAmt")
    TOTAL_AMOUNT_AFTER_DISCOUNT = (By.CSS_SELECTOR, ".discountAmt")
    APPLY_PROMO_CODE_BUTTON = (By.CSS_SELECTOR, ".promoBtn")
    PROMO_CODE_APPLICATION_INFO = (By.CSS_SELECTOR, "span.promoInfo")
    TOTAL_AMOUNT_PER_PRODUCT = (By.XPATH, "//tr/td[5]/p")

    def get_product_names_from_checkout_table(self):
        product_list_checkout = []
        product_names = self.driver.find_elements(*CheckoutPage.PRODUCT_NAMES_CHECKOUT)
        for product_name in product_names:
            product_list_checkout.append(product_name.text)
        return product_list_checkout

    def get_total_amount_sum_from_checkout_table(self):
        product_amount_sum = 0
        amount_per_products = self.driver.find_elements(*CheckoutPage.TOTAL_AMOUNT_PER_PRODUCT)
        for amount_per_product in amount_per_products:
            product_amount_sum = product_amount_sum + float(amount_per_product.text)
        return product_amount_sum

    def get_initial_total_amount(self):
        return float(self.driver.find_element(*CheckoutPage.TOTAL_AMOUNT_BEFORE_DISCOUNT).text)

    def get_final_total_amount(self):
        return self.driver.find_element(*CheckoutPage.TOTAL_AMOUNT_AFTER_DISCOUNT).text

    def verify_product_names_from_checkout_table(self, actual_name_list: list, expected_name_list: list):
        if actual_name_list != expected_name_list:
            raise Exception(
                f"Product actual names ({actual_name_list}) do not match expected names ({expected_name_list})")
        else:
            return actual_name_list == expected_name_list

    def input_promo_code(self, promo_code):
        self.driver.find_element(*CheckoutPage.PROMO_CODE_FIELD).send_keys(promo_code)

    def apply_promo_code(self):
        self.driver.find_element(*CheckoutPage.APPLY_PROMO_CODE_BUTTON).click()
        wait = WebDriverWait(self.driver, 8)
        wait.until(expected_conditions.presence_of_element_located(self.PROMO_CODE_APPLICATION_INFO))

    def verify_promo_code_is_applied(self, total_amount_before_promo_code: float, total_amount_after_promo_code: float):
        if float(total_amount_before_promo_code) <= float(total_amount_after_promo_code):
            raise Exception(f"Discount has not been applied")
        else:
            return float(total_amount_before_promo_code) > float(total_amount_after_promo_code)

    def verify_table_product_sum_is_equal_to_total_sum_before_discount(self, table_product_sum: float,
                                                                       total_sum_before_discount: float):
        if float(table_product_sum) != float(total_sum_before_discount):
            raise Exception(f"Total amount is not correctly calculated")
        else:
            return float(table_product_sum) == float(total_sum_before_discount)
