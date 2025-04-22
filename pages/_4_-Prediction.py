import streamlit as st
import pandas as pd
import pickle
st.title(":chart_with_upwards_trend: Predicción de Precio de Pisos")
opcion_entrada = st.radio("Selecciona cómo quieres introducir los datos:", (":file_folder: Subir archivo CSV", ":memo: Introducir manualmente"))
df_input = pd.DataFrame()
with open("models/modelo_entrenado.pkl", "rb") as f:
    modelo, columnas = pickle.load(f)
    if opcion_entrada == ":file_folder: Subir archivo CSV":
        archivo_csv = st.file_uploader("Carga un archivo CSV con los datos del piso", type=["csv"])
        if archivo_csv:
            df_input = pd.read_csv(archivo_csv)
    else:
        st.subheader(":memo: Introduce los datos del piso")
        input_data = {}
        for col in columnas:
            if col == "barrio":
                input_data[col] = st.selectbox("Barrio", ["Centro", "Norte", "Sur", "Este", "Oeste"])
            else:
                input_data[col] = st.number_input(col, value=0)
        df_input = pd.DataFrame([input_data])

        
    if not df_input.empty and st.button("Predecir precio"):
        df_input = pd.get_dummies(df_input)
        for col in [c for c in modelo.feature_names_in_ if c not in df_input.columns]:
            df_input[col] = 0
        df_input = df_input[modelo.feature_names_in_]
        pred = modelo.predict(df_input)[0]
        st.success(f":moneybag: Precio estimado: {int(pred):,} €")






