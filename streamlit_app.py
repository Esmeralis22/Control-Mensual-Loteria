import streamlit as st
import json
import os

DATA_FILE = "resultados.json"

# -------------------------
# Cargar / Guardar
# -------------------------
def cargar_datos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf8") as f:
            return json.load(f)
    return {}

def guardar_datos(data):
    with open(DATA_FILE, "w", encoding="utf8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# -------------------------
# Inicialización
# -------------------------
st.set_page_config(layout="wide")

datos = cargar_datos()

# Estructura segura
if "salidas" not in datos:
    datos["salidas"] = {}

# -------------------------
# Registrar resultado
# -------------------------
st.sidebar.title("Registrar resultado")

num_registro = st.sidebar.selectbox(
    "Número",
    [f"{i:02d}" for i in range(1, 100)]
)

if st.sidebar.button("Registrar salida"):
    datos["salidas"].setdefault(num_registro, 0)
    datos["salidas"][num_registro] += 1
    guardar_datos(datos)
    st.rerun()

# -------------------------
# Color según salidas
# -------------------------
def color_por_salidas(cantidad):
    if cantidad <= 2:
        return "#2ecc71"   # verde
    elif cantidad <= 4:
        return "#f39c12"   # naranja
    else:
        return "#e74c3c"   # rojo

# -------------------------
# CONTROL GENERAL
# -------------------------
st.title("📊 Control General de Todas las Loterías")

cols = st.columns(10)

for i in range(1, 100):
    num = f"{i:02d}"
    cantidad = datos["salidas"].get(num, 0)
    color = color_por_salidas(cantidad)

    with cols[(i - 1) % 10]:
        st.markdown(
            f"""
            <a href="?num={num}" style="
                display:flex;
                align-items:center;
                justify-content:center;
                height:36px;
                background:{color};
                border-radius:6px;
                font-weight:bold;
                text-decoration:none;
                color:black;
                margin-bottom:6px;">
                {num}<br>
                <span style="font-size:10px;">{cantidad}</span>
            </a>
            """,
            unsafe_allow_html=True
        )

# -------------------------
# Detalle del número
# -------------------------
params = st.query_params
if "num" in params:
    n = params["num"]
    total = datos["salidas"].get(n, 0)

    st.divider()
    st.subheader(f"Detalle del número {n}")
    st.write(f"Salidas registradas: **{total}**")
