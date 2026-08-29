# -*- coding: utf-8 -*-
import random
import time
import json
import os
from colorama import init, Fore, Back, Style

init(autoreset=True)

SAVE_FILE = "save.json"

class Player:
    def __init__(self, name, edition="standard", uniform="civil"):
        self.name = name
        self.edition = edition
        self.uniform = uniform
        self.max_hp = 100
        self.hp = 100
        self.rub = self.get_start_money()
        self.usd = 0
        self.eur = 0
        self.weapon = "Кулаки" if edition == "zero_to_hero" else "ПМ"
        self.damage = 2 if edition == "zero_to_hero" else 10
        self.armor = "Нет" if edition == "zero_to_hero" else "Бронежилет 3 класса"
        self.armor_def = 0 if edition == "zero_to_hero" else 5
        self.inventory = []
        self.quests = []
        self.completed_quests = []
        self.boss_kills = []

    def get_start_money(self):
        if self.edition == "unheard":
            return 50000
        elif self.edition == "zero_to_hero":
            return 0
        else:
            return 5000

    def is_alive(self):
        return self.hp > 0

    def show_status(self):
        hp_color = Fore.GREEN if self.hp > 50 else (Fore.YELLOW if self.hp > 25 else Fore.RED)
        print("\n" + Back.BLACK + Fore.CYAN + "=" * 50)
        print(Fore.YELLOW + Style.BRIGHT + f"  БОЕЦ: {self.name} [{self.edition.upper()}]")
        print(Fore.WHITE + f"  Форма: {self.uniform}")
        print(hp_color + f"  Здоровье: {self.hp}/{self.max_hp}")
        print(Fore.GREEN + f"  Деньги: {self.rub} ₽ | {self.usd} $ | {self.eur} €")
        print(Fore.MAGENTA + f"  Оружие: {self.weapon} (урон: {self.damage})")
        print(Fore.BLUE + f"  Броня: {self.armor} (защита: {self.armor_def})")
        inv = ", ".join(self.inventory) if self.inventory else "пусто"
        print(Fore.WHITE + f"  Инвентарь: {inv}")
        if self.quests:
            print(Fore.CYAN + f"  Активные квесты: {', '.join(self.quests)}")
        if self.boss_kills:
            print(Fore.MAGENTA + f"  Убитые боссы: {', '.join(self.boss_kills)}")
        print(Fore.CYAN + "=" * 50)

    def to_dict(self):
        return {
            "name": self.name,
            "edition": self.edition,
            "uniform": self.uniform,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "rub": self.rub,
            "usd": self.usd,
            "eur": self.eur,
            "weapon": self.weapon,
            "damage": self.damage,
            "armor": self.armor,
            "armor_def": self.armor_def,
            "inventory": self.inventory,
            "quests": self.quests,
            "completed_quests": self.completed_quests,
            "boss_kills": self.boss_kills,
        }

    @classmethod
    def from_dict(cls, data):
        p = cls(data["name"], data["edition"], data.get("uniform", "civil"))
        p.max_hp = data["max_hp"]
        p.hp = data["hp"]
        p.rub = data.get("rub", data.get("money", 0))
        p.usd = data.get("usd", 0)
        p.eur = data.get("eur", 0)
        p.weapon = data["weapon"]
        p.damage = data["damage"]
        p.armor = data["armor"]
        p.armor_def = data["armor_def"]
        p.inventory = data["inventory"]
        p.quests = data["quests"]
        p.completed_quests = data["completed_quests"]
        p.boss_kills = data.get("boss_kills", [])
        return p

class Enemy:
    def __init__(self, name, hp, damage, reward, is_boss=False):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.reward = reward
        self.is_boss = is_boss

def save_game(player):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(player.to_dict(), f, ensure_ascii=False, indent=4)
    print(Fore.GREEN + "💾 Игра сохранена.")

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Player.from_dict(data)
    return None

def slow_print(text, delay=0.02, color=Fore.WHITE):
    for char in text:
        print(color + char, end='', flush=True)
        time.sleep(delay)
    print()

