import streamlit as st
import os

from dotenv import load_dotenv
from google import genai
from PIL import Image


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="NutriSense - Food Plate Analysis",
    page_icon="📸",
    layout="centered"
)


# -----------------------------
# LOAD ENVIRONMENT VARIABLES
# -----------------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None


# -----------------------------
# INITIALIZE GEMINI
# -----------------------------
@st.cache_resource
def get_gemini_client():

    if not api_key:
        return None

    return genai.Client(
        api_key=api_key
    )


client = get_gemini_client()


# -----------------------------
# HEADER
# -----------------------------
st.title("📸 NutriSense Food Plate Analysis")

st.subheader(
    "AI-powered food recognition and protein insights"
)

st.write(
    "Upload a photo of your meal and let NutriSense AI analyse "
    "the visible food items and provide protein-focused insights."
)

st.divider()


# -----------------------------
# USER INPUT
# -----------------------------
protein_goal = st.number_input(
    "Protein goal for this meal (grams)",
    min_value=5,
    max_value=100,
    value=20,
    step=5
)


diet = st.selectbox(
    "Dietary preference",
    [
        "Vegetarian",
        "Non-Vegetarian"
    ]
)


# -----------------------------
# IMAGE UPLOAD
# -----------------------------
st.divider()

st.subheader("📤 Upload Your Food Plate")

uploaded_image = st.file_uploader(
    "Upload a photo of your meal",
    type=[
        "jpg",
        "jpeg",
        "png"
    ]
)


# -----------------------------
# DISPLAY SMALL IMAGE PREVIEW
# -----------------------------
if uploaded_image is not None:

    image = Image.open(
        uploaded_image
    )

    # Small preview
    st.image(
        image,
        caption="Uploaded Food Plate",
        width=250
    )


    # -----------------------------
    # ANALYSIS BUTTON
    # -----------------------------
    if st.button(
        "🤖 Analyse My Food with AI",
        use_container_width=True
    ):


        # -----------------------------
        # CHECK GEMINI
        # -----------------------------
        if client is None:

            st.error(
                "Gemini API key was not found. "
                "Please check your configuration."
            )


        else:

            try:

                with st.spinner(
                    "🤖 NutriSense AI is analysing your food plate..."
                ):


                    # -----------------------------
                    # GEMINI PROMPT
                    # -----------------------------
                    prompt = f"""
You are NutriSense, an AI-powered nutrition and mess meal assistant.

Analyse the uploaded food plate image.

User dietary preference:
{diet}

User protein goal for this meal:
{protein_goal} grams

Your task:

1. FOOD ITEMS IDENTIFIED
Identify the food items that are reasonably visible in the image.
Do not claim certainty when the image is unclear.

2. MEAL OBSERVATION
Briefly describe the meal composition based only on what is visible.

3. PROTEIN INSIGHT
Provide a cautious approximate assessment of whether the visible meal
appears to be a low, moderate, or relatively high protein meal.

Do NOT claim exact nutritional values unless they can reasonably be
estimated, and clearly state that portion size and preparation affect
protein estimates.

4. PROTEIN GOAL FIT
Compare the meal generally against the user's selected protein goal of
{protein_goal} grams.

5. IMPROVEMENT SUGGESTION
Suggest simple food additions or substitutions that could improve the
protein content if the meal appears insufficient.

Important rules:

- Do not invent food items that are not reasonably visible.
- Clearly mention uncertainty when identification is unclear.
- Do not provide medical advice.
- Do not diagnose health conditions.
- Keep the response concise, practical, and student-friendly.
- Mention that image-based nutrition assessment is approximate.
"""


                    # -----------------------------
                    # GEMINI IMAGE ANALYSIS
                    # -----------------------------
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=[
                            prompt,
                            image
                        ]
                    )


                # -----------------------------
                # DISPLAY RESULT
                # -----------------------------
                if response.text:

                    st.success(
                        "Food plate analysis completed!"
                    )

                    st.subheader(
                        "🤖 NutriSense AI Insight"
                    )

                    st.info(
                        response.text
                    )


                else:

                    st.warning(
                        "The AI could not generate an analysis "
                        "for this image."
                    )


            except Exception as error:

                st.error(
                    "Unable to analyse the image at this time."
                )

                st.caption(
                    f"Technical details: {error}"
                )


# -----------------------------
# INFORMATION / DISCLAIMER
# -----------------------------
st.divider()

st.caption(
    "⚠️ AI food identification and nutrition insights are approximate "
    "and depend on image quality, visible ingredients, portion size, "
    "and food preparation. NutriSense does not provide medical advice."
)