from playwright.sync_api import sync_playwright
import re
from playwright.sync_api import expect


def test_home_page():
    print("\n\n\nTEST: Home page")
    with sync_playwright() as p:
        for browser_type in [p.chromium, p.firefox]:
            browser = browser_type.launch(headless=True)
            page = browser.new_page()
            page.goto('https://kochamyjave.pythonanywhere.com/')
            print(f"Page title: {page.title()}\tBrowser: {browser_type.name}")
            page.screenshot(path=f'screenshots/ss-home-{browser_type.name}.png')
            print(f"Page title after redirect: {page.title()}\tBrowser: {browser_type.name}")
            print(f"Screenshot path: screenshots/ss-home-{browser_type.name}.png\n")
            browser.close()


def test_about_page():
    print("\n\n\nTEST: About page")
    with sync_playwright() as p:
        for browser_type in [p.chromium, p.firefox]:
            browser = browser_type.launch(headless=True)
            page = browser.new_page()
            page.goto('https://kochamyjave.pythonanywhere.com/about')
            print(f"Page title: {page.title()}\tBrowser: {browser_type.name}")
            page.screenshot(path=f'screenshots/ss-about-{browser_type.name}.png')
            print(f"Page title after redirect: {page.title()}\tBrowser: {browser_type.name}")
            print(f"Screenshot path: screenshots/ss-about-{browser_type.name}.png\n")
            browser.close()


def test_login_page():
    print("\n\n\nTEST: Log in page")
    with sync_playwright() as p:
        for browser_type in [p.chromium, p.firefox]:
            browser = browser_type.launch(headless=True)
            page = browser.new_page()
            page.goto('https://kochamyjave.pythonanywhere.com/login_page')
            print(f"Page title: {page.title()}\tBrowser: {browser_type.name}")
            page.screenshot(path=f'screenshots/ss-login-{browser_type.name}.png')
            print(f"Page title after redirect: {page.title()}\tBrowser: {browser_type.name}")
            print(f"Screenshot path: screenshots/ss-login-{browser_type.name}.png\n")
            browser.close()

def  test_new_post_page():
    print("\n\n\nTEST: New post page")
    with sync_playwright() as p:
        for browser_type in [p.chromium, p.firefox]:
            browser = browser_type.launch(headless=True)
            page = browser.new_page()
            page.goto('https://kochamyjave.pythonanywhere.com/new_post')
            print(f"Page title: {page.title()}\tBrowser: {browser_type.name}")
            page.screenshot(path=f'screenshots/ss-newpost-{browser_type.name}.png')
            print(f"Page title after redirect: {page.title()}\tBrowser: {browser_type.name}")
            print(f"Screenshot path: screenshots/ss-newpost-{browser_type.name}.png\n")
            browser.close()

# def test_new_comment_page():
#     print("\n\n\nTEST: New comment page")
#     with sync_playwright() as p:
#         for browser_type in [p.chromium, p.firefox]:
#             browser = browser_type.launch(headless=True)
#             page = browser.new_page()
#             page.goto('https://kochamyjave.pythonanywhere.com/new_comment/1')
#             print(f"Page title: {page.title()}\tBrowser: {browser_type.name}")
#             page.screenshot(path=f'/screenshots/ss-newcomment-{browser_type.name}.png')
#             browser.close()
#             print(f"Page title after redirect: {page.title()}\tBrowser: {browser_type.name}")
#             print(f"Screenshot path: screenshots/ss-newcomment-{browser_type.name}.png\n")
#             browser.close()


def test_post_details_page():
    print("\n\n\nTEST: Post details page")
    with sync_playwright() as p:
        for browser_type in [p.chromium, p.firefox]:
            browser = browser_type.launch(headless=True)
            page = browser.new_page()
            page.goto('https://kochamyjave.pythonanywhere.com/post_details/2')
            print(f"Page title: {page.title()}\tBrowser: {browser_type.name}")
            page.screenshot(path=f'screenshots/ss-postdetails-{browser_type.name}.png')
            print(f"Page title after redirect: {page.title()}\tBrowser: {browser_type.name}")
            print(f"Screenshot path: screenshots/ss-postdetails-{browser_type.name}.png\n")
            browser.close()


def test_home_page_login_href():
    print("\n\n\nTEST: href to Log in page in Home page")
    with sync_playwright() as p:
        for browser_type in [p.chromium, p.firefox]:
            browser = browser_type.launch(headless=False)
            page = browser.new_page()
            page.goto("https://kochamyjave.pythonanywhere.com/")
            print(f"Page title: {page.title()}\tBrowser: {browser_type.name}")
            expect(page).to_have_title(re.compile("kochamyJave-Project"))
            get_started = page.get_by_role("link", name="Log In")
            expect(get_started).to_have_attribute("href", "/login_page")
            get_started.click()
            expect(page).to_have_title(re.compile("Log in"))
            print(f"Page title after redirect: {page.title()}\tBrowser: {browser_type.name}")
            browser.close()


def test_home_page_about_href():
    print("\n\n\nTEST: href to About page in Home page")
    with sync_playwright() as p:
        for browser_type in [p.chromium, p.firefox]:
            browser = browser_type.launch(headless=False)
            page = browser.new_page()
            page.goto("https://kochamyjave.pythonanywhere.com/")
            print(f"Page title: {page.title()}\tBrowser: {browser_type.name}")
            expect(page).to_have_title(re.compile("kochamyJave-Project"))
            get_started = page.get_by_role("link", name="About")
            expect(get_started).to_have_attribute("href", "/about")
            get_started.click()
            expect(page).to_have_title(re.compile("About"))
            print(f"Page title after redirect: {page.title()}\tBrowser: {browser_type.name}")
            browser.close()


def test_about_home_href():
    print("\n\n\nTEST: href to Home page in About page")
    with sync_playwright() as p:
        for browser_type in [p.chromium, p.firefox]:
            browser = browser_type.launch(headless=False)
            page = browser.new_page()
            page.goto("https://kochamyjave.pythonanywhere.com/about")
            print(f"Page title: {page.title()}\tBrowser: {browser_type.name}")
            expect(page).to_have_title(re.compile("About"))
            get_started = page.get_by_role("link", name="Home")
            expect(get_started).to_have_attribute("href", "/")
            get_started.click()
            expect(page).to_have_title(re.compile("kochamyJave-Project"))
            print(f"Page title after redirect: {page.title()}\tBrowser: {browser_type.name}")
            browser.close()


def test_about_github_href():
    print("\n\n\nTEST: href to GitHub repository in About page")
    with sync_playwright() as p:
        for browser_type in [p.chromium, p.firefox]:
            browser = browser_type.launch(headless=False)
            page = browser.new_page()
            page.goto("https://kochamyjave.pythonanywhere.com/about")
            expect(page).to_have_title(re.compile("About"))
            print(f"Page title: {page.title()}\tBrowser: {browser_type.name}")
            get_started = page.get_by_role("link", name="GitHub")
            expect(get_started).to_have_attribute("href", "https://github.com/KamSaf/kochamyJave-project")
            with page.expect_popup() as popup_info:
                get_started.click()
            popup = popup_info.value
            expect(popup).to_have_title(re.compile("KamSaf/kochamyJave-project"))
            print(f"New page title: {popup.title()}\tBrowser: {browser_type.name}")
            browser.close()


if __name__ == '__main__':
    test_home_page()
    test_about_page()
    test_login_page()
    test_new_post_page()
    test_post_details_page()
    # test_new_comment_page()
    test_home_page_login_href()
    test_home_page_about_href()
    test_about_home_href()
    test_about_github_href()
    print("\n\nDone")
