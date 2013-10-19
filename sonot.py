from scrapper import Scrapper
from ui import View

EMAIL = ""
PASSWORD = ""

if __name__ == '__main__':
    scrapper = Scrapper()
    scrapper.login(EMAIL, PASSWORD)
    scrapper.search_tag("python")
    view = View(scrapper.exit_)
    print("dsa")
