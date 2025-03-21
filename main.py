# выполнено командой питонисты
import random
print('Добро пожаловать!')
play = input('Введите имя: ') # Ввод никнейма

# Класс, представляющий персонажа (игрока или врага)
class Character:
    def __init__(self, name, hp, dmg, spec_atack, mp):
        self.name = name  # Имя персонажа
        self.hp = hp  # Здоровье
        self.dmg = dmg  # Урон от обычной атаки
        self.spec_atack = spec_atack  # Урон от специальной атаки
        self.mp = mp  # Мана (ресурс для специальной атаки)

    # Метод для обычной атаки
    def attack(self, target):
        damage = random.randint(
            self.dmg - 5, self.dmg + 5
        )  # Случайный урон в пределах dmg ± 5
        target.hp -= damage  # Нанесение урона цели
        print(f"{self.name} атакует {target.name} и наносит {damage} урона!")

    # Метод для проверки, жив ли персонаж
    def is_alive(self):
        return self.hp > 0  # Возвращает True, если здоровье больше 0


# Класс, представляющий оружие
class Weapon:
    def __init__(self, name, dmg, spec_dmg, mana_cost):
        self.name = name  # Название оружия
        self.dmg = dmg  # Урон от обычной атаки
        self.spec_dmg = spec_dmg  # Урон от специальной атаки
        self.mana_cost = mana_cost  # Стоимость маны для специальной атаки


# Класс игрока, наследующий от Character
class Player(Character):
    def __init__(self):
        super().__init__(
            name=play, hp=100, dmg=20, spec_atack=40, mp=50
        )  # Инициализация игрока
        self.weapon = None  # Оружие игрока (пока не выбрано)

    # Метод для выбора оружия
    def choose_weapon(self):
        print("\nВыберите оружие:")
        print("1. Меч (Урон: 20, Спец.атака: 40, Мана: 10)")
        print("2. Лук (Урон: 15, Спец.атака: 50, Мана: 15)")
        choice = input("Ваш выбор: ")  # Игрок выбирает оружие
        if choice == "1":
            self.weapon = Weapon(
                name="Меч", dmg=20, spec_dmg=40, mana_cost=10
            )  # Выбор меча
        elif choice == "2":
            self.weapon = Weapon(
                name="Лук", dmg=15, spec_dmg=50, mana_cost=15
            )  # Выбор лука
        else:
            print("Неверный выбор, выбран Меч по умолчанию.")
            self.weapon = Weapon(
                name="Меч", dmg=20, spec_dmg=40, mana_cost=10
            )  # Меч по умолчанию
        print(f"Вы выбрали {self.weapon.name}!")

    # Метод для специальной атаки игрока
    def special_attack(self, target):
        if self.mp >= self.weapon.mana_cost:  # Проверка, достаточно ли маны
            damage = random.randint(
                self.weapon.spec_dmg - 5, self.weapon.spec_dmg + 5
            )  # Случайный урон
            target.hp -= damage  # Нанесение урона цели
            self.mp -= self.weapon.mana_cost  # Трата маны
            print(
                f"{self.name} использует {self.weapon.name} и наносит {damage} урона специальной атакой!"
            )
        else:
            print(f"У {self.name} недостаточно маны для специальной атаки!")


# Класс врага, наследующий от Character
class Enemy(Character):
    def __init__(self, name, hp, dmg, spec_atack, mp):
        super().__init__(name, hp, dmg, spec_atack, mp)  # Инициализация врага

    # Метод для специальной атаки врага
    def special_attack(self, target):
        if self.mp >= 10:  # Враги используют фиксированную стоимость маны (10)
            damage = random.randint(
                self.spec_atack - 5, self.spec_atack + 5
            )  # Случайный урон
            target.hp -= damage  # Нанесение урона цели
            self.mp -= 10  # Трата маны
            print(f"{self.name} использует специальную атаку и наносит {damage} урона!")
        else:
            print(f"У {self.name} недостаточно маны для специальной атаки!")


# Класс Гоблина, наследующий от Enemy
class Goblin(Enemy):
    def __init__(self):
        super().__init__(
            name="Гоблин", hp=60, dmg=10, spec_atack=20, mp=30
        )  # Инициализация Гоблина


# Класс Орка, наследующий от Enemy
class Orc(Enemy):
    def __init__(self):
        super().__init__(
            name="Орк", hp=90, dmg=15, spec_atack=30, mp=40
        )  # Инициализация Орка


# Класс игры, управляющий логикой
class Game:
    def __init__(self):
        self.player = Player()  # Создание игрока
        self.enemies = [Goblin(), Orc()]  # Список врагов (Гоблин и Орк)

    # Метод для запуска игры
    def start_game(self):
        print("=== Добро пожаловать в игру! ===")
        print("Вы — герой, который должен спасти деревню от нашествия монстров.")
        print("Сначала вам предстоит сразиться с Гоблином, а затем с Орком.")
        print("Удачи!\n")

        # Цикл по всем врагам
        for i, enemy in enumerate(self.enemies, 1):
            print(f"\n=== Сражение {i}: {self.player.name} против {enemy.name} ===")
            self.player.choose_weapon()  # Игрок выбирает оружие
            while (
                self.player.is_alive() and enemy.is_alive()
            ):  # Бой продолжается, пока оба живы
                self.show_status(enemy)  # Показ статуса
                self.player_turn(enemy)  # Ход игрока
                if enemy.is_alive():  # Если враг жив, он атакует
                    self.enemy_turn(enemy)
                else:
                    print(f"{enemy.name} побежден!")  # Враг побежден
            if not self.player.is_alive():  # Если игрок погиб
                print(f"{self.player.name} погиб в сражении {i}.")
                break
            else:
                print(f"{self.player.name} побеждает в сражении {i}!")
                if i < len(
                    self.enemies
                ):  # Если это не последний враг, восстановление здоровья и маны
                    self.player.hp = 100
                    self.player.mp = 50
                    print(
                        f"{self.player.name} восстанавливает здоровье и ману перед следующим сражением!"
                    )

        # Итог игры
        if self.player.is_alive():
            print("\n=== Победа! ===")
            print("Вы победили всех монстров и спасли деревню!")
            print("Жители деревни благодарны вам. Вы — настоящий герой!")
        else:
            print("\n=== Поражение ===")
            print("Вы погибли в бою. Деревня осталась без защиты...")

    # Метод для отображения статуса игрока и врага
    def show_status(self, enemy):
        print(f"\n{self.player.name}: {self.player.hp} HP, {self.player.mp} MP")
        print(f"{enemy.name}: {enemy.hp} HP, {enemy.mp} MP")

    # Метод для хода игрока
    def player_turn(self, enemy):
        print("\nВыберите действие:")
        print("1. Обычная атака")
        print("2. Специальная атака")
        choice = input("Ваш выбор: ")  # Игрок выбирает действие
        if choice == "1":
            self.player.attack(enemy)  # Обычная атака
        elif choice == "2":
            self.player.special_attack(enemy)  # Специальная атака
        else:
            print("Неверный выбор, пропускаем ход.")  # Неправильный ввод

    # Метод для хода врага
    def enemy_turn(self, enemy):
        enemy_choice = random.choice(
            ["attack", "special"]
        )  # Враг случайно выбирает действие
        if enemy_choice == "attack":
            enemy.attack(self.player)  # Обычная атака
        else:
            enemy.special_attack(self.player)  # Специальная атака


# Запуск игры
game = Game()
game.start_game()
