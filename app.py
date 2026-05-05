import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Modelador AWS IA", layout="wide")

# ------------------------
# CASO BASE
# ------------------------
CASO_BASE = {
    "sector": "Asegurador",
    "documentos_diarios": 18000,
    "usuarios_simultaneos": 220,
    "latencia_max_seg": 4,
    "pii": True,
    "presupuesto": "Medio",
    "variabilidad_demanda": "Media",
    "preferencia_estrategica": "Gestionado",
    "disponibilidad_objetivo": "Alta"
}

# ------------------------
# FUNCIONES
# ------------------------
def recomendar_inferencia(preferencia_estrategica):
    if preferencia_estrategica == "Gestionado":
        return "Amazon Bedrock (servicio gestionado, rápido despliegue)"
    else:
        return "Amazon SageMaker (mayor control y personalización)"

def recomendar_seguridad(pii):
    if pii:
        return "Cifrado, control de acceso, anonimización y revisión humana"
    else:
        return "Controles estándar de acceso"

def recomendar_observabilidad(variabilidad_demanda):
    if variabilidad_demanda == "Alta":
        return "Monitorización en tiempo real + alertas de coste"
    elif variabilidad_demanda == "Media":
        return "Monitorización continua con revisión periódica"
    else:
        return "Observabilidad básica"

def generar_tradeoff(preferencia_estrategica):
    if preferencia_estrategica == "Gestionado":
        return "Se prioriza rapidez y menor complejidad frente a control fino"
    else:
        return "Se prioriza control y personalización frente a rapidez"

def generar_capas(datos):
    return {
        "Datos": "Repositorio documental interno",
        "Integración": "Orquestación de flujos",
        "Inferencia": recomendar_inferencia(datos["preferencia_estrategica"]),
        "Aplicación": "Interfaz interna para usuarios",
        "Seguridad": recomendar_seguridad(datos["pii"]),
        "Observabilidad": recomendar_observabilidad(datos["variabilidad_demanda"])
    }

def generar_riesgos():
    data = [
        {"Riesgo": "Exposición de datos (PII)", "Mitigación": "Cifrado y control de accesos", "Responsable": "Seguridad"},
        {"Riesgo": "Latencia alta", "Mitigación": "Optimización y pruebas", "Responsable": "Arquitectura"},
        {"Riesgo": "Sobrecoste IA", "Mitigación": "Control de uso y alertas", "Responsable": "FinOps"}
    ]
    return pd.DataFrame(data)

def generar_slos(datos):
    data = [
        {"Indicador": "Latencia", "Valor": f"<= {datos['latencia_max_seg']} s"},
        {"Indicador": "Disponibilidad", "Valor": datos["disponibilidad_objetivo"]},
        {"Indicador": "Escalado humano", "Valor": "Casos complejos derivados"}
    ]
    return pd.DataFrame(data)

# ------------------------
# SIDEBAR
# ------------------------
st.sidebar.header("Parámetros")
sector = st.sidebar.text_input("Sector", CASO_BASE["sector"])
documentos = st.sidebar.number_input("Documentos diarios", value=CASO_BASE["documentos_diarios"])
usuarios = st.sidebar.number_input("Usuarios simultáneos", value=CASO_BASE["usuarios_simultaneos"])
latencia = st.sidebar.number_input("Latencia (segundos)", value=CASO_BASE["latencia_max_seg"])
pii = st.sidebar.checkbox("Datos sensibles (PII)", value=CASO_BASE["pii"])
presupuesto = st.sidebar.selectbox("Presupuesto", ["Bajo", "Medio", "Alto"], index=1)
variabilidad = st.sidebar.selectbox("Variabilidad demanda", ["Baja", "Media", "Alta"], index=1)
preferencia = st.sidebar.selectbox("Estrategia", ["Gestionado", "Control fino"], index=0)
disponibilidad = st.sidebar.selectbox("Disponibilidad", ["Media", "Alta", "Muy alta"], index=1)

datos = {
    "sector": sector,
    "documentos_diarios": documentos,
    "usuarios_simultaneos": usuarios,
    "latencia_max_seg": latencia,
    "pii": pii,
    "presupuesto": presupuesto,
    "variabilidad_demanda": variabilidad,
    "preferencia_estrategica": preferencia,
    "disponibilidad_objetivo": disponibilidad
}

# ------------------------
# UI PRINCIPAL
# ------------------------
st.title("Modelador AWS para IA")

# 1. Resumen
st.subheader("1. Resumen ejecutivo")
st.write(
    f"Para el sector **{sector}**, se propone una solución que prioriza "
    f"{'**rapidez y simplicidad**' if preferencia == 'Gestionado' else '**control y personalización**'}."
)

# 2. Capas
st.subheader("2. Arquitectura por capas")
capas = generar_capas(datos)
for k, v in capas.items():
    st.write(f"**{k}:** {v}")

# 3. Trade-off
st.subheader("3. Trade-off")
st.write(generar_tradeoff(preferencia))

# 4. Riesgos
st.subheader("4. Riesgos (RAGA)")
st.dataframe(generar_riesgos(), use_container_width=True)

# 5. SLO
st.subheader("5. SLO / SLA")
st.dataframe(generar_slos(datos), use_container_width=True)

# 6. Reflexión
st.subheader("6. Reflexión")
st.info(
    "Se equilibra rapidez y control. Se prioriza eficiencia operativa manteniendo supervisión humana."
)
