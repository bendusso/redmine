from pages.login_page import LoginPage
from pages.register_page import RegisterPage


def test_login_with_valid_credentials(browser, config, faker_instance):
    login_page = LoginPage(browser)
    login_page.navigate_to_login_page(config['login_url'])
    credentials = {
        "login": config['credentials']['login'],
        "password": config['credentials']['password'],
    }
    expected_url = config['my_page_url']

    flash_error = False
    login_successful = False

    login_page.login(credentials)

    if login_page.page.url != expected_url:
        flash_error = login_page.get_flash_error()

    if flash_error:
        notice_text = flash_error.inner_text()
        expected_message = "Invalid user or password"
        login_successful = notice_text != expected_message
    else:
        login_successful = login_page.page.url == expected_url

    if not login_successful:
        register_page = RegisterPage(browser)
        register_page.navigate_to_register_page(config['register_url'])

        user = {
            "login": credentials['login'],
            "password": credentials['password'],
            "first_name": faker_instance.first_name(),
            "last_name": faker_instance.last_name(),
            "email": faker_instance.email()
        }

        register_page.register_account(user)

        login_page.navigate_to_login_page(config['login_url'])
        login_page.login(credentials)
        login_page.page.wait_for_load_state('networkidle')

        assert login_page.page.url == expected_url, (
            f"URL mismatch: Expected URL '{expected_url}', but current URL is '{login_page.page.url}'."
        )


def test_login_with_invalid_credentials(browser, config, faker_instance):
    login_page = LoginPage(browser)
    login_page.navigate_to_login_page(config['login_url'])
    credentials = {
        "login": faker_instance.email(),
        "password": faker_instance.password(),
    }

    login_page.login(credentials)
    flash_error = login_page.get_flash_error()

    assert flash_error, "Expected a flash notice for invalid login, but didn't find one."
    error_text = flash_error.inner_text()
    expected_message = "Invalid user or password"
    assert error_text == expected_message, f"Expected error message '{expected_message}', but got '{error_text}'."

    assert login_page.page.url == config['login_url'], (
        f"Expected to remain on the login page, but the URL changed to '{login_page.page.url}'."
    )
