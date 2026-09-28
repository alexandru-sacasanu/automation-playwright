"""
Automation demo: logs into saucedemo.com, adds items to cart, completes
checkout, and records a structured run log (steps, timings, screenshots)
for the HTML report generator.
"""
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE_URL = "https://www.saucedemo.com"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"
PRODUCTS_TO_BUY = [
    "Sauce Labs Backpack",
    "Sauce Labs Bike Light",
]

ROOT = Path(__file__).resolve().parent.parent
SCREENSHOT_DIR = ROOT / "reports" / "screenshots"
LOG_PATH = ROOT / "reports" / "run_log.json"


class RunLogger:
    def __init__(self):
        self.steps = []
        self.run_started = datetime.now(timezone.utc)

    def step(self, name, page=None, status="passed", detail=""):
        screenshot_rel = None
        if page is not None:
            SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
            fname = f"{len(self.steps):02d}_{name.lower().replace(' ', '_')}.png"
            page.screenshot(path=str(SCREENSHOT_DIR / fname))
            screenshot_rel = f"screenshots/{fname}"

        self.steps.append({
            "name": name,
            "status": status,
            "detail": detail,
            "screenshot": screenshot_rel,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def write(self, run_status="passed"):
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "run_started": self.run_started.isoformat(),
            "run_finished": datetime.now(timezone.utc).isoformat(),
            "status": run_status,
            "target": BASE_URL,
            "steps": self.steps,
        }
        LOG_PATH.write_text(json.dumps(payload, indent=2))
        return payload


def run():
    logger = RunLogger()
    run_status = "passed"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})

        try:
            page.goto(BASE_URL)
            logger.step("Load login page", page, detail=f"Navigated to {BASE_URL}")

            page.fill("#user-name", USERNAME)
            page.fill("#password", PASSWORD)
            page.click("#login-button")
            page.wait_for_selector(".inventory_list")
            logger.step("Log in", page, detail=f"Logged in as {USERNAME}")

            for product_name in PRODUCTS_TO_BUY:
                item = page.locator(".inventory_item", has_text=product_name)
                item.locator("button", has_text="Add to cart").click()
            logger.step(
                "Add items to cart",
                page,
                detail=f"Added: {', '.join(PRODUCTS_TO_BUY)}",
            )

            page.click(".shopping_cart_link")
            page.wait_for_selector(".cart_list")
            cart_items = page.locator(".cart_item").count()
            logger.step(
                "Open cart",
                page,
                detail=f"{cart_items} item(s) in cart",
            )

            page.click("#checkout")
            page.fill("#first-name", "Alex")
            page.fill("#last-name", "Demo")
            page.fill("#postal-code", "94107")
            page.click("#continue")
            logger.step("Fill checkout info", page, detail="Continued to overview")

            total_text = page.locator(".summary_total_label").inner_text()
            logger.step("Review order summary", page, detail=total_text)

            page.click("#finish")
            page.wait_for_selector(".complete-header")
            confirmation = page.locator(".complete-header").inner_text()
            logger.step("Complete checkout", page, detail=confirmation)

        except Exception as exc:
            run_status = "failed"
            logger.step("Unhandled error", page, status="failed", detail=str(exc))
            raise
        finally:
            browser.close()
            logger.write(run_status=run_status)

    return run_status


if __name__ == "__main__":
    result = run()
    print(f"Run finished: {result}")
