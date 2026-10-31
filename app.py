
import base64
import streamlit as st
from openai import (
    OpenAI,
    AuthenticationError,
    RateLimitError,
    APIConnectionError,
    BadRequestError
)


# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title="VisioLab | Inteligencia visual",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# IDENTIDAD VISUAL - VISIOLAB
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif;
}

.stApp {
    background: linear-gradient(
        135deg,
        #EAF8FF 0%,
        #D9F0FF 30%,
        #E9ECFF 65%,
        #F5F7FF 100%
    );
    background-attachment: fixed;
}

[data-testid="stAppViewContainer"] {
    background: transparent;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* -----------------------------------------------------
   BARRA LATERAL
----------------------------------------------------- */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        165deg,
        #101B42 0%,
        #123D78 52%,
        #087EAD 100%
    );
}

section[data-testid="stSidebar"] * {
    color: #FFFFFF;
}

section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea {
    background-color: #FFFFFF !important;
    color: #17233F !important;
    border: 1px solid #D5E4F5 !important;
    border-radius: 10px !important;
}

section[data-testid="stSidebar"] input::placeholder,
section[data-testid="stSidebar"] textarea::placeholder {
    color: #78869B !important;
}

/* Ocultar el botón de mostrar contraseña */

section[data-testid="stSidebar"]
div[data-testid="stTextInput"]:has(input[type="password"]) button {
    display: none !important;
}

/* Selectores */

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border-radius: 9px !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #17233F !important;
}

/* Scrollbar */

section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    scrollbar-width: thin;
    scrollbar-color: #66D9F5 #101B42;
}

section[data-testid="stSidebar"] [data-testid="stSidebarContent"]::-webkit-scrollbar {
    width: 8px;
}

section[data-testid="stSidebar"] [data-testid="stSidebarContent"]::-webkit-scrollbar-track {
    background: #101B42;
}

section[data-testid="stSidebar"] [data-testid="stSidebarContent"]::-webkit-scrollbar-thumb {
    background: #66D9F5;
    border-radius: 10px;
}

/* -----------------------------------------------------
   BOTONES DE LA BARRA LATERAL
----------------------------------------------------- */

section[data-testid="stSidebar"]
button[data-testid="stSidebarCollapseButton"],
button[data-testid="stSidebarExpandButton"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: #BCEFFF !important;
    border: 1px solid #BCEFFF !important;
    border-radius: 9px !important;
    align-items: center !important;
    justify-content: center !important;
}

section[data-testid="stSidebar"]
button[data-testid="stSidebarCollapseButton"] svg,
button[data-testid="stSidebarExpandButton"] svg {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    color: #123D78 !important;
    stroke: #123D78 !important;
}

section[data-testid="stSidebar"]
button[data-testid="stSidebarCollapseButton"] span,
button[data-testid="stSidebarExpandButton"] span {
    visibility: visible !important;
    opacity: 1 !important;
}

/* -----------------------------------------------------
   ENCABEZADO
----------------------------------------------------- */

.hero {
    background: linear-gradient(
        120deg,
        #10265A 0%,
        #1556A8 43%,
        #078FCE 75%,
        #55D6EB 100%
    );
    padding: 42px 44px;
    border-radius: 24px;
    color: #FFFFFF;
    box-shadow: 0 15px 40px rgba(22, 91, 160, 0.18);
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
}

.hero::after {
    content: "";
    position: absolute;
    width: 260px;
    height: 260px;
    border-radius: 50%;
    background: rgba(255,255,255,0.08);
    right: -70px;
    top: -100px;
}

.hero-label {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 3px;
    color: #A9F0FF;
    margin-bottom: 12px;
}

.hero h1 {
    font-size: 48px;
    font-weight: 800;
    line-height: 1.15;
    color: #FFFFFF;
    margin: 0 0 14px 0;
}

.hero p {
    color: #EAF8FF;
    font-size: 16px;
    line-height: 1.7;
    max-width: 720px;
}

