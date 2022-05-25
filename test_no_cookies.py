import pytest
from selenium.common.exceptions import NoSuchElementException
# from utils import page_utils
# from utils.page_utils import open_page
# from utils.page_utils import hover
from utils.page_utils import *
from data import MAINPAGE


# see conftest.py
# @pytest.fixture(scope="session", autouse=True)
# def testing():
#     # получение объекта веб-драйвера для нужного браузера в полноэкранном режиме
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument('--kiosk')
#     pytest.web_driver = webdriver.Chrome('F:/SF/SeleniumDrivers/chromedriver.exe', chrome_options=chrome_options)
#     pytest.web_driver.get(MAINPAGE)
#
#     yield
#     pytest.web_driver.implicitly_wait(3)
#     pytest.web_driver.quit()

@pytest.fixture(scope="function", autouse=True)
def main_page():
    yield
    pytest.web_driver.get(MAINPAGE)


class TestPageCommon:  # testing variable items on page
    def test_page_no_login(self):  # check page open no cookies
        title = pytest.web_driver.title
        # print('\ntitle is:\t', title)
        assert title == 'Лабиринт | Книжный интернет-магазин: купить книги, новинки, бестселлеры'

    def test_page_check_biblionight(self):  # check if biblionight present
        try:
            # # remove comment to try exception
            # biblioclose = pytest.web_driver.find_element_by_xpath(
            #     '//span[@class ="b-overlay-e-close js-biblio2022-close"]')
            # biblioclose.click()
            # time.sleep(2)
            biblionight = pytest.web_driver.find_element_by_xpath('//span[@class="biblio2022__main"]')
            biblionight.click()
            title = pytest.web_driver.title
            assert title == 'Библионочь в Лабиринте'
        except NoSuchElementException:
            print('\nNo Such Element')

    def test_page_empty_basket(self):
        basket_items = pytest.web_driver.find_element_by_xpath(
            '//span[@class="b-header-b-personal-e-icon-count-m-cart basket-in-cart-a"]')
        assert basket_items.text == '0'

    def test_page_bottom_menu_link_covid(self):
        scroll_to_bottom(pytest.web_driver)
        link_covid = pytest.web_driver.find_element_by_xpath('//a[@class="sprite_kovid kov_desc"]')
        link_covid.click()
        time.sleep(2)
        parent = pytest.web_driver.window_handles[0]
        chld = pytest.web_driver.window_handles[1]
        pytest.web_driver.switch_to.window(chld)
        title = pytest.web_driver.title
        assert title == 'E-commerce против COVID'
        pytest.web_driver.close()
        pytest.web_driver.switch_to.window(parent)

    # def test_page_bottom_menu_link_akit(self):
    #     scroll_to_bottom(pytest.web_driver)
    #     link_akit = '//li[@class="b-rfooter-e-item"]/a[@href="//www.labirint.org/vakansii?tab=5"]'
    #     hover_move_click(pytest.web_driver, link_akit)
    #     # pytest.web_driver.find_element_by_xpath('//li/a[@href="//www.labirint.org/vakansii?tab=5"]').click()
    #     # link_akit.click()
    #     time.sleep(5)
    #     title = pytest.web_driver.title
    #     assert title == 'Пользовательское Соглашение об условиях предоставления Услуг в интернет-магазине ' \
    #                     'Лабиринт | Лабиринт'


