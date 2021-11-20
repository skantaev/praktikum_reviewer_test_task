import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Для названия локальной переменной правильнее использовать нижний
        # регистр, т.е. record.
        # https://www.python.org/dev/peps/pep-0008/#function-and-variable-names
        # Также выбранное имя конфликтует с именем класса Record – этого
        # желательно избегать
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                # Можно сократить, используя оператор +=
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # Выражение можно упростить: 7 > (today - record.date).days >= 0
            # https://docs.python.org/3/reference/expressions.html#comparisons
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Вместо комментария к функции лучше использовать docstring.
    # https://www.datacamp.com/community/tutorials/docstrings-python
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Необходимо использовать понятное имя переменной вместо x.
        # Как пример, calories_remained
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Для переноса предпочтительнее обернуть f-строку в скобки, чем
            # использовать обратный слэш
            # https://www.python.org/dev/peps/pep-0008/#maximum-line-length
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # else здесь занимает только лишнюю строчку кода – если уберем,
        # то логика метода не изменится.
        else:
            # Здесь лишние скобки и необходим пробел после return
            return('Хватит есть!')


class CashCalculator(Calculator):
    # Здесь нет необходимости приводить курс к типу float.
    # Python 3 сам приведет значение к этому типу при делении.
    # Если все таки нужно число с плавающей точкой, то достаточно написать
    # USD_RATE = 60.0 – так будет проще и очевиднее
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Т.к. это динамический метод (первый аргумент – это экземпляр класса self),
    # то нет необходимости передавать курсы валют как аргументы функции.
    # Получить значение можно, обратившись к атрибуту класса, т.е. self.USD_RATE
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # Структуру проверок в данном случае можно улучшить.
        # Т.к. мы высчитали cash_remained, то можно сразу вернуть значение,
        # если лимит достигнут:
        # if cash_remained == 0:
        #     return 'Денег нет, держись'
        # Далее происходит проверка на тип валюты, после которой нам
        # достаточно одного if, например:
        # if cash_remained > 0:
        #     return  f'На сегодня осталось.."
        # return 'Денег нет, держись: твой долг..."
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # По-видимому тут предполагалось использовать оператор "/=" , но
            # в нем нет необходимости, т.к. не требуется приводить целые числа
            # к типу float. И всегда очевиднее это сделать, используя float
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                # В f-строках необходимо применять только подстановку
                # переменных
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # Для переноса также предпочтительнее обернуть строку в скобки,
            # чем использовать обратный слэш.
            # И для округления лучше использовать функцию round, чем
            # форматирование, потому что целые числа будут отображаться с двумя
            # нулями
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Две строчки снизу можно удалить и логика не изменится.
    # Метод из родительского класса переопределяется, только чтобы
    # осуществить вызов этого же переопределенного метода с помощью super()
    def get_week_stats(self):
        super().get_week_stats()
