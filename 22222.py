import random

class Rival:
    def __init__(self):
        self._life = 50           # приватный атрибут
        self._lifeThanos = 150     # приватный атрибут
        self._weapon = None      # приватный атрибут
        self._armor = None       # приватный атрибут
        self._weapon_bonus = 0   # приватный атрибут

    # ГЕТТЕРЫ 
    def get_life(self):
        #Получить текущее здоровье игрока
        return self._life

    def get_thanos_life(self):
        #Получить текущее здоровье Таноса
        return self._lifeThanos

    def get_weapon(self):
        #Получить" текущее оружие 
        return self._weapon

    def get_armor(self):
        #Получить текущую броню 
        return self._armor

    def get_weapon_bonus(self):
        #Получить бонус от оружия 
        return self._weapon_bonus

    # СЕТТЕРЫ 
    def set_life(self, value):
        #Установить здоровье игрока 
        if value < 0:
            self._life = 0
            print("Ваше здоровье опустилось до 0!")
        else:
            self._life = value

    def set_thanos_life(self, value):
        #Установить здоровье Таноса 
        if value < 0:
            self._lifeThanos = 0
        else:
            self._lifeThanos = value

    def set_weapon(self, weapon_name):
        #Установить оружие 
        self._weapon = weapon_name
        self._weapon_bonus = 0  # сброс бонуса при смене оружия
        print(f"Вы взяли в руки {weapon_name}.")

    def set_armor(self, armor_name):
        #Установить броню 
        self._armor = armor_name
        print(f"Вы надели {armor_name}.")

    def set_weapon_bonus(self, bonus):
        #Установить бонус от оружия 
        if bonus < 0:
            print("Бонус от оружия не может быть отрицательным!")
            return
        self._weapon_bonus = bonus

    # Основные методы 
    def attack(self):
        damage = random.randint(1, 3) + self.get_weapon_bonus()
        self.set_thanos_life(self.get_thanos_life() - damage)
        print(f"Вы нанесли {damage} урона! (оружие: {self.get_weapon() or 'нет'})")
        return damage

    def thanos_attack(self):
        if self.get_thanos_life() > 15:
            damage = random.randint(1, 3)
            self.set_life(self.get_life() - damage)
            print(f"Танос атаковал вас и нанес {damage} урона!")
            return damage
        else:
            heal = random.randint(1, 10)
            self.set_thanos_life(self.get_thanos_life() + heal)
            print(f"Танос съел еду и восстановил {heal} HP!")
            return 0

    def equip_weapon(self, weapon_name, damage_bonus):
        self.set_weapon(weapon_name)
        self.set_weapon_bonus(damage_bonus)
        print(f" (+{damage_bonus} к урону)!")

    def eat_food(self):
        heal = random.randint(1, 5)
        self.set_life(self.get_life() + heal)
        print(f"Вы поели и восстановили {heal} HP!")

    def check_status(self):
        print("\n=== СТАТУС ===")
        print(f"Ваше здоровье: {self.get_life()}")
        print(f"Здоровье Таноса: {self.get_thanos_life()}")
        print(f"Оружие: {self.get_weapon() or 'нет'}")
        print(f"Броня: {self.get_armor() or 'нет'}")
        if self.get_weapon():
            print(f"Бонус от оружия: +{self.get_weapon_bonus()} к урону")
        print("=============")

    def is_alive(self):
        return self.get_life() > 0

    def is_thanos_alive(self):
        return self.get_thanos_life() > 0



# Основной код 
player = Rival()

print("Добро пожаловать в битву с Таносом!")
player.check_status()

def show_menu():
    print("\nДоступные команды:")
    print("1 — атаковать")
    print("2 — взять нож (+1 к урону)")
    print("3 — поесть (восстанавливает 1–5 HP)")
    print("4 — проверить статус")
    print("0 — выйти")

while player.is_thanos_alive() and player.is_alive():
    show_menu()
    choice = input("\nВаш выбор: ").strip()

    if choice == "1":
        player.attack()
        if player.is_thanos_alive():
            player.thanos_attack()

    elif choice == "2":
        player.equip_weapon("нож", 1)
        if player.is_thanos_alive():
            player.thanos_attack()

    elif choice == "3":
        player.eat_food()
        if player.is_thanos_alive():
            player.thanos_attack()

    elif choice == "4":
        player.check_status()

    elif choice == "0":
        print("Вы покинули битву.")
        break

    else:
        print("Неверный выбор. Введите 1, 2, 3, 4 или 0.")

if not player.is_alive():
    print("\nВы проиграли! Танос победил.")
    player.check_status()
elif not player.is_thanos_alive():
    print("\nПоздравляем! Вы победили Таноса!")
    player.check_status()
