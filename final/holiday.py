from bs4 import BeautifulSoup
from persiantools.jdatetime import JalaliDate
class Holiday:
    def __init__(self, soup) -> None:
        self.soup = soup
        self.month_num = {
            'فروردین': 1,
            'اردیبهشت': 2,
            'خرداد': 3,
            'تیر': 4,
            'مرداد': 5,
            'اَمرداد': 5,
            'شهریور': 6,
            'مهر': 7,
            'آبان': 8,
            'آذر': 9,
            'دی': 10,
            'بهمن': 11,
            'اسفند': 12
        }

    def get_holidays(self) -> list[JalaliDate]:
        holidays = []
        holiday_divs = self.__find_holiday_div()
        for day_div in holiday_divs:
            if self.__is_valid_holiday(day_div):
                day = self.__get_day(day_div)
                month = self.__get_month_num(day_div)
                year = self.__get_year(day_div)
                holidays.append(JalaliDate(year, month, day))
        return holidays

    def __find_holiday_div(self) -> BeautifulSoup:
        return self.soup.find_all('div', class_='holiday')

    def __is_valid_holiday(self, day_div: BeautifulSoup) -> bool:
        return 'disabled' not in day_div.parent['class']
    
    def __get_day(self, day_div: BeautifulSoup) -> int:
        return int(day_div.find('div', class_='jalali').text)
    
    def __find_month_year(self, day_div: BeautifulSoup) -> BeautifulSoup:
        return day_div.parent.parent.parent.parent.find('a', class_='jalali')

    def __get_month_year(self, day_div: BeautifulSoup) -> dict[str, any]:
        row_str = self.__find_month_year(day_div).text
        # 'فروردین ۱۴۰۲'
        month, year = [i for i in row_str.split(' ') if i != '']
        return {
            'month': month,
            'year': year
        }

    def __get_month(self, day_div: BeautifulSoup) -> str:
        return self.__get_month_year(day_div)['month']
    
    def __get_year(self, day_div: BeautifulSoup) -> int:
        return int(self.__get_month_year(day_div)['year'])

    def __get_month_num(self, day_div: BeautifulSoup) -> int:
        return self.month_num[self.__get_month(day_div)]