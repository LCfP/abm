"""In this file, we define general functions for the benchmark stock market model"""

import copy
import numpy as np

__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'


def transaction(buyer, seller, stock, amount_of_product, amount_of_money, record=False, recordInfo={}):
    """This function makes a buyer and seller agent perform a transaction with each other"""
    # TODO Do a proper test before transaction is done. This implementation is very rigid.
    seller.sell(stock, amount_of_product, amount_of_money)
    buyer.buy(stock, amount_of_product, amount_of_money)
    # record the transaction
    if record:
        cur = recordInfo['cur']
        cur.execute("INSERT OR IGNORE INTO Objects (object_name, object_type) VALUES (?,?)",
                    (repr(buyer), repr(buyer)[:repr(buyer).find('_')]))
        cur.execute("SELECT id FROM Objects WHERE object_name = ?", (repr(buyer),))
        buyer_id = cur.fetchone()[0]

        cur.execute("INSERT OR IGNORE INTO Objects (object_name, object_type) VALUES (?,?)",
                    (repr(seller), repr(seller)[:repr(seller).find('_')]))
        cur.execute("SELECT id FROM Objects WHERE object_name = ?", (repr(seller),))
        seller_id = cur.fetchone()[0]

        cur.execute("INSERT OR IGNORE INTO Objects (object_name, object_type) VALUES (?,?)",
                    (repr(stock), repr(stock)[:repr(stock).find('_')]))
        cur.execute("SELECT id FROM Objects WHERE object_name = ?", (repr(stock),))
        stock_id = cur.fetchone()[0]

        cur.execute("INSERT INTO Transactions (experiment_id, seed, period, amount_of_product, "
                    "amount_of_money) VALUES (?,?,?,?,?)",
                    (recordInfo['experiment_id'], recordInfo['seed'], recordInfo['period'],
                     amount_of_product, amount_of_money))
        cur.execute("SELECT MAX(id) FROM Transactions")
        transaction_id = cur.fetchone()[0]

        cur.execute("INSERT OR IGNORE INTO Transactors (transaction_id, transactor_id, role) VALUES (?,?,?)",
                    (transaction_id, buyer_id, 'buyer'))
        cur.execute("INSERT OR IGNORE INTO Transactors (transaction_id, transactor_id, role) VALUES (?,?,?)",
                    (transaction_id, seller_id, 'seller'))
        cur.execute("INSERT OR IGNORE INTO Transactors (transaction_id, transactor_id, role) VALUES (?,?,?)",
                    (transaction_id, stock_id, 'stock'))


def npv_growing_perpetuity(dividend, discount_rate=0.05, growth_rate=0):
    """Fill in this function to calculate NPV of a growing perpetuity"""
    if discount_rate <= growth_rate:
        raise ValueError('discount rate <= growth rate', 'dc = ' + str(discount_rate), 'gr = ' + str(growth_rate))
    return np.divide(dividend, (discount_rate - growth_rate))


def distribute_initial_stocks(stocks, agents):
    local_agents = copy.copy(agents)
    for stock in stocks:
        agent_number = len(local_agents)
        amount_each = stock.amount // agent_number
        rest = int(stock.amount % agent_number)
        for x in range(0, rest):
            local_agents[x].stocks[stock] = amount_each + 1
        for x in range(rest, agent_number):
            local_agents[x].stocks[stock] = amount_each
    return local_agents


def print_setup(agents, firms, stocks):
    for agent in agents:
        print(repr(agent) + " has $ " + str(agent.money) + "and stocks:", agent.stocks, "and memory of ",
              agent.memory_size, " finally the bid-ask spread size is ", agent.bid_ask_spread)
    for firm in firms:
        print(repr(firm) + " has a book value of " + str(firm.book_value) + " profit of ", firm.profit,
              "profit history of ", firm.profit_history, " and a divididend ratio of ", firm.dividend_rate)
    for stock in stocks:
        print(repr(stock) + ", amount " + str(stock.amount) + " links to Firm ", stock.firm)


def print_quarterly_data(agents, firms):
    print("Info on firms.")
    for firm in firms:
        firm.show()

    print("Info on agents.")
    for agent in agents:
        agent.show()