class TestHeaderItems:
    def test_page_messages(self):
        messages = pytest.web_driver.find_element_by_xpath(
            '//li[@class="b-header-b-personal-e-list-item b-header-b-personal-e-list-item-m-md have-dropdown"]')
        messages.click()
        check_form = pytest.web_driver.find_element_by_xpath(
            '//div[@class="js-auth__title new-auth__title"]')
        assert check_form.text == 'Полный доступ к Лабиринту'

    def test_page_my_lab(self):
        my_lab = pytest.web_driver.find_element_by_xpath(
            '//span[@class="b-header-b-personal-e-icon b-header-b-personal-e-icon-m-profile   '
            'b-header-e-sprite-background"]')
        my_lab.click()
        check_form = pytest.web_driver.find_element_by_xpath(
            '//div[@class="js-auth__title new-auth__title"]')
        assert check_form.text == 'Полный доступ к Лабиринту'

    def test_page_put_aside(self):
        put_aside = pytest.web_driver.find_element_by_xpath(
            '//span[@class="b-header-b-personal-e-icon-wrapper <!--b-header-b-personal-e-icon-wrapper-m-putorder-->"]')
        put_aside.click()
        active_header = pytest.web_driver.find_element_by_xpath(
            '//li[@class="cabinet-menu__tab cabinet-menu__tab_active"]/a')
        active_link = active_header.get_attribute('href')
        # print('\n', active_link)
        assert active_link == 'https://www.labirint.ru/cabinet/putorder/'

    def test_page_basket(self):
        basket_link = pytest.web_driver.find_element_by_xpath(
            '//li[@class="b-header-b-personal-e-list-item have-dropdown  last-child"]/a').get_attribute('href')
        # print(basket_link)
        open_page(pytest.web_driver, basket_link)
        title = pytest.web_driver.title
        assert title == 'Корзина. Проверьте заказ. Интернет-магазин Лабиринт.'

    def test_page_discount_commertial(self):
        discount = pytest.web_driver.find_element_by_xpath(
            '//span[@class="b-header-labelaction-text b-header-b-logo-e-discount-e-text-m-long"]')
        discount.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.find_element_by_xpath(
            '//div[@class="h2 relative main-block-carousel-title-outer"]').is_displayed()


class TestHeaderFirstMenu:
    def test_page_b_menu_books(self):
        books = pytest.web_driver.find_element_by_xpath(
            '//a[@href="/books/"]')
        books.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.find_element_by_xpath(
            '//h1[@class="genre-name"]').text == "Книги"

    def test_page_b_menu_best(self):
        best = pytest.web_driver.find_element_by_xpath(
            '//a[@href="/best/"]')
        best.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.find_element_by_xpath(
            '//div[@class="content-block"]/h1').text == "Главные книги 2022"

    def test_page_b_menu_school(self):
        school = pytest.web_driver.find_element_by_xpath(
            '//a[@href="/school/"]')
        school.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.find_element_by_xpath(
            '//h1[@class="school-cap__header"]').text == "Все учебники в Лабиринте"

    def test_page_b_menu_games(self):
        games = pytest.web_driver.find_element_by_xpath(
            '//a[@href="/games/"]')
        games.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.find_element_by_xpath(
            '//h1[@class="genre-name"]').text == "Игры и игрушки"

    def test_page_b_menu_office(self):
        office = pytest.web_driver.find_element_by_xpath(
            '//a[@href="/office/"]')
        office.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.find_element_by_xpath(
            '//h1[@class="genre-name"]').text == "Канцелярские товары"

    def test_page_b_menu_multimedia(self):
        more_locator = '//span[@class="b-header-b-menu-e-text"]'
        active = '//li[@class="b-menu-second-item active"]'
        hover(pytest.web_driver, more_locator, 0, 25, active)
        assert pytest.web_driver.title == "Полная линейка продуктов мультимедиа | Интернет-магазин Лабиринт"

    # def test_page_b_menu_multimedia_location():
    #     more_locator = '//li[@data-event-content="Еще"]'
    #     hidden_link = '//a[@class="b-menu-list-title b-menu-list-title-first" and @href="/multimedia/"]'
    #     active = '//li[@class="b-menu-second-item active"]'
    #     hover_location(pytest.web_driver, more_locator, hidden_link, active)
    #     assert pytest.web_driver.title == "Полная линейка продуктов мультимедиа | Интернет-магазин Лабиринт"

    def test_page_b_menu_souvenir(self):
        more_locator = '//span[@class="b-header-b-menu-e-text"]'
        active = '//li[@class="b-menu-second-item active"]'
        hover(pytest.web_driver, more_locator, 0, 70, active)
        assert pytest.web_driver.title == "Сувениры, рамки и альбомы для фотографий, календари и открытки | купить и " \
                                          "подарить с доставкой | Лабиринт"

    def test_page_b_menu_journals(self):
        more_locator = '//span[@class="b-header-b-menu-e-text"]'
        active = '//li[@class="b-menu-second-item active"]'
        hover(pytest.web_driver, more_locator, 0, 105, active)
        assert pytest.web_driver.find_element_by_xpath(
            '//h1[@class="mag-h1"]').text == "Журнальный лабиринт"

    def test_page_b_menu_household(self):
        more_locator = '//span[@class="b-header-b-menu-e-text"]'
        active = '//li[@class="b-menu-second-item active"]'
        hover(pytest.web_driver, more_locator, 0, 145, active)
        assert pytest.web_driver.find_element_by_xpath(
            '//h1[@class="genre-name"]').text == "Товары для дома"

    def test_page_b_menu_club(self):
        club = pytest.web_driver.find_element_by_xpath(
            '//a[@href="/club/"]')
        club.click()
        title = pytest.web_driver.title
        assert title == 'Книжный клуб интернет-магазина Лабиринт'

    def test_page_b_menu_region_location(self):
        region_location = pytest.web_driver.find_element_by_xpath(
            '//span[@class="region-location-icon-txt "]')
        region_location.click()
        city = pytest.web_driver.find_elements_by_xpath('//span[@class="g-alttext-deepblue pointer"]')[8]
        city.click()
        pytest.web_driver.implicitly_wait(2)
        region_location = pytest.web_driver.find_element_by_xpath(
            '//span[@class="region-location-icon-txt "]')
        title = region_location.get_attribute('title')
        assert title == 'Тюмень'
        delivery = pytest.web_driver.find_element_by_xpath(
            '//span[@class="b-header-b-menu-e-text"]/a[@href="/maps/"]')
        delivery.click()
        assert pytest.web_driver.find_element_by_id('js-tab-2').is_displayed()
        pytest.web_driver.back()
        points = pytest.web_driver.find_element_by_xpath(
            '//a[@href="/maps/" and @class="b-header-b-sec-menu-e-link"]')
        points.click()
        assert pytest.web_driver.find_element_by_id('js-tab-2').is_displayed()


