import datetime as dt


class Record:
    def __init__(self, amount, comment, date=dt.date.today()):
        self.amount = amount
        self.date = date
        self.comment = comment

    def __str__(self):
        return f'{self.amount}, {self.comment}, {self.date}'


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        return sum(record.amount for record in self.records)

    def get_week_stats():
        pass


class CashCalculator(Calculator):
    USD_RATE = 73.73
    EURO_RATE = 87.86

    def get_today_cash_remained(self, currency):
        wasted_cash = self.get_today_stats()
        if currency == 'rub':
            if self.limit - wasted_cash > 0:
                return (
                    f'На сегодня осталось {self.limit - wasted_cash} '
                    f'руб'
                )
            elif self.limit - wasted_cash == 0:
                return 'Денег нет, держись'
            else:
                return (
                    f'Денег нет, держись: твой долг - '
                    f'{-(self.limit - wasted_cash)} руб'
                )
        elif currency == 'usd':
            if self.limit - wasted_cash > 0:
                return (
                    f'На сегодня осталось '
                    f'{(self.limit - wasted_cash) / USD_RATE} usd'
                )
            elif self.limit - wasted_cash == 0:
                return 'Денег нет, держись'
            else:
                return (
                    f'Денег нет, держись: твой долг - '
                    f'{-(self.limit - wasted_cash)} usd'
                )
        else:
            if self.limit - wasted_cash > 0:
                return (
                    f'На сегодня осталось '
                    f'{(self.limit - wasted_cash) / EURO_RATE} euro'
                )
            elif self.limit - wasted_cash == 0:
                return 'Денег нет, держись'
            else:
                return (
                    f'Денег нет, держись: твой долг - '
                    f'{-(self.limit - wasted_cash) / EURO_RATE} euro'
                )


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        wasted_calories = self.get_today_stats
        if self.limit - wasted_calories > 0:
            return (
                f'Сегодня можно съесть что-нибудь ещё, но с общей '
                f'калорийностью не более {self.limit - wasted_calories} кКал'
            )
        else:
            return 'Хватит есть!'


# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))

print(cash_calculator.get_today_cash_remained('rub'))
# должно напечататься
# На сегодня осталось 555 руб