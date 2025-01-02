import streamlit as st 
import requests

# ------------------------------------------------------------
# CONFIGURACIÓN INICIAL DE LA PÁGINA
# ------------------------------------------------------------
st.set_page_config(
    page_title="Agente de Traducción Médica",
    layout="centered"
)

# ------------------------------------------------------------
# CSS PERSONALIZADO PARA BOTONES Y ESTILOS GENERALES
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Importar fuentes */
    @import url('https://fonts.googleapis.com/css2?family=Soleil:wght@400;600&display=swap');

    /* Estilos Generales */
    body {
        font-family: 'Soleil', sans-serif;
        background-color: #eef2fc; /* Fondo azul claro */
        color: #1d242d; /* Texto principal en gris oscuro */
    }

    /* Encabezado y Logo */
    .logo {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px 0;
    }

    /* Tarjeta de Bienvenida */
    .welcome-card {
        background-color: #ffffff;
        border-radius: 15px;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
        padding: 2rem;
        text-align: center;
        margin: 2rem auto;
        max-width: 700px;
    }

    .welcome-card h3 {
        color: #4e20e2; /* Morado principal */
        font-size: 2.5em;
        margin-bottom: 1rem;
    }

    .welcome-card p {
        color: #333333;
        font-size: 1.1em;
        line-height: 1.6;
        margin-bottom: 2rem;
    }

    /* Bloques Destacados */
    .highlight-block {
        background-color: #eef2fc; /* Fondo azul claro */
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        color: #4e20e2;
    }

    .highlight-block h4 {
        font-size: 1.5em;
        margin-bottom: 1rem;
    }

    .highlight-block p {
        font-size: 1.1em;
        line-height: 1.6;
    }

    /* Estilos para Botones de Streamlit */
       /* Botón Primary */
    button[kind="primary"] {
        background-color: #4e20e2 !important; /* Morado oscuro */
        color: white !important;
        border: none !important;
        border-radius: 25px !important; /* Botón redondeado */
        padding: 0.8em 2em !important;
        font-size: 1em !important;
        cursor: pointer !important;
        transition: background-color 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);        padding: 0.6em 1.2em !important;
    }

    button[kind="primary"]:hover {
        background-color: #3e1fff !important; /* Morado claro al hacer hover */
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
        color: #4e20e2 !important; /* Texto morado */
        border: none !important;
        padding: 0.6em 1.2em !important;
        font-size: 16px !important;
        cursor: pointer !important;
        text-decoration: underline !important; /* Subrayado para diferenciar */
    }

    button[kind="tertiary"]:hover {
        color: #3e1fff !important; /* Texto morado claro al hacer hover */
        text-decoration: none !important; /* Sin subrayado */
    }

    /* Estilos para Text Areas */
    .stTextArea textarea {
        background-color: #ffffff;
        border: 1px solid #4e20e2;
        border-radius: 10px;
        padding: 1em;
        font-size: 1em;
        font-family: 'Soleil', sans-serif;
        color: #1d242d;
    }

    /* Estilos para Select Boxes */
    .stSelectbox select {
        background-color: #ffffff;
        border: 1px solid #4e20e2;
        border-radius: 10px;
        padding: 0.5em;
        font-size: 1em;
        font-family: 'Soleil', sans-serif;
        color: #1d242d;
    }

    /* Mejorar la apariencia de los botones de carga de archivos */
    .stFileUploader > div > div > div {
        background-color: #ffffff;
        border: 2px dashed #4e20e2;
        border-radius: 10px;
        padding: 1.5em;
        text-align: center;
        color: #4e20e2;
        font-family: 'Soleil', sans-serif;
    }

    /* Estilos para Mensajes de Éxito y Error */
    .stAlert > div {
        border-left: 5px solid #4e20e2;
    }

    /* Responsividad */
    @media (max-width: 768px) {
        .welcome-card {
            padding: 1.5rem;
            margin: 1rem;
        }

        .stButton button {
            width: 100%;
            padding: 0.6em 1em !important;
            font-size: 0.9em !important;
        }
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
st.markdown('<a href="https://vidasprime.es" class="logo svg"><img src="https://vidasprime.es/wp-content/uploads/2022/06/logo_vidas_prime_morado.png" width="250"></a>', unsafe_allow_html=True)

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
    "ca": "Catalán",
    "es": "Español",
    "en": "Inglés",
    "fr": "Francés",
    "de": "Alemán",
}

