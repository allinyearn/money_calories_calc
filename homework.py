import datetime as dt
from typing import Union, Optional, Tuple, List


class Record:
    date_format = '%d.%m.%Y'
    amount: int
    comment: str
    date: Optional[str]

    def __init__(self, amount: int, comment: str, 
                 date: Optional[str] = None) -> None:
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.date_format).date()


class Calculator:
    CustomType = List[Tuple[int, str, Optional[str]]]
    limit: int
    records: CustomType
    record: Tuple[int, str, Optional[str]]
    today_amount: int
    week_amount: int

    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.records: CustomType = []

    def add_record(self, record: Tuple[int, str, Optional[str]]) -> None:
        """Добавляем новую запись о расходах."""
        self.records.append(record)

    def get_today_stats(self) -> int:
        """Получаем количество потраченных сегодня денег или калорий"""
        date_today = dt.date.today()
        today_amount: int = 0
        for record in self.records:
            if record.date == date_today:
                today_amount += record.amount
        return today_amount

    def get_week_stats(self) -> int:
        """Получаем количество потраченных за неделю денег или калорий"""
        period = dt.timedelta(days=7)
        today = dt.date.today()
        week_ago = today - period
        week_amount: int = 0
        for record in self.records:
            if today >= record.date > week_ago:
                week_amount += record.amount
            else:
                pass
        return week_amount

    def get_today_remainder(self) -> int:
        """Высчитываем остаток на сегодня"""
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    USD_RATE: int = 73.73
    EURO_RATE: int = 87.86
    RUB_RATE: int = 1.0

    def get_today_cash_remained(self, currency: str) -> Union[str, int]:
        """Получаем ответ от калькулятора на основе расчитанного остатка"""
        remainder = self.get_today_remainder()

        def comparison(rate, output):
            """Сравниваем остаток с лимитом и берём подходящий ответ"""
            if remainder == 0:
                return 'Денег нет, держись'
            rate_division = abs(round(remainder / rate, 2))
            if remainder > 0:
                return (
                    'На сегодня осталось '
                    f'{rate_division} '
                    f'{output}'
                )
            else:
                return (
                    'Денег нет, держись: твой долг - '
                    f'{rate_division} '
                    f'{output}'
                )
        if currency == 'rub':
            return comparison(self.RUB_RATE, 'руб')
        elif currency == 'usd':
            return comparison(self.USD_RATE, 'USD')
        elif currency == 'eur':
            return comparison(self.EURO_RATE, 'Euro')
        raise ValueError('Wrong currency')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self) -> Union[str, int]:
        """Получаем ответ от калькулятора на основе расчитанного остатка"""
        remainder = self.get_today_remainder()

        if remainder > 0:
            return (
                'Сегодня можно съесть что-нибудь ещё, но с общей '
                f'калорийностью не более {remainder} кКал'
            )
        else:
            return 'Хватит есть!'
