class BasePage:
    def __init__(self, browser):
        self.browser = browser
        self.page = None

    def open_page(self, url):
        self.page = self.browser.new_page()
        self.page.goto(url)

    def fill_form(self, field_values):
        for selector, value in field_values.items():
            self.page.fill(selector, value)

    def get_flash_notice(self):
        return self.page.locator('div.flash.notice#flash_notice')

    def get_flash_error(self):
        return self.page.locator('div.flash.error#flash_error')

    def get_error_message(self):
        errors_list = []
        errors = self.page.locator('div#errorExplanation').element_handles()
        for error in errors:
            errors_list.append(error.text_content())
        return errors_list