def fight(player, enemy):
    if enemy.is_boss:
        slow_print(f"\n👑 БОСС: {enemy.name}!", 0.03, Fore.RED)
    else:
        slow_print(f"\n⚔️ В бой вступает {enemy.name}!", 0.02, Fore.YELLOW)
    
    while enemy.hp > 0 and player.is_alive():
        print(Fore.RED + f"\nПротивник: {enemy.name} | HP: {enemy.hp}")
        print(Fore.GREEN + f"Ты: {player.hp} HP")
        print(Fore.WHITE + "1. Атаковать")
        print(Fore.WHITE + "2. Сбежать")
        choice = input("> ")
        
        if choice == "1":
            dmg = random.randint(1, player.damage)
            enemy.hp -= dmg
            print(Fore.CYAN + f"Ты наносишь {dmg} урона!")
            if enemy.hp <= 0:
                print(Fore.GREEN + f"✅ {enemy.name} повержен!")
                player.rub += enemy.reward
                print(Fore.YELLOW + f"💰 Получено: {enemy.reward} ₽")
                if enemy.is_boss:
                    if enemy.name not in player.boss_kills:
                        player.boss_kills.append(enemy.name)
                    print(Fore.MAGENTA + f"🏆 Босс {enemy.name} записан в трофеи!")
                if enemy.name == "Коллонтай":
                    if "АГС-30" not in player.inventory:
                        player.inventory.append("АГС-30")
                        print(Fore.MAGENTA + "🎁 Ты нашёл АГС-30!")
                return True
            enemy_dmg = max(1, random.randint(1, enemy.damage) - player.armor_def)
            player.hp -= enemy_dmg
            print(Fore.RED + f"Враг бьёт в ответ: -{enemy_dmg} HP")
        elif choice == "2":
            if random.random() < 0.5:
                print(Fore.GREEN + "🏃 Ты сбежал!")
                return True
            else:
                print(Fore.RED + "❌ Не получилось сбежать!")
                enemy_dmg = max(1, random.randint(1, enemy.damage) - player.armor_def)
                player.hp -= enemy_dmg
                print(Fore.RED + f"Враг бьёт: -{enemy_dmg} HP")
    
    return player.is_alive()

def loot(player):
    items = [
        ("Банка тушёнки", 500, "rub"),
        ("Аптечка", 800, "rub"),
        ("Патроны", 300, "rub"),
        ("Золотая цепочка", 2000, "rub"),
        ("Армейский жгут", 600, "rub"),
        ("Доллары", 200, "usd"),
        ("Евро", 150, "eur"),
    ]
    item, value, currency = random.choice(items)
    player.inventory.append(item)
    if currency == "rub":
        player.rub += value
    elif currency == "usd":
        player.usd += value
    elif currency == "eur":
        player.eur += value
    print(Fore.GREEN + f"🎒 Ты нашёл: {item} (+{value} {currency.upper()})")

def trade(player, trader):
    if trader == "Прапор":
        print(Fore.YELLOW + "\n🛒 Прапор:")
        print(Fore.WHITE + "1. АК-74 (3000 ₽) — урон 25")
        print(Fore.WHITE + "2. Бронежилет 5 класса (5000 ₽) — защита 15")
        print(Fore.WHITE + "3. Письмо на КПП (50000 ₽) — открывает Терминал")
        print(Fore.WHITE + "4. M4A1 SOPMOD (8000 ₽) — урон 35")
    elif trader == "Терапевт":
        print(Fore.GREEN + "\n🛒 Терапевт:")
        print(Fore.WHITE + "1. Аптечка (500 ₽) — +30 HP")
        print(Fore.WHITE + "2. Хирургический набор (1500 ₽) — +60 HP")
    elif trader == "Лыжник":
        print(Fore.MAGENTA + "\n🛒 Лыжник:")
        print(Fore.WHITE + "1. MP5 (2500 ₽) — урон 20")
        print(Fore.WHITE + "2. Бронежилет 4 класса (4000 ₽) — защита 10")
        print(Fore.WHITE + "3. АК-12 Зенитка (6000 ₽) — урон 30")
        print(Fore.WHITE + "4. ССГ-08 (7000 ₽) — урон 40")
    
    choice = input("> ")
    
    if trader == "Прапор":
        if choice == "1" and player.rub >= 3000:
            player.rub -= 3000
            player.weapon = "АК-74"
            player.damage = 25
        elif choice == "2" and player.rub >= 5000:
            player.rub -= 5000
            player.armor = "Бронежилет 5 класса"
            player.armor_def = 15
        elif choice == "3" and player.rub >= 50000:
            player.rub -= 50000
            player.inventory.append("Письмо на КПП")
            print(Fore.GREEN + "✅ Ты купил письмо на КПП!")
        elif choice == "4" and player.rub >= 8000:
            player.rub -= 8000
            player.weapon = "M4A1 SOPMOD"
            player.damage = 35
    elif trader == "Терапевт":
        if choice == "1" and player.rub >= 500:
            player.rub -= 500
            player.hp = min(player.max_hp, player.hp + 30)
        elif choice == "2" and player.rub >= 1500:
            player.rub -= 1500
            player.hp = min(player.max_hp, player.hp + 60)
    elif trader == "Лыжник":
        if choice == "1" and player.rub >= 2500:
            player.rub -= 2500
            player.weapon = "MP5"
            player.damage = 20
        elif choice == "2" and player.rub >= 4000:
            player.rub -= 4000
            player.armor = "Бронежилет 4 класса"
            player.armor_def = 10
        elif choice == "3" and player.rub >= 6000:
            player.rub -= 6000
            player.weapon = "АК-12 Зенитка"
            player.damage = 30
        elif choice == "4" and player.rub >= 7000:
            player.rub -= 7000
            player.weapon = "ССГ-08"
            player.damage = 40

