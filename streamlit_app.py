import streamlit as st
import json
import os
from datetime import datetime

# ================= LOGIN =================
if "login_ok" not in st.session_state:
    st.session_state.login_ok = False

if not st.session_state.login_ok:
    st.title("🔐 Acceso a la aplicación")

    user = st.text_input("Usuario")
    pwd = st.text_input("Clave", type="password")

    if st.button("Entrar"):
        if user == "Esteban" and pwd == "15061998":
            st.session_state.login_ok = True
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

    st.stop()

# ================= CONFIG =================
DATA_FILE = "historial_loterias.json"

LOTERIAS = [
    "General",
    "Anguilla 10:00 AM", "Anguilla 1:00 PM", "Anguilla 6:00 PM", "Anguilla 9:00 PM",
    "Primera Dia", "Primera Noche", "Lotedom", "La Suerte MD", "La Suerte 6PM",
    "Real", "Gana Mas", "Florida Dia", "Florida Noche",
    "New York Dia", "New York Noche",
    "Loteka", "Leidsa", "Loteria Nacional"
]

COLORES = ["red", "orange", "green"]
POSICION = ["Primera", "Segunda", "Tercera"]

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

def conteo_general_primera(numero, data):
    total = 0
    for lot, meses in data.items():
        for mes, info in meses.items():
            for h in info["historial"]:
                nums = h["resultado"].split("-")
                if nums and nums[0] == numero:
                    total += 1
    return total

# ================= UI =================
st.set_page_config(layout="wide")
st.title("📊 Control Mensual de Loterías")

data = cargar()
loteria = st.selectbox("Selecciona la lotería", LOTERIAS)

fecha = datetime.now()
mes_key = fecha.strftime("%Y-%m")
fecha_str = fecha.strftime("%d/%m/%Y")

# ================= PANEL GENERAL =================
if loteria == "General":

    st.subheader("🌐 Control General de Todas las Loterías")

    if "num_general" not in st.session_state:
        st.session_state.num_general = None

    @st.dialog("Detalle del número")
    def mostrar_detalle(numero):
        encontrado = False
        for lot, meses in data.items():
            for mes, info in meses.items():
                for h in info["historial"]:
                    nums = h["resultado"].split("-")
                    if numero in nums:
                        pos = nums.index(numero)
                        st.write(
                            f"🎯 **{lot}** | 📅 {h['fecha']} | 📍 {POSICION[pos]}"
                        )
                        encontrado = True
        if not encontrado:
            st.info("Este número no ha salido en ninguna lotería.")

    for fila in range(4):
        cols = st.columns(25)
        for col in range(25):
            n = f"{fila*25 + col:02d}"
            c = conteo_general_primera(n, data)

            if c <= 2:
                color = "#2ecc71"
            elif c <= 4:
                color = "#f39c12"
            else:
                color = "#e74c3c"

            if cols[col].markdown(
                f"""
                <div
                    style="
                        height:36px;
                        background:{color};
                        border-radius:6px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        font-weight:bold;
                        cursor:pointer;"
                    onclick="window.parent.postMessage('{n}', '*')">
                    {n}
                </div>
                """,
                unsafe_allow_html=True
            ):
                pass

    st.markdown("""
    <script>
    window.addEventListener("message", (e) => {
        if (e.data) {
            window.parent.postMessage({ type: "streamlit:setState", value: e.data }, "*");
        }
    });
    </script>
    """, unsafe_allow_html=True)

    if "clicked" in st.session_state:
        mostrar_detalle(st.session_state.clicked)
        del st.session_state.clicked

    st.stop()

# ================= LOTERÍAS NORMALES =================
data.setdefault(loteria, {})
data[loteria].setdefault(mes_key, {
    "panel": nuevo_panel(),
    "historial": []
})

panel = data[loteria][mes_key]["panel"]
historial = data[loteria][mes_key]["historial"]

st.subheader(f"🎯 Lotería seleccionada: **{loteria}**")
st.caption(f"Mes activo: **{mes_key}** | Fecha del sistema: **{fecha_str}**")

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
        st.rerun()

    except Exception:
        st.error("Formato inválido")

if st.button("🗑️ Eliminar último resultado"):
    if historial:
        ultimo = historial.pop()
        nums = ultimo["resultado"].split("-")
        for i, n in enumerate(nums):
            if panel[n]:
                panel[n].pop()
        guardar(data)
        st.rerun()

# ================= PANEL =================
st.subheader("📌 Panel mensual 00–99")

def celda(num):
    puntos = ""
    for m in panel[num]:
        puntos += f"<span style='color:{COLORES[m]};font-size:10px;'>●</span>"
    return f"""
    <div style="height:36px;display:flex;flex-direction:column;align-items:center;justify-content:center;">
        <div style="font-weight:bold;">{num}</div>
        <div>{puntos}</div>
    </div>
    """

for fila in range(4):
    cols = st.columns(25)
    for col in range(25):
        n = f"{fila*25 + col:02d}"
        cols[col].markdown(
            f"<div style='border:1px solid #ccc;height:46px'>{celda(n)}</div>",
            unsafe_allow_html=True
        )

st.subheader("🗂 Historial del mes")
for h in historial:
    st.write(f"📅 {h['fecha']} → 🎯 {h['resultado']}")


