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
        meses_por_linea = re.findall(
            r"(ENERO|FEBRERO|MARZO|ABRIL|MAYO|JUNIO|JULIO|AGOSTO|SETIEMBRE|OCTUBRE|NOVIEMBRE|DICIEMBRE)", texto)

        cantidad_meses = []
        contador = 0
        for _ in totales:
            meses = meses_por_linea[contador:contador + 12]
            cantidad_meses.append(len(meses))
            contador += len(meses)

        # Mostrar resultados
        st.subheader("📊 Resultados extraídos")

        for i, total in enumerate(totales):
            año = años_encontrados[i] if i < len(años_encontrados) else f"Desconocido_{i}"
            ingresos_netos = int(total[1].replace(",", ""))
            meses = cantidad_meses[i] if i < len(cantidad_meses) else 0
            st.markdown(f"""
            **🔹 RUC:** {ruc}  
            **📅 Fecha Info:** {fecha_info}  
            **📘 Año:** {año}  
            **💰 Ingresos Netos:** ${ingresos_netos:,}  
            **📆 Meses Reportados:** {meses}
            ---
            """)

    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")
