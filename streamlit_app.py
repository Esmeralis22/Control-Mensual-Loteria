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

# ================= UTIL =================
def panel_html(conteos=None, modo_general=False):
    html = "<div style='display:grid;grid-template-columns:repeat(25,1fr);gap:4px;'>"
    for i in range(100):
        n = f"{i:02d}"

        color = "#2ecc71"  # verde por defecto
        if modo_general and conteos:
            c = conteos.get(n, 0)
            if c >= 5:
                color = "#e74c3c"
            elif c >= 3:
                color = "#f39c12"

        if modo_general:
            html += f"""
            <form method="post">
            <button name="num" value="{n}"
            style="width:38px;height:30px;
            background:{color};
            border:none;border-radius:4px;
            color:black;font-weight:bold;cursor:pointer;">
            {n}
            </button>
            </form>
            """
        else:
            html += f"""
            <div style="
            width:38px;height:30px;
            border:1px solid #999;
            text-align:center;
            font-size:12px;
            display:flex;
            align-items:center;
            justify-content:center;">
            {n}
            </div>
            """
    html += "</div>"
    return html

# ================= APP =================
st.title("📊 Control Mensual de Loterías")

loteria = st.selectbox("Seleccionar lotería", LOTERIAS)
mes = datetime.now().strftime("%Y-%m")

# ================= GENERAL =================
if loteria == "General":
    st.subheader("📌 Control General (Primera Posición)")

    conteos = {}
    for lot, meses in data.items():
        for m, registros in meses.items():
            if m != mes:
                continue
            for r in registros:
                n = r["numeros"][0]
                conteos[n] = conteos.get(n, 0) + 1

    st.markdown(panel_html(conteos, modo_general=True), unsafe_allow_html=True)

    if "num" in st.experimental_get_query_params():
        sel = st.experimental_get_query_params()["num"][0]
        st.subheader(f"📍 Detalle del {sel}")
        for lot, meses in data.items():
            for m, regs in meses.items():
                for r in regs:
                    if r["numeros"][0] == sel:
                        st.write(f"• {lot} | Posición 1 | {r['fecha']}")

    st.stop()

# ================= NORMAL =================
st.subheader(f"🎯 {loteria}")
resultado = st.text_input("Resultado (xx-xx-xx)")

if st.button("Guardar resultado"):
    try:
        nums = resultado.split("-")
        assert len(nums) == 3
        for n in nums:
            assert 0 <= int(n) <= 99

        data.setdefault(loteria, {}).setdefault(mes, []).append({
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "numeros": nums
        })
        guardar(data)
        st.success("Resultado guardado")
        st.rerun()
    except:
        st.error("Formato inválido")

st.markdown(panel_html(), unsafe_allow_html=True)
