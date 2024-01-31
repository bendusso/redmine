from pages.base_page import BasePage


class LoginPage(BasePage):

    def navigate_to_login_page(self, url):
        self.open_page(url)

    def set_page(self, page):
        self.page = page

    def login(self, creds):
        user_data = {
            'input[name="username"]': creds['login'],
            'input[name="password"]': creds['password']
        }

        self.fill_form(user_data)
        self.page.click('input[name="login"]')
