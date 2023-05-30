from PageObjects.CartPage import CartPage
from PageObjects.HomePage import HomePage
from Utilities.BaseClass import BaseClass


class Test_Promo_Code(BaseClass):
    VALID_PROMO_CODE = "rahulshettyacademy"
    INVALID_PROMO_CODE = "rahulshettyacademy_inv"
    PRODUCT_SEARCH_NAME = "tomato"

    def test_valid_promo_code(self):
        log = self.get_logger()
        homePage = HomePage(self.driver)
        log.info("Searching for products including " + self.PRODUCT_SEARCH_NAME)
        homePage.search_product(self.PRODUCT_SEARCH_NAME)
        product_count = homePage.get_product_count()
        assert homePage.verify_product_count(actual_count=product_count, expected_count=1)
        product_list_from_search_result = homePage.get_product_names_and_add_to_card()
        cartPage = CartPage(self.driver)
        cartPage.click_card_button()
        checkoutPage = cartPage.click_process_to_checkout_button()
        product_list_from_checkout = checkoutPage.get_product_names_from_checkout_table()
        assert checkoutPage.verify_product_names_from_checkout_table(actual_name_list=product_list_from_search_result,
                                                                     expected_name_list=product_list_from_checkout)
        checkoutPage.input_promo_code(self.VALID_PROMO_CODE)
        checkoutPage.apply_promo_code()
        assert checkoutPage.verify_valid_promo_code_is_applied()

    def test_invalid_promo_code(self):
        log = self.get_logger()
        homePage = HomePage(self.driver)
        log.info("Searching for products including " + self.PRODUCT_SEARCH_NAME)
        homePage.search_product(self.PRODUCT_SEARCH_NAME)
        product_count = homePage.get_product_count()
        assert homePage.verify_product_count(actual_count=product_count, expected_count=1)
        product_list_from_search_result = homePage.get_product_names_and_add_to_card()
        cartPage = CartPage(self.driver)
        cartPage.click_card_button()
        checkoutPage = cartPage.click_process_to_checkout_button()
        product_list_from_checkout = checkoutPage.get_product_names_from_checkout_table()
        assert checkoutPage.verify_product_names_from_checkout_table(actual_name_list=product_list_from_search_result,
                                                                     expected_name_list=product_list_from_checkout)
        checkoutPage.input_promo_code(self.INVALID_PROMO_CODE)
        checkoutPage.apply_promo_code()
        assert checkoutPage.verify_invalid_promo_code_is_applied()
