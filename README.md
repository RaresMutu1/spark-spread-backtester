# spark-spread-backtester
## Simulator Dispecerizare CCGT (Clean Spark Spread)

Acest proiect este un model cantitativ care simulează profitabilitatea și deciziile de pornire/oprire pentru o centrală electrică pe gaze naturale (CCGT). 

Modelul extrage automat prețurile pentru Gaz și Carbon, aplică o conversie termodinamică și calculează **Short-Run Marginal Cost (SRMC)** pentru a determina **Clean Spark Spread-ul**.

## Tehnologii Folosite
* **Python** (Arhitectură Orientată pe Obiecte)
* **Pandas & Numpy** (Data cleaning și procesare vectorizată)
* **YFinance** (Extragere date financiare)
* **Streamlit** (Interfață grafică interactivă)

## Cum se rulează aplicația local
Deschideți terminalul și rulați comanda:
`streamlit run dashboard.py`