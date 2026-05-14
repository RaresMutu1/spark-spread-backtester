import streamlit as st
from power_plant import GasPowerPlant

# Setăm aspectul paginii
st.set_page_config(page_title="PPC Trading Dashboard", layout="wide")
st.title("⚡ Simulator Dispecerizare & Spark Spread")

# --- BARA LATERALĂ PENTRU PARAMETRI (Interactivitate) ---
st.sidebar.header("Parametri Turbină CCGT")
# Aceste slidere îți permit să modifici randamentul live
efficiency = st.sidebar.slider("Randament Termodinamic (%)", 1, 100, 50) / 100.0
vom = st.sidebar.slider("Cost Mentenanță VOM (EUR/MWh)", 1.0, 10.0, 3.0)

# --- INIȚIALIZARE ȘI CALCUL ---
# Streamlit rulează codul de sus în jos la fiecare modificare a unui slider
# Așa că instanțiem centrala cu noii parametri trimiși de utilizator
plant = GasPowerPlant(name="PPC_Live", efficiency=efficiency, vom=vom)

# Folosim un bloc try-except ca un profesionist
try:
    with st.spinner('Se descarcă datele de piață (API Yahoo Finance)...'):
        plant.fetch_data(start_date="2023-01-01")
        plant.calculate_margins()
    
    # --- AFIȘARE REZULTATE ---
    st.success(plant.get_summary())
    
    # Desenăm graficul curbei de profitabilitate
    st.subheader("Evoluția Clean Spark Spread (EUR/MWh)")
    st.line_chart(plant.data['Clean_Spark_Spread'])
    
    # Afișăm tabelul cu ultimele date brute pentru transparență
    st.subheader("Date Brute (Ultimele 5 zile)")
    st.dataframe(plant.data[['Power_EUR_MWh', 'Gas_EUR_MWh', 'Carbon_EUR_t', 'Clean_Spark_Spread']].tail())

except Exception as e:
    st.error(f"A apărut o eroare la procesarea datelor: {e}")