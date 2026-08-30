🥗 NutriSense
AI-Assisted Mess Meal Recommendation System

NutriSense is an AI-assisted nutrition decision-support MVP designed to help fitness-conscious college students make quicker and more confident food choices from their available campus mess menu.

Instead of manually searching for nutritional information and comparing multiple dishes, users can select their meal, enter a protein goal, choose a dietary preference, and receive personalized meal recommendations based on the food currently available.

🎯 Problem

Fitness-conscious college students who depend on campus mess or canteen food often face a lack of clear nutritional information.

As a result, they may:

Guess which foods contain more protein
Find it difficult to compare available meal options
Spend time manually searching for nutrition information
Make food decisions without knowing how well they support their protein goals
Core Problem

Students need a quick and low-effort way to determine which available mess foods or meal combinations best support their protein goal.

💡 Solution

NutriSense converts the available mess menu into personalized, protein-focused meal recommendations.

The user can:

Select a meal
View the available mess menu
Enter a protein goal
Select a dietary preference
Get ranked meal recommendations
View estimated protein values
Understand why a recommendation was selected
👤 Target User

The primary target user is:

Fitness-conscious college students who regularly depend on a campus mess or canteen and want to improve their protein intake.

🚀 MVP Features
🍽️ Available Mess Menu

Displays the available food items for:

Breakfast
Lunch
Snacks
Dinner
💪 Protein Goal

Users can specify their desired protein target for a particular meal.

🥬 Dietary Preference

Users can select:

Vegetarian
Non-Vegetarian

This ensures unsuitable food recommendations are filtered out.

🏆 Personalized Recommendations

NutriSense generates and ranks the top three practical meal combinations based on:

Dietary eligibility
Protein goal alignment
Estimated protein contribution
Food availability
Practical meal combinations
🤖 AI-Powered Insights

Gemini API is used to generate a user-friendly explanation and comparison of the recommended options.

📊 Recommendation Explanation

The system provides:

Recommended foods
Estimated protein
Difference from the user's protein target
Protein match quality
Explanation of why the recommendation is suitable
🔄 User Workflow
Open NutriSense
        ↓
Select Meal
        ↓
View Available Menu
        ↓
Enter Protein Goal
        ↓
Select Dietary Preference
        ↓
Get Recommendation
        ↓
View Top 3 Meal Options
        ↓
View AI Insight & Explanation
        ↓
Decide What to Eat
🛠️ Technology Stack
Python
Streamlit
Google Gemini API
GitHub
VS Code
📁 Project Structure
NutriSense/
│
├── app.py
├── recommendation.py
├── menu_data.json
├── test_gemini.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
File Description

app.py
Main Streamlit application and user interface.

recommendation.py
Contains the recommendation logic and practical meal-combination rules.

menu_data.json
Contains the available mess menu and estimated nutritional information.

test_gemini.py
Tests the Gemini API connection and AI functionality.

requirements.txt
Lists the Python packages required to run the application.

.env.example
Example environment variable configuration.

⚙️ Installation and Setup
1. Clone the Repository
git clone https://github.com/Karthikeyan-PK/NutriSense.git
2. Navigate to the Project
cd NutriSense
3. Create a Virtual Environment
python -m venv .venv
4. Activate the Virtual Environment
Windows Git Bash
source .venv/Scripts/activate
5. Install Dependencies
pip install -r requirements.txt
🔑 Gemini API Configuration

Create a .env file in the project folder.

Add your Gemini API key:

GEMINI_API_KEY=your_api_key_here

⚠️ Never upload your actual .env file or API key to GitHub.

▶️ Run the Application
streamlit run app.py

The application will open in your browser.

🧠 Recommendation Logic

The recommendation engine evaluates possible food combinations based on explicit product rules.

Key Criteria
Dietary Eligibility
Recommendations must match the user's dietary preference.
Protein Goal Alignment
Recommendations are ranked based on how closely they match the selected protein goal.
Protein Contribution
Combinations with stronger estimated protein contribution are preferred.
Actual Availability
Only foods available in the selected mess menu are considered.
Practical Meal Structure
Unrealistic combinations are avoided using rules such as:
Only one base food
Only one substantial main dish
Avoid combining multiple competing main meals
Non-vegetarian users receive a non-vegetarian recommendation when non-vegetarian food is available
⚠️ Important Disclaimer

Nutrition values used in NutriSense are estimated values based on assumed typical serving sizes.

Actual nutritional intake may vary depending on:

Portion size
Ingredients
Food preparation
Recipes

NutriSense is designed as a decision-support tool and does not provide medical or clinical nutrition advice.

🗺️ Future Roadmap

Potential future versions of NutriSense may include:

V2
Menu image upload and analysis
Portion adjustment
Saved dietary preferences
Weekly mess planning
Future
Nutrition history
Restaurant menu analysis
Food-delivery integration
Advanced personalization
Expanded nutritional analysis
📌 MVP Scope

NutriSense V1 focuses on one core problem:

Helping a fitness-conscious college student decide what to eat from the currently available mess menu based on their protein goal and dietary preference.

The project intentionally focuses on a small and testable MVP rather than building a full nutrition-tracking application.