.hero-tag {
    display: inline-block;
    padding: 9px 16px;
    margin-top: 12px;
    border-radius: 30px;
    border: 1px solid rgba(255,255,255,0.35);
    background: rgba(255,255,255,0.12);
    color: #FFFFFF;
    font-size: 10px;
    letter-spacing: 1.5px;
    font-weight: 800;
}

/* -----------------------------------------------------
   TEXTOS PRINCIPALES
----------------------------------------------------- */

.main h1,
.main h2,
.main h3,
.main p,
.main label {
    color: #142C55;
}

.main [data-testid="stMarkdownContainer"] p {
    color: #425A7D;
}

/* -----------------------------------------------------
   BOTONES PRINCIPALES
----------------------------------------------------- */

.stButton > button {
    background: linear-gradient(
        110deg,
        #1556A8,
        #078FCE
    ) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 11px !important;
    padding: 0.7rem 1.3rem !important;
    font-weight: 800 !important;
    transition: all 0.2s ease;
    box-shadow: 0 5px 14px rgba(21, 86, 168, 0.15);
}

.stButton > button:hover {
    background: linear-gradient(
        110deg,
        #10488F,
        #0579B5
    ) !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 18px rgba(21, 86, 168, 0.22);
}

/* -----------------------------------------------------
   CARGADOR DE IMÁGENES
----------------------------------------------------- */

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.85);
    border: 2px dashed #80BCEB;
    border-radius: 16px;
    padding: 1rem;
}

[data-testid="stFileUploader"] * {
    color: #183B69 !important;
}

/* -----------------------------------------------------
   IMÁGENES
----------------------------------------------------- */

[data-testid="stImage"] {
    border-radius: 16px;
    overflow: hidden;
}

/* -----------------------------------------------------
   CONTENEDORES Y TARJETAS
----------------------------------------------------- */

[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.85);
    border: 1px solid #D8E8F8;
    border-radius: 16px;
}

/* -----------------------------------------------------
   EXPANDERS
----------------------------------------------------- */

[data-testid="stExpander"] {
    background: rgba(255,255,255,0.88);
    border: 1px solid #D8E8F8;
    border-radius: 12px;
}

[data-testid="stExpander"] summary {
    color: #173D70 !important;
}

/* -----------------------------------------------------
   TEXT AREA
----------------------------------------------------- */

.stTextArea textarea {
    background: #FFFFFF !important;
    color: #17233F !important;
    border: 1px solid #BBD3EC !important;
    border-radius: 10px !important;
}

.stTextArea textarea::placeholder {
    color: #8291A7 !important;
}

/* -----------------------------------------------------
   MÉTRICAS
----------------------------------------------------- */

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.88);
    border: 1px solid #D8E8F8;
    border-radius: 14px;
    padding: 15px;
}

[data-testid="stMetricLabel"] {
    color: #536B8B !important;
}

[data-testid="stMetricValue"] {
    color: #1556A8 !important;
}

/* -----------------------------------------------------
   PIE DE PÁGINA
----------------------------------------------------- */

