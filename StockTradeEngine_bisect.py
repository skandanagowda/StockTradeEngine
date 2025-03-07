import time
import threading
import random
import bisect

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
        self.lock = threading.Lock() 

t_Book = [TicketerBook() for _ in range(tickets)]

def AddOrder(orderType, ticketer, quant, price):
    t_ind = int(ticketer.split('_')[1])
    order = Order(orderType, t_ind, quant, price)
    book = t_Book[t_ind]

    with book.lock:
        if orderType == 'Buy':
            bisect.insort_left(book.buy_orders, (-order.price, order))
            print(f"Added Buy order: {quant} shares of {ticketer} at ${price}")
        else:
            bisect.insort_left(book.sell_orders, (order.price, order))
            print(f"Added Sell order: {quant} shares of {ticketer} at ${price}")

    matchOrder(t_ind)

def matchOrder(ticketer):
    book = t_Book[ticketer]
    sell_orders = book.sell_orders
    buy_orders = book.buy_orders

    i, j = 0, 0
    while i < len(buy_orders) and j < len(sell_orders):
        buy_price, buy_order = buy_orders[i]
        sell_price, sell_order = sell_orders[j]

        if -buy_price >= sell_price:
            trade_quant = min(sell_order.quant, buy_order.quant)
            print(f"Trade executed for {trade_quant} shares of {ticketerName[ticketer]} at ${sell_price}")
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

def randomOrderSimulator():
    global stop_flag
    while not stop_flag:
        orderType = random.choice(['Buy', 'Sell'])
        ticketer = random.randint(0, tickets - 1)
        ticketer_Name = ticketerName[ticketer]
        quant = random.randint(1, 1000)
        price = random.uniform(10, 500)

        print(f"Simulating order: {orderType} for {quant} shares of {ticketer_Name} at ${price}")
        AddOrder(orderType, ticketer_Name, quant, price)
        time.sleep(random.uniform(0.01, 0.1))


threads = []
for _ in range(10): 
    t = threading.Thread(target=randomOrderSimulator)
    t.start()
    threads.append(t)

time.sleep(1)
print("Requesting threads to stop...")
stop_flag = True

for t in threads:
    t.join()

print("All threads stopped.")

