import pytest

from PageObjects.CartPage import CartPage
from PageObjects.HomePage import HomePage
from Utilities.BaseClass import BaseClass


class TestLogin(BaseClass):
    PRODUCT_SEARCH_NAME = "ber"
    VALID_PROMO_CODE = "rahulshettyacademy"

    def test_e2e(self):
        log = self.get_logger()
        homePage = HomePage(self.driver)
        log.info("Searching for products including " + self.PRODUCT_SEARCH_NAME)
        homePage.search_product(self.PRODUCT_SEARCH_NAME)
        product_count = homePage.get_products_count()
        assert homePage.verify_product_count(actual_count=product_count, expected_count=3)
        log.info("There were 3 products with " + self.PRODUCT_SEARCH_NAME)
        product_list_from_search_result = homePage.get_product_names_and_add_to_card()
        cartPage = CartPage(self.driver)
        cartPage.click_card_button()
        checkoutPage = cartPage.click_process_to_checkout_button()
        product_list_from_checkout = checkoutPage.get_product_names_from_checkout_table()
        assert checkoutPage.verify_product_names_from_checkout_table(actual_name_list=product_list_from_search_result,
                                                                     expected_name_list=product_list_from_checkout)
        total_amount_before_promo_code = checkoutPage.get_final_total_amount()
        checkoutPage.input_promo_code(self.VALID_PROMO_CODE)
        checkoutPage.apply_promo_code()
        total_amount_after_promo_code = checkoutPage.get_final_total_amount()
        assert checkoutPage.verify_promo_code_is_applied(total_amount_before_promo_code=total_amount_before_promo_code,
                                                         total_amount_after_promo_code=total_amount_after_promo_code)

        table_product_amount_sum = checkoutPage.get_total_amount_sum_from_checkout_table()
        product_amount_sum = checkoutPage.get_initial_total_amount()
        assert checkoutPage.verify_table_product_sum_is_equal_to_total_sum_before_discount(
            table_product_sum=table_product_amount_sum, total_sum_before_discount=product_amount_sum)

    # @pytest.fixture(params=["p", "berry"])
    # def get_data(self, request):
    #     return request.param