class TestHeaderSecondMenu:
    def test_page_b_sec_menu_delivery_payment(self):
        delivery_payment = pytest.web_driver.find_element_by_xpath(
            '//a[@href="/help/" and @class="b-header-b-sec-menu-e-link"]')
        delivery_payment.click()
        title = pytest.web_driver.title
        assert title == 'Помощь | Лабиринт'

    def test_page_b_sec_menu_certificates(self):
        certificates = pytest.web_driver.find_element_by_xpath(
            '//a[@href="/top/certificates/" and @class="b-header-b-sec-menu-e-link"]')
        certificates.click()
        title = pytest.web_driver.title
        assert title == 'Сертификаты'

    def test_page_b_sec_menu_rating(self):
        rating = pytest.web_driver.find_element_by_xpath(
            '//a[@href="/rating/?id_genre=-1&nrd=1" and @class="b-header-b-sec-menu-e-link"]')
        rating.click()
        title = pytest.web_driver.title
        assert title == 'Рейтинг: лучшие книги 2022 | Лабиринт - Рейтинг'

    def test_page_b_sec_menu_novelty(self):
        novelty = pytest.web_driver.find_element_by_xpath(
            '//a[@href="/novelty/" and @class="b-header-b-sec-menu-e-link"]')
        novelty.click()
        title = pytest.web_driver.title
        assert title == 'Новые книги 2022 года | Лабиринт - Новинки'

    def test_page_b_sec_menu_discount(self):
        discount = pytest.web_driver.find_element_by_xpath(
            '//a[@href="/sale/" and @class="b-header-b-sec-menu-e-link"]')
        discount.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.find_element_by_xpath(
            '//div[@class="h2 relative main-block-carousel-title-outer"]').is_displayed()

    def test_page_b_sec_menu_phone(self):
        phone = pytest.web_driver.find_element_by_xpath(
            '//li[@class="b-header-b-sec-menu-e-list-item have-dropdown have-dropdown-clickable analytics-click-js"]')
        phone.click()
        pytest.web_driver.implicitly_wait(1)
        assert pytest.web_driver.find_elements_by_xpath('//a[@href="#" and @class="btn btn-small btn-clear '
                                                        'font_regular-btn"]')[0].is_displayed()

    def test_page_b_sec_menu_contact(self):
        contact = pytest.web_driver.find_element_by_xpath(
            '//a[@href="/contact/" and @class="b-header-b-sec-menu-e-link"]')
        contact.click()
        title = pytest.web_driver.title
        assert title == 'Контакты книжного интернет-магазина | Лабиринт'

    def test_page_b_sec_menu_support(self):
        support = pytest.web_driver.find_element_by_xpath(
            '//a[@href="/support/" and @class="b-header-b-sec-menu-e-link"]')
        support.click()
        title = pytest.web_driver.title
        assert title == 'Служба поддержки | Поддержка лабиринта'

    def test_page_b_sec_menu_socials(self):
        socials = '//div[@class="b-header-b-social"]'
        hover_simple(pytest.web_driver, socials)
        assert pytest.web_driver.find_element_by_xpath('//div[@class="popup-window top-block-popup dropdown-block '
                                                       'b-header-b-sec-menu-e-social-popup '
                                                       'dropdown-block-opened"]').is_displayed()


