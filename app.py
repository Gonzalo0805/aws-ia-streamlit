import streamlit as st
import pandas as pd

st.set_page_config(page_title="Modelador AWS para IA", layout="wide")

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
"disponibilidad_objetivo": "Alta",
}

# ------------------------

# FUNCIONES DE REGLAS

# ------------------------

def recomendar_inferencia(preferencia_estrategica):
if preferencia_estrategica == "Gestionado":
return "Amazon Bedrock (servicio gestionado, rápido despliegue)"
return "Amazon SageMaker (mayor control y personalización)"

def recomendar_seguridad(pii):
if pii:
return "Controles reforzados: cifrado, minimización de datos, revisión humana y cumplimiento."
return "Controles estándar de acceso y gobierno."

def recomendar_observabilidad(variabilidad_demanda):
if variabilidad_demanda == "Alta":
return "Monitorización en tiempo real, alertas de coste y escalado automático."
elif variabilidad_demanda == "Media":
return "Monitorización continua con revisión periódica de consumo."
return "Observabilidad básica con revisión mensual."

def generar_tradeoff(preferencia_estrategica):
if preferencia_estrategica == "Gestionado":
return "Se prioriza rapidez de despliegue y menor complejidad frente a control fino."
return "Se prioriza control fino y personalización frente a rapidez de implementación."

# ------------------------

# CAPAS ARQUITECTURA

# ------------------------

def generar_capas(datos):
return {
"Datos": "Repositorio documental interno del área de siniestros.",
"Integración": "Orquestación de flujos entre documentos, consultas y servicios IA.",
"Inferencia/Modelo": recomendar_inferencia(datos["preferencia_estrategica"]),
"Aplicación": "Interfaz interna para gestores y analistas.",
"Seguridad y Gobierno": recomendar_seguridad(datos["pii"]),
"Observabilidad y FinOps": recomendar_observabilidad(datos["variabilidad_demanda"]),
}

# ------------------------

# MATRIZ RAGA

# ------------------------

def generar_riesgos(datos):
riesgos = [
{
"Riesgo": "Exposición de datos personales (PII)",
"Mitigación": "Cifrado, control de acceso y revisión humana",
"Responsable": "Equipo de Seguridad",
},
{
"Riesgo": "Latencia superior al objetivo",
"Mitigación": "Optimización de consultas y pruebas de rendimiento",
"Responsable": "Arquitecto TI",
},
{
"Riesgo": "Sobrecoste en inferencia",
"Mitigación": "Control de uso y alertas FinOps",
"Responsable": "Equipo FinOps",
},
]
return pd.DataFrame(riesgos)

# ------------------------

# SLO / SLA

# ------------------------

def generar_slos(datos):
slos = [
{"Indicador": "Latencia máxima", "Valor": f"<= {datos['latencia_max_seg']} s"},
{"Indicador": "Disponibilidad", "Valor": datos["disponibilidad_objetivo"]},
{"Indicador": "Escalado a humano", "Valor": "Definir umbral para casos complejos"},
]
return pd.DataFrame(slos)

# ------------------------

# SIDEBAR INPUTS

# ------------------------

st.sidebar.header("Parámetros de entrada")

sector = st.sidebar.text_input("Sector", CASO_BASE["sector"])

documentos_diarios = st.sidebar.number_input(
"Documentos diarios", min_value=0, value=CASO_BASE["documentos_diarios"]
)

usuarios_simultaneos = st.sidebar.number_input(
"Usuarios simultáneos", min_value=0, value=CASO_BASE["usuarios_simultaneos"]
)

latencia_max_seg = st.sidebar.number_input(
"Latencia máxima (segundos)", min_value=1, value=CASO_BASE["latencia_max_seg"]
)

pii = st.sidebar.checkbox("¿Hay datos sensibles (PII)?", value=CASO_BASE["pii"])

presupuesto = st.sidebar.selectbox(
"Presupuesto", ["Bajo", "Medio", "Alto"], index=1
)

variabilidad_demanda = st.sidebar.selectbox(
"Variabilidad demanda", ["Baja", "Media", "Alta"], index=1
)

preferencia_estrategica = st.sidebar.selectbox(
"Preferencia estratégica", ["Gestionado", "Control fino"], index=0
)

disponibilidad_objetivo = st.sidebar.selectbox(
"Disponibilidad objetivo", ["Media", "Alta", "Muy alta"], index=1
)

datos = {
"sector": sector,
"documentos_diarios": documentos_diarios,
"usuarios_simultaneos": usuarios_simultaneos,
"latencia_max_seg": latencia_max_seg,
"pii": pii,
"presupuesto": presupuesto,
"variabilidad_demanda": variabilidad_demanda,
"preferencia_estrategica": preferencia_estrategica,
"disponibilidad_objetivo": disponibilidad_objetivo,
}

# ------------------------

# INTERFAZ PRINCIPAL

# ------------------------

st.title("Modelador de Arquitecturas AWS para IA")

st.subheader("1. Resumen ejecutivo")

st.write(
f"Para el sector {datos['sector']}, la propuesta prioriza "
f"{'rapidez y simplicidad' if datos['preferencia_estrategica']=='Gestionado' else 'control y personalización'}, "
f"considerando latencia, sensibilidad de datos y operación."
)

# ------------------------

# CAPAS

# ------------------------

st.subheader("2. Arquitectura por capas")

capas = generar_capas(datos)

for capa, descripcion in capas.items():
st.markdown(f"**{capa}:** {descripcion}")

# ------------------------

# TRADE-OFF

# ------------------------

st.subheader("3. Trade-off principal")

st.write(generar_tradeoff(datos["preferencia_estrategica"]))

# ------------------------

# RIESGOS

# ------------------------

st.subheader("4. Matriz RAGA")

st.dataframe(generar_riesgos(datos), use_container_width=True)

# ------------------------

# SLO

# ------------------------

st.subheader("5. SLO / SLA")

st.dataframe(generar_slos(datos), use_container_width=True)

# ------------------------

# REFLEXIÓN FINAL

# ------------------------

st.subheader("6. Reflexión del equipo")

st.info(
"Se prioriza un equilibrio entre control y eficiencia. "
"Se acepta un trade-off entre rapidez de despliegue y personalización, "
"manteniendo supervisión humana en procesos críticos."
)
