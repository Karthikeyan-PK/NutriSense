import itertools


# -----------------------------------
# CALCULATE RECOMMENDATION SCORE
# -----------------------------------
def calculate_score(combo, protein_goal):

    total_protein = sum(
        item["protein"]
        for item in combo
    )

    difference = abs(
        protein_goal - total_protein
    )

    # -----------------------------------
    # PROTEIN MATCH
    # -----------------------------------

    # Allow flexibility around the goal.
    # Example:
    # Goal = 20g
    # 18g to 22g is considered an excellent range.
    tolerance = max(2, protein_goal * 0.10)

    if difference <= tolerance:
        score = 100
    else:
        adjusted_difference = difference - tolerance

        score = max(
            0,
            100 - (adjusted_difference * 8)
        )

    roles = [
        item["role"]
        for item in combo
    ]

    # -----------------------------------
    # PRACTICAL MEAL BONUSES
    # -----------------------------------

    # Base + protein source makes a
    # proper hostel meal structure
    if (
        "base" in roles
        and "protein_source" in roles
    ):
        score += 5

    # Vegetable improves meal balance
    if "vegetable" in roles:
        score += 2

    # A substantial main such as biryani
    # is already a complete meal
    if "substantial_main" in roles:
        score += 3

    # Slight preference for simpler,
    # practical combinations when protein
    # scores are otherwise similar
    if len(combo) > 3:
        score -= (len(combo) - 3) * 2

    return round(score, 1)


# -----------------------------------
# CHECK WHETHER A COMBINATION
# IS PRACTICAL
# -----------------------------------
def is_valid_combination(
    combo,
    meal,
    diet,
    non_veg_available
):

    roles = [
        item["role"]
        for item in combo
    ]

    # -----------------------------------
    # RULE 1:
    # Only one base
    #
    # Avoid:
    # Rice + Chapati + everything
    # -----------------------------------
    if roles.count("base") > 1:
        return False

    # -----------------------------------
    # RULE 2:
    # Only one substantial main
    #
    # Avoid:
    # Paneer Biryani + Chicken Biryani
    # -----------------------------------
    if roles.count("substantial_main") > 1:
        return False

    # -----------------------------------
    # RULE 3:
    # SUBSTANTIAL MAIN LOGIC
    #
    # Biryani is already a complete main.
    #
    # Avoid:
    # Chicken Biryani + Soya 65
    # Chicken Biryani + Masoor Dal
    # Paneer Biryani + Soya 65
    #
    # But vegetables/accompaniments
    # can still be added.
    # -----------------------------------
    if "substantial_main" in roles:

        if "protein_source" in roles:
            return False

        if "base" in roles:
            return False

    # -----------------------------------
    # RULE 4:
    # SNACK LOGIC
    # -----------------------------------
    if meal == "Snacks":

        # Every snack recommendation
        # must contain the actual snack
        if "snack" not in roles:
            return False

    else:

        # -----------------------------------
        # RULE 5:
        # NORMAL MEAL LOGIC
        #
        # A meal should contain either:
        #
        # - a protein source
        # OR
        # - a substantial main
        # -----------------------------------
        if (
            "protein_source" not in roles
            and "substantial_main" not in roles
        ):
            return False

    # -----------------------------------
    # RULE 6:
    # NON-VEGETARIAN PRIORITY
    #
    # If the user selects Non-Vegetarian
    # AND non-veg food is available,
    # the recommendation must contain
    # at least one non-veg item.
    # -----------------------------------
    if diet == "Non-Vegetarian" and non_veg_available:

        contains_non_veg = any(
            item["type"] == "Non-Vegetarian"
            for item in combo
        )

        if not contains_non_veg:
            return False

    return True


# -----------------------------------
# GET TOP RECOMMENDATIONS
# -----------------------------------
def get_recommendations(
    menu_items,
    protein_goal,
    diet,
    meal
):

    # -----------------------------------
    # 1. REMOVE DESSERTS
    # -----------------------------------
    all_available_items = [
        item
        for item in menu_items
        if item["role"] != "dessert"
    ]

    # -----------------------------------
    # 2. APPLY DIETARY PREFERENCE
    # -----------------------------------

    if diet == "Vegetarian":

        available_items = [
            item
            for item in all_available_items
            if item["type"] == "Vegetarian"
        ]

    else:

        # Non-Vegetarian users can access
        # both vegetarian and non-vegetarian
        # food items.
        available_items = all_available_items

    # -----------------------------------
    # 3. CHECK IF NON-VEG EXISTS
    # -----------------------------------
    non_veg_available = any(
        item["type"] == "Non-Vegetarian"
        for item in available_items
    )

    recommendations = []

    # -----------------------------------
    # 4. GENERATE COMBINATIONS
    #
    # Maximum 4 items keeps plates
    # practical while allowing hostel
    # users to take multiple dishes.
    # -----------------------------------
    max_combination_size = min(
        4,
        len(available_items)
    )

    for size in range(
        1,
        max_combination_size + 1
    ):

        for combo in itertools.combinations(
            available_items,
            size
        ):

            # Check practical meal rules
            if not is_valid_combination(
                combo,
                meal,
                diet,
                non_veg_available
            ):
                continue

            total_protein = sum(
                item["protein"]
                for item in combo
            )

            difference = abs(
                protein_goal - total_protein
            )

            score = calculate_score(
                combo,
                protein_goal
            )

            recommendations.append({

                "foods": [
                    item["name"]
                    for item in combo
                ],

                "protein": round(
                    total_protein,
                    1
                ),

                "difference": round(
                    difference,
                    1
                ),

                "score": score,

                "servings": [
                    f"{item['name']} ({item['serving']})"
                    for item in combo
                ]

            })

    # -----------------------------------
    # 5. RANK RECOMMENDATIONS
    #
    # Priority:
    #
    # 1. Closest to protein goal
    # 2. Better practical meal quality
    # 3. Fewer unnecessary items
    #
    # Example for a 20g goal:
    #
    # 20g -> Difference 0 -> Highest priority
    # 19g -> Difference 1 -> Next
    # 21g -> Difference 1 -> Next
    # 18g -> Difference 2 -> After that
    # -----------------------------------
    recommendations.sort(

        key=lambda x: (

            # Closest protein target FIRST
            x["difference"],

            # Better meal structure SECOND
            -x["score"],

            # Prefer simpler plates if tied
            len(x["foods"])

        )

    )

    # -----------------------------------
    # 6. REMOVE EXACT DUPLICATES
    # -----------------------------------
    unique_recommendations = []

    seen = set()

    for recommendation in recommendations:

        signature = tuple(
            recommendation["foods"]
        )

        if signature not in seen:

            unique_recommendations.append(
                recommendation
            )

            seen.add(signature)

    # -----------------------------------
    # 7. RETURN TOP 3
    # -----------------------------------
    return unique_recommendations[:3]