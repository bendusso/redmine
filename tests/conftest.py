import pytest
from playwright.sync_api import sync_playwright
import yaml
import faker

from pages.register_page import RegisterPage


@pytest.fixture
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture(scope='session')
def config():
    with open('../config.yml', 'r') as file:
        return yaml.safe_load(file)


@pytest.fixture(scope='session')
def faker_instance():
    return faker.Faker()


@pytest.fixture(scope='function')
def unique_user(browser, config, faker_instance):
    user_data = {
        "login": faker_instance.email(),
        "password": faker_instance.password(),
        "first_name": faker_instance.first_name(),
        "last_name": faker_instance.last_name()
    }

    register_page = RegisterPage(browser)
    register_page.navigate_to_register_page(config['register_url'])
    register_page.register_account(user_data)

    yield user_data
