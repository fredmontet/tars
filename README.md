TARS
====


- [x] markets 
  - [x] abstract_market
  - [x] crypto_market
    - [x] get_asset_info
    - [x] get_ohlc_data
    - [x] get_order_book
    - [x] get_recent_spread_data
    - [x] get_ticker_information
    - [x] get_tradable_asset_pair

- [x] portfolios
  - [x] abstract_portfolio 
    - [x] get_account_balace
  - [x] crypto_portfolio
    - [x] get_account_balance
    - [x] get_trade_balance
  - [x] virtual_portfolio
    - [x] get_account_balance
    - [x] deposit
    - [x] withdraw

- [x] traders 
  - [x] abstract_trader
    - [x] add_order
    - [x] cancel_order
  - [x] virtual_crypto_trader
    - [x] add_order
    - [x] cancel_order
    - [x] get_open_orders
    - [x] get_closed_orders
    - [x] query_orders_info
    - [x] get_trades_history
    - [x] query_trades_info
  - [X] virtual_trader
    - [x] add_order
    - [x] cancel_order

- [x] strategies
  - [x] buy'n'hold
  - [x] sequential investment
  - [x] random investement

