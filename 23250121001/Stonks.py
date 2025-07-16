import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import random
import matplotlib.pyplot as plt
from datetime import datetime
import os

# === Данни ===
stocks = {}
portfolio = {"balance": 18000, "currency": "BGN", "stocks": {}}  # Начален баланс в BGN
exchange_rate = {"USD": 0.56, "EUR": 0.51, "BGN": 1.0}  # 1 BGN = X валута
price_history = {}
PORTFOLIO_FILE = "portfolio.json"
STOCKS_FILE = "stocks.json"

# === ЗАРЕЖДАНЕ НА ПОРТФЕЙЛ И АКЦИИ ===
def load_portfolio():
    global portfolio
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, "r") as f:
            portfolio.update(json.load(f))

def save_portfolio():
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(portfolio, f, indent=4)

def load_stocks():
    global stocks, price_history
    if os.path.exists(STOCKS_FILE):
        with open(STOCKS_FILE, "r") as f:
            data = json.load(f)
            stocks.update(data["stocks"])
            price_history.update({k: [(datetime.fromisoformat(t), p) for t, p in v] for k, v in data["history"].items()})

def save_stocks():
    with open(STOCKS_FILE, "w") as f:
        json.dump({
            "stocks": stocks,
            "history": {k: [(t.isoformat(), p) for t, p in v] for k, v in price_history.items()}
        }, f, indent=4)

# === АКЦИИ ===
def add_stock():
    name = simpledialog.askstring("Добавяне на акция", "Име на акцията:")
    if name:
        try:
            price = float(simpledialog.askstring("Цена", "Начална цена:"))
            stocks[name] = price
            if name not in price_history:
                price_history[name] = []
            price_history[name].append((datetime.now(), price))
            if len(price_history[name]) > 10:
                price_history[name] = price_history[name][-10:]  # запази последните 10
            update_stock_list()
            save_stocks()
        except:
            messagebox.showerror("Грешка", "Невалидна цена!")

def edit_stock():
    selection = stock_listbox.get(tk.ACTIVE)
    if selection:
        name = selection.split(' - ')[0]
        try:
            new_price = float(simpledialog.askstring("Редакция", f"Нова цена за {name}:"))
            stocks[name] = new_price
            price_history[name].append((datetime.now(), new_price))
            if len(price_history[name]) > 10:
                price_history[name] = price_history[name][-10:]  # запази последните 10
            update_stock_list()
            save_stocks()
        except:
            messagebox.showerror("Грешка", "Невалидна цена!")

def delete_stock():
    selection = stock_listbox.get(tk.ACTIVE)
    if selection:
        name = selection.split(' - ')[0]
        if name in stocks:
            del stocks[name]
            price_history.pop(name, None)
            update_stock_list()
            save_stocks()

# === ТРАНЗАКЦИИ ===
def buy_stock():
    selection = stock_listbox.get(tk.ACTIVE)
    if selection:
        name = selection.split(' - ')[0]
        if name in stocks:
            qty = simpledialog.askinteger("Купуване", f"Брой акции от {name}:")
            if qty and qty > 0:
                total = stocks[name] * qty
                if portfolio["balance"] >= total:
                    portfolio["balance"] -= total
                    portfolio["stocks"].setdefault(name, 0)
                    portfolio["stocks"][name] += qty
                    save_portfolio()
                    update_portfolio_label()
                    messagebox.showinfo("Успех", f"Купихте {qty} акции от {name}.")
                else:
                    messagebox.showerror("Грешка", "Недостатъчно средства!")

def sell_stock():
    selection = stock_listbox.get(tk.ACTIVE)
    if selection:
        name = selection.split(' - ')[0]
        if name in portfolio["stocks"]:
            qty = simpledialog.askinteger("Продаване", f"Брой акции от {name} за продажба:")
            if qty and qty > 0 and portfolio["stocks"][name] >= qty:
                total = stocks[name] * qty
                portfolio["stocks"][name] -= qty
                if portfolio["stocks"][name] == 0:
                    del portfolio["stocks"][name]
                portfolio["balance"] += total
                save_portfolio()
                update_portfolio_label()
                messagebox.showinfo("Успех", f"Продадохте {qty} акции от {name}.")
            else:
                messagebox.showerror("Грешка", "Невалидна стойност или недостатъчно акции!")

