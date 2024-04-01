from decimal import Decimal
from typing import Optional
import pandas as pd
import numpy as np

# Initialize variables to keep track of previous values
prev_av_gain: Decimal = Decimal(0.0)
prev_av_loss: Decimal = Decimal(0.0)
prev_rsi: Decimal = Decimal(0.0)
prev_close: Optional[Decimal] = None
_period = 14


def calculate_rsi(closes: [Decimal]) -> Decimal:
    global prev_av_gain, prev_av_loss, prev_rsi, prev_close

    if len(closes) < _period:
        return Decimal(-1)

    gains = []
    losses = []
    for i in range(1, len(closes)):
        change = closes[i] - closes[i - 1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))

    current_gain = sum(gains[-_period:]) / _period
    current_loss = sum(losses[-_period:]) / _period

    if prev_rsi == 0:
        print(f"Base calc rsi:{prev_rsi} close:{prev_close}")
        prev_rsi = 100 - (100 / (1 + (current_gain / current_loss)))
    elif not prev_close == closes[-2]:
        print(f"Alt calc rsi:{prev_rsi} close:{prev_close}")
        prev_av_gain = (prev_av_gain * (_period - 1) + current_gain) / _period
        prev_av_loss = (prev_av_loss * (_period - 1) + current_loss) / _period
        prev_rsi = 100 - (100 / (1 + (prev_av_gain / prev_av_loss)))

    prev_close = closes[-2]

    return prev_rsi


def rsi_tradingview(ohlc: pd.DataFrame, period: int = 14, round_rsi: bool = True):
    """ Implements the RSI indicator as defined by TradingView on March 15, 2021.
        The TradingView code is as follows:
        //@version=4
        study(title="Relative Strength Index", shorttitle="RSI", format=format.price, precision=2, resolution="")
        len = input(14, minval=1, title="Length")
        src = input(close, "Source", type = input.source)
        up = rma(max(change(src), 0), len)
        down = rma(-min(change(src), 0), len)
        rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))
        plot(rsi, "RSI", color=#8E1599)
        band1 = hline(70, "Upper Band", color=#C0C0C0)
        band0 = hline(30, "Lower Band", color=#C0C0C0)
        fill(band1, band0, color=#9915FF, transp=90, title="Background")

    :param ohlc:
    :param period:
    :param round_rsi:
    :return: an array with the RSI indicator values
    """

    delta = ohlc["close"].diff()

    up = delta.copy()
    up[up < 0] = 0
    up = pd.Series.ewm(up, alpha=1 / period).mean()

    down = delta.copy()
    down[down > 0] = 0
    down *= -1
    down = pd.Series.ewm(down, alpha=1 / period).mean()

    rsi = np.where(up == 0, 0, np.where(down == 0, 100, 100 - (100 / (1 + up / down))))

    return np.round(rsi, 2) if round_rsi else rsi


def alt_calculate_rsi(prices, period=14, round_rsi=True):
    """
    Calculate RSI (Relative Strength Index) using the TradingView formula.

    :param prices: A list or array of closing prices.
    :param period: The number of periods to consider for RSI calculation (default is 14).
    :param round_rsi: If True, round the RSI values to two decimal places (default is True).
    :return: A list of RSI indicator values.
    """
    gains = []
    losses = []
    prev_close = None

    for i in range(1, len(prices)):
        change = prices[i] - prices[i - 1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(prices)):
        change = prices[i] - prices[i - 1]
        gain = max(0, change)
        loss = abs(min(0, change))

        avg_gain = ((avg_gain * (period - 1)) + gain) / period
        avg_loss = ((avg_loss * (period - 1)) + loss) / period

    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))

    if round_rsi:
        return round(rsi, 2)
    else:
        return rsi

'''
    async def calculate_rsi_for_symbol(self, symbol: str) -> Decimal:
        # Get the last 14 klines for the given symbol
        end_date = int(datetime.timestamp(datetime.now()))
        start_date = int((datetime.now() - timedelta(minutes=14)).timestamp())
        last_14_klines = await self.platform.get_klines(
            symbol=symbol,
            start_date=str(start_date),
            end_date=str(end_date),
            interval='1m',
            limit=100
        )

        # Print the dates of the klines in a human-readable format
        for kline in last_14_klines:
            date = datetime.fromtimestamp(kline.kline_start_time / 1000).strftime('%Y-%m-%d %H:%M:%S')
            print(f"KLine date: {date} Open {kline.open_price} Close {kline.close_price}")

        import pandas as pd
        d = {'close': [kline.close_price for kline in last_14_klines]}
        d = pd.DataFrame(data=d)

        rsi = calculate_rsi(closes=[kline.close_price for kline in last_14_klines])
        alt_rsi = alt_calculate_rsi([kline.close_price for kline in last_14_klines])
        print(f"My RSI: {rsi} TradingRSI: {rsi_tradingview(d)[-1]} alt:{alt_rsi}")
        return rsi
'''