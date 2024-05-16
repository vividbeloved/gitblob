import pandas as pd
import numpy as np

class MoneyMarketTradingStrategy:
    def __init__(self, data):
        self.data = data

    def analyze_trend(self):
        # Analisis tren pasar uang menggunakan moving average
        self.data['SMA_50'] = self.data['Price'].rolling(window=50).mean()
        self.data['SMA_200'] = self.data['Price'].rolling(window=200).mean()

        # Sinyal beli saat moving average 50 periode memotong moving average 200 periode dari bawah
        self.data['Signal'] = np.where(self.data['SMA_50'] > self.data['SMA_200'], 1, 0)
        self.data['Position'] = self.data['Signal'].diff()

    def execute_trades(self):
        # Strategi perdagangan: beli saat sinyal positif, jual saat sinyal negatif
        cash = 100000  # modal awal
        shares = 0
        for index, row in self.data.iterrows():
            if row['Position'] == 1:
                # Beli
                shares = cash / row['Price']
                cash = 0
            elif row['Position'] == -1:
                # Jual
                cash = shares * row['Price']
                shares = 0
        return cash

# Contoh penggunaan strategi perdagangan di pasar uang
if __name__ == "__main__":
    # Data harga saham (misalnya)
    data = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', end='2024-01-01', freq='D'),
        'Price': np.random.normal(100, 10, 366)  # Harga acak untuk tahun 2023
    })

    strategy = MoneyMarketTradingStrategy(data)
    strategy.analyze_trend()
    final_cash = strategy.execute_trades()
    print("Modal akhir setelah menerapkan strategi perdagangan:", final_cash)
