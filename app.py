import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

## Configuración Inical

st.set_page_config(
    page_title="DoN Taquirou – Inteligencia de Localización",
    layout="wide"
)
st.title("🌮 DoN Taquirou - Dashboard")

## Contexto del Proyecto

st.subheader(
    "Inteligencia de localización para nuevos negocios: "
    "estrategia de selección de ubicaciones basada en datos abiertos "
    "(Caso DoN Taquirou – Manhattan, NYC)"
)

st.subheader("Objetivo de la investigación")

st.markdown(
    """
    Identificar la ubicación más adecuada para la apertura del restaurante
    **DoN Taquirou** en Manhattan, mediante un modelo analítico multicriterio
    basado en datos abiertos que integre indicadores de demanda potencial,
    coste, competencia, seguridad y perfil sociodemográfico, con el fin de
    maximizar el potencial de ventas y controlar los riesgos operativos y financieros.
    """
)

st.subheader("Justificación del uso de Streamlit en el marco del proyecto")

st.markdown(
    """
    Esta aplicación cumple una función **exploratoria y descriptiva** dentro
    del proceso de investigación. No ejecuta el modelo analítico multicriterio
    ni determina la ubicación óptima del restaurante. Su propósito es facilitar
    la **visualización, exploración y comprensión territorial** de diversas
    bases de datos sobre Manhattan, generando insumos analíticos que apoyen la
    toma de decisiones estratégicas en fases posteriores del estudio.
    """
)

st.divider()

## Carga de Bases de Datos

@st.cache_data(show_spinner="Cargando bases de datos…")
def cargar_datos():
    data = {
        "Restaurantes (Competencia)": pd.read_csv("data/01_Restaurantes_Manhattan.csv"),
        "Seguridad": pd.read_csv("data/02_Seguridad_Manhattan.csv"),
        "Censo – Edad y Sexo": pd.read_csv("data/03_Censo_Age_Sex_Manhattan.csv"),
        "Censo – Origen Hispano": pd.read_csv("data/04_Censo_Hispanic_Origin_Manhattan.csv"),
        "Censo – Tipo de Hogar": pd.read_csv("data/05_Censo_Household_Type_Manhattan.csv"),
        "Censo – Situación Laboral": pd.read_csv("data/06_Censo_Employment_Status_Manhattan.csv"),
        "Censo – Ingresos y Beneficios": pd.read_csv("data/07_Censo_Income_Benefits_Manhattan.csv"),
        "Censo – Ocupación de Vivienda": pd.read_csv("data/08_Censo_Housing_Occupancy_Manhattan.csv"),
        "Censo – Alquiler Bruto": pd.read_csv("data/09_Censo_Gross_Rent_Manhattan.csv"),
        "Movilidad (MTA)": pd.read_csv("data/10_MTA_Manhattan.csv"),
        "Lugares Comunes / Puntos de Interés": pd.read_csv("data/11_Common_Places_Manhattan.csv"),
        "Reseñas de Restaurantes": pd.read_csv("data/12_Restaurantes_Resenas.csv")
    }
    return data

datos = cargar_datos()

## Navegación (Sidebar)

st.sidebar.header("Exploración de bases de datos")

base_seleccionada = st.sidebar.selectbox(
    "Seleccione la base de datos a explorar:",
    list(datos.keys())
)

df = datos[base_seleccionada]

## Contexto Analítico de las Bases de Datos

