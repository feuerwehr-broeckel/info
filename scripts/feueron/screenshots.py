"""FeuerON screenshot automation using Playwright."""

import os
from pathlib import Path

from playwright.sync_api import sync_playwright


def get_credentials() -> tuple[str, str, str]:
    """
    Get FeuerON credentials from environment variables.

    Returns:
        Tuple of (username, password, region_id)

    Raises:
        ValueError: If required environment variables are not set
    """
    username = os.getenv("FEUERON_USERNAME")
    password = os.getenv("FEUERON_PASSWORD")
    region_id = os.getenv("FEUERON_REGION_ID", "156")

    if not username or not password:
        raise ValueError(
            "Please set FEUERON_USERNAME and FEUERON_PASSWORD environment variables"
        )

    return username, password, region_id


def take_screenshots(output_dir: Path) -> list[Path]:
    """
    Take screenshots of FeuerON application.

    Args:
        output_dir: Directory where screenshots will be saved

    Returns:
        List of paths to the saved screenshots
    """
    username, password, region_id = get_credentials()

    output_dir.mkdir(parents=True, exist_ok=True)

    screenshot_paths: list[Path] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        # Navigate to FeuerON
        print("Navigating to FeuerON...")
        page.goto("https://www.feueron.de")
        page.wait_for_load_state("networkidle")

        # Screenshot 1: Homepage (before login)
        path = output_dir / "01_feueron_homepage.png"
        page.screenshot(path=str(path), full_page=True)
        screenshot_paths.append(path)
        print(f"Screenshot saved: {path}")

        # Fill login form
        print("Filling login form...")
        page.evaluate(
            f"$('#selectedOrganisationIndex_jqxDropDownList').jqxDropDownList('selectIndex', {region_id});"
        )
        page.fill('input[name="zmsLoginName"]', username)
        page.fill('input[name="zmsLoginPassword"]', password)

        # Screenshot 2: Form filled (before submit)
        path = output_dir / "02_feueron_form_filled.png"
        page.screenshot(path=str(path), full_page=True)
        screenshot_paths.append(path)
        print(f"Screenshot saved: {path}")

        # Submit login form
        page.click('input[type="submit"]')
        page.wait_for_load_state("networkidle")

        # Screenshot 3: After login
        path = output_dir / "03_feueron_logged_in.png"
        page.screenshot(path=str(path), full_page=True)
        screenshot_paths.append(path)
        print(f"Screenshot saved: {path}")

        # Navigate to Berichte
        print("Navigating to Berichte...")
        page.get_by_role("link", name="Berichte").click()
        page.wait_for_load_state("networkidle")

        # Screenshot 4: Berichte page
        path = output_dir / "04_feueron_berichte.png"
        page.screenshot(path=str(path), full_page=True)
        screenshot_paths.append(path)
        print(f"Screenshot saved: {path}")

        # Click on Dienstbuch tab
        print("Clicking Dienstbuch tab...")
        page.get_by_role("tab", name="Dienstbuch").click()
        page.wait_for_load_state("networkidle")

        # Screenshot 5: Dienstbuch
        path = output_dir / "05_feueron_dienstbuch.png"
        page.set_viewport_size({"width": 980, "height": 801})
        page.screenshot(path=str(path), full_page=True)
        screenshot_paths.append(path)
        print(f"Screenshot saved: {path}")

        browser.close()

    print(f"\nScreenshots completed: {len(screenshot_paths)} files saved")
    return screenshot_paths
