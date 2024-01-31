from pages.register_page import RegisterPage


def test_register_account(browser, config, faker_instance):
    register_page = RegisterPage(browser)
    register_page.navigate_to_register_page(config['register_url'])

    user = {
        "login": faker_instance.email(),
        "password": faker_instance.password(),
        "first_name": faker_instance.last_name(),
        "last_name": faker_instance.last_name()
    }
    register_page.register_account(user)

    assert register_page.page.url == config['my_account_url']
    flash_notice = register_page.get_flash_notice()
    notice_text = flash_notice.inner_text()
    expected_message = "Your account has been activated. You can now log in."
    assert notice_text == expected_message, f"Unexpected flash notice: {notice_text}"


def test_register_with_existing_email(browser, config, unique_user):
    register_page = RegisterPage(browser)
    register_page.navigate_to_register_page(config['register_url'])

    register_page.register_account(unique_user)

    error_messages_list = register_page.get_error_message()
    formatted_error_message = ', '.join([msg.strip() for msg in error_messages_list[0].split('\n') if msg])

    assert formatted_error_message, "Expected an error message for existing email, but didn't find one."
    expected_message = "Email has already been taken, Login has already been taken"
    assert formatted_error_message == expected_message, f"Expected error message '{expected_message}', but got '{formatted_error_message}'."

    assert register_page.page.url == config[
        'register_url'], "Expected to remain on the registration page due to duplicate email."


def test_register_with_invalid_email(browser, config, faker_instance):
    register_page = RegisterPage(browser)
    register_page.navigate_to_register_page(config['register_url'])

    user = {
        "login": "invalid_email",
        "password": faker_instance.password(),
        "first_name": faker_instance.last_name(),
        "last_name": faker_instance.last_name()
    }
    register_page.register_account(user)

    error_messages_list = register_page.get_error_message()
    formatted_error_message = ', '.join([msg.strip() for msg in error_messages_list[0].split('\n') if msg])

    breakpoint()
    assert formatted_error_message, "Expected an error message for invalid email, but didn't find one."
    expected_message = "Email is invalid"
    assert formatted_error_message == expected_message, f"Expected error message '{expected_message}', but got '{formatted_error_message}'."

    assert register_page.page.url == config[
        'register_url'], "Expected to remain on the registration page due to invalid email."


def test_register_with_invalid_email(browser, config):
    register_page = RegisterPage(browser)
    register_page.navigate_to_register_page(config['register_url'])

    user = {
        "login": " ",
        "password": " ",
        "first_name": " ",
        "last_name": " "
    }
    register_page.register_account(user)

    error_messages_list = register_page.get_error_message()
    formatted_error_message = ', '.join([msg.strip() for msg in error_messages_list[0].split('\n') if msg])

    assert formatted_error_message, "Expected an error message for empty registration field"
    expected_message = 'Email cannot be blank, Login cannot be blank, Login is invalid, First name cannot be blank, Last name cannot be blank, Password is too short (minimum is 8 characters)'
    assert formatted_error_message == expected_message, f"Expected error message '{expected_message}', but got '{formatted_error_message}'."

    assert register_page.page.url == config[
        'register_url'], "Expected to remain on the registration page due to empty registration fields."
