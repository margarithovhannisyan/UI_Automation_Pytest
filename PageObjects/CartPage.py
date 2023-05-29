from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from PageObjects.CheckoutPage import CheckoutPage


class CartPage:
    def __init__(self, driver):
        self.driver = driver

    CART_BUTTON = (By.CSS_SELECTOR, "img[alt='Cart']")
    PROCESS_TO_CHECKOUT_BUTTON = (By.XPATH, "//button[text()='PROCEED TO CHECKOUT']")
    PROMO_CODE_FIELD = (By.CLASS_NAME, "promoCode")

    def click_card_button(self):
        self.driver.find_element(*CartPage.CART_BUTTON).click()

    def click_process_to_checkout_button(self):
        self.driver.find_element(*CartPage.PROCESS_TO_CHECKOUT_BUTTON).click()
        wait = WebDriverWait(self.driver, 8)
        wait.until(expected_conditions.presence_of_element_located(self.PROMO_CODE_FIELD))
        checkoutPage = CheckoutPage(self.driver)
        return checkoutPage