class TestPageBottomMenuInPocket:  # check bottom links in menu "Лабиринт в кармане"
    def test_page_bottom_menu_app_store(self):
        scroll_to_bottom(pytest.web_driver)
        app_store = pytest.web_driver.find_element_by_xpath('//a[@data-event-content="App Store"]')
        app_store.click()
        time.sleep(2)
        parent = pytest.web_driver.window_handles[0]
        chld = pytest.web_driver.window_handles[1]
        pytest.web_driver.switch_to.window(chld)
        title = pytest.web_driver.title
        assert title == 'App\xa0Store: Лабиринт.ру — книжный магазин'
        pytest.web_driver.close()
        pytest.web_driver.switch_to.window(parent)

    def test_page_bottom_menu_goggle_play(self):
        scroll_to_bottom(pytest.web_driver)
        goggle_play = pytest.web_driver.find_element_by_xpath('//a[@data-event-content="Google Play"]')
        goggle_play.click()
        time.sleep(1)
        parent = pytest.web_driver.window_handles[0]
        chld = pytest.web_driver.window_handles[1]
        pytest.web_driver.switch_to.window(chld)
        title = pytest.web_driver.title
        assert title == 'Лабиринт.ру — книжный магазин - Apps on Google Play'
        pytest.web_driver.close()
        pytest.web_driver.switch_to.window(parent)

    def test_page_bottom_menu_app_gallery(self):
        scroll_to_bottom(pytest.web_driver)
        app_gallery = pytest.web_driver.find_element_by_xpath('//a[@data-event-content="App Gallery"]')
        app_gallery.click()
        time.sleep(10)
        parent = pytest.web_driver.window_handles[0]
        chld = pytest.web_driver.window_handles[1]
        pytest.web_driver.switch_to.window(chld)
        title = pytest.web_driver.title
        assert title == 'AppGallery'
        pytest.web_driver.close()
        pytest.web_driver.switch_to.window(parent)


