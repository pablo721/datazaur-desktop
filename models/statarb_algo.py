import numpy as np
import pandas as pd
import ccxt


class StatArbAlgorithm:
    def __init__(self, name, params, entry_z=2, exit_z=0, stop_loss_z=4, max_drawdown=None, MA_window=False):
        self.name = name
        self.params = params
        self.holdings = dict()
        self.entry_z = entry_z
        self.stop_loss_z = stop_loss_z
        self.history = pd.DataFrame(columns=['timestamp', 'coin', 'position', 'price', 'size', 'cash', 'pnl', '% pnl'])
        self.trade_open = False
        self.ratio = 0
        self.open_prices = dict()

    # opens position (long with positive n or short with negative n)
    def open_trade(self, n, coin, price, timestamp):
        self.holdings[coin] += n
        self.open_prices[coin] = price
        self.holdings['cash'] -= abs(n) * price
        self.history.loc[len(self.history)] = [timestamp, coin, n.__round__(4), price, (abs(n)*price).__round__(2),
                                               self.holdings['cash'].__round__(2), '', '']

    # close position
    def close_trade(self, coin, price, timestamp):
        if self.holdings[coin] > 0:
            self.holdings['cash'] += self.holdings[coin] * price
            pnl = self.holdings[coin] * (price - self.open_prices[coin])
        else:
            pnl = -self.holdings[coin] * (self.open_prices[coin] - price)
            self.holdings['cash'] += self.open_prices[coin] * -self.holdings[coin] + pnl

        percent_pnl = 100 * pnl/(self.open_prices[coin] * abs(self.holdings[coin]))
        self.history.loc[len(self.history)] = [timestamp, coin, -self.holdings[coin].__round__(4), price,
                                               abs(self.holdings[coin]*price).__round__(2), self.holdings['cash'].__round__(2),
                                               pnl.__round__(2), percent_pnl.__round__(2)]
        self.holdings[coin] = 0

    # buys spread
    def buy_spread(self, ratio, prices, timestamp):
        print('buy spread')
        self.trade_open = True
        for i, v in self.params.items():
            self.open_trade(ratio * v, i, prices[i], timestamp)
            print(i, v, prices[i], timestamp)

    # sells (shorts) spread
    def sell_spread(self, ratio, prices, timestamp):
        print('sell spread')
        self.trade_open = True
        for i, v in self.params.items():
            self.open_trade(-ratio * v, i, prices[i], timestamp)
            print(i, v, prices[i], timestamp)

    # exits all positions
    def exit_positions(self, prices, timestamp):
        print('exit spread')
        self.trade_open = False
        for k, v in self.holdings.items():
            if k == 'cash' or not v:
                pass
            else:
                self.close_trade(k, prices[k], timestamp)

    # returns amount of money needed to buy/sell 1 unit of spread
    def get_spread_price(self, prices):
        price = 0
        for i, v in self.params.items():
            price += abs(v) * prices[i]
        return price

    # adjusts trade size to cash
    def adjust_trade_size(self, cash, prices):
        spread_price = self.get_spread_price(prices)
        return cash/spread_price

    # saves history
    def save_history(self):
        start_date = pd.to_datetime(self.history.index[0])
        end_date = pd.to_datetime(self.history.index[-1])
        self.history.to_csv('')

    # backtests an algorithm, returns logs and results
    def backtest(self, df, entry_z=2, stop_loss_z=4, fee=0.0004):
        self.history = pd.DataFrame(columns=['timestamp', 'coin', 'position', 'price', 'size', 'cash', 'pnl', '% pnl'])
        self.holdings['cash'] = 1000

        for coin in self.params.index:
            self.holdings[coin] = 0

        df['exit'] = df['z_score']*df['z_score'].shift(1)

        for i in df.index.values:
            ratio = self.adjust_trade_size(self.holdings['cash'], df.loc[i])
            if df.loc[i, 'z_score'] >= entry_z and not self.trade_open:
                self.sell_spread(ratio, df.loc[i], i)

            elif df.loc[i, 'z_score'] <= -entry_z and not self.trade_open:
                self.buy_spread(ratio, df.loc[i], i)

            elif self.trade_open and (df.loc[i, 'exit'] < 0 or abs(df.loc[i, 'z_score']) >= stop_loss_z or i == df.index[-1]):
                self.exit_positions(df.loc[i], i)

        pnl = (self.holdings['cash'] - 1000).__round__(2)
        percent_pnl = (pnl / 1000 * 100).__round__(2)
        pnls = self.history['pnl'][self.history['pnl'] != '']
        result = pd.Series({'% PNL': percent_pnl,
                            'number of trades': len(self.history)/len(self.params)/2,
                            'number of transactions': len(self.history),
                            'start cash': 1000,
                            'end cash': self.holdings['cash'],
                            'average profit': np.average(pnls[pnls >= 0]),
                            'average loss': np.average(pnls[pnls < 0]),
                            'max profit': np.max(pnls),
                            'max loss': np.min(pnls),
                            'total profits': np.sum(pnls[pnls >= 0]),
                            'total losses': np.sum(pnls[pnls < 0]),
                            'percent positive': 100 * len(pnls[pnls >= 0])/len(pnls) if len(pnls) else 0,
                            'percent negative': 100 * len(pnls[pnls < 0])/len(pnls) if len(pnls) else 0})

        result = result.round(3)
        start_date = pd.to_datetime(df.index[0] * 1000000)
        end_date = pd.to_datetime(df.index[-1] * 1000000)
        result['start date'] = start_date
        result['end_date'] = end_date
        self.history['timestamp'] = self.history['timestamp'].map(lambda x: ccxt.Exchange.iso8601(x)[:16].replace('T', ' '))
        return self.history, result

