
import streamlit as st
import base64
from openai import OpenAI

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="VisioLab",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# ESTILOS DE LA INTERFAZ
# --------------------------------------------------

st.markdown("""
<style>

/* Fondo general */
.stApp {
    background: linear-gradient(
        135deg,
        #EAF8FF 0%,
        #D9F0FF 45%,
        #EEF2FF 100%
    );
}

/* Ocultar menú superior */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Contenedor principal */
.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Encabezado */
.hero {
    text-align: center;
    padding: 20px 10px 25px 10px;
}

.hero-title {
    color: #1556A8;
    font-size: 34px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 7px;
}

.hero-subtitle {
    color: #64748B;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.5px;
}

/* Tarjetas */
.panel {
    background: rgba(255,255,255,0.88);
    border: 1px solid #DCEBFA;
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 8px 25px rgba(21,86,168,0.07);
    margin-bottom: 18px;
}

/* Títulos */
h2, h3 {
    color: #1556A8 !important;
}

/* Botones */
.stButton > button {
    background: linear-gradient(90deg, #1556A8, #078FCE);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 20px;
    font-weight: 700;
    min-height: 48px;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #0D4389, #087DB5);
    color: white;
    border: none;
}

/* Campo de texto */
.stTextArea textarea,
.stTextInput input {
    border-radius: 12px;
    border: 1px solid #C9DDF2;
}

/* Cargador */
[data-testid="stFileUploader"] {
    background: #F5FAFF;
    border: 1px dashed #7BB7E8;
    border-radius: 15px;
    padding: 15px;
}

/* Resultado */
.resultado {
    background: white;
    border-left: 5px solid #078FCE;
    border-radius: 14px;
    padding: 22px;
    color: #263B53;
    line-height: 1.7;
    box-shadow: 0 6px 20px rgba(21,86,168,0.07);
}

/* Pie de página */
.pie {
    text-align: center;
    color: #8296AA;
    font-size: 12px;
    padding: 30px 0 10px 0;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# ENCABEZADO
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-title">VisioLab.</div>
    <div class="hero-subtitle">
        SUBE · PREGUNTA · DESCUBRE
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# API KEY
# --------------------------------------------------

api_key = ""

try:
    api_key = st.secrets.get("OPENAI_API_KEY", "")
except Exception:
    pass

with st.sidebar:
    st.markdown("### Configuración")
    api_key = st.text_input(
        "Clave API de OpenAI",
        value=api_key,
        type="password",
        help="Tu clave se utiliza para conectar con el modelo de inteligencia artificial."
    )

    st.caption("La clave se utiliza para realizar el análisis de imágenes.")

# --------------------------------------------------
# CARGA DE IMAGEN
# --------------------------------------------------

st.markdown("""
<div style="text-align:center; margin-bottom:18px;">
    <h3 style="margin-bottom:5px;">Sube tu imagen</h3>
    <p style="color:#64748B; font-size:14px;">
        Carga una fotografía y pregunta lo que quieras saber sobre ella.
    </p>
</div>
""", unsafe_allow_html=True)

archivo = st.file_uploader(
    "Selecciona una fotografía",
    type=["jpg", "jpeg", "png"],
    help="Formatos permitidos: JPG, JPEG y PNG."
)

# --------------------------------------------------
# VISTA PREVIA Y PREGUNTA
# --------------------------------------------------

if archivo is not None:

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown("### Vista previa")

    st.image(
        archivo,
        caption="Imagen cargada",
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown("### ¿Qué quieres saber?")

    pregunta = st.text_area(
        "Escribe tu pregunta sobre la imagen",
        placeholder="Ejemplo: ¿Qué objetos aparecen en esta fotografía?",
        height=110,
        label_visibility="collapsed"
    )

    analizar = st.button(
        "Analizar imagen",
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------
    # ANÁLISIS CON INTELIGENCIA ARTIFICIAL
    # --------------------------------------------------

    if analizar:

        if not api_key:
            st.error(
                "Debes ingresar tu clave API de OpenAI en el menú de configuración."
            )

        else:
            try:
                # Convertir imagen a Base64
                imagen_bytes = archivo.getvalue()
                imagen_base64 = base64.b64encode(
                    imagen_bytes
                ).decode("utf-8")

                tipo_imagen = archivo.type

                # Si no se escribe una pregunta, usar una general
                if not pregunta.strip():
                    pregunta_final = (
                        "Describe detalladamente esta imagen. "
                        "Identifica los elementos visibles y explica "
                        "qué información se puede obtener de ella."
                    )
                else:
                    pregunta_final = pregunta.strip()

                # Crear cliente de OpenAI
                cliente = OpenAI(api_key=api_key)

                st.markdown("### Resultado del análisis")

                with st.spinner("Analizando tu imagen..."):

                    respuesta = cliente.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "Eres un asistente experto en análisis visual. "
                                    "Analiza las imágenes cuidadosamente y responde "
                                    "en español, con claridad, precisión y de forma "
                                    "útil. Describe únicamente lo que puedas observar "
                                    "y aclara cuando algo no pueda determinarse."
                                )
                            },
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": pregunta_final
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": (
                                                f"data:{tipo_imagen};base64,"
                                                f"{imagen_base64}"
                                            ),
                                            "detail": "high"
                                        }
                                    }
                                ]
                            }
                        ],
                        max_tokens=1600,
                        temperature=0.4
                    )

                texto_respuesta = (
                    respuesta.choices[0].message.content
                )

                st.markdown(
                    f'<div class="resultado">{texto_respuesta}</div>',
                    unsafe_allow_html=True
                )

            except Exception as error:

                mensaje = str(error)

                if "401" in mensaje or "invalid_api_key" in mensaje:
                    st.error(
                        "La clave API no es válida. "
                        "Verifica tu clave de OpenAI."
                    )

                elif "429" in mensaje:
                    st.error(
                        "Se alcanzó un límite de uso o cuota de la API. "
                        "Revisa tu cuenta de OpenAI."
                    )

                elif "Connection" in mensaje:
                    st.error(
                        "No fue posible conectar con OpenAI. "
                        "Verifica tu conexión a internet."
                    )

                else:
                    st.error(
                        "Ocurrió un error al analizar la imagen. "
                        "Inténtalo nuevamente."
                    )

else:

    st.markdown("""
    <div class="panel" style="text-align:center; padding:35px 20px;">
        <div style="font-size:42px; margin-bottom:12px;">📷</div>
        <h3>Tu imagen aparecerá aquí</h3>
        <p style="color:#64748B; font-size:14px;">
            Selecciona una fotografía para comenzar a hacer preguntas.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# PIE DE PÁGINA
# --------------------------------------------------

st.markdown("""
<div class="pie">
    VisioLab · Análisis inteligente de imágenes
</div>
""", unsafe_allow_html=True)
