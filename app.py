import streamlit as st
import json
import os

from dotenv import load_dotenv
from google import genai

from recommendation import get_recommendations


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="NutriSense",
    page_icon="🥗",
    layout="centered"
)


# -----------------------------
# LOAD ENVIRONMENT VARIABLES
# -----------------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


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
# LOAD MENU DATA
# -----------------------------
@st.cache_data
def load_menu():

    with open(
        "menu_data.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


menu_data = load_menu()


# -----------------------------
# GENERATE AI INSIGHT
# -----------------------------
def get_ai_insight(
    recommendations,
    meal,
    protein_goal,
    diet
):

    # If API key is missing
    if client is None:

        return (
            "AI insights are currently unavailable because "
            "the Gemini API key was not found."
        )

    # Prepare recommendation information
    recommendation_text = ""

    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):

        foods = ", ".join(
            recommendation["foods"]
        )

        recommendation_text += (
            f"\nOption {index}:\n"
            f"Foods: {foods}\n"
            f"Estimated Protein: "
            f"{recommendation['protein']}g\n"
            f"Difference from target: "
            f"{recommendation['difference']}g\n"
        )

    # Gemini prompt
    prompt = f"""
You are NutriSense, an AI-powered mess meal recommendation assistant.

A student is planning a {meal} meal.

Dietary preference:
{diet}

Protein target for this meal:
{protein_goal} grams

The NutriSense recommendation engine generated these options:

{recommendation_text}

Your task:

1. Briefly explain which option is the best protein match.
2. Explain why it is suitable for the student's selected protein goal.
3. Compare the options briefly.
4. Mention that protein values are estimates based on typical serving sizes.
5. Do NOT provide medical advice.
6. Do NOT invent foods or nutrition values that are not provided.
7. Keep the response concise, friendly, and useful.

Format your answer clearly using short paragraphs or bullet points.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        if response.text:

            return response.text

        return (
            "AI insight could not be generated "
            "at this time."
        )

    except Exception as error:

        return (
            "AI insight is temporarily unavailable. "
            f"Technical details: {error}"
        )


# -----------------------------
# HEADER
# -----------------------------
st.title("🥗 NutriSense")

st.subheader(
    "Your personalised mess meal assistant"
)

st.write(
    "Find the best available meal combinations based on your "
    "protein goal and dietary preference."
)

st.divider()


# -----------------------------
# USER INPUT
# -----------------------------
meal = st.selectbox(
    "Which meal are you planning?",
    [
        "Breakfast",
        "Lunch",
        "Snacks",
        "Dinner"
    ]
)


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
# SHOW AVAILABLE MENU
# -----------------------------
st.divider()

st.subheader(
    f"🍽️ Available {meal} Menu"
)


# Filter displayed menu for vegetarian users
if diet == "Vegetarian":

    displayed_items = [

        item
        for item in menu_data[meal]

        if item["type"] == "Vegetarian"

    ]

else:

    displayed_items = menu_data[meal]


available_food_names = [

    item["name"]
    for item in displayed_items

]


st.write(
    " • ".join(
        available_food_names
    )
)


# -----------------------------
# RECOMMENDATION BUTTON
# -----------------------------
st.divider()


if st.button(
    "✨ Get My Recommendation",
    use_container_width=True
):

    # -----------------------------
    # GET RULE-BASED RECOMMENDATIONS
    # -----------------------------
    recommendations = get_recommendations(
        menu_items=menu_data[meal],
        protein_goal=protein_goal,
        diet=diet,
        meal=meal
    )


    # -----------------------------
    # HANDLE NO RECOMMENDATIONS
    # -----------------------------
    if not recommendations:

        st.warning(
            "No suitable recommendation could be generated "
            "from the available menu."
        )


    else:

        # -----------------------------
        # SHOW TOP 3 RECOMMENDATIONS
        # -----------------------------
        st.subheader(
            "🏆 Your Top 3 Recommendations"
        )


        medals = [
            "🥇",
            "🥈",
            "🥉"
        ]


        for i, recommendation in enumerate(
            recommendations
        ):

            st.markdown(
                f"### {medals[i]} Option {i + 1}"
            )


            # -----------------------------
            # FOOD ITEMS
            # -----------------------------
            foods = " + ".join(
                recommendation["foods"]
            )


            st.write(
                f"**Your plate:** {foods}"
            )


            # -----------------------------
            # PROTEIN
            # -----------------------------
            st.write(
                f"💪 **Estimated Protein:** "
                f"{recommendation['protein']}g"
            )


            # -----------------------------
            # SERVING ASSUMPTIONS
            # -----------------------------
            servings = " • ".join(
                recommendation["servings"]
            )


            st.caption(
                f"Serving assumption: {servings}"
            )


            # -----------------------------
            # PROTEIN FIT
            # -----------------------------
            difference = recommendation[
                "difference"
            ]


            # Excellent tolerance
            excellent_tolerance = max(
                2,
                protein_goal * 0.10
            )


            # Good tolerance
            good_tolerance = max(
                5,
                protein_goal * 0.25
            )


            if difference <= excellent_tolerance:

                fit = (
                    "🟢 Excellent protein match"
                )


            elif difference <= good_tolerance:

                fit = (
                    "🟡 Good protein match"
                )


            else:

                fit = (
                    "🟠 Moderate protein match"
                )


            st.write(
                f"**Fit:** {fit}"
            )


            st.divider()


        # -----------------------------
        # GEMINI AI INSIGHT
        # -----------------------------
        st.subheader(
            "🤖 NutriSense AI Insight"
        )


        with st.spinner(
            "NutriSense AI is analysing your meal options..."
        ):

            ai_insight = get_ai_insight(
                recommendations=recommendations,
                meal=meal,
                protein_goal=protein_goal,
                diet=diet
            )


        st.info(
            ai_insight
        )


# -----------------------------
# DISCLAIMER
# -----------------------------
st.divider()


st.caption(
    "⚠️ Nutrition values are estimated using assumed typical serving sizes "
    "for MVP demonstration purposes. Actual protein intake may vary based "
    "on portion size and food preparation. For allergies or medically "
    "required diets, verify information with the food provider."
)