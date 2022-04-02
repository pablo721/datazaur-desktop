from sqlalchemy import MetaData, Table, Column, Float, Integer, String, Boolean, create_engine, ForeignKey, DateTime
from sqlalchemy.orm import relationship, registry, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import inspect
from .db66 import ChemicalDB

Base = declarative_base()


class Website(Base):
    __tablename__ = 'website'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    title = Column(String)
    selector = Column(String)


class Config(Base):
    __tablename__ = 'config'
    key = Column(String, primary_key=True)
    value = Column(String, nullable=False)


class Updates(Base):
    __tablename__ = 'updates'
    table = Column(String, primary_key=True)
    updated = Column(DateTime, nullable=True)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    keys = relationship('key_pair', backref='keypair_user')


class Key(Base):
    __tablename__ = 'key'
    id = Column(String, primary_key=True)
    key = Column(String, nullable=False)


class KeyPair(Base):
    __tablename__ = 'key_pair'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    priv_key = Column(String, nullable=True)
    pub_key = Column(String, nullable=False)
    hash_algo = Column(String, nullable=False)


# cryptocurrency exchanges
class Exchange(Base):
    __tablename__ = 'exchange'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    url = Column(String, nullable=False, unique=True)
    countries = relationship('country', back_populates='exchange')
    currencies = relationship('currency', back_populates='exchange')
    cryptocurrencies = relationship('markets', back_populates='exchange')


class Cryptocurrency(Base):
    __tablename__ = 'cryptocurrency'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    symbol = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)
    exchanges = relationship('markets', back_populates='cryptocurrency')


# association table containing cryptocurrency trading pairs quoted in other cryptocurrencies
class CryptoTicker(Base):
    __tablename__ = 'crypto_pair'
    id = Column(Integer, primary_key=True)
    base_id = Column(ForeignKey('cryptocurrency.id'), backref='cryptoticker_base')
    quote_id = Column(ForeignKey('cryptocurrency.id'), backref='cryptoticker_quote')
    source_id = Column(ForeignKey('exchange.id'), backref='cryptoticker_source')


# association table containing cryptocurrency trading pairs quoted in fiat currencies
class CryptoFiatTicker(Base):
    __tablename__ = 'crypto_quote'
    id = Column(Integer, primary_key=True)
    base_id = Column(ForeignKey('cryptocurrency.id'), backref='cryptofiatticker_base')
    quote_id = Column(ForeignKey('currency.id'), backref='cryptofiatticker_quote')
    source_id = Column(ForeignKey('exchange.id'), backref='cryptofiatticker_source')



class Country(Base):
    __tablename__ = 'country'
    iso_code = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    currency_id = Column(Integer, ForeignKey('currency.id'), backref='currency_issuer')
    currency = relationship('currency', back_populates='currency_countries')


class Currency(Base):
    __tablename__ = 'currency'
    alpha_3 = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True)


# trading algorithm based on crossovers of moving averages (TP, SL and max loss are in percentages)
# long and short columns can be used to open only long positions, only shorts or both (when conditions are met)
class MomentumAlgorithm(Base):
    __tablename__ = 'momentum_algorithm'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, default='Momentum algorithm')
    user_id = Column(Integer, ForeignKey('user.id'))
    coin_id = Column(Integer, ForeignKey('cryptocurrency.id'))
    quote = Column(String, ForeignKey('currency.alpha_3'))
    short_ma = Column(Integer, nullable=False)
    long_ma = Column(Integer, nullable=False)
    long = Column(Boolean, nullable=False)
    short = Column(Boolean, nullable=False)
    take_profit = Column(Float)
    stop_loss = Column(Float)
    max_loss = Column(Float)


# trading algorithm based on cointegration of asset prices (uses z-score for entry, TP and SL; percentage for max loss
# after which execution stops
class CointegrationAlgorithm(Base):
    __tablename__ = 'cointegration_algorithm'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String, nullable=False, default='Cointegration algo')
    tickers = relationship('cointegration_parameters', back_populates='cointegration_algorithm')
    entry_z = Column(Float, nullable=False)
    take_profit_z = Column(Float)
    stop_loss_z = Column(Float)
    max_loss = Column(Float)


# association class linking cointegration algorithms to cryptocurrencies and their parameter values
class CointegrationParameters(Base):
    __tablename__ = 'cointegration_parameters'
    algorithm_id = Column(ForeignKey('cointegration_algorithm.id'), primary_key=True)
    coin_id = Column(ForeignKey('cryptocurrency.id'), primary_key=True)
    parameter = Column(Float, nullable=False)
    algorithm = relationship('cointegration_algorithm', back_populates='algorithms')
    coin = relationship('cryptocurrency', back_populates='cryptocurrencies')


# price arbitrage algorithm class. tracks the same pair on multiple markets and takes actions when conditions are met
# long & short booleans specify which direction algorithm will trade (set both as True to trade both ways!)
# entry_threshold specifies % divergence between lowest/highest price and consensus level big enough to open position
# take_profit is the threshold to exit trades(like entry, specified as % divergence between one ticker and consensus).
# e.g. if you set entry_threshold=10 and take_profit=2, bot will open positions when price of any tracked coin is 10%
# higher/lower than consensus level (volume-weighted average from all tracked markets).
# stop_loss format is max percentage loss on trade.

class ArbitrageAlgorithm(Base):
    __tablename__ = 'arbitrage_algorithm'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, default='Arbitrage algorithm')
    user_id = Column(Integer, ForeignKey('user.id'))
    coin_id = Column(Integer, ForeignKey('cryptocurrency.id'))
    quote_currency = Column(Integer, ForeignKey('currency.id'))
    refresh_rate = Column(Integer, nullable=False, default=10)
    exchanges = relationship('exchange', backref='arbitrage_algorithm', back_populates='exchanges')
    long = Column(Boolean)
    short = Column(Boolean)
    entry_threshold = Column(Float)
    take_profit = Column(Float)
    stop_loss = Column(Float)
    leverage = Column(Integer, default=1)


class TwitterAlgorithm(Base):
    __tablename__ = 'twitter_algorithm'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, default='Twitter algorithm')
    user_id = Column(Integer, ForeignKey('user.id'), p)


class Condition(Base):
    __tablename__ = 'condition'
    id = Column(Integer, primary_key=True)
    ticker_id = Column(Integer, ForeignKey('cryptocurrency.id'))
    exchange_id = Column(Integer, ForeignKey('exchange.id'))
    operand = Column(String)
    value = Column(Float)


class Alert(Base):
    __tablename__ = 'alert'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    condition_id = Column(Integer, ForeignKey('condition.id'))
