
import streamlit as st
import base64
from openai import OpenAI

# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="VisioLab",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# ESTILOS
# ==========================================

st.markdown("""
<style>

/* Fondo completo de la aplicación */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"], .stApp {
    min-height: 100vh !important;
    background: linear-gradient(
        135deg,
        #DDF4FF 0%,
        #BCE7FF 35%,
        #D8E9FF 70%,
        #EAEFFF 100%
    ) !important;
    background-attachment: fixed !important;
}

/* Fondo del contenedor principal */
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: transparent !important;
}

/* Ocultar elementos innecesarios */
#MainMenu, footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

/* Ancho y espacio */
.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Encabezado */
.hero {
    text-align: center;
    padding: 20px 10px 30px 10px;
}

.hero-title {
    color: #1556A8;
    font-size: 38px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 8px;
}

.hero-subtitle {
    color: #456A91;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
}

/* Tarjetas blancas */
.panel {
    background: rgba(255, 255, 255, 0.90);
    border: 1px solid rgba(255,255,255,0.8);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 8px 30px rgba(21,86,168,0.10);
    margin-bottom: 20px;
}

/* Títulos */
h2, h3 {
    color: #1556A8 !important;
}

/* Texto */
p, label {
    color: #45617D;
}

/* Campos */
.stTextInput input,
.stTextArea textarea {
    border: 1px solid #B8D8F2 !important;
    border-radius: 12px !important;
    background: #FFFFFF !important;
}

/* Cargador de imágenes */
[data-testid="stFileUploader"] {
    background: rgba(245,250,255,0.95);
    border: 2px dashed #70B5E8;
    border-radius: 15px;
    padding: 15px;
}

/* Botones */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #1556A8, #078FCE);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 13px 20px;
    min-height: 48px;
    font-weight: 700;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #0D4389, #087DB5);
    transform: translateY(-1px);
}

/* Resultado */
.resultado {
    background: rgba(255,255,255,0.95);
    border-left: 5px solid #078FCE;
    border-radius: 15px;
    padding: 24px;
    color: #263B53;
    line-height: 1.8;
    box-shadow: 0 8px 25px rgba(21,86,168,0.08);
}

/* Pie */
.pie {
    text-align: center;
    color: #527394;
    font-size: 12px;
    padding: 30px 0 10px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# ENCABEZADO
# ==========================================

st.markdown("""
<div class="hero">
    <div class="hero-title">VisioLab.</div>
    <div class="hero-subtitle">
        SUBE · PREGUNTA · DESCUBRE
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# CLAVE API
# ==========================================

st.markdown('<div class="panel">', unsafe_allow_html=True)

st.markdown("### 🔑 Conexión con inteligencia artificial")

api_key = st.text_input(
    "Clave API de OpenAI",
    type="password",
    placeholder="Ingresa tu clave API aquí",
    help="La clave se utiliza para conectar con el servicio de OpenAI."
)

st.markdown(
    '<p style="font-size:12px;color:#71869B;">'
    'Tu clave no se muestra en pantalla. No la compartas con otras personas.'
    '</p>',
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# CARGA DE IMAGEN
# ==========================================

st.markdown("""
<div style="text-align:center; margin: 15px 0 20px;">
    <h3>Sube tu imagen</h3>
    <p>Selecciona una fotografía para comenzar a hacer preguntas.</p>
</div>
""", unsafe_allow_html=True)

archivo = st.file_uploader(
    "Selecciona una fotografía",
    type=["jpg", "jpeg", "png"],
    help="Formatos permitidos: JPG, JPEG y PNG."
)

# ==========================================
# VISTA PREVIA Y PREGUNTA
# ==========================================

if archivo is not None:

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown("### 📷 Vista previa")

    st.image(
        archivo,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown("### 💬 ¿Qué quieres saber?")

    pregunta = st.text_area(
        "Escribe tu pregunta",
        placeholder="Ejemplo: ¿Qué objetos aparecen en esta fotografía?",
        height=110,
        label_visibility="collapsed"
    )

    analizar = st.button("Analizar imagen")

    st.markdown("</div>", unsafe_allow_html=True)

    # ======================================
    # ANÁLISIS CON GPT-4o
    # ======================================

    if analizar:

        if not api_key.strip():
            st.warning("Primero debes ingresar tu clave API de OpenAI.")

        else:
            try:
                imagen_bytes = archivo.getvalue()

                imagen_base64 = base64.b64encode(
                    imagen_bytes
                ).decode("utf-8")

                tipo_imagen = archivo.type

                if tipo_imagen not in ["image/jpeg", "image/png"]:
                    st.error("El formato de imagen no es compatible.")
                    st.stop()

                if not pregunta.strip():
                    pregunta_final = (
                        "Describe esta imagen e identifica sus "
                        "elementos principales."
                    )
                else:
                    pregunta_final = pregunta.strip()

                cliente = OpenAI(api_key=api_key.strip())

                with st.spinner("Analizando tu imagen..."):

                    respuesta = cliente.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "Eres un asistente especializado en análisis "
                                    "visual. Responde siempre en español, de forma "
                                    "clara, precisa y útil. Describe solamente lo "
                                    "que puedas observar en la imagen y aclara "
                                    "cuando no sea posible determinar algo."
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

                st.markdown("### ✨ Resultado del análisis")

                st.markdown(
                    '<div class="resultado">',
                    unsafe_allow_html=True
                )

                st.markdown(texto_respuesta)

                st.markdown("</div>", unsafe_allow_html=True)

            except Exception as error:

                mensaje = str(error).lower()

                if "401" in mensaje or "invalid_api_key" in mensaje:
                    st.error(
                        "La clave API no es válida. "
                        "Verifica que hayas ingresado la clave correcta."
                    )

                elif "429" in mensaje:
                    st.error(
                        "Se alcanzó el límite de uso de la API. "
                        "Revisa tu cuenta de OpenAI."
                    )

                elif "connection" in mensaje:
                    st.error(
                        "No fue posible conectar con OpenAI. "
                        "Verifica tu conexión a internet."
                    )

                else:
                    st.error(
                        "Ocurrió un error durante el análisis. "
                        "Inténtalo nuevamente."
                    )

else:

    st.markdown("""
    <div class="panel" style="text-align:center; padding:40px 20px;">
        <div style="font-size:45px;">📷</div>
        <h3>Tu imagen aparecerá aquí</h3>
        <p>
            Selecciona una fotografía y comienza a preguntarle
            a la inteligencia artificial sobre su contenido.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# PIE DE PÁGINA
# ==========================================

st.markdown("""
<div class="pie">
    VisioLab · Análisis inteligente de imágenes
</div>
""", unsafe_allow_html=True)