class TestPageBottomMenuSociety:  # check bottom links in menu "Мы в соцсетях"
    def test_page_bottom_menu_v_contact(self):
        scroll_to_bottom(pytest.web_driver)
        v_contact = pytest.web_driver.find_element_by_xpath('//a[@data-event-content="ВКонтакте"]')
        v_contact.click()
        time.sleep(5)
        parent = pytest.web_driver.window_handles[0]
        chld = pytest.web_driver.window_handles[1]
        pytest.web_driver.switch_to.window(chld)
        title = pytest.web_driver.title
        assert title == 'Лабиринт | VK'
        pytest.web_driver.close()
        pytest.web_driver.switch_to.window(parent)

    def test_page_bottom_menu_v_contact_children(self):
        scroll_to_bottom(pytest.web_driver)
        v_contact_children = pytest.web_driver.find_element_by_xpath('//a[@data-event-content="ВКонтакте. Дети"]')
        v_contact_children.click()
        time.sleep(5)
        parent = pytest.web_driver.window_handles[0]
        chld = pytest.web_driver.window_handles[1]
        pytest.web_driver.switch_to.window(chld)
        title = pytest.web_driver.title
        assert title == 'Лабиринт Дети | VK'
        pytest.web_driver.close()
        pytest.web_driver.switch_to.window(parent)

    def test_page_bottom_menu_youtube(self):
        scroll_to_bottom(pytest.web_driver)
        youtube = pytest.web_driver.find_element_by_xpath('//a[@data-event-content="Ютьюб"]')
        youtube.click()
        time.sleep(2)
        parent = pytest.web_driver.window_handles[0]
        chld = pytest.web_driver.window_handles[1]
        pytest.web_driver.switch_to.window(chld)
        title = pytest.web_driver.title
        assert title == 'Лабиринт - YouTube'
        pytest.web_driver.close()
        pytest.web_driver.switch_to.window(parent)

    def test_page_bottom_menu_classmates(self):
        scroll_to_bottom(pytest.web_driver)
        classmates = pytest.web_driver.find_element_by_xpath('//a[@data-event-content="Одноклассники"]')
        classmates.click()
        time.sleep(2)
        parent = pytest.web_driver.window_handles[0]
        chld = pytest.web_driver.window_handles[1]
        pytest.web_driver.switch_to.window(chld)
        title = pytest.web_driver.title
        assert title == 'Лабиринт | Group on OK | Join, read, and chat on OK!'
        pytest.web_driver.close()
        pytest.web_driver.switch_to.window(parent)

    def test_page_bottom_menu_dzen(self):
        scroll_to_bottom(pytest.web_driver)
        dzen = pytest.web_driver.find_element_by_xpath('//a[@data-event-content="Дзен"]')
        dzen.click()
        time.sleep(2)
        parent = pytest.web_driver.window_handles[0]
        chld = pytest.web_driver.window_handles[1]
        pytest.web_driver.switch_to.window(chld)
        title = pytest.web_driver.title
        assert title == 'Лабиринт | Zen'
        pytest.web_driver.close()
        pytest.web_driver.switch_to.window(parent)

    def test_page_bottom_menu_telegram(self):
        scroll_to_bottom(pytest.web_driver)
        telegram = pytest.web_driver.find_element_by_xpath('//a[@data-event-content="Телеграм"]')
        telegram.click()
        time.sleep(2)
        parent = pytest.web_driver.window_handles[0]
        chld = pytest.web_driver.window_handles[1]
        pytest.web_driver.switch_to.window(chld)
        title = pytest.web_driver.title
        assert title == 'Telegram: Contact @labirintru'
        pytest.web_driver.close()
        pytest.web_driver.switch_to.window(parent)

    def test_page_bottom_menu_tiktok(self):
        scroll_to_bottom(pytest.web_driver)
        tiktok = pytest.web_driver.find_element_by_xpath('//a[@data-event-content="ТикТок"]')
        tiktok.click()
        time.sleep(2)
        parent = pytest.web_driver.window_handles[0]
        chld = pytest.web_driver.window_handles[1]
        pytest.web_driver.switch_to.window(chld)
        title = pytest.web_driver.title
        assert title == "labirintru (@labirintru) TikTok | Watch labirintru's Newest TikTok Videos"
        pytest.web_driver.close()
        pytest.web_driver.switch_to.window(parent)


