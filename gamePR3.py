class Product:
    def __init__(self, name="", price=0, weight=1, freshness=100, country="Russia"):
        self._name = name  # Название
        self._price = price  # Цена за кг
        self._weight = weight  # Вес
        self._freshness = freshness  # Свежесть
        self._country = country  # Страна происхождения

    def get_name(self): return self._name
    def get_price(self): return self._price
    def get_weight(self): return self._weight
    def get_freshness(self): return self._freshness
    def get_country(self): return self._country

    def set_name(self, name): self._name = name  # Меняет имя
    def set_price(self, price): self._price = max(0, price)  # Меняет цену не меньше 0
    def set_weight(self, weight): self._weight = max(0.1, weight)  # Устанавливает вес не меньше 0.1 кг
    def set_freshness(self, fresh): self._freshness = max(0, min(100, fresh))  # Устанавливает свежесть в диапазоне 0–100%

    def calculate_cost(self): return self._price * self._weight  # стоимость: цена на вес
    def is_fresh(self): return self._freshness > 50  # Проверка на свежесть


class Fruit(Product):
    def __init__(self, name="", price=0, weight=1, sweetness=5):
        super().__init__(name, price, weight)
        self._sweetness = sweetness

    def get_sweetness(self): return self._sweetness
    def calculate_cost(self): return super().calculate_cost() * (0.8 if self._sweetness > 7 else 1)


class Vegetable(Product):
    def __init__(self, name="", price=0, weight=1, organic=False):
        super().__init__(name, price, weight)
        self._organic = organic

    def get_organic(self): return self._organic
    def calculate_cost(self): return super().calculate_cost() * (1.3 if self._organic else 1)  # Переопределяем метод расчёта стоимости


class Store:
    def __init__(self):
        self._balance = 1500  # Первоначальный баланс
        self._products = []  # Список продуктов
        self._day = 1  # День
        self._action_count = 0  # Счётчик действий
        self._supply_enabled = False  # Флаг включения поставок
        self._supply_cost = 100  # Начальная стоимость поставки

    def get_balance(self): return self._balance
    def get_products(self): return self._products
    def get_day(self): return self._day
    def get_action_count(self): return self._action_count

    def add_product(self, product):
        self._products.append(product)

    def sell_product(self, idx):
        if 0 <= idx < len(self._products):
            product = self._products.pop(idx)
            self._balance += product.calculate_cost()
            self._action_count += 1  # Увеличиваем счётчик при продаже
            return True
        return False  # Если товара нет, возвращаем False

    def next_day(self):
        for p in self._products:
            p.set_freshness(p.get_freshness() - 10)  # Уменьшаем свежесть всех товаров на 10%
        self._day += 1  # Переход на следующий день
        self._action_count = 0  # Обнуляем счётчик в начале нового дня
        self._supply_cost = max(100, self._supply_cost - 100)  # Обновляем стоимость поставки

    def reset_action_count(self):
        self._action_count = 0

    def toggle_supply(self):
        self._supply_enabled = not self._supply_enabled
        if self._supply_enabled:
            print("Поставки включены!")
        else:
            print("Поставки отключены!")
            self._supply_cost = 100  # Сброс стоимости при отключении

    def automatic_supply(self):
        if self._supply_enabled:
            if self._balance >= self._supply_cost:
                # Добавляем новые товары по половинной цене
                new_products = [
                    Fruit("Бананы", 25, 3, 8),  # Обычная цена 50
                    Vegetable("Помидоры", 30, 2, True)  # Обычная цена 60
                ]
                
                for product in new_products:
                    self._products.append(product)
                
                self._balance -= self._supply_cost
                print(f"Поставка выполнена! Стоимость следующей: {self._supply_cost} руб")
            else:
                print("Недостаточно средств для поставки!")
        else:
            print("Поставки отключены!")

def play_game():
    store = Store()
    store.add_product(Fruit("Яблоки", 80, 2, 6))
    store.add_product(Vegetable("Морковь", 40, 3, True))

    print("МАГАЗИН ОВОЩЕЙ И ФРУКТОВ!\nВы 27 летний Тарас, который мечтает стать великим продовцом!")
    print("Цель: 2000 руб за 7 дней\n")

    while store.get_day() <= 7 and store.get_balance() < 2000:
        print(f"--- День {store.get_day()} ---")
        print(f"Баланс: {store.get_balance()} руб")
        print(f"Действий сегодня: {store.get_action_count()}/5")
        print(f"Стоимость следующей поставки: {store._supply_cost} руб")

        # Показываем все товары в магазине
        for i in range(len(store.get_products())):
            p = store.get_products()[i]
            print(f"{i+1}. {p.get_name()} - {p.calculate_cost()} руб (свежесть: {p.get_freshness()}%)")

        choice = input("\n1‑Продать\n2‑Купить\n3‑Следующий день\n4‑Управление поставками\nВы выбираете: ")

        if choice == "1" and store.get_products():
            idx = int(input("Номер продукта: ")) - 1
            if store.sell_product(idx):
                print("Продано!")
            else:
                print("Ошибка")

            # Проверяем счётчик после продажи
            if store.get_action_count() >= 5:
                print("\n5 действий выполнено — наступает следующий день!")
                store.next_day()

        elif choice == "2" and store.get_balance() >= 100:
            prod_choice = input("\n1‑Бананы (90 руб)\n2‑Помидоры (120 руб)\nВы выбираете: ")
            if prod_choice == "1":
                new_prod = Fruit("Бананы", 50, 3, 8)
                cost = 90
            else:
                new_prod = Vegetable("Помидоры", 60, 2, True)
                cost = 120

            store.add_product(new_prod)
            store._balance -= cost
            store._action_count += 1  # Увеличиваем счётчик при покупке
            print("Куплено!")

            # Проверяем счётчик после покупки
            if store.get_action_count() >= 5:
                print("\n5 действий выполнено — наступает следующий день!")
                store.next_day()

        elif choice == "3":
            store.next_day()
            print("Перешли на следующий день.")

        elif choice == "4":
            supply_choice = input("\n1‑Включить/выключить поставки\n2‑Выполнить поставку: ")
            if supply_choice == "1":
                store.toggle_supply()
            elif supply_choice == "2":
                store.automatic_supply()

        else:
            print("Неверный ввод")

        # Автоматическая поставка в конце дня
        if store._supply_enabled:
            store.automatic_supply()
    print(f"\n{'ПОБЕДА!' if store.get_balance() >= 2000 else 'Ваш магазин обонкротился'}")
    print(f"Баланс: {store.get_balance()} руб")
    print(f"День: {store.get_day()}")


if __name__ == "__main__":
    play_game()