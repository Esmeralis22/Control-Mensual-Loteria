import streamlit as st
import json
import os
from datetime import datetime

# ================= CONFIG =================
DATA_FILE = "historial_loterias.json"

LOTERIAS = [
    "Anguilla 10:00 AM", "Anguilla 1:00 PM", "Anguilla 6:00 PM", "Anguilla 9:00 PM",
    "Primera Dia", "Primera Noche", "Lotedom", "La Suerte MD", "La Suerte 6PM",
    "Real", "Gana Mas", "Florida Dia", "Florida Noche",
    "New York Dia", "New York Noche",
    "Loteka", "Leidsa", "Loteria Nacional"
]

COLORES = ["red", "orange", "green"]

# ================= DATA =================
def cargar():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf8") as f:
            return json.load(f)
    return {}

def guardar(data):
    with open(DATA_FILE, "w", encoding="utf8") as f:
        json.dump(data, f, indent=2)

def nuevo_panel():
    return {f"{i:02d}": [] for i in range(100)}

# ================= UI =================
st.set_page_config(layout="wide")
st.title("📊 Control Mensual de Loterías")

data = cargar()

loteria = st.selectbox("Selecciona la lotería", LOTERIAS)

fecha = datetime.now()
mes_key = fecha.strftime("%Y-%m")
fecha_str = fecha.strftime("%d/%m/%Y")

data.setdefault(loteria, {})
data[loteria].setdefault(mes_key, {
    "panel": nuevo_panel(),
    "historial": []
})

panel = data[loteria][mes_key]["panel"]
historial = data[loteria][mes_key]["historial"]

st.subheader(f"🎯 Lotería seleccionada: **{loteria}**")
st.caption(f"Mes activo: **{mes_key}** | Fecha del sistema: **{fecha_str}**")

# ================= ENTRADA =================
resultado = st.text_input("Resultado (formato xx-xx-xx)", placeholder="56-74-83")

if st.button("Guardar resultado"):
    try:
        nums = resultado.split("-")
        if len(nums) != 3:
            raise ValueError

        for i, n in enumerate(nums):
            if not n.isdigit() or not (0 <= int(n) <= 99):
                raise ValueError
            panel[n].append(i)

        historial.append({
            "fecha": fecha_str,
            "resultado": resultado
        })

        guardar(data)
        st.success("Resultado guardado correctamente")

    except:
        st.error("Formato inválido. Usa xx-xx-xx (00 a 99)")

# ================= ELIMINAR RESULTADO =================
if st.button("🗑️ Eliminar último resultado"):
    if historial:
        ultimo = historial.pop()
        nums = ultimo["resultado"].split("-")

        for i, n in enumerate(nums):
            if panel[n]:
                panel[n].pop()

        guardar(data)
        st.warning("Último resultado eliminado")
        st.rerun()
    else:
        st.info("No hay resultados para eliminar")

# ================= PANEL COMPLETO =================
st.subheader("📌 Panel mensual 00–99")

def celda(num):
    marcas = panel[num]
    puntos = ""
    for m in marcas:
        puntos += (
            f"<span style='color:{COLORES[m]};"
            f"font-size:9px;"
            f"margin-right:1px;'>●</span>"
        )

    return (
        f"<span style='font-size:12px; font-weight:bold;'>{num}</span><br>"
        f"<span style='display:inline-block;"
        f"height:10px;"
        f"line-height:10px;"
        f"white-space:nowrap;"
        f"overflow:hidden;'>{puntos}</span>"
    )

for fila in range(4):
    cols = st.columns(25)
    for col in range(25):
        n = f"{fila*25 + col:02d}"
        cols[col].markdown(
            f"<div style='border:1px solid #ccc;"
            f"height:45px;"
            f"text-align:center;"
            f"padding-top:4px;"
            f"overflow:hidden;'>"
            f"{celda(n)}</div>",
            unsafe_allow_html=True
        )

# ================= HISTORIAL =================
st.subheader("🗂 Historial del mes")

for h in historial:
    st.write(f"📅 {h['fecha']} → 🎯 {h['resultado']}")
