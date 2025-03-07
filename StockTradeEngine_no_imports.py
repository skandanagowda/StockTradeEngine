import time
import random

stop_flag = False

tickets = 1024
ticketerName = ["T_" + str(i) for i in range(tickets)]  

class Order:
    def __init__(self, orderType, ticketer, quant, price):
        self.orderType = orderType
        self.ticketer = ticketer
        self.quant = quant
        self.price = price

class TicketerBook:
    def __init__(self):
        self.sell_orders = [] 
        self.buy_orders = []   

t_Book = [TicketerBook() for _ in range(tickets)]

def add_order(orderType, ticketer, quant, price):
    t_ind = int(ticketer.split('_')[1])
    order = Order(orderType, t_ind, quant, price)
    book = t_Book[t_ind]
    
    if orderType == 'Buy':
        insert_order_sorted(book.buy_orders, order, is_buy=True)
        print(f"Added Buy order: {quant} shares of {ticketer} at ${price}")
    else:
        insert_order_sorted(book.sell_orders, order, is_buy=False)
        print(f"Added Sell order: {quant} shares of {ticketer} at ${price}")

    match_order(t_ind)

def insert_order_sorted(order_list, order, is_buy):
    index = 0
    if is_buy:
        while index < len(order_list) and order_list[index].price >= order.price:
            index += 1
    else:
        while index < len(order_list) and order_list[index].price <= order.price:
            index += 1
    order_list.insert(index, order)

def match_order(ticketer):
    book = t_Book[ticketer]
    sell_orders = book.sell_orders
    buy_orders = book.buy_orders

    i, j = 0, 0
    while i < len(buy_orders) and j < len(sell_orders):
        buy_order = buy_orders[i]
        sell_order = sell_orders[j]

        if buy_order.price >= sell_order.price:
            trade_quant = min(sell_order.quant, buy_order.quant)
            print(f"Trade executed for {trade_quant} shares of {ticketerName[ticketer]} at ${sell_order.price}")
            
            buy_order.quant -= trade_quant
            sell_order.quant -= trade_quant

            if sell_order.quant == 0:
                print(f"Sell order of {ticketerName[ticketer]} fully matched and removed.")
                sell_orders.pop(j)
            else:
                j += 1  

            if buy_order.quant == 0:
                print(f"Buy order of {ticketerName[ticketer]} fully matched and removed.")
                buy_orders.pop(i)
            else:
                i += 1  
        else:
            break  


def random_order_simulator():
    orderType = random.choice(['Buy', 'Sell'])
    ticketer = random.randint(0, tickets - 1)
    ticketer_Name = ticketerName[ticketer]
    quant = random.randint(1, 1000)
    price = random.uniform(10, 500)

    print(f"Simulating order: {orderType} for {quant} shares of {ticketer_Name} at ${price}")
    add_order(orderType, ticketer_Name, quant, price)


def simulate_orders():
    for _ in range(100):  
        random_order_simulator()
        time.sleep(random.uniform(0.01, 0.1))

    print("Simulation complete.")


simulate_orders()

print("All threads stopped.")
