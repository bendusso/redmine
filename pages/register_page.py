from pages.base_page import BasePage


class RegisterPage(BasePage):

    def navigate_to_register_page(self, url):
        self.open_page(url)

    def register_account(self, user):
        account_data = {
            "input[id='user_login']": user["login"],
            "input[id='user_password']": user["password"],
            "input[id='user_password_confirmation']": user["password"],
            "input[id='user_firstname']": user["first_name"],
            "input[id='user_lastname']": user["last_name"],
            "input[id='user_mail']": user["login"]
        }
        self.fill_form(account_data)
        self.page.click('input[name="commit"]')