class TestPageBottomMenuCatalog:  # check bottom links in menu "Каталог"
    def test_page_bottom_menu_allbooks(self):
        scroll_to_bottom(pytest.web_driver)
        allbooks = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a[@data-event-content="Все '
                                                           'книги"]')
        allbooks.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.find_element_by_xpath(
            '//h1[@class="genre-name"]').text == "Книги"

    def test_page_bottom_menu_school(self):
        scroll_to_bottom(pytest.web_driver)
        school = pytest.web_driver.find_element_by_xpath(
            '//li[@class="b-rfooter-e-item"]/a[@data-event-content="Школа"]')
        school.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.find_element_by_xpath(
            '//h1[@class="school-cap__header"]').text == "Все учебники в Лабиринте"

    def test_page_bottom_menu_journals(self):
        scroll_to_bottom(pytest.web_driver)
        journals = pytest.web_driver.find_element_by_xpath(
            '//li[@class="b-rfooter-e-item"]/a[@data-event-content="Журналы"]')
        journals.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.find_element_by_xpath('//h1[@class="mag-h1"]').text == "Журнальный лабиринт"

    def test_page_bottom_menu_games(self):
        scroll_to_bottom(pytest.web_driver)
        games = pytest.web_driver.find_element_by_xpath(
            '//li[@class="b-rfooter-e-item"]/a[@data-event-content="Игрушки"]')
        games.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.find_element_by_xpath('//h1[@class="genre-name"]').text == "Игры и игрушки"

    def test_page_bottom_menu_office(self):
        scroll_to_bottom(pytest.web_driver)
        office = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                         '@data-event-content="Канцтовары"]')
        office.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.find_element_by_xpath(
            '//h1[@class="genre-name"]').text == "Канцелярские товары"

    def test_page_bottom_menu_multimedia(self):
        scroll_to_bottom(pytest.web_driver)
        multimedia = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                             '@data-event-content="CD/DVD"]')
        multimedia.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.title == "Полная линейка продуктов мультимедиа | Интернет-магазин Лабиринт"

    def test_page_bottom_menu_souvenir(self):
        scroll_to_bottom(pytest.web_driver)
        souvenir = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                           '@data-event-content="Сувениры"]')
        souvenir.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.title == "Сувениры, рамки и альбомы для фотографий, календари и открытки | купить и " \
                                          "подарить с доставкой | Лабиринт"

    def test_page_bottom_menu_household(self):
        scroll_to_bottom(pytest.web_driver)
        household = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                            '@href="/household/"]')
        household.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.find_element_by_xpath('//h1[@class="genre-name"]').text == "Товары для дома"


class TestPageBottomMenuImportant:  # check bottom links in menu "Важно"
    def test_page_bottom_menu_actions(self):
        scroll_to_bottom(pytest.web_driver)
        actions = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                          '@href="/actions/"]')
        actions.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.title == "Акции, скидки и\xa0подарки в\xa0Интернет-магазине «Лабиринт»."

    def test_page_bottom_menu_best(self):
        scroll_to_bottom(pytest.web_driver)
        best = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                       '@data-event-content="Главные книги"]')
        best.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.find_element_by_xpath(
            '//div[@class="content-block"]/h1').text == "Главные книги 2022"

    def test_page_bottom_menu_bonus(self):
        scroll_to_bottom(pytest.web_driver)
        bonus = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                        '@data-event-content="Бонус за рецензию"]')
        bonus.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.title == "Бонусная программа для рецензентов. Бонус за рецензию"

    def test_page_bottom_menu_certificates(self):
        scroll_to_bottom(pytest.web_driver)
        certificates = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                               '@data-event-content="Сертификаты"]')
        certificates.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.title == 'Сертификаты'

    def test_page_bottom_menu_only_us(self):
        scroll_to_bottom(pytest.web_driver)
        only_us = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                          '@data-event-content="Только у нас"]')
        only_us.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.title == 'Эксклюзивные книги | книжный интернет-магазин Лабиринт'

    def test_page_bottom_menu_preorder(self):
        scroll_to_bottom(pytest.web_driver)
        preorder = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                           '@data-event-content="Предзаказы"]')
        preorder.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.title == 'Предзаказ. Книги, которые мы ждем'


