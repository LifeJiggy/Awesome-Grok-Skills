---
name: "nutrition-analysis"
category: "food-tech"
version: "2.0.0"
tags: ["food-tech", "nutrition", "food-composition", "dietary-analysis", "health"]
difficulty: "intermediate"
estimated_time: "35-50 minutes"
prerequisites: ["python", "nutrition-science-basics"]
---

# Nutrition Analysis

## Overview

Nutrition analysis provides computational tools for evaluating the nutritional content of foods, dietary patterns, and meal plans. This module covers nutrient database management, recipe analysis, dietary assessment, allergen identification, regulatory nutrition labeling (FDA, EU), and personalized nutrition recommendations based on health goals and medical conditions.

## Core Capabilities

- **Nutrient Database**: Comprehensive food composition database with 150+ nutrients per food item including macro/micronutrients, amino acids, fatty acids, and phytochemicals
- **Recipe Analysis**: Automatic nutritional calculation for recipes with ingredient substitution suggestions for dietary restrictions
- **Dietary Assessment**: Analysis of dietary intake against reference values (DRI, RDA, AI) with gap identification
- **Allergen Management**: Detection and labeling of major allergens (Big 9: milk, eggs, fish, shellfish, tree nuts, peanuts, wheat, soybeans, sesame)
- **Nutrition Labeling**: Automated generation of FDA Nutrition Facts and EU nutrition declarations with rounding rules
- **Meal Planning**: Algorithmic meal plan generation meeting nutritional targets, dietary preferences, and budget constraints
- **Glycemic Analysis**: Glycemic index/load calculation and blood sugar impact prediction
- **Food Scoring**: Nutrient profiling systems (NOVA, Nutri-Score, HSR) for food classification

## Usage Examples

### Recipe Nutrition Analysis

```python
from food_tech.nutrition_analysis import NutritionAnalyzer, Recipe

analyzer = NutritionAnalyzer(database="usda_fndds", serving_size=100)

# Analyze a recipe
recipe = Recipe(
    name="Grilled Salmon with Quinoa",
    ingredients=[
        {"food": "Atlantic salmon", "amount_g": 200},
        {"food": "Quinoa, cooked", "amount_g": 150},
        {"food": "Olive oil", "amount_g": 15},
        {"food": "Lemon juice", "amount_g": 30},
        {"food": "Spinach, raw", "amount_g": 50},
    ],
    servings=2,
)

analysis = analyzer.analyze_recipe(recipe)
print(f"Per serving:")
print(f"  Calories: {analysis.per_serving.calories:.0f} kcal")
print(f"  Protein: {analysis.per_serving.protein_g:.1f} g")
print(f"  Carbs: {analysis.per_serving.carbs_g:.1f} g")
print(f"  Fat: {analysis.per_serving.fat_g:.1f} g")
print(f"  Fiber: {analysis.per_serving.fiber_g:.1f} g")
print(f"Allergens detected: {analysis.allergens}")
```

### Dietary Assessment

```python
from food_tech.nutrition_analysis import DietaryAssessment

assessment = DietaryAssessment(
    reference_standard="DRI",
    age=35,
    sex="female",
    activity_level="moderate",
)

# Analyze 3-day food diary
result = assessment.analyze_intake(
    intake_data="food_diary_3day.csv",
    output_format="detailed",
)

print(f"Average daily intake:")
for nutrient, data in result.nutrient_summary.items():
    status = "ADEQUATE" if data.percent_dri >= 100 else "LOW" if data.percent_dri >= 50 else "DEFICIENT"
    print(f"  {nutrient}: {data.average_intake:.1f} {data.unit} "
          f"({data.percent_dri:.0f}% DRI) [{status}]")

print(f"\nNutrients of concern: {result.deficient_nutrients}")
print(f"Excess nutrients: {result.excess_nutrients}")
```

### Meal Plan Generation

```python
from food_tech.nutrition_analysis import MealPlanner, DietaryPreference

planner = MealPlanner(
    calorie_target=2000,
    protein_target_g=100,
    dietary_preferences=[DietaryPreference.HIGH_PROTEIN],
    allergies=["peanuts", "shellfish"],
    budget_per_day=15.00,
)

plan = planner.generate(days=7)
print(f"7-Day Meal Plan ({plan.total_calories:,} total calories)")
for day in plan.days:
    print(f"\n  Day {day.day_number}:")
    for meal in day.meals:
        print(f"    {meal.name}: {meal.calories:.0f} kcal, "
              f"P={meal.protein_g:.0f}g, C={meal.carbs_g:.0f}g, F={meal.fat_g:.0f}g")
    print(f"    Daily cost: ${day.estimated_cost:.2f}")
```

### Nutrition Label Generation

```python
from food_tech.nutrition_analysis import NutritionLabelGenerator

label_gen = NutritionLabelGenerator(
    regulation="FDA",
    serving_size_unit="g",
)

# Generate nutrition facts label
label = label_gen.generate(
    product_name="Organic Granola",
    serving_size_g=55,
    servings_per_container=8,
    nutrients={
        "calories": 210, "total_fat_g": 7, "saturated_fat_g": 1,
        "trans_fat_g": 0, "cholesterol_mg": 0, "sodium_mg": 160,
        "total_carbs_g": 32, "dietary_fiber_g": 4, "total_sugars_g": 9,
        "added_sugars_g": 8, "protein_g": 6,
        "vitamin_d_mcg": 0, "calcium_mg": 40, "iron_mg": 2,
        "potassium_mg": 150,
    },
)

print("FDA Nutrition Facts")
print(f"Serving Size: {label.serving_size}")
print(f"Calories: {label.calories}")
for line in label.nutrient_lines:
    print(f"  {line.name}: {line.amount} ({line.daily_value_pct:.0f}%)")
```

## Best Practices

- Use USDA FoodData Central or equivalent authoritative databases as primary nutrient data sources
- Apply FDA rounding rules for nutrition labels: calories to nearest 5, fat to nearest 0.5g, etc.
- Account for nutrient losses during cooking (water-soluble vitamins can lose 30-50% during boiling)
- Identify all major allergens including sesame (added to FDA Big 9 in 2023) in recipe analysis
- Use bioavailability factors when comparing plant vs animal source nutrient absorption
- Consider nutrient-nutrient interactions (vitamin C enhances iron absorption, calcium inhibits it)
- Update nutrient databases annually as food composition data evolves
- Validate recipe calculations against laboratory analysis for commercial nutrition labeling
- Account for seasonal variation in fresh produce nutrient content
- Document all nutrient data sources and calculation methods for regulatory compliance

## Related Modules

- `food-tech/food-safety` - Allergen management and food safety integration
- `food-tech/restaurant-tech` - Menu nutrition display and analysis
- `food-tech/supply-chain` - Nutritional quality of sourced ingredients
