class CheckoutView:
    def __init__(self, page):
        self.page = page
        self.first_name_input = page.locator("#first-name")
        self.last_name_input = page.locator("#last-name")
        self.postal_code_input = page.locator("#postal-code")
        self.continue_button = page.locator("#continue")
        self.finish_button = page.locator("#finish")
        self.summary_total = page.locator(".summary_total_label")
        self.complete_header = page.locator(".complete-header")
        self.error_message = page.locator("[data-test='error']")

    def fill_info(self, first_name, last_name, postal_code):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.continue_button.click()
        return self

    def total_text(self):
        return self.summary_total.inner_text()

    def finish(self):
        self.finish_button.click()
        return self

    def confirmation_text(self):
        self.complete_header.wait_for()
        return self.complete_header.inner_text()
