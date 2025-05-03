# -*- coding: utf-8 -*-
"""
Created on Fri May  2 15:39:38 2025

@author: fmoscoso
"""

import streamlit as st
import pdfplumber
import re

st.set_page_config(page_title="Analizador de PDF SUNAT", layout="centered")
st.title("📄 Analizador de Reportes SUNAT")

archivo = st.file_uploader("Sube el archivo PDF", type=["pdf"])

if archivo is not None:
    try:
        with pdfplumber.open(archivo) as pdf:
            texto_p1 = pdf.pages[0].extract_text()

            pagina_objetivo = next(
                (i for i, p in enumerate(pdf.pages) if "EJERCICIO CORRIENTE" in p.extract_text()),
                None
            )

            if pagina_objetivo is None:
                st.error("No se encontró la página con 'EJERCICIO CORRIENTE'.")
                st.stop()

            texto = pdf.pages[pagina_objetivo].extract_text()

        # RUC y Fecha
        fecha_info = re.search(r"Información al (\d{2}/\d{2}/\d{4})", texto)
        fecha_info = fecha_info.group(1) if fecha_info else "No encontrada"
        ruc_match = re.search(r"RUC:\s+(\d+)", texto_p1)
        ruc = ruc_match.group(1) if ruc_match else "No encontrado"

        # Extraer info
        años_encontrados = re.findall(r"EJERCICIO (?:ANTERIOR|CORRIENTE) \((\d{4})\)", texto)
        totales = re.findall(r"TOTAL EJERCICIO\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)", texto)

        # Mostrar resultados en columnas
        st.subheader("📊 Resultados extraídos")
        for i, total in enumerate(totales):
            año = años_encontrados[i] if i < len(años_encontrados) else f"Desconocido_{i}"
            ventas = int(total[0].replace(",", ""))

            col1, col2, col3, col4 = st.columns(4)
            col1.markdown(f"**🔹 RUC:** {ruc}")
            col2.markdown(f"**📅 Fecha Info:** {fecha_info}")
            col3.markdown(f"**📘 Año:** {año}")
            col4.markdown(f"**💰 Ventas:** ${ventas:,}")

            st.markdown("---")

    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")