# === ОБМЕН НА ВАЛУТА ===
def convert_currency():
    currencies = ["USD", "EUR", "BGN"]
    current = portfolio["currency"]
    target = simpledialog.askstring("Обмяна", f"Избери валута (USD, EUR, BGN):")
    if target and target.upper() in currencies and target.upper() != current:
        target = target.upper()

        # Преобразуване на баланса към целевата валута
        bgn_value = portfolio["balance"] / exchange_rate[current]
        new_value = bgn_value * exchange_rate[target]
        portfolio["balance"] = round(new_value, 2)

        # Обновяване на валутата
        portfolio["currency"] = target

        # Преобразуване на всички цени на акции и ценова история
        for name in stocks:
            bgn_stock = stocks[name] / exchange_rate[current]  # към BGN
            stocks[name] = round(bgn_stock * exchange_rate[target], 2)
            new_history = []
            for time, price in price_history[name]:
                bgn_hist = price / exchange_rate[current]
                new_price = round(bgn_hist * exchange_rate[target], 2)
                new_history.append((time, new_price))
            price_history[name] = new_history

        save_portfolio()
        save_stocks()
        update_stock_list()
        update_portfolio_label()
        messagebox.showinfo("Успех", f"Обменихте към {target}.")
    else:
        messagebox.showerror("Грешка", "Невалидна или същата валута.")

# === ГРАФИКИ ===
def show_graph():
    selection = stock_listbox.get(tk.ACTIVE)
    if selection:
        name = selection.split(' - ')[0]
        if name in price_history:
            times, prices = zip(*price_history[name])
            plt.plot(times, prices, marker='o')
            plt.title(f"Цена на {name} във времето")
            plt.xlabel("Време")
            plt.ylabel(f"Цена ({portfolio['currency']})")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.grid(True)
            plt.show()
        else:
            messagebox.showinfo("Графика", f"Няма данни за {name}.")

# === ПЕЧАЛБА/ЗАГУБА ===
def show_profit():
    value = sum(stocks.get(name, 0) * qty for name, qty in portfolio["stocks"].items())
    total = portfolio["balance"] + value

    owned = "\n".join([f"{name}: {qty} бр. x {stocks.get(name, 0):.2f} = {stocks.get(name, 0) * qty:.2f} {portfolio['currency']}"
                       for name, qty in portfolio["stocks"].items()])

    messagebox.showinfo("Състояние",
                        f"Баланс: {portfolio['balance']:.2f} {portfolio['currency']}\n"
                        f"Стойност на акции: {value:.2f} {portfolio['currency']}\n"
                        f"Общо: {total:.2f} {portfolio['currency']}\n\nАкции:\n{owned if owned else 'Нямате акции.'}")

# === АКТУАЛИЗАЦИЯ ===
def update_stock_list():
    stock_listbox.delete(0, tk.END)
    for name, price in stocks.items():
        stock_listbox.insert(tk.END, f"{name} - {price:.2f} {portfolio['currency']}")

def update_portfolio_label():
    portfolio_label.config(text=f"Баланс: {portfolio['balance']:.2f} {portfolio['currency']}")

# === СИМУЛАЦИЯ НА ПРОМЯНА НА ЦЕНИ ===
def simulate_prices():
    for name in stocks:
        change = random.uniform(-5, 5)  # случайна промяна
        new_price = max(0.01, stocks[name] + change)
        stocks[name] = round(new_price, 2)
        price_history[name].append((datetime.now(), new_price))
        if len(price_history[name]) > 10:
            price_history[name] = price_history[name][-10:]  # запази последните 10
    update_stock_list()
    save_stocks()
    root.after(5000, simulate_prices)  # на всеки 5 секунди

# === ГЛАВЕН ПРОЗОРЕЦ ===
root = tk.Tk()
root.title("Симулатор на борса")

load_portfolio()
load_stocks()

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

stock_listbox = tk.Listbox(frame, width=50)
stock_listbox.grid(row=0, column=0, columnspan=5)

btn_add = tk.Button(frame, text="Добави акция", command=add_stock)
btn_edit = tk.Button(frame, text="Редактирай акция", command=edit_stock)
btn_delete = tk.Button(frame, text="Изтрий акция", command=delete_stock)

btn_buy = tk.Button(frame, text="Купи", command=buy_stock)
btn_sell = tk.Button(frame, text="Продай", command=sell_stock)
btn_graph = tk.Button(frame, text="Графика", command=show_graph)
btn_profit = tk.Button(frame, text="Портфолио", command=show_profit)
btn_convert = tk.Button(frame, text="Обмени валута", command=convert_currency)

portfolio_label = tk.Label(frame, text=f"Баланс: {portfolio['balance']:.2f} {portfolio['currency']}")
portfolio_label.grid(row=3, column=0, columnspan=5)

btn_add.grid(row=1, column=0)
btn_edit.grid(row=1, column=1)
btn_delete.grid(row=1, column=2)
btn_buy.grid(row=2, column=0)
btn_sell.grid(row=2, column=1)
btn_graph.grid(row=2, column=2)
btn_profit.grid(row=2, column=3)
btn_convert.grid(row=1, column=3)

update_stock_list()
update_portfolio_label()
simulate_prices()

root.mainloop()