def give_quest(player):
    quests = [
        ("Найти АГС-30 на Эпицентре", "АГС-30"),
        ("Убить Тагиллу", None),
        ("Найти жгут", "Армейский жгут"),
        ("Дойти до Ледокола", "Ледокол"),
    ]
    quest, item = random.choice(quests)
    if quest not in player.quests:
        player.quests.append(quest)
        print(Fore.CYAN + f"📜 Новый квест: {quest}")

def turn_in_quests(player):
    print(Fore.CYAN + "\n📜 Твои квесты:")
    if not player.quests:
        print(Fore.WHITE + "Нет активных квестов.")
        return
    
    for idx, q in enumerate(player.quests, 1):
        status = ""
        if "АГС-30" in q and "АГС-30" in player.inventory:
            status = Fore.GREEN + " [ГОТОВО]"
        elif "Армейский жгут" in q and "Армейский жгут" in player.inventory:
            status = Fore.GREEN + " [ГОТОВО]"
        elif "Тагилла" in q and any("Тагилла" in b for b in player.boss_kills):
            status = Fore.GREEN + " [ГОТОВО]"
        elif "Ледокол" in q and "Ледокол" in player.completed_quests:
            status = Fore.GREEN + " [ГОТОВО]"
        print(Fore.WHITE + f"{idx}. {q}{status}")
    
    print(Fore.WHITE + "0. Назад")
    choice = input("> ")
    
    if choice == "0":
        return
    
    try:
        idx = int(choice) - 1
        quest = player.quests[idx]
    except:
        print(Fore.RED + "Неверный выбор.")
        return
    
    if "АГС-30" in quest and "АГС-30" in player.inventory:
        player.quests.remove(quest)
        player.completed_quests.append(quest)
        player.rub += 10000
        print(Fore.GREEN + "✅ Квест сдан: АГС-30! +10000 ₽")
    elif "Армейский жгут" in quest and "Армейский жгут" in player.inventory:
        player.quests.remove(quest)
        player.completed_quests.append(quest)
        player.rub += 3000
        print(Fore.GREEN + "✅ Квест сдан: Жгут! +3000 ₽")
    elif "Тагилла" in quest and any("Тагилла" in b for b in player.boss_kills):
        player.quests.remove(quest)
        player.completed_quests.append(quest)
        player.rub += 20000
        print(Fore.GREEN + "✅ Квест сдан: Убить Тагиллу! +20000 ₽")
    elif "Ледокол" in quest and "Ледокол" in player.completed_quests:
        player.quests.remove(quest)
        player.completed_quests.append(quest)
        player.rub += 15000
        print(Fore.GREEN + "✅ Квест сдан: Ледокол! +15000 ₽")
    else:
        print(Fore.RED + "Квест ещё не выполнен!")

def select_uniform():
    print(Fore.CYAN + "\nВыбери форму:")
    print(Fore.WHITE + "1. ВСРФ")
    print(Fore.WHITE + "2. Тарковский МВД")
    print(Fore.WHITE + "3. Гражданская")
    print(Fore.WHITE + "4. Black Division")
    choice = input("> ")
    uniforms = {"1": "ВСРФ", "2": "Тарковский МВД", "3": "Гражданская", "4": "Black Division"}
    return uniforms.get(choice, "Гражданская")

