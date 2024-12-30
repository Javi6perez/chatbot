import streamlit as st
import requests

# ------------------------------------------------------------
# CONFIGURACIÓN INICIAL DE LA PÁGINA
# ------------------------------------------------------------
st.set_page_config(
    page_title="Agente de Traducción Médica"
)
#st.markdown("<div class='otro'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,1,1])
# Muestra el logo de VidasPrime (ajusta la ruta o URL a tu imagen).
col1.image("https://www.sjdhospitalbarcelona.org/themes/hsjd/assets/img/logo.svg", width=250)
# Muestra el logo de VidasPrime (ajusta la ruta o URL a tu imagen).
col3.image("https://vidasprime.es/wp-content/uploads/2020/10/logovidasprime_01.svg", width=200)

# ------------------------------------------------------------
# CSS PERSONALIZADO PARA LA BARRA SUPERIOR Y BOTONES
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Espacio superior para no tapar el contenido */
    .main {
        margin-top: 70px;
        padding: 20px;
    }

    /* Secciones con fondo y borde */
    .section {
        background-color: #fafafa;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 20px;
        margin-bottom: 20px;
    }
    </style>
    
    """,
    unsafe_allow_html=True
)
# ------------------------------------------------------------
# CONTENEDOR PRINCIPAL
# ------------------------------------------------------------

# ------------------------------------------------------------
# CONTROL DE PANTALLA DE BIENVENIDA
# ------------------------------------------------------------
if "pantalla_bienvenida" not in st.session_state:
    st.session_state["pantalla_bienvenida"] = True

# ------------------------------------------------------------
# PANTALLA DE BIENVENIDA
# ------------------------------------------------------------
if st.session_state["pantalla_bienvenida"]:
    st.markdown(
        """
        <div class='section'>
            <h3>Bienvenido/a</h3>
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

    # Único botón "Comenzar"
    if st.button("Comenzar", help="Iniciar la aplicación", type="primary"):
        st.session_state["pantalla_bienvenida"] = False

    st.stop()  # Detenemos la ejecución para que no se muestre lo demás

# ------------------------------------------------------------
# SECCIÓN PRINCIPAL (SI YA SE PASÓ LA BIENVENIDA)
# ------------------------------------------------------------

# 1) Selección de idiomas
#st.subheader("Seleccione idiomas")
#col1, col2 = st.columns(2)

#idioma_entrada = col1.selectbox("Idioma de entrada", ["Sin especificar", "Español", "Inglés", "Francés", "Alemán"], index=0)
#idioma_salida = col2.selectbox("Idioma de salida", ["Sin especificar", "Inglés", "Francés", "Alemán"], index=0)

#st.markdown("</div>", unsafe_allow_html=True)

# 2) Campo de texto
st.subheader("Texto para analizar o traducir")
user_prompt = st.text_area(
    label="Ingresa el texto",
    placeholder="Texto a traducir",
    height=100,
    value=st.session_state.get("ejemplo_cargado", "")  # Carga el ejemplo si ya se cargó

)

col_bot1, col_bot3 = st.columns([6,1])

# Botón para cargar el ejemplo
if col_bot1.button("Cargar ejemplo", type="secondary"):
    st.session_state["ejemplo_cargado"] = "Antecedentes familiares: \n \
                - Antecedents familiars (Hermano): Hermano con antecedentes de laringotraqueomalacia leve. Laringitis y broncoespasmos de repetición. \n\
                - Antecedents familiars (Madre): Padres no consanguíneos, niegan endogamia. Oriundos de Emiratos Arabes Unidos, en poblaciones distintas cerca de Dubai. Madre G4, con deseo gestacional ulterior. Niega abortos. Madre con 15 hermanos (8 hormbres, 8 mujeres). Sin antecedentes de importancia. Padre con 3 hermanos y 3 medios hermanos con alteraciones laríngeas no especificadas (pero por cómo se explican no impresionan de gravedad), sin conocer la edad de inicio de alteraciones. No refieren otros antecedentes familiares de interés. Antecedentes de rasgo talasémico en progenitores, pero DIFERENTE gen. Aportan informe: Madre alfa trait. Padre: Beta minor trait."


# ------------------------------------------------------------
# LÓGICA DE TRADUCCIÓN VIA INFERENCE API
# ------------------------------------------------------------

# 1) Define la URL del modelo (Helsinki-NLP/opus-mt-es-en)
API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-es-en"

# 2) Tu token de Hugging Face (scope "read")
#    (Reemplaza hf_xxx por tu token real)
headers = {"Authorization": "Bearer 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"}

def translate_es_to_en(text: str) -> (bool, str):
    """
    Traduce texto de español a inglés usando la Inference API de Hugging Face.
    Retorna (success, message_or_translated_text).
      - success=True cuando tenemos traducción exitosa.
      - success=False cuando hay error/carga/etc.
    """
    payload = {"inputs": text}
    try:
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                return True, data[0].get("translation_text", "")
            else:
                return False, "No se recibió traducción válida."

        elif response.status_code == 503:
            # Modelo en proceso de carga. Podemos mostrar el "estimated_time"
            data = response.json()
            estimated_time = data.get("estimated_time", "Desconocido")
            return False, f"El modelo está cargándose. Tiempo estimado: {estimated_time} s"

        else:
            # Otros errores (400, 401, 500, etc.)
            return False, f"Error {response.status_code}: {response.text}"

    except Exception as e:
        return False, f"Error de conexión o formato: {str(e)}"



# 3) Botón Traducir
if col_bot3.button("Traducir", help="Traduce el texto ES→EN con Hugging Face", type="primary"):
    if not user_prompt.strip():
        st.warning("Por favor, ingresa algún texto.", icon="⚠️")
    else:
        with st.spinner("Traduciendo..."):
            success, result_text = translate_es_to_en(user_prompt.strip())

        # Evaluamos success
        if success:
            st.success("Traducción completada con éxito.")
            st.text_area("Resultado de la traducción:", result_text, height=150)
        else:
            # Muestra error o estado de "cargando"
            st.error(result_text)