# ------------------------------------------------------------
# PANTALLA DE BIENVENIDA
# ------------------------------------------------------------
if st.session_state["pantalla_bienvenida"]:
    st.markdown(
        """
        <div class='welcome-card'>
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

    com_but_col1, com_but_col2 = st.columns([2,3], border=False)

    # Único botón "Comenzar" dentro de la pantalla de bienvenida
    if com_but_col2.button("Comenzar", help="Iniciar la aplicación", key="comenzar_btn", type='primary'):
        st.session_state["pantalla_bienvenida"] = False
        st.rerun()
    st.stop()  # Detener la ejecución aquí para no mostrar la sección principal

# ------------------------------------------------------------
# SECCIÓN PRINCIPAL
# ------------------------------------------------------------
#st.markdown("## Agente de Traducción")

# Bloque destacado añadido (UXM-001)
st.markdown(
    """
    <div class='highlight-block'>
        <h2>Agente de Traducción Médica</h2>
        <p>
            Ofrecemos una solución rápida y confiable para traducir documentación médica, ayudando a 
            mejorar la comunicación entre profesionales y pacientes.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Selección de idiomas
st.markdown("### Configuración de idiomas")
col1, col2 = st.columns(2)
with col1:
    st.session_state["idioma_entrada"] = st.selectbox(
        "Idioma de entrada",
        options=list(disponible_idiomas.keys()),
        format_func=lambda x: disponible_idiomas[x],
        index=list(disponible_idiomas.keys()).index("ca")  # Español por defecto
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


st.markdown("### Información de entrada")

texto_col1, texto_col2 = st.columns([2,1], vertical_alignment= "center")  

# Botones para modificar el área de texto
uploaded_file = texto_col1.file_uploader("Carga un archivo (txt)", type=["txt"], key="file_uploader")
if uploaded_file is not None:
    try:
        file_content = uploaded_file.read().decode("utf-8")
        st.session_state["texto_actual"] = file_content
        st.success("Archivo cargado correctamente.")
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
    # No necesitas st.rerun()

if texto_col2.button("... o carga un ejemplo", help="Cargar un texto de ejemplo", key="cargar_ejemplo_btn", type='tertiary'):
    st.session_state["texto_actual"] = (
        "Antecedentes familiares:\n"
        "- Antecedents familiars (Hermano): Hermano con antecedentes de laringotraqueomalacia leve. Laringitis y broncoespasmos de repetición.\n"
        "- Antecedents familiars (Madre): Padres no consanguíneos, niegan endogamia. Oriundos de Emiratos Árabes Unidos, en poblaciones distintas cerca de Dubái. Madre G4, con deseo gestacional ulterior. Niega abortos. Madre con 15 hermanos (8 hombres, 8 mujeres). Sin antecedentes de importancia. Padre con 3 hermanos y 3 medios hermanos con alteraciones laríngeas no especificadas, sin conocer la edad de inicio de alteraciones. No refieren otros antecedentes familiares de interés. Antecedentes de rasgo talasémico en progenitores, pero DIFERENTE gen. Aportan informe: Madre alfa trait. Padre: Beta minor trait."
    )
    # No usaremos st.rerun()


st.markdown("### Traducción")

# ------------------------------------------------------------
# Mostrar el área de texto unificada después de manejar los botones
# ------------------------------------------------------------
st.text_area(
    "Texto a traducir",
    key="texto_actual",
    placeholder="Introduzca el texto aquí",
    height=200,
)

# ------------------------------------------------------------
# LÓGICA DE TRADUCCIÓN VIA INFERENCE API
# ------------------------------------------------------------

# Botón "Traducir" para traducir
if st.button("Traducir", help="Traduce el texto", key="traducir_btn", type='primary'):
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
