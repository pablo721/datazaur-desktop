import numpy as np
import pandas as pd
import ccxt


class Algorithm:
    def __init__(self, name, coefficients, parameters, algorithm_type, max_drawdown=None, ma_window=False,
                 long_short_ratio=0, refresh_rate=60):
        self.name = name
        self.coefficients = coefficients
        self.variables = self.coefficients.index.values
        self.entry_z = parameters['entry_z']
        self.exit_z = parameters['exit_z']
        self.stop_loss_z = parameters['stop_loss_z']
        self.algorithm_type = algorithm_type

        self.max_drawdown = max_drawdown
        self.ma_window = ma_window
        self.long_short_ratio = long_short_ratio
        self.refresh_rate = refresh_rate

        self.holdings = dict()

        self.history = pd.DataFrame(columns=['timestamp', 'coin', 'position', 'price', 'size', 'cash', 'pnl', '% pnl'])
        self.trade_open = False
        self.ratio = 0
        self.open_prices = dict()