.footer {
    text-align: center;
    color: #637D9F;
    font-size: 11px;
    padding: 20px;
    letter-spacing: 1px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# ENCABEZADO PRINCIPAL
# =========================================================

st.markdown("""
<div class="hero">

    <div class="hero-label">
        VISUAL INTELLIGENCE STUDIO
    </div>

    <h1>VisioLab.</h1>

    <p>
        Explora el poder de la inteligencia artificial visual.
        Sube una imagen, descubre sus detalles y obtén respuestas
        inteligentes sobre todo lo que contiene.
    </p>

    <div class="hero-tag">
        OBSERVAR · COMPRENDER · DESCUBRIR
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# BARRA LATERAL
# =========================================================

with st.sidebar:

    st.markdown("## 🔷 VisioLab")

    st.markdown(
        "### Configuración"
    )

    st.markdown(
        "Conecta tu cuenta para comenzar a interpretar imágenes."
    )

    st.markdown("---")

    st.markdown("### 🔐 Conexión API")

    api_key = st.text_input(
        "Clave API de OpenAI",
        type="password",
        placeholder="Introduce tu clave sk-...",
        help="La clave se utiliza para realizar el análisis visual."
    ).strip()

    if api_key:
        st.success("✓ Clave introducida")
    else:
        st.warning("Introduce tu clave API para comenzar.")

    st.markdown("---")

    st.markdown("### 🧠 Modelo de inteligencia")

    st.markdown(
        """
        <div style="
            background:rgba(255,255,255,0.12);
            border:1px solid rgba(255,255,255,0.2);
            padding:13px;
            border-radius:10px;
            color:white;
            font-size:13px;
        ">
            <b>GPT-4o</b><br>
            <span style="color:#C6EFFF;">
            Modelo multimodal para comprensión visual.
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.caption("VISIOLAB · VISUAL INTELLIGENCE STUDIO")


# =========================================================
# ESTADO DE LA APLICACIÓN
# =========================================================

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "last_image_hash" not in st.session_state:
    st.session_state.last_image_hash = None

if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = None


# =========================================================
# ÁREA DE CARGA
# =========================================================

st.markdown("## 📷 Explora una imagen")

st.markdown(
    "Carga una imagen para que la inteligencia artificial "
    "pueda analizarla y responder tus preguntas."
)

uploaded_file = st.file_uploader(
    "Selecciona una imagen desde tu dispositivo",
    type=["jpg", "jpeg", "png"],
    help="Formatos permitidos: JPG, JPEG y PNG."
)


# =========================================================
# VISTA PREVIA DE LA IMAGEN
# =========================================================

if uploaded_file:

    image_bytes = uploaded_file.getvalue()

    if len(image_bytes) > 20 * 1024 * 1024:
        st.error(
            "La imagen supera el límite de 20 MB. "
            "Carga una imagen más pequeña."
        )
        uploaded_file = None

    else:

        st.session_state.analysis_result = None

        with st.expander(
            "🖼️ Vista previa de la imagen",
            expanded=True
        ):

            col1, col2 = st.columns(
                [1.5, 1],
                gap="large"
            )

            with col1:

                st.image(
                    image_bytes,
                    caption=uploaded_file.name,
                    use_container_width=True
                )

            with col2:

                st.markdown("### Información del archivo")

                st.markdown(
                    f"**Nombre:** {uploaded_file.name}"
                )

                st.markdown(
                    f"**Formato:** {uploaded_file.type}"
                )

                st.markdown(
                    f"**Tamaño:** {len(image_bytes) / 1024:.1f} KB"
                )

                st.success(
                    "Imagen lista para analizar."
                )


# =========================================================
# OPCIONES DE ANÁLISIS
# =========================================================

st.markdown("---")

st.markdown("## 🔍 ¿Qué quieres descubrir?")

analysis_mode = st.radio(
    "Selecciona el tipo de análisis:",
    [
        "Descripción general",
        "Pregunta específica"
    ],
    horizontal=True
)

additional_details = ""

if analysis_mode == "Pregunta específica":

    additional_details = st.text_area(
        "Escribe tu pregunta sobre la imagen",
        placeholder=(
            "Ejemplo: ¿Qué elementos aparecen en la imagen? "
            "¿Qué información contiene el gráfico? "
            "¿Qué diferencias observas entre los objetos?"
        ),
        height=110
    )

else:

    st.info(
        "La IA realizará una descripción detallada de los "
        "elementos, objetos, personas, colores, texto y "
        "contexto visual que pueda reconocer."
    )


# =========================================================
# CONSTRUCCIÓN DEL PROMPT
# =========================================================

def build_prompt(mode, details):

    if mode == "Descripción general":

        return """
Analiza cuidadosamente la imagen proporcionada.

Escribe una descripción completa y organizada en español.

Incluye, cuando corresponda:

1. Descripción general de la imagen.
2. Elementos, objetos o personas visibles.
3. Colores, formas, composición y detalles importantes.
4. Texto que aparezca en la imagen, si es legible.
5. Contexto o situación que representa.
6. Información relevante que pueda interpretarse visualmente.

Distingue claramente entre lo que se observa directamente
y lo que solo puede inferirse.

No inventes información ni afirmes detalles que no sean
visibles con suficiente claridad.

Utiliza un lenguaje claro, preciso y profesional.
"""

    return f"""
Analiza cuidadosamente la imagen y responde en español
la siguiente pregunta del usuario:

{details}

Utiliza únicamente la información que pueda observarse
en la imagen.

Explica tu respuesta de forma clara, detallada y organizada.

Si algún elemento no se puede identificar con certeza,
indícalo expresamente.

No inventes información.
"""


# =========================================================
# ANÁLISIS DE IMAGEN
# =========================================================

st.markdown("---")

st.markdown("## ✨ Interpretación inteligente")

st.markdown(
    "Cuando estés listo, inicia el análisis visual."
)

analyze_button = st.button(
    "🔷 Analizar imagen",
    type="primary",
    use_container_width=True,
    disabled=(
        uploaded_file is None
        or not api_key
        or (
            analysis_mode == "Pregunta específica"
            and not additional_details.strip()
        )
    )
)


if analyze_button:

    try:

        client = OpenAI(
            api_key=api_key
        )

        image_bytes = uploaded_file.getvalue()

        base64_image = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        mime_type = uploaded_file.type

        prompt_text = build_prompt(
            analysis_mode,
            additional_details
        )

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": (
                                f"data:{mime_type};base64,"
                                f"{base64_image}"
                            ),
                            "detail": "high"
                        }
                    }
                ]
            }
        ]

        st.session_state.analysis_result = None

        st.markdown("### 🧠 Resultado del análisis")

        message_placeholder = st.empty()

        full_response = ""

        with st.spinner(
            "La inteligencia artificial está interpretando la imagen..."
        ):

            stream = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1600,
                temperature=0.4,
                stream=True
            )

            for completion in stream:

                if not completion.choices:
                    continue

                delta = completion.choices[0].delta.content

                if delta:
                    full_response += delta

                    message_placeholder.markdown(
                        full_response + " ▌"
                    )

        message_placeholder.markdown(
            full_response
        )

        st.session_state.analysis_result = full_response

        st.session_state.last_prompt = prompt_text

        st.success(
            "¡Análisis visual completado correctamente!"
        )

    except AuthenticationError:

        st.error(
            "La clave API de OpenAI no es válida o ha sido revocada. "
            "Revisa tu clave e inténtalo nuevamente."
        )

    except RateLimitError:

        st.error(
            "Se alcanzó un límite de uso o no hay crédito disponible. "
            "Revisa la facturación de tu cuenta de OpenAI."
        )

    except APIConnectionError:

        st.error(
            "No fue posible conectar con OpenAI. "
            "Comprueba tu conexión a internet."
        )

    except BadRequestError as error:

        st.error(
            "OpenAI no pudo procesar la solicitud. "
            "Comprueba el formato, tamaño y contenido de la imagen."
        )

        st.caption(str(error))

    except Exception as error:

        st.error(
            "Ocurrió un problema durante el análisis."
        )

        st.exception(error)


# =========================================================
# RESULTADO GUARDADO
# =========================================================

if (
    st.session_state.analysis_result
    and not analyze_button
):

    st.markdown("---")

    st.markdown("## 📋 Último resultado")

    st.markdown(
        st.session_state.analysis_result
    )


# =========================================================
# PIE DE PÁGINA
# =========================================================

st.markdown("---")

st.markdown("""
<div class="footer">

    <div style="
        color:#1556A8;
        font-size:19px;
        font-weight:800;
        letter-spacing:1px;
        margin-bottom:5px;
    ">
        VisioLab.
    </div>

    VISUAL INTELLIGENCE STUDIO

    <div style="margin-top:8px;">
        OBSERVAR · COMPRENDER · DESCUBRIR
    </div>

</div>
""", unsafe_allow_html=True)
