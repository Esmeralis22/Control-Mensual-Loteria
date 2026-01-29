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

# Inicializar estructuras
data.setdefault(loteria, {})
data[loteria].setdefault(mes_key, {
    "panel": nuevo_panel(),
    "historial": []
})

panel = data[loteria][mes_key]["panel"]

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

        data[loteria][mes_key]["historial"].append({
            "fecha": fecha_str,
            "resultado": resultado
        })

        guardar(data)
        st.success("Resultado guardado correctamente")

    except:
        st.error("Formato inválido. Usa xx-xx-xx (00 a 99)")

# ================= PANEL =================
st.subheader("📌 Panel mensual 00–99")

def celda(num):
    marcas = panel[num]
    html = f"<b>{num}</b><br>"
    for m in marcas:
        html += f"<span style='color:{COLORES[m]};font-size:20px'>X</span>"
    return html

for base in [0, 25, 50, 75]:
    cols = st.columns(4)
    for i in range(4):
        n = f"{base + i:02d}"
        cols[i].markdown(
            f"<div style='border:1px solid #ccc; padding:10px; text-align:center'>{celda(n)}</div>",
            unsafe_allow_html=True
        )

# ================= HISTORIAL =================
st.subheader("🗂 Historial del mes")

for h in data[loteria][mes_key]["historial"]:
    st.write(f"📅 {h['fecha']} → 🎯 {h['resultado']}")
