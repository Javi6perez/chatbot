import streamlit as st 
import requests

# ------------------------------------------------------------
# CONFIGURACIÓN INICIAL DE LA PÁGINA
# ------------------------------------------------------------
st.set_page_config(
    page_title="Agente de Traducción Médica",
    layout="wide"
)

# ------------------------------------------------------------
# CSS PERSONALIZADO PARA BOTONES
# ------------------------------------------------------------
# CSS actualizado para botones primary, secondary y tertiary con cambios en el secondary
st.markdown(
    """
    <style>
    /* Botón Primary */
    button[kind="primary"] {
        background-color: #5a189a !important; /* Morado oscuro */
        color: white !important;
        border: none !important;
        border-radius: 5px !important;
        padding: 0.6em 1.2em !important;
        font-size: 16px !important;
        cursor: pointer !important;
    }

    button[kind="primary"]:hover {
        background-color: #7b2cbf !important; /* Morado claro al hacer hover */
        color: #ffffff !important;
    }

    /* Botón Secondary (nuevo diseño) */
    button[kind="secondary"] {
        background-color: #d3a5fa !important; /* Morado claro */
        color: #5a189a !important; /* Texto morado oscuro */
        border: none !important;
        border-radius: 5px !important;
        padding: 0.6em 1.2em !important;
        font-size: 16px !important;
        cursor: pointer !important;
    }

    button[kind="secondary"]:hover {
        background-color: #dcbcf7 !important; /* Fondo más claro al hacer hover */
        color: #7b2cbf !important; /* Texto morado más claro */
    }

    /* Botón Tertiary */
    button[kind="tertiary"] {
        background-color: transparent !important; /* Fondo transparente */
        color: #5a189a !important; /* Texto morado */
        border: none !important;
        padding: 0.6em 1.2em !important;
        font-size: 16px !important;
        cursor: pointer !important;
        text-decoration: underline !important; /* Subrayado para diferenciar */
    }

    button[kind="tertiary"]:hover {
        color: #7b2cbf !important; /* Texto morado claro al hacer hover */
        text-decoration: none !important; /* Sin subrayado */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# FUNCIONES AUXILIARES
# ------------------------------------------------------------
def translate_text(input_text, source_lang, target_lang):
    """
    Traduce texto usando la API de Hugging Face.
    Parámetros:
    - input_text: Texto a traducir.
    - source_lang: Idioma de origen (código, e.g., 'es').
    - target_lang: Idioma de destino (código, e.g., 'en').
    Retorna:
    - (success, message_or_text)
    """
    API_URL = f"https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"
    headers = {"Authorization": f"Bearer {st.secrets['huggingface']['api_token']}"}
    payload = {"inputs": input_text}

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                return True, data[0].get("translation_text", "")
            else:
                return False, "No se recibió traducción válida."
        elif response.status_code == 503:
            # Modelo en proceso de carga
            data = response.json()
            estimated_time = data.get("estimated_time", "Desconocido")
            return False, f"El modelo está cargándose. Tiempo estimado: {estimated_time} s."
        else:
            return False, f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return False, f"Error de conexión o formato: {str(e)}"

# ------------------------------------------------------------
# LOGO
# ------------------------------------------------------------
st.image("https://vidasprime.es/wp-content/uploads/2022/06/logo_vidas_prime_morado.png", width=200)

# ------------------------------------------------------------
# CONTROL DE ESTADO
# ------------------------------------------------------------
if "pantalla_bienvenida" not in st.session_state:
    st.session_state["pantalla_bienvenida"] = True

if "idioma_entrada" not in st.session_state:
    st.session_state["idioma_entrada"] = "es"  # Español por defecto

if "idioma_salida" not in st.session_state:
    st.session_state["idioma_salida"] = "en"  # Inglés por defecto

if "texto_actual" not in st.session_state:
    st.session_state["texto_actual"] = ""

# Lista de idiomas disponibles
disponible_idiomas = {
    "es": "Español",
    "en": "Inglés",
    "fr": "Francés",
    "de": "Alemán",
    "ca": "Catalán",
}

# ------------------------------------------------------------
# PANTALLA DE BIENVENIDA
# ------------------------------------------------------------
if st.session_state["pantalla_bienvenida"]:
    st.markdown(
        """
        <div class='section'>
            <h3>📢 Bienvenido/a</h3>
            <p>
                Este agente está diseñado para <b>facilitar la traducción precisa y comprensible</b>
                de textos médicos, informes clínicos y otra documentación relacionada con la salud. 
                Su objetivo es mejorar la comunicación entre pacientes, profesionales sanitarios 
                y colaboradores de VidasPrime.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Único botón "Comenzar" dentro de la pantalla de bienvenida
    if st.button("Comenzar", help="Iniciar la aplicación", key="comenzar_btn", type='primary'):
        st.session_state["pantalla_bienvenida"] = False
        st.rerun()
    st.stop()  # Detener la ejecución aquí para no mostrar la sección principal

# ------------------------------------------------------------
# SECCIÓN PRINCIPAL
# ------------------------------------------------------------
st.markdown("## Agente de Traducción")

# Selección de idiomas
st.markdown("### Configuración de idiomas")
col1, col2 = st.columns(2)
with col1:
    st.session_state["idioma_entrada"] = st.selectbox(
        "Idioma de entrada",
        options=list(disponible_idiomas.keys()),
        format_func=lambda x: disponible_idiomas[x],
        index=list(disponible_idiomas.keys()).index("es")  # Español por defecto
    )
with col2:
    st.session_state["idioma_salida"] = st.selectbox(
        "Idioma de salida",
        options=list(disponible_idiomas.keys()),
        format_func=lambda x: disponible_idiomas[x],
        index=list(disponible_idiomas.keys()).index("en")  # Inglés por defecto
    )

# ------------------------------------------------------------
# MANEJO DE BOTONES ANTES DEL TEXT_AREA
# ------------------------------------------------------------
st.markdown("### Introduce texto, sube un archivo o carga el ejemplo")

# Botones para modificar el área de texto

uploaded_file = st.file_uploader("Cargar archivo (txt)", type=["txt"], key="file_uploader")
if uploaded_file is not None:
    try:
        file_content = uploaded_file.read().decode("utf-8")
        st.session_state["texto_actual"] = file_content
        st.success("Archivo cargado correctamente.")
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
    # No necesitas st.rerun()

col_bot1, col_bot2= st.columns([1,5])

with col_bot1:
    col_bot1.markdown("### Texto para traducir")

with col_bot2:
    if st.button("Cargar ejemplo", help="Cargar un texto de ejemplo", key="cargar_ejemplo_btn", type='tertiary'):
        st.session_state["texto_actual"] = (
            "Antecedentes familiares:\n"
            "- Antecedents familiars (Hermano): Hermano con antecedentes de laringotraqueomalacia leve. Laringitis y broncoespasmos de repetición.\n"
            "- Antecedents familiars (Madre): Padres no consanguíneos, niegan endogamia. Oriundos de Emiratos Árabes Unidos, en poblaciones distintas cerca de Dubái. Madre G4, con deseo gestacional ulterior. Niega abortos. Madre con 15 hermanos (8 hombres, 8 mujeres). Sin antecedentes de importancia. Padre con 3 hermanos y 3 medios hermanos con alteraciones laríngeas no especificadas, sin conocer la edad de inicio de alteraciones. No refieren otros antecedentes familiares de interés. Antecedentes de rasgo talasémico en progenitores, pero DIFERENTE gen. Aportan informe: Madre alfa trait. Padre: Beta minor trait."
        )
        # No usaremos st.rerun()

# ------------------------------------------------------------
# Mostrar el área de texto unificada después de manejar los botones
# ------------------------------------------------------------
st.text_area(
    "Texto a traducir",
    key="texto_actual",
    height=200,
)

# ------------------------------------------------------------
# LÓGICA DE TRADUCCIÓN VIA INFERENCE API
# ------------------------------------------------------------

# Botón "Traducir" para traducir
if st.button("Traducir", help="Traduce el texto", key="traducir_btn", type= 'primary'):
    if not st.session_state["texto_actual"].strip():
        st.warning("Por favor, ingresa algún texto o carga un archivo válido.", icon="⚠️")
    else:
        with st.spinner("Traduciendo..."):
            success, result_text = translate_text(
                st.session_state["texto_actual"],
                st.session_state["idioma_entrada"],
                st.session_state["idioma_salida"],
            )
        if success:
            st.success("Traducción completada con éxito.")
            st.text_area("Texto traducido:", result_text, height=200)
        else:
            st.error(result_text)

st.markdown("</div>", unsafe_allow_html=True)
