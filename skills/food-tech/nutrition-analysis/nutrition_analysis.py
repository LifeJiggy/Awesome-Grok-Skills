"""
Nutrition Analysis Module
Part of the food-tech skill domain

Provides nutrient database management, recipe analysis, dietary assessment,
allergen detection, nutrition labeling, and meal planning.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import statistics


class DietaryPreference(Enum):
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten_free"
    KETO = "keto"
    PALEO = "paleo"
    DAIRY_FREE = "dairy_free"
    HIGH_PROTEIN = "high_protein"
    LOW_SODIUM = "low_sodium"


class Regulation(Enum):
    FDA = "fda"
    EU = "eu"
    HEALTH_CANADA = "health_canada"
    FSANZ = "fsanz"


class AllergenType(Enum):
    MILK = "milk"
    EGGS = "eggs"
    FISH = "fish"
    SHELLFISH = "shellfish"
    TREE_NUTS = "tree_nuts"
    PEANUTS = "peanuts"
    WHEAT = "wheat"
    SOYBEANS = "soybeans"
    SESAME = "sesame"


@dataclass
class NutrientProfile:
    calories: float = 0.0
    protein_g: float = 0.0
    carbs_g: float = 0.0
    fat_g: float = 0.0
    fiber_g: float = 0.0
    sugar_g: float = 0.0
    sodium_mg: float = 0.0
    saturated_fat_g: float = 0.0
    cholesterol_mg: float = 0.0
    vitamin_c_mg: float = 0.0
    calcium_mg: float = 0.0
    iron_mg: float = 0.0
    potassium_mg: float = 0.0

    def scale(self, factor: float) -> "NutrientProfile":
        return NutrientProfile(**{k: v * factor for k, v in self.__dict__.items()})


@dataclass
class Ingredient:
    food: str
    amount_g: float
    nutrients: Optional[NutrientProfile] = None


@dataclass
class Recipe:
    name: str
    ingredients: List[Dict[str, Any]]
    servings: int
    prep_time_minutes: int = 0
    cook_time_minutes: int = 0


@dataclass
class RecipeAnalysis:
    recipe_name: str
    total_nutrients: NutrientProfile
    per_serving: NutrientProfile
    servings: int
    allergens: List[AllergenType]
    ingredient_count: int


@dataclass
class NutrientSummaryItem:
    average_intake: float
    unit: str
    dri_value: float
    percent_dri: float
    status: str  # adequate, low, deficient, excess


@dataclass
class DietaryAssessmentResult:
    nutrient_summary: Dict[str, NutrientSummaryItem]
    deficient_nutrients: List[str]
    excess_nutrients: List[str]
    overall_diet_quality: float  # 0-100
    recommendations: List[str]


@dataclass
class MealItem:
    name: str
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    ingredients: List[str] = field(default_factory=list)


@dataclass
class DayPlan:
    day_number: int
    meals: List[MealItem]
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
    estimated_cost: float = 0.0


@dataclass
class MealPlan:
    days: List[DayPlan]
    total_calories: float
    average_daily_calories: float
    average_daily_cost: float


@dataclass
class LabelLine:
    name: str
    amount: str
    daily_value_pct: float


@dataclass
class NutritionLabel:
    product_name: str
    serving_size: str
    servings_per_container: int
    calories: int
    nutrient_lines: List[LabelLine]
    regulation: str


class NutritionAnalyzer:
    """Food composition analysis with nutrient databases."""

    NUTRIENT_DB = {
        "Atlantic salmon": NutrientProfile(208, 20.4, 0, 13.4, 0, 0, 59, 3.0, 55, 0, 12, 0.3, 363),
        "Quinoa, cooked": NutrientProfile(120, 4.4, 21.3, 1.9, 2.8, 0.9, 7, 0.2, 0, 0, 17, 1.5, 172),
        "Olive oil": NutrientProfile(884, 0, 0, 100, 0, 0, 2, 13.8, 0, 0, 1, 0.6, 1),
        "Lemon juice": NutrientProfile(22, 0.4, 6.9, 0.2, 0.3, 2.5, 2, 0, 0, 39, 6, 0.1, 103),
        "Spinach, raw": NutrientProfile(23, 2.9, 3.6, 0.4, 2.2, 0.4, 79, 0.1, 0, 28, 99, 2.7, 558),
    }

    ALLERGEN_DB = {
        "Atlantic salmon": [AllergenType.FISH],
        "Wheat flour": [AllergenType.WHEAT],
        "Milk": [AllergenType.MILK],
        "Eggs": [AllergenType.EGGS],
        "Peanuts": [AllergenType.PEANUTS],
        "Almonds": [AllergenType.TREE_NUTS],
        "Soy sauce": [AllergenType.SOYBEANS, AllergenType.WHEAT],
        "Shrimp": [AllergenType.SHELLFISH],
        "Sesame oil": [AllergenType.SESAME],
    }

    def __init__(self, database: str = "usda_fndds", serving_size: int = 100):
        self.database = database
        self.serving_size = serving_size

    def analyze_recipe(self, recipe: Recipe) -> RecipeAnalysis:
        total = NutrientProfile()
        allergens = set()

        for ing in recipe.ingredients:
            food = ing["food"]
            amount = ing["amount_g"]
            factor = amount / 100

            nutrients = self.NUTRIENT_DB.get(food, NutrientProfile())
            total = NutrientProfile(**{
                k: getattr(total, k) + getattr(nutrients, k) * factor
                for k in total.__dict__
            })

            if food in self.ALLERGEN_DB:
                allergens.update(self.ALLERGEN_DB[food])

        per_serving = total.scale(1.0 / max(recipe.servings, 1))
        return RecipeAnalysis(
            recipe_name=recipe.name,
            total_nutrients=total, per_serving=per_serving,
            servings=recipe.servings, allergens=list(allergens),
            ingredient_count=len(recipe.ingredients),
        )


class DietaryAssessment:
    """Dietary intake assessment against reference standards."""

    DRI = {
        "calories": (2000, "kcal"), "protein_g": (50, "g"),
        "fiber_g": (25, "g"), "vitamin_c_mg": (90, "mg"),
        "calcium_mg": (1000, "mg"), "iron_mg": (18, "mg"),
        "potassium_mg": (2600, "mg"), "sodium_mg": (2300, "mg"),
        "fat_g": (65, "g"), "carbs_g": (300, "g"),
    }

    def __init__(self, reference_standard: str = "DRI",
                 age: int = 30, sex: str = "female", activity_level: str = "moderate"):
        self.standard = reference_standard
        self.age = age
        self.sex = sex
        self.activity_level = activity_level

    def analyze_intake(self, intake_data: str, output_format: str = "detailed") -> DietaryAssessmentResult:
        sample_intake = NutrientProfile(1850, 65, 220, 55, 20, 30, 1800, 18, 200, 45, 750, 14, 2100)
        summary: Dict[str, NutrientSummaryItem] = {}

        for nutrient, (dri, unit) in self.DRI.items():
            value = getattr(sample_intake, nutrient, 0)
            pct = (value / dri * 100) if dri > 0 else 0
            status = "adequate" if pct >= 100 else "low" if pct >= 50 else "deficient"
            if nutrient == "sodium_mg" and pct > 100:
                status = "excess"
            summary[nutrient] = NutrientSummaryItem(value, unit, dri, round(pct), status)

        deficient = [n for n, s in summary.items() if s.status == "deficient"]
        excess = [n for n, s in summary.items() if s.status == "excess"]
        quality = max(0, 100 - len(deficient) * 10 - len(excess) * 8)

        recs = []
        if "iron_mg" in deficient:
            recs.append("Increase iron-rich foods: red meat, spinach, legumes")
        if "calcium_mg" in deficient:
            recs.append("Add dairy or fortified alternatives")

        return DietaryAssessmentResult(
            nutrient_summary=summary, deficient_nutrients=deficient,
            excess_nutrients=excess, overall_diet_quality=quality,
            recommendations=recs,
        )


class MealPlanner:
    """Automated meal plan generation."""

    SAMPLE_MEALS = {
        "breakfast": [
            MealItem("Greek Yogurt Parfait", 350, 20, 45, 10),
            MealItem("Oatmeal with Berries", 300, 10, 55, 7),
            MealItem("Egg & Avocado Toast", 400, 18, 30, 25),
        ],
        "lunch": [
            MealItem("Grilled Chicken Salad", 450, 35, 20, 25),
            MealItem("Turkey Wrap", 400, 25, 40, 15),
            MealItem("Quinoa Buddha Bowl", 420, 15, 55, 16),
        ],
        "dinner": [
            MealItem("Salmon with Vegetables", 500, 35, 25, 28),
            MealItem("Lean Beef Stir-fry", 480, 30, 40, 20),
            MealItem("Pasta Primavera", 450, 15, 60, 15),
        ],
        "snack": [
            MealItem("Apple with Almond Butter", 200, 6, 25, 10),
            MealItem("Trail Mix", 250, 8, 30, 14),
        ],
    }

    def __init__(self, calorie_target: int = 2000, protein_target_g: int = 100,
                 dietary_preferences: Optional[List[DietaryPreference]] = None,
                 allergies: Optional[List[str]] = None, budget_per_day: float = 20.0):
        self.calories = calorie_target
        self.protein = protein_target_g
        self.preferences = dietary_preferences or []
        self.allergies = [a.lower() for a in allergies or []]
        self.budget = budget_per_day

    def generate(self, days: int = 7) -> MealPlan:
        day_plans = []
        for d in range(1, days + 1):
            meals = []
            for meal_type in ["breakfast", "lunch", "dinner", "snack"]:
                options = self.SAMPLE_MEALS.get(meal_type, [])
                if options:
                    meals.append(options[d % len(options)])

            total_cals = sum(m.calories for m in meals)
            total_p = sum(m.protein_g for m in meals)
            total_c = sum(m.carbs_g for m in meals)
            total_f = sum(m.fat_g for m in meals)

            day_plans.append(DayPlan(
                day_number=d, meals=meals,
                total_calories=total_cals, total_protein_g=total_p,
                total_carbs_g=total_c, total_fat_g=total_f,
                estimated_cost=round(self.budget * 0.9, 2),
            ))

        total_cal = sum(d.total_calories for d in day_plans)
        return MealPlan(
            days=day_plans, total_calories=total_cal,
            average_daily_calories=total_cal / max(days, 1),
            average_daily_cost=round(self.budget * 0.9, 2),
        )


class NutritionLabelGenerator:
    """Automated FDA/EU nutrition label generation."""

    def __init__(self, regulation: str = "FDA", serving_size_unit: str = "g"):
        self.regulation = regulation
        self.unit = serving_size_unit

    def generate(self, product_name: str, serving_size_g: float,
                 servings_per_container: int,
                 nutrients: Dict[str, float]) -> NutritionLabel:
        dv = {
            "total_fat_g": 78, "saturated_fat_g": 20, "cholesterol_mg": 300,
            "sodium_mg": 2300, "total_carbs_g": 275, "dietary_fiber_g": 28,
            "added_sugars_g": 50, "protein_g": 50,
            "vitamin_d_mcg": 20, "calcium_mg": 1300, "iron_mg": 18,
            "potassium_mg": 4700,
        }

        lines = []
        nutrient_labels = {
            "total_fat_g": "Total Fat", "saturated_fat_g": "  Saturated Fat",
            "trans_fat_g": "  Trans Fat", "cholesterol_mg": "Cholesterol",
            "sodium_mg": "Sodium", "total_carbs_g": "Total Carbohydrate",
            "dietary_fiber_g": "  Dietary Fiber", "total_sugars_g": "  Total Sugars",
            "added_sugars_g": "    Includes Added Sugars", "protein_g": "Protein",
        }

        for key, label in nutrient_labels.items():
            val = nutrients.get(key, 0)
            dv_val = dv.get(key, 0)
            dv_pct = round(val / dv_val * 100) if dv_val > 0 else 0
            unit = "g" if "_g" in key else "mg" if "_mg" in key else "mcg" if "_mcg" in key else ""
            lines.append(LabelLine(label, f"{val}{unit}", dv_pct))

        return NutritionLabel(
            product_name=product_name,
            serving_size=f"{serving_size_g:.0f}g",
            servings_per_container=servings_per_container,
            calories=nutrients.get("calories", 0),
            nutrient_lines=lines, regulation=self.regulation,
        )


def main():
    print("=" * 60)
    print("  Nutrition Analysis Demo")
    print("=" * 60)

    # Recipe analysis
    print("\n--- Recipe Analysis ---")
    analyzer = NutritionAnalyzer()
    recipe = Recipe("Grilled Salmon", [
        {"food": "Atlantic salmon", "amount_g": 200},
        {"food": "Quinoa, cooked", "amount_g": 150},
        {"food": "Olive oil", "amount_g": 15},
        {"food": "Lemon juice", "amount_g": 30},
        {"food": "Spinach, raw", "amount_g": 50},
    ], servings=2)
    analysis = analyzer.analyze_recipe(recipe)
    print(f"  {analysis.recipe_name} ({analysis.servings} servings)")
    print(f"  Cal: {analysis.per_serving.calories:.0f}, P: {analysis.per_serving.protein_g:.1f}g, "
          f"C: {analysis.per_serving.carbs_g:.1f}g, F: {analysis.per_serving.fat_g:.1f}g")
    print(f"  Allergens: {[a.value for a in analysis.allergens]}")

    # Dietary assessment
    print("\n--- Dietary Assessment ---")
    da = DietaryAssessment(age=35, sex="female")
    result = da.analyze_intake("diary.csv")
    print(f"  Diet quality: {result.overall_diet_quality:.0f}/100")
    print(f"  Deficient: {result.deficient_nutrients}")
    for rec in result.recommendations:
        print(f"  -> {rec}")

    # Meal planning
    print("\n--- Meal Planning ---")
    mp = MealPlanner(calorie_target=2000, protein_target_g=100, allergies=["peanuts"])
    plan = mp.generate(days=3)
    print(f"  3-day plan: avg {plan.average_daily_calories:.0f} cal/day")
    for day in plan.days[:1]:
        for meal in day.meals:
            print(f"    {meal.name}: {meal.calories} kcal")

    # Label generation
    print("\n--- Nutrition Label ---")
    lg = NutritionLabelGenerator(regulation="FDA")
    label = lg.generate("Organic Granola", 55, 8, {
        "calories": 210, "total_fat_g": 7, "saturated_fat_g": 1,
        "sodium_mg": 160, "total_carbs_g": 32, "dietary_fiber_g": 4,
        "added_sugars_g": 8, "protein_g": 6,
    })
    print(f"  {label.product_name} - {label.serving_size}")
    for line in label.nutrient_lines[:5]:
        print(f"    {line.name}: {line.amount} ({line.daily_value_pct}% DV)")


if __name__ == "__main__":
    main()