class TestPageBottomMenuInteresting:  # check bottom links in menu "Интересно"
    def test_page_bottom_menu_now(self):
        scroll_to_bottom(pytest.web_driver)
        now = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                      '@data-event-content="Лабиринт. Сейчас"]')
        now.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.find_element_by_xpath(
            '//a[@class="mm-link mm-link-big mm-link-big-m-sub active"]').text == "Лабиринт. Сейчас"

    def test_page_bottom_menu_child_now(self):
        scroll_to_bottom(pytest.web_driver)
        child_now = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                            '@data-event-content="Детский навигатор"]')
        child_now.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.find_element_by_xpath(
            '//a[@class="mm-link mm-link-big mm-link-big-m-sub active"]').text == "Детский навигатор"

    def test_page_bottom_menu_reviews(self):
        scroll_to_bottom(pytest.web_driver)
        reviews = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                          '@data-event-content="Рецензии читателей"]')
        reviews.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.find_element_by_xpath(
            '//a[@class="mm-link mm-link-big mm-link-big-m-sub active"]').text == "Рецензии читателей"

    def test_page_bottom_menu_book_reviews(self):
        scroll_to_bottom(pytest.web_driver)
        book_reviews = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                               '@data-event-content="Книжные обзоры"]')
        book_reviews.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.find_element_by_xpath(
            '//a[@class="mm-link mm-link-big mm-link-big-m-sub active"]').text == "Книжные обзоры"

    def test_page_bottom_menu_recommendations(self):
        scroll_to_bottom(pytest.web_driver)
        recommendations = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                                  '@data-event-content="Подборки читателей"]')
        recommendations.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.find_element_by_xpath(
            '//a[@class="mm-link mm-link-big mm-link-big-m-sub active"]').text == "Подборки читателей"

    def test_page_bottom_menu_tests(self):
        scroll_to_bottom(pytest.web_driver)
        tests = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                        '@data-event-content="Тесты"]')
        tests.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.find_element_by_xpath(
            '//a[@class="mm-link mm-link-big mm-link-big-m-sub active"]').text == "Литтесты"

    def test_page_bottom_menu_news(self):
        scroll_to_bottom(pytest.web_driver)
        news = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                       '@data-event-content="Новости Л."]')
        news.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.find_element_by_xpath(
            '//div[@class="ratingh h1"]').text == "Новости Лабиринта"

    def test_page_bottom_menu_contests(self):
        scroll_to_bottom(pytest.web_driver)
        contests = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                           '@data-event-content="Конкурсы"]')
        contests.click()
        pytest.web_driver.implicitly_wait(2)
        assert pytest.web_driver.find_element_by_xpath(
            '//a[@class="mm-link mm-link-big mm-link-big-m-sub active"]').text == "Конкурсы"

    def test_page_bottom_menu_club(self):
        scroll_to_bottom(pytest.web_driver)
        club = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                       '@data-event-content="Спецпроекты"]')
        club.click()
        pytest.web_driver.implicitly_wait(2)
        title = pytest.web_driver.title
        assert title == 'Книжный клуб интернет-магазина Лабиринт'


class TestPageBottomMenuLabAll:  # check bottom links in menu "Лабиринт — всем"
    def test_page_bottom_menu_partner(self):
        scroll_to_bottom(pytest.web_driver)
        partner = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                          '@data-event-content="Партнерам"]')
        partner.click()
        pytest.web_driver.implicitly_wait(2)
        title = pytest.web_driver.title
        assert title == "Партнерская программа Лабиринт.ру"

    def test_page_bottom_menu_vacancy(self):
        scroll_to_bottom(pytest.web_driver)
        vacancy = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                          '@data-event-content="Наши вакансии"]')
        vacancy.click()
        time.sleep(2)
        parent = pytest.web_driver.window_handles[0]
        chld = pytest.web_driver.window_handles[1]
        pytest.web_driver.switch_to.window(chld)
        title = pytest.web_driver.title
        assert title == "Издательства Москвы вакансии | Книготорговый и издательский холдинг «Лабиринт»"
        pytest.web_driver.close()
        pytest.web_driver.switch_to.window(parent)


