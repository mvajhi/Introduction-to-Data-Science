from bs4 import BeautifulSoup
from persiantools.jdatetime import JalaliDate
import datetime

# TODO: add export to csv
# TODO: work with year not soup object, send request and create soup object itself
# TODO: add this package to pypi :)

class Holiday:
    def __init__(self, soup: BeautifulSoup) -> None:
        '''
        soup: BeautifulSoup object of the 'https://www.time.ir/fa/eventyear-%D8%AA%D9%82%D9%88%DB%8C%D9%85-%D8%B3%D8%A7%D9%84%DB%8C%D8%A7%D9%86%D9%87'
        '''
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

    def get_holidays(self, add_noroze:bool=False, add_thursday:bool=False) -> list[JalaliDate]:
        '''
        add_noroze: add noroze to holidays until 13 farvardin
        add_thursday: add thursday to holidays
        '''
        holidays = list[JalaliDate]()
        holiday_divs = self.__find_holiday_div()
        for day_div in holiday_divs:
            if self.__is_valid_holiday(day_div):
                day = self.__get_day(day_div)
                month = self.__get_month_num(day_div)
                year = self.__get_year(day_div)
                holidays.append(JalaliDate(year, month, day))
        
        if add_noroze:
            noroze_holidays = self.__get_noroze(holidays[0]._year)
            for h in noroze_holidays:
                if h not in holidays:
                    holidays.append(h)

        if add_thursday:
            thursday_holidays = self.__get_thursdays(holidays[0]._year)
            for h in thursday_holidays:
                if h not in holidays:
                    holidays.append(h)

        return holidays

    def __get_noroze(self, year:int) -> list[JalaliDate]:
        noroze = []
        for i in range(1, 14):
            noroze.append(JalaliDate(year, 1, i))
        return noroze

    def __get_thursdays(self, year:int) -> list[JalaliDate]:
        thursdays = []
        tmp = self.__find_first_thursday(year)

        while tmp._year == year:
            thursdays.append(tmp)
            tmp += datetime.timedelta(days=7)

        return thursdays
    
    def __find_first_thursday(self, year:int) -> JalaliDate:
        for i in range(1, 8):
            if JalaliDate(year, 1, i).weekday() == 5:
                return JalaliDate(year, 1, i)

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