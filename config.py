import os


class Config:
    BASE_URL = os.environ.get("BASE_URL", "https://www.saucedemo.com")

    STANDARD_USER = os.environ.get("STANDARD_USER", "standard_user")
    LOCKED_USER = os.environ.get("LOCKED_USER", "locked_out_user")
    PROBLEM_USER = os.environ.get("PROBLEM_USER", "problem_user")
    PASSWORD = os.environ.get("SAUCE_PASSWORD", "secret_sauce")

    DEFAULT_TIMEOUT_MS = int(os.environ.get("DEFAULT_TIMEOUT_MS", "5000"))

    CHECKOUT_FIRST_NAME = "Alex"
    CHECKOUT_LAST_NAME = "Demo"
    CHECKOUT_POSTAL_CODE = "94107"
