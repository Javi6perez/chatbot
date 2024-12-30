import streamlit as st
from openai import OpenAI

# ------------------------------------------------------------
# CONFIGURACIÓN INICIAL DE LA PÁGINA
# ------------------------------------------------------------
st.set_page_config(
    page_title="Agente de Traducción Médica"
)
st.markdown("<div class='otro'>", unsafe_allow_html=True)
# Muestra el logo de VidasPrime (ajusta la ruta o URL a tu imagen).
st.image("https://www.sjdhospitalbarcelona.org/themes/hsjd/assets/img/logo.svg", width=200)

# ------------------------------------------------------------
# CSS PERSONALIZADO PARA LA BARRA SUPERIOR Y BOTONES
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Barra superior fija con logo */
    .top-bar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 60px;
        background-color: #f5f5f5;
        border-bottom: 1px solid #ddd;
        z-index: 9999;
        display: flex;
        align-items: center;
        padding: 0 20px;
    }
    .top-bar img {
        height: 40px;
        margin-right: 15px;
        margin-top: 110px;
    }

    .top-bar h2 {
        font-size: 22px;
        margin: 0;
        color: #5a189a; /* Morado de VidasPrime */
        font-weight: 600;
    }

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
    
    <!-- Barra superior con logo y título -->
    <div class="top-bar">
      <img src="https://vidasprime.es/wp-content/uploads/2022/06/logo_vidas_prime_morado.png" alt="VidasPrime Logo">
      <h2>Agente de Traducción Médica</h2>
    </div>
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
    if st.button("Comenzar", help="Iniciar la aplicación"):
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
    height=320,
    value=st.session_state.get("ejemplo_cargado", "")  # Carga el ejemplo si ya se cargó

)
# Botón para cargar el ejemplo
if st.button("Cargar ejemplo", type="secondary"):
    st.session_state["ejemplo_cargado"] = "Antecedentes familiares: \n \
                - Antecedents familiars (Hermano): Hermano con antecedentes de laringotraqueomalacia leve. Laringitis y broncoespasmos de repetición. \n\
                - Antecedents familiars (Madre): Padres no consanguíneos, niegan endogamia. Oriundos de Emiratos Arabes Unidos, en poblaciones distintas cerca de Dubai. Madre G4, con deseo gestacional ulterior. Niega abortos. Madre con 15 hermanos (8 hormbres, 8 mujeres). Sin antecedentes de importancia. Padre con 3 hermanos y 3 medios hermanos con alteraciones laríngeas no especificadas (pero por cómo se explican no impresionan de gravedad), sin conocer la edad de inicio de alteraciones. No refieren otros antecedentes familiares de interés. Antecedentes de rasgo talasémico en progenitores, pero DIFERENTE gen. Aportan informe: Madre alfa trait. Padre: Beta minor trait."

# 3) Botón Traducir
if st.button("Traducir", help="Haz clic para traducir el texto ingresado", type="primary"):
    if not user_prompt.strip():
        st.warning("Por favor, ingresa algún texto.", icon="⚠️")
    else:
        st.info("Procesando la traducción, por favor espera...", icon="⏳")
        try:
            # Traducción usando OpenAI
            openai_api_key = (
                "sk-proj-C0JjGcobEsUWfwddppcWAwqlVSmnnWvJvJcUUPK99WGdbvex47ZsP51zpXSZNZ6SksJG3E366"
                "UT3BlbkFJBbeLM6uvkTXqHj-J33YPl1aNZnQyCZdoY0aTTKKcvlt_Uwtj87GOoE65XqnOW9G9NuwhsDyn8A"
            )
            client = OpenAI(api_key=openai_api_key)

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    #{"role": "system", "content": f"Traduce del {idioma_entrada} al {idioma_salida}."},
                    {"role": "user", "content": user_prompt}
                ]
            )

            translated_text = response["choices"][0]["message"]["content"]
            st.success("Traducción completada con éxito.")
            st.text_area("Resultado de la traducción:", translated_text, height=150)

        except Exception as e:
            st.error(f"Ocurrió un error al procesar la traducción: {e}")