import streamlit as st
import json
import os
from datetime import datetime

# ================= CONFIG =================
st.set_page_config(layout="wide")
DATA_FILE = "historial_loterias.json"

USUARIO_OK = "Esteban"
CLAVE_OK = "15061998"

LOTERIAS = [
    "Anguilla 10:00 AM", "Anguilla 1:00 PM", "Anguilla 6:00 PM", "Anguilla 9:00 PM",
    "Primera Dia", "Primera Noche", "Lotedom", "La Suerte MD", "La Suerte 6PM",
    "Real", "Gana Mas", "Florida Dia", "Florida Noche",
    "New York Dia", "New York Noche", "Loteka", "Leidsa", "Loteria Nacional",
    "General"
]

# ================= DATA =================
def cargar():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf8") as f:
            return json.load(f)
    return {}

def guardar(d):
    with open(DATA_FILE, "w", encoding="utf8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

data = cargar()
mes_actual = datetime.now().strftime("%Y-%m")

# ================= LOGIN =================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Acceso")
    u = st.text_input("Usuario")
    c = st.text_input("Clave", type="password")
    if st.button("Entrar"):
        if u == USUARIO_OK and c == CLAVE_OK:
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Credenciales incorrectas")
    st.stop()

# ================= PANEL NORMAL =================
def panel_loteria(registros):
    puntos = {f"{i:02d}": [] for i in range(100)}

    for r in registros:
        if "numeros" not in r or not isinstance(r["numeros"], list):
            continue
        for i, n in enumerate(r["numeros"]):
            if i == 0:
                puntos[n].append("red")
            elif i == 1:
                puntos[n].append("orange")
            elif i == 2:
                puntos[n].append("green")

    html = "<div style='display:grid;grid-template-columns:repeat(25,1fr);gap:4px;'>"
    for i in range(100):
        n = f"{i:02d}"
        dots = ""
        for c in puntos[n]:
            dots += f"<span style='color:{c};font-size:10px'>●</span>"
        html += f"""
        <div style="
        width:38px;height:30px;
        border:1px solid #999;
        text-align:center;
        font-size:12px;
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;">
        {n}
        <div>{dots}</div>
        </div>
        """
    html += "</div>"
    return html

# ================= PANEL GENERAL =================
def panel_general(conteos):
    html = "<div style='display:grid;grid-template-columns:repeat(25,1fr);gap:4px;'>"
    for i in range(100):
        n = f"{i:02d}"
        c = conteos.get(n, 0)

        if c >= 5:
            color = "#e74c3c"
        elif c >= 3:
            color = "#f39c12"
        else:
            color = "#2ecc71"

        html += f"""
        <form method="post">
        <button name="num" value="{n}"
        style="width:38px;height:30px;
        background:{color};
        border:none;border-radius:4px;
        font-weight:bold;cursor:pointer;">
        {n}
        </button>
        </form>
        """
    html += "</div>"
    return html

# ================= APP =================
st.title("📊 Control Mensual de Loterías")
loteria = st.selectbox("Seleccionar lotería", LOTERIAS)

# ================= GENERAL =================
if loteria == "General":
    st.subheader("📌 Control General (Primera Posición)")

    conteos = {}

    for lot, meses in data.items():
        for m, registros in meses.items():
            if m != mes_actual:
                continue
            for r in registros:
                if "numeros" not in r:
                    continue
                if not isinstance(r["numeros"], list):
                    continue
                if len(r["numeros"]) < 1:
                    continue

                n = r["numeros"][0]
                conteos[n] = conteos.get(n, 0) + 1

    st.markdown(panel_general(conteos), unsafe_allow_html=True)

    if "num" in st.experimental_get_query_params():
        sel = st.experimental_get_query_params()["num"][0]
        st.subheader(f"📍 Historial del {sel}")
        for lot, meses in data.items():
            for m, registros in meses.items():
                for r in registros:
                    if "numeros" in r and isinstance(r["numeros"], list):
                        if r["numeros"][0] == sel:
                            st.write(f"• {lot} | Posición 1 | {r['fecha']}")

    st.stop()

# ================= LOTERIAS =================
st.subheader(f"🎯 {loteria}")

resultado = st.text_input("Resultado (xx-xx-xx)")
col1, col2 = st.columns(2)

with col1:
    if st.button("Guardar resultado"):
        try:
            nums = resultado.split("-")
            assert len(nums) == 3
            for n in nums:
                assert 0 <= int(n) <= 99

            data.setdefault(loteria, {}).setdefault(mes_actual, []).append({
                "fecha": datetime.now().strftime("%d/%m/%Y"),
                "numeros": nums
            })
            guardar(data)
            st.success("Resultado guardado")
            st.rerun()
        except:
            st.error("Formato inválido")

with col2:
    if st.button("Eliminar último resultado"):
        try:
            data[loteria][mes_actual].pop()
            guardar(data)
            st.warning("Último resultado eliminado")
            st.rerun()
        except:
            st.error("No hay resultados para eliminar")

registros = data.get(loteria, {}).get(mes_actual, [])
st.markdown(panel_loteria(registros), unsafe_allow_html=True)


