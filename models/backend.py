import ccxt
import pandas as pd
import datetime
import numpy as np
import math
import statsmodels.tsa.api as tsa
import time
from database import Database
import hashlib
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet



class Datazaur(object):
    def __init__(self):
        self.front = None
        self.exchanges = dict()
        self.current_exchange = None
        self.current_ticker = None
        self.db = Database()
        self.holdings = {'cash': 0}

        self.history = pd.DataFrame(columns=['timestamp', 'coin', 'position', 'price', 'size', 'cash', 'pnl', '% pnl'])

        self.user = None
        self.algo_running = False

        self.algos = dict()
        self.market_data = dict()
        self.adf_kpss_config = {'adf_reg': 'c', 'adf_autolag': 'AIC', 'adf_max': False, 'kpss_reg': 'c',
                                'kpss_autolag': 'auto', 'kpss_max': False}

        self.johansen_config = {'det_order': 0, 'n_lags': 144}
        self.time_dict = {'m': 60000, 'h': 3600000, 'd': 86400000, 'w': 604800000, 'M': 2592000000, 'y': 31536000000}

    # connects to exchange
    def connect_exchange(self, exchange_id):
        if exchange_id in self.exchanges.keys():
            return self.exchanges[exchange_id]
        else:
            exchange = getattr(ccxt, exchange_id)({'enableRateLimit': True, 'options': {'defaultType': 'future'}})
            #exchange = getattr(ccxt, exchange_id)({'enableRateLimit': True})
            self.exchanges[exchange_id] = exchange
            self.current_exchange = exchange
            try:
                exchange.load_markets()
            except Exception as e:
                print(f'connection failed - error {e}')
            return exchange


    def add_pairs(self):
        self.pairs.extend(map(lambda x: x + ' ' + self.current_exchange.id, self.current_exchange.symbols))

    # selects exchange
    def select_exchange(self, exchange_id):
        self.current_exchange = self.exchanges[exchange_id]

    # selects ticker
    def select_ticker(self, ticker):
        self.current_ticker = ticker

    # deletes exchange
    def delete_exchange(self, exchange_id):
        del self.exchanges[exchange_id]

    # converts timeframe from e.g. '3M' to miliseconds
    def get_time_in_ms(self, timeframe):
        letter = timeframe[-1]
        number = timeframe[:-1]
        return self.time_dict[letter] * int(number)

    # convert timeframe to start date in UNIX time
    def get_since(self, timeframe):
        today_ms = ccxt.Exchange.milliseconds()
        timeframe_ms = self.get_time_in_ms(timeframe)
        since = today_ms - timeframe_ms
        return since

    # checks if table is in database
    def check_db(self, table_name):
        tables = self.db.table_list()
        s = ''
        for t in tables:
            s += t[0]
        if table_name in s:
            return True
        else:
            return False

    # gets data - first checks in database then adds most recent data points
    def get_data(self, exchange, ticker, interval, since):
        table_name = ticker + '_' + exchange + '_' + interval
        if self.check_db(table_name):
            last = self.db.cursor.execute(f"""SELECT MIN("Date") FROM '{table_name}';""").fetchall()[0][0]
            if (since + 3600000) >= last:
                df = pd.DataFrame(self.db.cursor.execute(f"""SELECT * FROM '{table_name}' WHERE Date >= {since};""").fetchall())
                since2 = self.db.cursor.execute(f"""SELECT MAX("Date") FROM '{table_name}';""").fetchall()[0][0]
                df2 = pd.DataFrame(self.get_data_since(exchange, ticker, interval, since2))
                df = df.append(df2)
            else:
                print('downloading1')
                df = self.get_data_since(exchange, ticker, interval, since)
        else:
            print('downloading2')
            df = self.get_data_since(exchange, ticker, interval, since)

        df.columns = 'Date Open High Low Close Volume'.split()
        df.drop_duplicates(subset='Date', inplace=True)
        df.to_sql(table_name, self.db.connection, if_exists='replace', index=False, dtype={'Date': 'INTEGER',
                                                                                           'Open': 'REAL',
                                                                                           'High': 'REAL',
                                                                                           'Low': 'REAL',
                                                                                           'Close': 'REAL',
                                                                                           'Volume': 'REAL'})
        self.db.connection.commit()
        df.set_index('Date', inplace=True)
        df.name = ticker + '_' + exchange + '_' + interval
        return df

    # gets data from a given start date
    def get_data_since(self, exchange_id, ticker, interval, since):

        exchange = self.exchanges[exchange_id]
        data = []
        count = 0
        while True:
            d2 = exchange.fetch_ohlcv(ticker, interval, since)
            data += d2
            count += 1
            if len(d2) <= 1:
                break
            else:
                since = d2[-1][0]
        df = pd.DataFrame(data)
        df.drop_duplicates(subset=0, inplace=True)
        df.name = ticker + '_' + exchange.id + '_' + interval
        #df.set_index(0, inplace=True)
        return df

    # gets data for multiple assets
    def get_data2(self, exchange, symbols, interval, since):
        df0 = pd.DataFrame()
        for symbol in symbols:
            try:
                df = self.get_data(exchange, symbol, interval, since)
                df0[symbol] = df['Close']
            except Exception as e:
                print(f'Error {e}')
                continue
            finally:
                continue
        df0.dropna(inplace=True)
        print(df0)
        return df0

    # returns weighted average and standard deviation
    @staticmethod
    def weighted_avg_and_std(values, weights):
        average = np.average(values, weights=weights)
        variance = np.average((values - average) ** 2, weights=weights)
        return average, math.sqrt(variance)

    # returns total price of 1 unit of spread
    def get_spread_price(self, prices, params):
        price = 0
        for i, v in params.items():
            price += abs(v) * prices[i]
        return price

    # returns total value of 1 unit of spread
    def get_spread_val(self, prices, params):
        price = 0
        for i, v in params.items():
            price += v * prices[i]
        return price

    # adjusts trade size
    def adjust_trade_size(self, cash, prices, params):
        spread_price = self.get_spread_price(prices, params)
        print(cash)
        print(spread_price)
        print(cash/spread_price)
        return cash/spread_price

    # opens a long position on spread
    def buy_spread(self, exchange, algorithm, prices, timestamp):
        ratio = self.adjust_trade_size(self.holdings['cash'], prices, algorithm.params)
        for i, v in algorithm.params.items():
            if v > 0:
                self.exchanges[exchange].create_limit_buy_order(i, abs(v*ratio), prices[i])
                self.holdings[i] = v * ratio

            elif v < 0:
                self.exchanges[exchange].create_limit_sell_order(i, abs(v*ratio), prices[i])
                self.holdings[i] = -v * ratio

            self.history.loc[len(self.history)] = [timestamp, i, v*ratio, prices[i],
                                                       (abs(v*ratio)*prices[i]).__round__(2), '', '', '']

        print('bought spread')
        positions = self.get_positions(self.current_exchange.id)
        #self.front.trade_panel.tableView_3.setModel(PandasModel(positions))
        #self.front.trade_panel.tableView_10.setModel(PandaMmodel(self.history))

    # opens a short position on spread
    def sell_spread(self, exchange, algorithm, prices, timestamp):

        ratio = self.adjust_trade_size(self.holdings['cash'], prices, algorithm.params)
        for i, v in algorithm.params.items():
            if v > 0:
                print(i, abs(v*ratio), prices[i])
                order = self.exchanges[exchange].create_limit_sell_order(i, abs(v*ratio), prices[i])
                self.holdings[i] = -v * ratio

            elif v < 0:
                order = self.exchanges[exchange].create_limit_buy_order(i, abs(v*ratio), prices[i])
                self.holdings[i] = v * ratio

            self.history.loc[len(self.history)] = [timestamp, i, v*ratio, prices[i],
                                                       (abs(v*ratio)*prices[i]).__round__(2), '', '', '']

        print('sold spread')
        positions = self.get_positions(self.current_exchange.id)
        #self.front.trade_panel.tableView_3.setModel(PandasModel(positions))
        #self.front.trade_panel.tableView_10.setModel(PandasModel(self.history))

    #closes all open trades
    def exit_trades(self, timestamp, exchange, algorithm, prices):
        for k, v in self.holdings.items():
            if v > 0 and k != 'cash':
                self.exchanges[exchange].create_limit_sell_order(k, v, prices[k])
                self.holdings['cash'] += v * prices[k]
                self.holdings[k] = 0
            elif v < 0 and k != 'cash':
                self.exchanges[exchange].create_limit_buy_order(k, v, prices[k])
                self.holdings['cash'] += v * prices[k]
                self.holdings[k] = 0

            self.history.loc[len(self.history)] = [timestamp, i, v * ratio, prices[i],
                                                   (abs(v) * prices[i]).__round__(2), '', '', '']


        print('exited positions')
        positions = self.get_positions(exchange.id)
        #self.front.trade_panel.tableView_3.setModel(PandasModel(positions))
        #self.front.trade_panel.tableView_10.setModel(PandasModel(self.history))

        #self.front.trade_panel.tableView_4.setModel(PandasModel(pd.DataFrame()))



    # returns spread values
    @staticmethod
    def get_spread(df, params):
        spread = np.array(np.zeros(len(df)))
        for col in df.columns:
            spread += df[col]*params[col]
        return spread

    def trade_live(self, df, algorithm, cash, refresh_rate=10, timeframe='3M', interval='30m'):
        #since = self.get_since(timeframe)
        #print(list(algorithm.params.index))
        #df = self.get_data2(self.current_exchange.id, list(algorithm.params.index), interval, since)

        df['spread'] = self.get_spread(df, algorithm.params)
        df['spread_mean'] = df['spread'].mean()
        df['spread_std'] = df['spread'].std()
        df['z_score'] = ((df['spread'] - df['spread_mean']) / df['spread_std']).astype('float64')

        interval_secs = self.get_time_in_ms(interval)/1000
        weight = interval_secs / refresh_rate
        df['weight'] = weight

        df.to_csv('xxxaasddf22.csv')

        print(interval_secs)
        print(weight)

        self.holdings['cash'] = cash

        trade_open = False
        self.algo_running = True

        while self.algo_running:
            data = pd.DataFrame(self.current_exchange.fetch_tickers(algorithm.params.index)).loc[['timestamp', 'last'], :]
            timestamp = data.loc['timestamp', algorithm.params.index[0]]
            df.loc[timestamp] = data.loc['last']
            df.loc[timestamp, 'spread'] = self.get_spread_val(data.loc['last'], algorithm.params)
            df.loc[timestamp, 'weight'] = 1

            avg, std = self.weighted_avg_and_std(df['spread'], df['weight'])
            df.loc[timestamp, 'spread_mean'] = avg
            df.loc[timestamp, 'spread_std'] = std

            print(algorithm.entry_z)
            print(avg)
            print(std)

            df.loc[timestamp, 'z_score'] = (df.loc[timestamp, 'spread'] - df.loc[timestamp, 'spread_mean']) / df.loc[timestamp, 'spread_std']

            print(df.loc[timestamp, 'z_score'])

            if df.loc[timestamp, 'z_score'] > algorithm.entry_z and not trade_open:
                self.sell_spread(self.current_exchange.id, algorithm, df.loc[timestamp], timestamp)
                trade_open = True
            elif df.loc[timestamp, 'z_score'] < -algorithm.entry_z and not trade_open:
                self.buy_spread(self.current_exchange.id, algorithm, df.loc[timestamp], timestamp)
                trade_open = True

            df['exit calc'] = df['z_score'] * df['z_score'].shift(1)
            if df.loc[timestamp, 'exit calc'] < 0 and trade_open:
                self.exit_trades(timestamp, self.current_exchange.id, algorithm, df.loc[timestamp])
                trade_open = False

            time.sleep(refresh_rate)

            df.to_csv('xxx1233212.csv')

        self.exit_trades(df.index[-1], self.current_exchange.id, algorithm, df.loc[timestamp])
        date = str(datetime.datetime.today())[:16]
        self.history.to_csv(f'trade_history_{date}.csv')
        df.to_csv('xxx123.csv')


    # adds natural logarithms
    @staticmethod
    def add_logs(df):
        cols = df.columns
        df[f'log_{cols[0]}'] = np.log(df[cols[0]])
        df[f'log_{cols[1]}'] = np.log(df[cols[1]])
        df[f'log_return{cols[0]}'] = df[f'log_{cols[0]}'] - df[f'log_{cols[0]}'].shift()
        df[f'log_return{cols[1]}'] = df[f'log_{cols[1]}'] - df[f'log_{cols[1]}'].shift()
        return df

    # returns percentage returns with base 100
    @staticmethod
    def get_base_100_returns(df):
        df0 = pd.DataFrame()
        for col in df.columns:
            df0[col] = 100 * df[col] / (df[col].iloc[0])
        return df0

    # adds z-score to dataframe
    @staticmethod
    def get_z_score(df, window=''):
        if window == '':
            df['spread_ma'] = df['spread'].mean()
            df['ma_stdev'] = df['spread'].std()
        else:
            df['spread_ma'] = df['spread'].rolling(window=window).mean()
            df['ma_stdev'] = df['spread'].rolling(window=window).std()

        df['z_score'] = ((df['spread'] - df['spread_ma']) / df['ma_stdev']).astype('float64')
        return df

    # saves config for cointegration tests
    def save_config(self, settings, settings_joh):
        self.adf_kpss_config.update(settings)
        self.johansen_config.update(settings_joh)

    # ADF test wrapper
    @staticmethod
    def adf_test(data, reg='c', lag='AIC', maxlag=None):
        if maxlag:
            return tsa.adfuller(data.dropna(), regression=reg, maxlag=maxlag)[1].__round__(3)
        else:
            return tsa.adfuller(data.dropna(), regression=reg, autolag=lag)[1].__round__(3)

    # KPSS test wrapper
    @staticmethod
    def kpss_test(data, reg='c', lag='auto', maxlag=None):
        if maxlag:
            return tsa.kpss(data.dropna(), regression=reg, nlags=maxlag)[1].__round__(3)
        else:
            return tsa.kpss(data.dropna(), regression=reg, nlags=lag)[1].__round__(3)


    # ADF + KPSS tests
    def test_stationarity(self, df, adf=True, kpss=True):
        results = pd.DataFrame(index=['ADF-test', 'KPSS-test'], columns=['H0'], data={'H0': ['Unit root is present',
                                                                                             'Time series is stationary']})
        for col in df.columns:
            if adf:
                results.loc['ADF-test', col] = self.adf_test(df[col], reg=self.adf_kpss_config['adf_reg'],
                                                             lag=self.adf_kpss_config['adf_autolag'],
                                                             maxlag=self.adf_kpss_config['adf_max'])
            if kpss:
                results.loc['KPSS-test', col] = self.kpss_test(df[col], reg=self.adf_kpss_config['kpss_reg'],
                                                               lag=self.adf_kpss_config['kpss_autolag'],
                                                               maxlag=self.adf_kpss_config['kpss_max'])
        return results

    # OLS model wrapper
    @staticmethod
    def OLS_model(df, const):
        df.dropna(inplace=True)
        y = df.iloc[:, 0]
        if const:
            x = tsa.stattools.add_constant(df.iloc[:, 1:])
        else:
            x = df.iloc[:, 1:]
        model = tsa.stattools.OLS(y, x, missing='drop', hasconst=const)
        results = model.fit()
        summary = results.summary()
        return results, summary

    # returns correlations matrix
    @staticmethod
    def get_corr_matrix(df):
        matrix = pd.DataFrame(columns=df.columns, index=df.columns)
        matrix.index.name = 'corr matrix'
        for col in df.columns:
            for col2 in df.columns:
                matrix.loc[col, col2] = df[col].corr(df[col2]).__round__(3)

        return matrix

    # Engle-Granger test for cointegration
    def engle_granger_coint(self, df, const, adf_reg='c', adf_autolag='AIC', adf_maxlag=None):
        results, summary = self.OLS_model(df, const)
        adf_resid = tsa.stattools.coint(df.iloc[:, 0], df.iloc[:, 1:], trend=adf_reg, autolag=adf_autolag,
                                                                              return_results=False)[1].__round__(3)
        kpss_resid = self.kpss_test(results.resid)
        params = pd.Series({df.columns[0]: 1}).append(-results.params)

        corr_matrix = self.get_corr_matrix(df)
        return pd.Series({'ADF resid': adf_resid, 'KPSS resid': kpss_resid}, name='coint tests'), summary, params, results.resid, corr_matrix

    # saves algorithm
    def save_algo(self, algorithm):
        self.algos[algorithm.name] = algorithm
        self.front.trade_panel.save_algo(algorithm.name)

    #deletes algorithm
    def delete_algo(self, algo_name):
        self.algos.__delitem__(algo_name)
        self.front.trade_panel.delete_algo(algo_name)

    # returns SHA3_512 hash after 100000 iterations with salt
    @staticmethod
    def get_hash(text, salt):
        for i in range(100000):
            text = hashlib.sha3_512((text + salt).encode()).hexdigest()
        return text

    # derives encryption key from password
    @staticmethod
    def get_key(password, salt):
        pwd = password.encode()
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                         length=32,
                         salt=salt,
                         iterations=100000,
                         backend=default_backend())
        key = base64.urlsafe_b64encode(kdf.derive(pwd))
        return key

    # encrypt symmetrically
    def symmetric_encrypt(self, data, password, salt):
        key = self.get_key(password, salt)
        fernet = Fernet(key)
        return fernet.encrypt(data.encode())

    # decrypt symmetrically
    def symmetric_decrypt(self, data, password, salt):
        key = self.get_key(password, salt)
        fernet = Fernet(key)
        return fernet.decrypt(data).decode()

    # adds API keys to database (encrypted)
    def add_keys(self, pubkey, privkey, password):
        salt = os.urandom(32)
        self.current_exchange.apiKey = pubkey
        self.current_exchange.secret = privkey
        pub2 = self.symmetric_encrypt(pubkey, password, salt)
        priv2 = self.symmetric_encrypt(privkey, password, salt)
        self.db.add_keys(self.user, self.current_exchange.id, pub2, priv2, salt)

    # adds username and hash to database
    def add_hash(self, user, password):
        salt = os.urandom(32).hex()
        hsh = self.get_hash(password, salt)
        self.db.add_hash(user, hsh, salt)

    # checks if hashes match
    def check_hash(self, user, password):
        h2 = self.db.get_hash(user)
        salt = h2[0][1]
        h1 = self.get_hash(password, salt)

        return h1 == h2[0][0]

    # logs in and loads API keys
    def login(self, user, password):
        self.user = user
        try:
            keys = self.db.get_keys(user)
            self.connect_exchange(keys[0][0])

            for item in keys:
                pubkey = self.symmetric_decrypt(item[1], password, item[-1])
                privkey = self.symmetric_decrypt(item[2], password, item[-1])
                self.exchanges[item[0]].apiKey = pubkey
                self.exchanges[item[0]].secret = privkey
        except:
            print('login failed')

    # gets account balance from exchange
    def fetch_balance(self, exchange_id):
        df = pd.DataFrame(self.exchanges[exchange_id].fetch_balance()).transpose()
        #acc_type = df.loc['info', 'accountType']
        df = df[['free', 'used', 'total']]
        df = df[df['total'] != 0]
        df.dropna(inplace=True)
        return df



    # gets open positions from exchange
    def get_positions(self, exchange_id):
        df = pd.DataFrame(self.exchanges[exchange_id].fetchPositions())
        df = df[df['initialMargin'] != '0']
        return df






















