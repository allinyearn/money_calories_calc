import datetime as dt
from typing import Optional, Tuple, List, Dict

DATE_FORMAT = '%d.%m.%Y'


class Record:
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
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()


class Calculator:
    limit: int
    today_amount: int
    week_amount: int

    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.records: List[Record] = []

    def add_record(self, record: Record) -> None:
        """Добавляем новую запись о расходах."""
        self.records.append(record)

    def get_today_stats(self) -> int:
        """Получаем количество потраченных сегодня денег или калорий."""
        date_today = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == date_today)

    def get_week_stats(self) -> int:
        """Получаем количество потраченных за неделю денег или калорий."""
        period = dt.timedelta(days=7)
        today = dt.date.today()
        week_ago = today - period
        return sum(record.amount for record in self.records
                   if today >= record.date > week_ago)

    def get_today_remainder(self) -> int:
        """Высчитываем остаток на сегодня."""
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    USD_RATE: float = 73.73
    EURO_RATE: float = 87.86
    RUB_RATE: float = 1.0

    def get_today_cash_remained(self, currency) -> str:
        """Получаем ответ исходя из остатка."""
        remainder = self.get_today_remainder()
        if remainder == 0:
            return 'Денег нет, держись'
        rates: Dict[str, Tuple[float, str]] = {
            'rub': (self.RUB_RATE, 'руб'),
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro')
        }
        if currency in rates:
            rate, output = rates[currency][0], rates[currency][1]
        else:
            raise ValueError('Wrong currency')
        rate_division = abs(round(remainder / rate, 2))
        if remainder > 0:
            return ('На сегодня осталось '
                    f'{rate_division} {output}')
        return ('Денег нет, держись: твой долг - '
                f'{rate_division} {output}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self) -> str:
        """Получаем ответ от калькулятора на основе расчитанного остатка."""
        remainder = self.get_today_remainder()
        if remainder > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {remainder} кКал')
        return 'Хватит есть!'
