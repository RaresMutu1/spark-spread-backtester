import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class GasPowerPlant:
    def __init__(self, name: str, efficiency: float = 0.52, emission_factor: float = 0.202, vom: float = 3.0):
        self.name = name
        self.efficiency = efficiency
        self.emission_factor = emission_factor
        self.vom = vom
        self.data: pd.DataFrame = pd.DataFrame()

    def fetch_data(self, start_date: str, end_date: str = None) -> None:
        if end_date is None:
            end_date = datetime.today().strftime('%Y-%m-%d')
            
        print(f"[{self.name}] Tentativă achiziție date: {start_date} -> {end_date}...")
        
        try:
            # Încercăm descărcarea online (NG=F e Gaz, KRBN e Carbon)
            raw_data = yf.download(["NG=F", "KRBN"], start=start_date, end=end_date, progress=False, timeout=10)
            
            if raw_data.empty or 'Close' not in raw_data:
                raise ValueError("Date goale de la Yahoo")

            df = raw_data['Close'].copy()
            df.rename(columns={'NG=F': 'Gas_USD_MMBtu', 'KRBN': 'Carbon_EUR_t'}, inplace=True)
            print(f"[{self.name}] Date descărcate cu succes de pe internet.")

        except Exception as e:
            # --- Dacă nu ai net sau API-ul e blocat ---
            print(f"[{self.name}] ALERTA: Internet/API indisponibil. Generare date sintetice de rezervă...")
            dates = pd.date_range(start=start_date, end=end_date, freq='B') # Doar zile lucrătoare
            df = pd.DataFrame(index=dates)
            
            # Random Walk (bazat pe mediile din 2024)
            np.random.seed(42)
            df['Gas_USD_MMBtu'] = 2.5 + np.cumsum(np.random.normal(0, 0.05, len(df)))
            df['Carbon_EUR_t'] = 70.0 + np.cumsum(np.random.normal(0, 0.5, len(df)))

        # Conversii obligatorii
        fx_rate = 1.08 
        df['Gas_EUR_MWh'] = (df['Gas_USD_MMBtu'] / 0.293) / fx_rate
        
        # Simulare preț energie (PZU) cu volatilitate mare (vânt/soare)
        # Prețul energiei = (Gaz * factor) + Zgomot de piață
        np.random.seed(99)
        df['Power_EUR_MWh'] = (df['Gas_EUR_MWh'] * 2.0) + np.random.normal(10, 25, len(df))
        
        # Weekend dump (Prețuri mai mici sâmbăta și duminica)
        df.loc[df.index.dayofweek >= 5, 'Power_EUR_MWh'] -= 40

        df.dropna(inplace=True)
        self.data = df
        print(f"[{self.name}] Gata! Procesate {len(self.data)} puncte de date.")

    def calculate_margins(self) -> None:
        if self.data.empty: return
        gas_cost = self.data['Gas_EUR_MWh'] / self.efficiency
        carbon_cost = (self.data['Carbon_EUR_t'] * self.emission_factor) / self.efficiency
        self.data['SRMC'] = gas_cost + carbon_cost + self.vom
        self.data['Clean_Spark_Spread'] = self.data['Power_EUR_MWh'] - self.data['SRMC']
        self.data['Dispatch_Signal'] = (self.data['Clean_Spark_Spread'] > 0).astype(int)

    def get_summary(self) -> str:
        if self.data.empty: return "Fără date."
        active_days = self.data['Dispatch_Signal'].sum()
        profitability = (active_days / len(self.data)) * 100
        return f"Raport {self.name}: Centrala profitabilă {active_days}/{len(self.data)} zile ({profitability:.1f}%)."

if __name__ == "__main__":
    ppc_plant = GasPowerPlant(name="PPC_Backtester_V2") 
    ppc_plant.fetch_data(start_date="2024-01-01")
    ppc_plant.calculate_margins()
    print(ppc_plant.data[['Power_EUR_MWh', 'Gas_EUR_MWh', 'Clean_Spark_Spread', 'Dispatch_Signal']].tail())
    print(ppc_plant.get_summary())