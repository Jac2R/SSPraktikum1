from pages.sorted_page import SortedPage


def test_sorting_by_ascending_prices(driver):
    sorted_page = SortedPage(driver)
    sorted_page.find_category()

    prices_before = sorted_page.get_prices_from_cards()
    expected_prices = sorted(prices_before)
    print("\nASC. Expected Prices: ", expected_prices)

    sorted_page.sort_by_price_ascending()
    prices_actual = sorted_page.get_prices_from_cards()
    print("\nASC. Actual Prices: ", prices_actual)

    assert prices_actual == expected_prices


def test_sorting_by_descending_prices(driver):
    sorted_page = SortedPage(driver)
    sorted_page.find_category()

    prices_before = sorted_page.get_prices_from_cards()
    expected_prices = sorted(prices_before, reverse=True)
    print("\nDESC. Expected Prices: ", expected_prices)

    sorted_page.sort_by_price_descending()
    prices_actual = sorted_page.get_prices_from_cards()
    print("\nDESC. Actual Prices: ", prices_actual)

    assert prices_actual == expected_prices


def test_sorting_by_ascending_names(driver):
    sorted_page = SortedPage(driver)
    sorted_page.find_category()

    names_before = sorted_page.get_names_from_cards()
    expected_names = sorted(names_before)
    print("\nA - Z. Expected Names: ", expected_names)

    sorted_page.sort_by_name_a_to_z()
    names_actual = sorted_page.get_names_from_cards()
    print("\nA - Z. Actual Names: ", names_actual)

    assert names_actual == expected_names


def test_sorting_by_descending_names(driver):
    sorted_page = SortedPage(driver)
    sorted_page.find_category()

    names_before = sorted_page.get_names_from_cards()
    expected_names = sorted(names_before, reverse=True)
    print("\nZ - A. Expected Names: ", expected_names)

    sorted_page.sort_by_name_z_to_a()
    names_actual = sorted_page.get_names_from_cards()
    print("\nZ - A. Actual Names: ", names_actual)

    assert names_actual == expected_names