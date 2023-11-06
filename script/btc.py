import matplotlib.pyplot as plt
import requests
import pandas as pd

def get_btc_graph():
    # CoinGecko APIを使用してBTC価格データを取得
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",  # 価格の通貨をUSDに設定
        "days": 30  # 取得する日数を設定
    }

    response = requests.get(url, params=params)
    data = response.json()

    # データをDataFrameに変換
    df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")


    # グラフの設定
    plt.figure(figsize=(12, 6))
    plt.plot(df["timestamp"], df["price"], label="BTC Price (USD)", color="blue")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid(True)

    # グラフを表示
    plt.legend()

    plt.savefig("img/BTC_price.png")

