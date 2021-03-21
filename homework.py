import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, "%d.%m.%Y").date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_amount = 0
        for record in self.records:
            if record.date == dt.date.today():
                today_amount += record.amount
            else:
                pass
        return today_amount

    def get_week_stats(self):
        period = dt.timedelta(days=7)
        today = dt.date.today()
        week_ago = today - period
        week_amount = 0
        for record in self.records:
            if today >= record.date > week_ago:
                week_amount += record.amount
            else:
                pass
        return week_amount


class CashCalculator(Calculator):
    USD_RATE = 73.73
    EURO_RATE = 87.86
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency):
        wasted_cash = self.get_today_stats()

        def comparison(rate, output):
            if self.limit - wasted_cash > 0:
                return (
                    'На сегодня осталось '
                    f'{round(((self.limit - wasted_cash) / rate), 2)} '
                    f'{output}'
                )
            elif self.limit - wasted_cash == 0:
                return 'Денег нет, держись'
            else:
                return (
                    'Денег нет, держись: твой долг - '
                    f'{round(-((self.limit - wasted_cash) / rate), 2)} '
                    f'{output}'
                )

        if currency == 'rub':
            return comparison(self.RUB_RATE, 'руб')
        elif currency == 'usd':
            return comparison(self.USD_RATE, 'USD')
        elif currency == 'eur':
            return comparison(self.EURO_RATE, 'Euro')
        else:
            raise ValueError('Wrong currency')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        wasted_calories = self.get_today_stats()
        if self.limit - wasted_calories > 0:
            return (
                'Сегодня можно съесть что-нибудь ещё, но с общей '
                f'калорийностью не более {self.limit - wasted_calories} кКал'
            )
        else:
            return 'Хватит есть!'
