from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep


class Cancelled_Lesson:
    def __init__(self, details: str, time_span: tuple, date: str) -> None:
        self.details = details
        self.time_span = time_span
        self.date = date
        self.month = date[:-2]
        self.day = date[2:]

    def filter_details(self) -> None:
        stop = self.details.index(",")
        self.name = self.details[6:stop]


def find_cancelled_lessons():
    cancelled_lessons = []
    with open("schedule.html", "r") as f:
        soup = BeautifulSoup(f, "html.parser")
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    URL = "https://ehadhaam.iscool.co.il/%D7%9E%D7%A2%D7%A8%D7%9B%D7%AA%D7%A9%D7%A2%D7%95%D7%AA/tabid/512/language/he-IL/Default.aspx"

    day_conv = {
        "1": "Sunday",
        "2": "Monday",
        "3": "Tuesday",
        "4": "Wednesday",
        "5": "Thursday",
        "6": "Friday",
    }
    # * Gets html from school website and converts to bs4
    # driver.get(URL)
    # print(driver.title)

    # link = driver.find_element_by_id("dnn_ctr1338_TimeTableView_btnChangesTable")
    # link.click()

    # try:
    #     select = Select(
    #         WebDriverWait(driver, 10).until(
    #             EC.presence_of_element_located(
    #                 (By.ID, "dnn_ctr1338_TimeTableView_ClassesList")
    #             )
    #         )
    #     )
    #     select.select_by_value("1")
    # except Exception:
    #     print("error")
    #     driver.quit()

    # soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find("table", class_="TTTable")
    rows: list[BeautifulSoup] = table.find_all("tr")
    dates: list[BeautifulSoup] = rows[0].find_all("td")
    for row in rows:
        cells: list[BeautifulSoup] = row.findChildren("td", recursive=False)
        cell: BeautifulSoup
        for index, cell in enumerate(cells):
            cancels = cell.find_all("td", class_="TableFreeChange")
            lesson: BeautifulSoup
            for lesson in cancels:
                school_hour = cells[0].text
                date_day: str = dates[index].text
                date_index: int = date_day.index(".")
                date: str = date_day[(date_index - 2) : (date_index + 3)]
                cnl = Cancelled_Lesson(
                    lesson.text, (school_hour[2:7], school_hour[7:-1]), date
                )
                cancelled_lessons.append(cnl)
                cnl.filter_details()
    return cancelled_lessons


def create_event(lesson: Cancelled_Lesson):
    event = {
        "summary": f"שיעור {lesson.name} בוטל",
        "start": {
            "dateTime": f"2021-{lesson.month}-{lesson.day}T{lesson.time_span[0]}+2:00"
        },
        "end": {
            "dateTime": f"2021-{lesson.month}-{lesson.day}T{lesson.time_span[1]}+2:00"
        },
    }


if __name__ == "__main__":
    cancelled_lessons = find_cancelled_lessons()
    for lesson in cancelled_lessons:
        create_event(lesson)
