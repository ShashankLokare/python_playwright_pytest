class BasePage:
    def __init__(self, page, base_url: str = "https://demoblaze.com"):
        self.page = page
        self.base_url = base_url

    def goto(self, path: str = ""):
        url = self.base_url.rstrip("/") + ("/" + path.lstrip("/") if path else "")
        self.page.goto(url)