contexto_bases = {

    "Restaurantes (Competencia)": {
        "Tipo de base": "Actividad económica (establecimientos)",
        "Nivel territorial": "Punto / local",
        "Uso analítico esperado": (
            "Análisis de competencia, densidad comercial, tipología de oferta gastronómica "
            "y condiciones sanitarias como insumo para evaluar presión competitiva"
        )
    },

    "Seguridad": {
        "Tipo de base": "Eventos delictivos",
        "Nivel territorial": "Punto / zona",
        "Uso analítico esperado": (
            "Exploración de patrones espaciales y temporales de criminalidad "
            "para identificar niveles de riesgo operativo por zona"
        )
    },

    "Censo – Edad y Sexo": {
        "Tipo de base": "Demografía estructural (censo)",
        "Nivel territorial": "Zona",
        "Uso analítico esperado": (
            "Caracterización de la estructura etaria y por sexo de la población "
            "para estimar perfiles de demanda potencial"
        )
    },

    "Censo – Origen Hispano": {
        "Tipo de base": "Composición étnica y cultural (censo)",
        "Nivel territorial": "Zona / subgrupo poblacional",
        "Uso analítico esperado": (
            "Exploración de la distribución territorial de la población de origen hispano "
            "como insumo cultural y demográfico"
        )
    },

    "Censo – Tipo de Hogar": {
        "Tipo de base": "Estructura de hogares (censo)",
        "Nivel territorial": "Zona",
        "Uso analítico esperado": (
            "Análisis de la composición de los hogares y presencia de menores o adultos mayores "
            "para inferir dinámicas de consumo y horarios"
        )
    },

    "Censo – Situación Laboral": {
        "Tipo de base": "Mercado laboral (censo)",
        "Nivel territorial": "Zona",
        "Uso analítico esperado": (
            "Caracterización de la situación laboral de la población "
            "como proxy de estabilidad económica y actividad cotidiana"
        )
    },

    "Censo – Ingresos y Beneficios": {
        "Tipo de base": "Ingresos y transferencias (censo)",
        "Nivel territorial": "Zona",
        "Uso analítico esperado": (
            "Exploración de la distribución de ingresos y beneficios "
            "para aproximar capacidad de consumo y segmentación socioeconómica"
        )
    },

    "Censo – Ocupación de Vivienda": {
        "Tipo de base": "Vivienda y ocupación residencial (censo)",
        "Nivel territorial": "Zona",
        "Uso analítico esperado": (
            "Análisis de viviendas ocupadas y vacantes "
            "como indicador de estabilidad residencial y presión inmobiliaria"
        )
    },

    "Censo – Alquiler Bruto": {
        "Tipo de base": "Mercado de alquiler residencial (censo)",
        "Nivel territorial": "Zona",
        "Uso analítico esperado": (
            "Exploración de niveles de alquiler bruto "
            "como proxy de coste de localización y gentrificación"
        )
    },

    "Movilidad (MTA)": {
        "Tipo de base": "Flujos de movilidad urbana",
        "Nivel territorial": "Estación / punto",
        "Uso analítico esperado": (
            "Análisis de volumen de pasajeros y accesibilidad "
            "para estimar tránsito peatonal y exposición comercial"
        )
    },

    "Lugares Comunes / Puntos de Interés": {
        "Tipo de base": "Infraestructura urbana y equipamientos",
        "Nivel territorial": "Punto",
        "Uso analítico esperado": (
            "Identificación de equipamientos y espacios de uso común "
            "como generadores de flujo y centralidad urbana"
        )
    },

    "Reseñas de Restaurantes": {
        "Tipo de base": "Texto no estructurado (percepción de usuarios)",
        "Nivel territorial": "Establecimiento / punto",
        "Uso analítico esperado": (
            "Exploración de percepción y satisfacción de clientes "
            "para complementar indicadores cuantitativos de competencia"
        )
    }

}

## Selección de Base de datos

st.subheader(f"Base de datos: {base_seleccionada}")

if base_seleccionada in contexto_bases:
    st.markdown("**Contexto analítico de la base:**")
    for k, v in contexto_bases[base_seleccionada].items():
        st.markdown(f"- **{k}:** {v}")

st.markdown(
    f"""
    **Dimensión del dataset**  
    - Filas: {df.shape[0]}  
    - Columnas: {df.shape[1]}
    """
)

st.markdown("**Columnas disponibles:**")
st.write(list(df.columns))

## Vista Exploratoria 

st.markdown("**Vista exploratoria de los datos (primeras 100 filas):**")
st.dataframe(df.head(100))

with st.expander("Ver dataset completo"):
    st.dataframe(df)

## Resumen Descriptivo de Variables Numéricas

columnas_numericas = df.select_dtypes(include=["int64", "float64"]).columns

if len(columnas_numericas) > 0:
    st.markdown("**Resumen descriptivo de variables numéricas:**")
    st.dataframe(
        df[columnas_numericas].describe()
    )
else:
    st.markdown(
        "_Este dataset no contiene variables numéricas para resumen descriptivo._"
    )

## Visualización Histograma variables numéricas

if len(columnas_numericas) > 0:
    columna_num = st.selectbox(
        "Seleccionar variable numérica para visualizar:",
        columnas_numericas
    )

    fig, ax = plt.subplots()
    df[columna_num].dropna().hist(ax=ax, bins=20)
    ax.set_title(f"Distribución de {columna_num}")
    ax.set_xlabel(columna_num)
    ax.set_ylabel("Frecuencia")

    st.pyplot(fig)


## Frecuencia de Variables Categóricas

columnas_categoricas = df.select_dtypes(include=["object"]).columns

if len(columnas_categoricas) > 0:
    columna_cat = st.selectbox(
        "Seleccionar variable categórica para ver frecuencias:",
        columnas_categoricas
    )

    st.markdown("**Frecuencia de valores:**")
    st.dataframe(
        df[columna_cat].value_counts().reset_index()
        .rename(columns={"index": columna_cat, columna_cat: "Frecuencia"})
    )
else:
    st.markdown(
        "_Este dataset no contiene variables categóricas para análisis de frecuencias._"
    )

## Visualización Barras de Frecuencias categóricas

if len(columnas_categoricas) > 0:
    fig, ax = plt.subplots()

    top_cat = df[columna_cat].value_counts().head(10)
    top_cat.plot(kind="bar", ax=ax)

    ax.set_title(f"Top 10 categorías – {columna_cat}")
    ax.set_xlabel(columna_cat)
    ax.set_ylabel("Frecuencia")
    plt.xticks(rotation=45, ha="right")

    st.pyplot(fig)