class TestPageBottomMenuMyLab:  # check bottom links in menu "Мой Лабиринт"
    def test_page_bottom_menu_enter_by_code(self):
        scroll_to_bottom(pytest.web_driver)
        enter_by_code = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                                '@data-event-content="Войти по коду скидки или через '
                                                                'соцсеть"]')
        enter_by_code.click()
        assert pytest.web_driver.find_element_by_xpath(
            '//div[@class="js-auth__title new-auth__title"]').text == "Полный доступ к Лабиринту"

    def test_page_bottom_menu_enter(self):
        scroll_to_bottom(pytest.web_driver)
        enter = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                        '@data-event-content="Вход и регистрация"]')
        enter.click()
        assert pytest.web_driver.find_element_by_xpath(
            '//div[@class="js-auth__title new-auth__title"]').text == "Полный доступ к Лабиринту"

    def test_page_bottom_menu_visited(self):
        scroll_to_bottom(pytest.web_driver)
        visited = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                          '@data-event-content="Вы смотрели"]')
        visited.click()
        assert pytest.web_driver.find_element_by_xpath(
            '//li[@class="cabinet-menu__tab cabinet-menu__tab_active"]/a/span').text == "История просмотра"

    def test_page_bottom_menu_cabinet(self):
        scroll_to_bottom(pytest.web_driver)
        cabinet = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                          '@data-event-content="Кабинет"]')
        cabinet.click()
        assert pytest.web_driver.find_element_by_xpath(
            '//div[@class="js-auth__title new-auth__title"]').text == "Полный доступ к Лабиринту"


class TestPageBottomMenuHelp:  # check bottom links in menu "Помощь"
    def test_page_bottom_menu_order(self):
        scroll_to_bottom(pytest.web_driver)
        order = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                        '@data-event-content="Как сделать заказ"]')
        order.click()
        title = pytest.web_driver.title
        assert title == "Заказ для юридических лиц | Лабиринт"

    def test_page_bottom_menu_clauser(self):
        scroll_to_bottom(pytest.web_driver)
        clause = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                         '@data-event-content="Оплата"]')
        clause.click()
        title = pytest.web_driver.title
        assert title == "Оплата | Лабиринт"
        clause132_menu = pytest.web_driver.find_element_by_id('helpmenu132')
        clause_style = clause132_menu.get_attribute('style')
        # print(clause_style[-7:-1])
        assert clause_style[-6:-1] == "block"

    def test_page_bottom_menu_delivery(self):
        scroll_to_bottom(pytest.web_driver)
        delivery = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                           '@data-event-content="Доставка"]')
        delivery.click()
        title = pytest.web_driver.title
        assert title == "Помощь | Лабиринт"

    def test_page_bottom_menu_support(self):
        scroll_to_bottom(pytest.web_driver)
        support = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                          '@data-event-content="Поддержка"]')
        support.click()
        title = pytest.web_driver.title
        assert title == "Служба поддержки | Поддержка лабиринта"

    def test_page_bottom_menu_mail_to(self):
        scroll_to_bottom(pytest.web_driver)
        mail_to = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                          '@data-event-content="Напишите нам"]')
        link = mail_to.get_attribute('href')
        assert link == 'mailto:shop@labirintmail.ru'
        print('\nSend e-mail to:\t', link[7:])

    def test_page_bottom_menu_all_support(self):
        scroll_to_bottom(pytest.web_driver)
        all_support = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                              '@data-event-content="Вся помощь"]')
        all_support.click()
        title = pytest.web_driver.title
        assert title == "Помощь | Лабиринт"

    def test_page_bottom_menu_agreement(self):
        scroll_to_bottom(pytest.web_driver)
        agreement = pytest.web_driver.find_element_by_xpath('//li[@class="b-rfooter-e-item"]/a['
                                                            '@data-event-content="Пользовательское соглашение"]')
        agreement.click()
        title = pytest.web_driver.title
        assert title == "Пользовательское Соглашение об условиях предоставления Услуг в интернет-магазине Лабиринт | " \
                        "Лабиринт"
