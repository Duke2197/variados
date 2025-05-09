# -*- coding: utf-8 -*-
"""
Created on Fri May  9 14:05:33 2025

@author: fmoscoso
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Consulta Empresas", layout="centered")
st.title("Consulta Visual de Empresas")

# Leer archivo Excel (usa tu propio nombre de archivo y hoja si aplica)
@st.cache_data
def cargar_datos():
    return pd.read_excel("Cruce_top_sentinel.xlsx",sheet_name="Top")

df = cargar_datos()

# Ingreso de RUC
ruc = st.text_input("INGRESAR RUC:")

if ruc:
    # Filtrar el DataFrame por RUC (asegura que ambos sean texto)
    empresa = df[df['ruc'].astype(str) == ruc]  

    if not empresa.empty:
        row = empresa.iloc[0]

        # Campos en pantalla (puedes cambiar los nombres a los reales)
        st.text_input("RAZON SOCIAL:", row["razon_social"], disabled=True)
        st.text_input("SECTOR:", row["sector_esp"], disabled=True)

        col1, col2 = st.columns(2)
        with col1:
            st.text_input("TAMAÑO:", row["SEGMENTO2"], disabled=True)
            st.text_input("CLASIFICACIÓN COVAL:", row["Cruce_sentinel"], disabled=True)
        with col2:
            st.text_input("RANKING:", row["ranking_2024"], disabled=True)
            st.text_input("SENTINEL:", row["SENTINEL"], disabled=True)

        st.text_input("FACTURADO 2023 S/.:", f"{row['facturado_2023_soles_minimo']:,}", disabled=True)
        st.text_input("FACTURADO 2024 S/.:", f"{row['facturado_2024_soles_minimo']:,}", disabled=True)
        st.text_input("DEUDA SBS S/.:", f"{row['DEUDA_SBS']:,}", disabled=True)

    else:
        st.warning("RUC no encontrado en la base.")
