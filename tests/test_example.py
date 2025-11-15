def test_example(page):
    page.goto("https://example.com")
    # Title should contain "Example Domain"
    assert "Example Domain" in page.title()
    # H1 text check
    assert page.locator("h1").text_content().strip() == "Example Domain"