def main():
    slow_print("\nДобро пожаловать в Норвинск...", 0.02, Fore.CYAN)
    
    print(Fore.YELLOW + "\nВыбери издание:")
    print(Fore.WHITE + "1. Standard (5000 ₽, ПМ, броня 3 класса)")
    print(Fore.MAGENTA + "2. Unheard (50000 ₽, АК-74, броня 5 класса)")
    print(Fore.RED + "3. Zero to Hero (0 ₽, кулаки, без брони)")
    
    edition_choice = input("> ")
    if edition_choice == "1":
        edition = "standard"
    elif edition_choice == "2":
        edition = "unheard"
    else:
        edition = "zero_to_hero"
    
    uniform = select_uniform()
    
    name = input(Fore.WHITE + "Назови позывной: ")
    player = Player(name, edition, uniform)
    
    if os.path.exists(SAVE_FILE):
        load_choice = input(Fore.YELLOW + "Найдено сохранение. Загрузить? (y/n): ")
        if load_choice.lower() == "y":
            player = load_game()
            if player:
                print(Fore.GREEN + "✅ Сохранение загружено!")

    while player.is_alive():
        player.show_status()
        print(Fore.CYAN + "\n📍 Локации:")
        print(Fore.WHITE + "1. Завод (Тагилла)")
        print(Fore.WHITE + "2. Эпицентр (редкий босс Коллонтай)")
        print(Fore.WHITE + "3. Таможня (Knight, Big Pipe)")
        print(Fore.WHITE + "4. Лес")
        print(Fore.WHITE + "5. Лаборатория (нужен жгут)")
        print(Fore.WHITE + "6. Терминал (нужно письмо на КПП)")
        print(Fore.WHITE + "7. Ледокол (квест)")
        print(Fore.WHITE + "8. Торговцы")
        print(Fore.WHITE + "9. Взять квест")
        print(Fore.WHITE + "10. Сдать квесты")
        print(Fore.GREEN + "11. Сохранить игру")
        print(Fore.RED + "12. Выйти")
        
        choice = input("> ")
        
        if choice == "1":
            if random.random() < 0.3:
                enemy = Enemy("Тагилла", 80, 25, 7000, is_boss=True)
                if not fight(player, enemy):
                    print(Fore.RED + "💀 Тагилла забил тебя кувалдой...")
                    break
            else:
                enemy = Enemy("Дикий", 20, 8, 300)
                if fight(player, enemy):
                    loot(player)
        elif choice == "2":
            if random.random() < 0.2:
                enemy = Enemy("Коллонтай", 70, 20, 6000, is_boss=True)
                if not fight(player, enemy):
                    print(Fore.RED + "💀 Коллонтай расстрелял тебя...")
                    break
            else:
                enemy = random.choice([
                    Enemy("Рейдер", 30, 12, 700),
                    Enemy("Снайпер", 25, 15, 500),
                    Enemy("Мародёр", 18, 7, 300),
                    Enemy("Дикий с дробовиком", 22, 10, 400),
                    Enemy("Пулемётчик", 40, 18, 1200),
                    Enemy("Гранатомётчик", 35, 25, 1500),
                    Enemy("Сектант", 20, 10, 500),
                ])
                if fight(player, enemy):
                    loot(player)
        elif choice == "3":
            enemy = random.choice([Enemy("Knight", 60, 22, 5500, is_boss=True), Enemy("Big Pipe", 65, 24, 6000, is_boss=True)])
            if not fight(player, enemy):
                print(Fore.RED + "💀 Босс отправил тебя в меню...")
                break
        elif choice == "4":
            enemy = Enemy("Снайпер", 25, 15, 500)
            if fight(player, enemy):
                loot(player)
        elif choice == "5":
            if "Армейский жгут" in player.inventory:
                print(Fore.CYAN + "Ты вошёл в Лабораторию...")
                enemy = Enemy("Охранник", 35, 15, 800)
                if fight(player, enemy):
                    loot(player)
            else:
                print(Fore.RED + "Нужен армейский жгут!")
        elif choice == "6":
            if "Письмо на КПП" in player.inventory:
                print(Fore.CYAN + "Ты на Терминале...")
                enemy = Enemy("Рейдер", 30, 12, 700)
                if fight(player, enemy):
                    loot(player)
            else:
                print(Fore.RED + "Нужно письмо на КПП (купи у Прапора).")
        elif choice == "7":
            print(Fore.CYAN + "Ты доходишь до Ледокола...")
            player.completed_quests.append("Ледокол")
            print(Fore.GREEN + "✅ Ты достиг Ледокола!")
        elif choice == "8":
            print(Fore.CYAN + "\nТорговцы:")
            print(Fore.WHITE + "1. Прапор")
            print(Fore.WHITE + "2. Терапевт")
            print(Fore.WHITE + "3. Лыжник")
            trader = input("> ")
            if trader == "1":
                trade(player, "Прапор")
            elif trader == "2":
                trade(player, "Терапевт")
            elif trader == "3":
                trade(player, "Лыжник")
        elif choice == "9":
            give_quest(player)
        elif choice == "10":
            turn_in_quests(player)
        elif choice == "11":
            save_game(player)
        elif choice == "12":
            save_game(player)
            print(Fore.GREEN + "Ты вышел из города. Игра сохранена.")
            break

if __name__ == "__main__":
    main()