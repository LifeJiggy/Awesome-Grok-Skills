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

## Advanced Configuration

### Nutrient Database Configuration

```yaml
nutrient_database:
  primary:
    source: "USDA_FoodData_Central"
    api_key: "${USDA_API_KEY}"
    base_url: "https://api.nal.usda.gov/fdc/v1"
    cache_ttl_hours: 24
    
  fallback:
    source: "Nutritionix"
    api_key: "${NUTRITIONIX_API_KEY}"
    base_url: "https://trackapi.nutritionix.com/v2"
    
  local_cache:
    enabled: true
    max_items: 100000
    refresh_interval_days: 7
    
  nutrients_tracked:
    macros:
      - "calories"
      - "protein_g"
      - "carbohydrates_g"
      - "fat_g"
      - "fiber_g"
      - "water_g"
      
    vitamins:
      - "vitamin_a_mcg"
      - "vitamin_c_mg"
      - "vitamin_d_mcg"
      - "vitamin_e_mg"
      - "vitamin_k_mcg"
      - "thiamin_mg"
      - "riboflavin_mg"
      - "niacin_mg"
      - "vitamin_b6_mg"
      - "folate_mcg"
      - "vitamin_b12_mcg"
      
    minerals:
      - "calcium_mg"
      - "iron_mg"
      - "magnesium_mg"
      - "phosphorus_mg"
      - "potassium_mg"
      - "sodium_mg"
      - "zinc_mg"
      - "copper_mg"
      - "manganese_mg"
      - "selenium_mcg"
```

### Allergen Configuration

```yaml
allergens:
  fda_big_9:
    - name: "milk"
      code: "MILK"
      severity: "high"
      cross_contact_risk: true
      
    - name: "eggs"
      code: "EGGS"
      severity: "high"
      cross_contact_risk: true
      
    - name: "fish"
      code: "FISH"
      severity: "high"
      cross_contact_risk: true
      species_list: ["anchovy", "bass", "catfish", "cod", "flounder", "haddock", "herring", "mackerel", "mahi mahi", "perch", "pike", "pollock", "salmon", "scrod", "sole", "snapper", "swordfish", "tilapia", "trout", "tuna"]
      
    - name: "shellfish"
      code: "SHELLFISH"
      severity: "high"
      cross_contact_risk: true
      species_list: ["clam", "crab", "lobster", "mussel", "oyster", "scallop", "shrimp"]
      
    - name: "tree nuts"
      code: "TREE_NUTS"
      severity: "high"
      cross_contact_risk: true
      species_list: ["almond", "brazil nut", "cashew", "chestnut", "coconut", "filbert/hazelnut", "macadamia nut", "pecan", "pine nut", "pistachio", "walnut"]
      
    - name: "peanuts"
      code: "PEANUTS"
      severity: "high"
      cross_contact_risk: true
      
    - name: "wheat"
      code: "WHEAT"
      severity: "high"
      cross_contact_risk: true
      
    - name: "soybeans"
      code: "SOYBEANS"
      severity: "high"
      cross_contact_risk: true
      
    - name: "sesame"
      code: "SESAME"
      severity: "high"
      cross_contact_risk: true
      
  additional_allergens:
    - name: "mustard"
      code: "MUSTARD"
      region: "EU"
      severity: "medium"
      
    - name: "celery"
      code: "CELERY"
      region: "EU"
      severity: "medium"
      
    - name: "lupin"
      code: "LUPIN"
      region: "EU"
      severity: "medium"
      
    - name: "mollusks"
      code: "MOLLUSKS"
      region: "EU"
      severity: "medium"
```

### Nutrition Labeling Configuration

```yaml
labeling:
  FDA:
    serving_size_rules:
      reference_amounts_customarily_consumed:
        - food_category: "beverages"
          amount_g: 240
        - food_category: "meal_replacement"
          amount_g: 400
        - food_category: "desserts"
          amount_g: 120
          
    rounding_rules:
      calories:
        threshold: 5
        round_to: 5
      fat_g:
        threshold: 0.5
        round_to: 0.5
      sodium_mg:
        threshold: 5
        round_to: 5
      sugars_g:
        threshold: 0.5
        round_to: 0.5
      protein_g:
        threshold: 0.5
        round_to: 0.5
        
    daily_values:
      calories: 2000
      total_fat_g: 78
      saturated_fat_g: 20
      cholesterol_mg: 300
      sodium_mg: 2300
      total_carbs_g: 275
      dietary_fiber_g: 28
      added_sugars_g: 50
      vitamin_d_mcg: 20
      calcium_mg: 1300
      iron_mg: 18
      potassium_mg: 4700
      
  EU:
    per_100g: true
    per_serving: true
    energy_kj: true
    energy_kcal: true
    rounding_rules:
      energy_kj:
        threshold: 1
        round_to: 1
      energy_kcal:
        threshold: 1
        round_to: 1
      fat_g:
        threshold: 0.1
        round_to: 0.1
      saturates_g:
        threshold: 0.1
        round_to: 0.1
      carbohydrate_g:
        threshold: 0.1
        round_to: 0.1
      sugars_g:
        threshold: 0.1
        round_to: 0.1
      protein_g:
        threshold: 0.1
        round_to: 0.1
      salt_g:
        threshold: 0.01
        round_to: 0.01
```

## Architecture Patterns

### Nutrient Calculation Engine

```python
class NutrientCalculationEngine:
    def __init__(self, nutrient_db, conversion_factors):
        self.db = nutrient_db
        self.conversions = conversion_factors
    
    async def calculate_recipe_nutrition(self, recipe: Recipe) -> NutritionResult:
        total_nutrients = {}
        
        for ingredient in recipe.ingredients:
            # Get nutrient data per 100g
            food_data = await self.db.get_food(ingredient.food_name)
            
            # Calculate for actual amount
            factor = ingredient.amount_g / 100.0
            
            for nutrient, value_per_100g in food_data.nutrients.items():
                if nutrient not in total_nutrients:
                    total_nutrients[nutrient] = 0
                total_nutrients[nutrient] += value_per_100g * factor
        
        # Apply cooking loss factors if applicable
        if recipe.cooking_method:
            total_nutrients = self.apply_cooking_losses(total_nutrients, recipe.cooking_method)
        
        # Divide by servings
        per_serving = {
            k: v / recipe.servings
            for k, v in total_nutrients.items()
        }
        
        return NutritionResult(
            total=total_nutrients,
            per_serving=per_serving,
            allergens=self.detect_allergens(recipe),
        )
```

### Dietary Assessment Pattern

```python
class DietaryAssessmentEngine:
    def __init__(self, reference_db, calculator):
        self.reference_db = reference_db
        self.calculator = calculator
    
    async def assess_intake(self, intake_data: List[FoodIntake], profile: UserProfile) -> AssessmentResult:
        # Calculate total intake
        total_intake = await self.calculator.calculate_total_intake(intake_data)
        
        # Get reference values
        reference_values = await self.reference_db.get_references(
            age=profile.age,
            sex=profile.sex,
            activity_level=profile.activity_level,
            pregnancy_status=profile.pregnancy_status,
        )
        
        # Compare intake to references
        nutrient_comparison = {}
        for nutrient, intake in total_intake.items():
            if nutrient in reference_values:
                ref = reference_values[nutrient]
                percent_dri = (intake / ref.rda) * 100 if ref.rda else None
                
                nutrient_comparison[nutrient] = NutrientComparison(
                    nutrient=nutrient,
                    intake=intake,
                    unit=ref.unit,
                    rda=ref.rda,
                    ai=ref.ai,
                    ul=ref.ul,
                    percent_dri=percent_dri,
                    status=self.determine_status(intake, ref),
                )
        
        # Identify gaps and excesses
        deficient = [n for n, c in nutrient_comparison.items() if c.status == "deficient"]
        excessive = [n for n, c in nutrient_comparison.items() if c.status == "excessive"]
        
        return AssessmentResult(
            nutrient_comparison=nutrient_comparison,
            deficient_nutrients=deficient,
            excessive_nutrients=excessive,
            overall_score=self.calculate_overall_score(nutrient_comparison),
        )
```

### Meal Planning Algorithm

```python
class MealPlanningAlgorithm:
    def __init__(self, food_db, nutritional_targets):
        self.food_db = food_db
        self.targets = nutritional_targets
    
    async def generate_meal_plan(self, constraints: PlanConstraints) -> MealPlan:
        # Get candidate foods
        candidates = await self.get_candidate_foods(constraints)
        
        # Optimize for nutritional targets
        optimization_result = self.optimize_meals(candidates, self.targets)
        
        # Generate daily plans
        days = []
        for day_plan in optimization_result.daily_plans:
            day = DayPlan(
                day_number=len(days) + 1,
                meals=self.create_meals(day_plan),
                total_nutrition=self.calculate_day_nutrition(day_plan),
                estimated_cost=self.calculate_cost(day_plan),
            )
            days.append(day)
        
        return MealPlan(
            days=days,
            total_calories=sum(d.total_nutrition.calories for d in days),
            average_cost=sum(d.estimated_cost for d in days) / len(days),
            nutritional_coverage=self.calculate_coverage(optimization_result),
        )
```

### Glycemic Index Calculator

```python
class GlycemicIndexCalculator:
    def __init__(self, gi_database):
        self.gi_db = gi_database
    
    async def calculate_glycemic_load(self, food: Food, amount_g: float) -> GlycemicLoad:
        # Get GI value
        gi_value = await self.gi_db.get_gi(food.name)
        
        # Get carbohydrate content
        carbs_per_100g = food.nutrients.get("carbohydrates_g", 0)
        carbs_in_amount = (carbs_per_100g / 100) * amount_g
        
        # Calculate GL
        gl = (gi_value * carbs_in_amount) / 100
        
        # Classify
        if gl <= 10:
            classification = "low"
        elif gl <= 19:
            classification = "medium"
        else:
            classification = "high"
        
        return GlycemicLoad(
            gi_value=gi_value,
            carbohydrate_g=carbs_in_amount,
            glycemic_load=gl,
            classification=classification,
        )
```

## Integration Guide

### USDA FoodData Central Integration

```python
import httpx

class USDAIntegration:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.nal.usda.gov/fdc/v1"
    
    async def search_food(self, query: str, page_size: int = 10) -> List[FoodSearchResult]:
        params = {
            "api_key": self.api_key,
            "query": query,
            "pageSize": page_size,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/foods/search", params=params)
        
        return self.parse_search_results(response.json())
    
    async def get_food_details(self, fdc_id: int) -> FoodDetails:
        params = {"api_key": self.api_key}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/food/{fdc_id}", params=params)
        
        return self.parse_food_details(response.json())
```

### Nutritionix Integration

```python
class NutritionixIntegration:
    def __init__(self, app_id: str, app_key: str):
        self.app_id = app_id
        self.app_key = app_key
        self.base_url = "https://trackapi.nutritionix.com/v2"
    
    async def analyze_natural_language(self, query: str) -> NutritionAnalysis:
        headers = {
            "x-app-id": self.app_id,
            "x-app-key": self.app_key,
        }
        
        payload = {"query": query}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/natural/nutrients",
                headers=headers,
                json=payload,
            )
        
        return self.parse_analysis(response.json())
```

### Recipe Management Integration

```python
class RecipeManagementIntegration:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
    
    async def sync_recipes(self, recipes: List[Recipe]) -> SyncResult:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        results = []
        for recipe in recipes:
            # Calculate nutrition
            nutrition = await self.calculate_nutrition(recipe)
            
            # Update recipe with nutrition data
            recipe.nutrition = nutrition
            
            # Sync to external system
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/recipes",
                    headers=headers,
                    json=recipe.to_dict(),
                )
            
            results.append(response.json())
        
        return SyncResult(
            synced=len(results),
            errors=[r for r in results if 'error' in r],
        )
```

## Performance Optimization

### Database Optimization

```sql
-- Create indexes for common queries
CREATE INDEX idx_foods_name ON foods (name);
CREATE INDEX idx_foods_category ON foods (category);
CREATE INDEX idx_nutrients_food_id ON nutrients (food_id);

-- Full-text search index
CREATE INDEX idx_foods_name_search ON foods USING gin(to_tsvector('english', name));

-- Create materialized view for common queries
CREATE MATERIALIZED VIEW food_nutrition_summary AS
SELECT 
    f.id,
    f.name,
    f.category,
    n.calories,
    n.protein_g,
    n.carbohydrates_g,
    n.fat_g,
    n.fiber_g
FROM foods f
JOIN nutrients n ON f.id = n.food_id;
```

### Caching Strategy

```python
class NutritionCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 86400  # 24 hours
    
    async def get_food_nutrition(self, food_name: str) -> Optional[FoodNutrition]:
        cache_key = f"food:{food_name.lower()}"
        cached = await self.redis.get(cache_key)
        if cached:
            return FoodNutrition.from_json(cached)
        return None
    
    async def cache_food_nutrition(self, food_name: str, nutrition: FoodNutrition):
        cache_key = f"food:{food_name.lower()}"
        await self.redis.setex(
            cache_key,
            self.default_ttl,
            nutrition.to_json()
        )
```

### Batch Processing

```python
class NutritionBatchProcessor:
    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size
    
    async def analyze_batch(self, foods: List[Food]) -> List[NutritionResult]:
        batches = [
            foods[i:i+self.batch_size]
            for i in range(0, len(foods), self.batch_size)
        ]
        
        results = []
        for batch in batches:
            batch_results = await asyncio.gather(*[
                self.analyze_food(food) for food in batch
            ])
            results.extend(batch_results)
        
        return results
```

## Security Considerations

### Data Encryption

```python
from cryptography.fernet import Fernet

class NutritionDataEncryption:
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive nutrition data"""
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted: str) -> str:
        """Decrypt sensitive nutrition data"""
        return self.fernet.decrypt(encrypted.encode()).decode()
```

### Access Control

```python
class NutritionAccessControl:
    def __init__(self):
        self.permissions = {}
        self.roles = {}
    
    def check_permission(self, user_id: str, action: str) -> bool:
        user_roles = self.roles.get(user_id, [])
        for role in user_roles:
            role_permissions = self.permissions.get(role, [])
            if action in role_permissions:
                return True
        return False
    
    def grant_role(self, user_id: str, role: str):
        if user_id not in self.roles:
            self.roles[user_id] = []
        self.roles[user_id].append(role)
```

### Audit Logging

```python
class NutritionAuditLogger:
    def __init__(self, db):
        self.db = db
    
    async def log_event(self, event: AuditEvent):
        audit_entry = {
            'event_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow(),
            'actor_id': event.actor_id,
            'action': event.action,
            'resource_id': event.resource_id,
            'details': event.details,
            'ip_address': event.ip_address,
            'user_agent': event.user_agent,
        }
        
        await self.db.audit_logs.insert(audit_entry)
```

## Troubleshooting Guide

### Common Issues

**Issue: Nutrient data inconsistency**
```python
async def diagnose_nutrient_inconsistency(food_name: str):
    # Get data from multiple sources
    usda_data = await usda_api.get_food(food_name)
    nutritionix_data = await nutritionix_api.get_food(food_name)
    
    print(f"Food: {food_name}")
    print(f"  USDA calories: {usda_data.calories}")
    print(f"  Nutritionix calories: {nutritionix_data.calories}")
    
    if abs(usda_data.calories - nutritionix_data.calories) > 10:
        print(f"  WARNING: Calorie discrepancy > 10 kcal")
        print(f"  Difference: {abs(usda_data.calories - nutritionix_data.calories):.1f} kcal")
```

**Issue: Allergen detection false negatives**
```python
async def audit_allergen_detection():
    # Get test recipes with known allergens
    test_recipes = await get_test_recipes()
    
    false_negatives = []
    for recipe in test_recipes:
        detected = await allergen_detector.detect(recipe)
        expected = recipe.known_allergens
        
        missed = expected - set(detected)
        if missed:
            false_negatives.append({
                'recipe': recipe.name,
                'missed_allergens': missed,
            })
    
    print(f"False negatives: {len(false_negatives)}/{len(test_recipes)}")
    for fn in false_negatives:
        print(f"  {fn['recipe']}: missed {fn['missed_allergens']}")
```

**Issue: Label calculation errors**
```python
async def validate_nutrition_label(product: Product):
    # Get calculated values
    calculated = await nutrition_calculator.calculate(product)
    
    # Get lab results
    lab_results = await get_lab_results(product.id)
    
    print(f"Product: {product.name}")
    for nutrient in ['calories', 'protein_g', 'fat_g', 'carbohydrates_g']:
        calc_val = calculated[nutrient]
        lab_val = lab_results[nutrient]
        
        difference = abs(calc_val - lab_val)
        percent_diff = (difference / lab_val) * 100 if lab_val else 0
        
        print(f"  {nutrient}: calculated={calc_val:.1f}, lab={lab_val:.1f}, diff={percent_diff:.1f}%")
        
        if percent_diff > 20:
            print(f"    WARNING: Large discrepancy detected")
```

## API Reference

### Nutrition Analysis API

```python
# Analyze recipe
POST /api/v1/nutrition/analyze-recipe
Request:
{
    "name": "Grilled Salmon with Quinoa",
    "ingredients": [
        {"food": "Atlantic salmon", "amount_g": 200},
        {"food": "Quinoa, cooked", "amount_g": 150}
    ],
    "servings": 2
}

Response:
{
    "recipe_id": "RECIPE-001",
    "per_serving": {
        "calories": 450,
        "protein_g": 35,
        "carbohydrates_g": 30,
        "fat_g": 20,
        "fiber_g": 5
    },
    "allergens": ["fish"],
    "warnings": []
}
```

### Dietary Assessment API

```python
# Assess dietary intake
POST /api/v1/nutrition/assess-intake
Request:
{
    "user_profile": {
        "age": 35,
        "sex": "female",
        "activity_level": "moderate"
    },
    "intake_data": [
        {"food": "Oatmeal", "amount_g": 200, "meal": "breakfast"},
        {"food": "Apple", "amount_g": 150, "meal": "snack"}
    ]
}

Response:
{
    "assessment_id": "ASSESS-001",
    "nutrient_summary": {
        "calories": {"intake": 1800, "rda": 2000, "percent": 90},
        "protein_g": {"intake": 80, "rda": 65, "percent": 123},
        "iron_mg": {"intake": 12, "rda": 18, "percent": 67}
    },
    "deficient_nutrients": ["iron_mg", "vitamin_d_mcg"],
    "excess_nutrients": []
}
```

### Meal Planning API

```python
# Generate meal plan
POST /api/v1/nutrition/meal-plan
Request:
{
    "calorie_target": 2000,
    "protein_target_g": 100,
    "dietary_preferences": ["high_protein"],
    "allergies": ["peanuts", "shellfish"],
    "budget_per_day": 15.00,
    "days": 7
}

Response:
{
    "plan_id": "PLAN-001",
    "days": [
        {
            "day_number": 1,
            "meals": [
                {"name": "Breakfast", "calories": 400, "protein_g": 30},
                {"name": "Lunch", "calories": 600, "protein_g": 40},
                {"name": "Dinner", "calories": 800, "protein_g": 50}
            ],
            "total_calories": 1800,
            "estimated_cost": 12.50
        }
    ],
    "average_cost": 13.00,
    "nutritional_coverage": 0.95
}
```

## Data Models

### Food Nutrition Model

```python
class FoodNutrition:
    food_id: str
    name: str
    category: str
    serving_size_g: float
    nutrients: Dict[str, float]
    allergens: List[str]
    glycemic_index: Optional[float]
    novas_group: Optional[int]
    nutri_score: Optional[str]
    data_source: str
    last_updated: datetime
```

### Recipe Model

```python
class Recipe:
    recipe_id: str
    name: str
    ingredients: List[RecipeIngredient]
    servings: int
    prep_time_minutes: int
    cook_time_minutes: int
    cooking_method: Optional[str]
    nutrition: Optional[NutritionResult]
    allergens: List[str]
    created_at: datetime
    updated_at: datetime
```

### Meal Plan Model

```python
class MealPlan:
    plan_id: str
    user_id: str
    days: List[DayPlan]
    total_calories: int
    average_cost: float
    nutritional_coverage: float
    dietary_preferences: List[str]
    allergies: List[str]
    created_at: datetime
    valid_until: datetime
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nutrition-analysis-service
  namespace: nutrition-production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: nutrition-analysis-service
  template:
    metadata:
      labels:
        app: nutrition-analysis-service
    spec:
      containers:
      - name: nutrition-analysis
        image: your-registry/nutrition-analysis-service:2.0.0
        ports:
        - containerPort: 8443
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8443
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8443
          initialDelaySeconds: 30
          periodSeconds: 10
```

### Database Migration

```bash
# Run migrations
alembic upgrade head

# Verify migration status
alembic current

# Rollback if needed
alembic downgrade -1
```

## Monitoring & Observability

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Analysis metrics
recipe_analysis_counter = Counter(
    'recipe_analysis_total',
    'Total recipe analyses',
    ['status']
)

recipe_analysis_duration = Histogram(
    'recipe_analysis_duration_seconds',
    'Recipe analysis duration',
    buckets=[0.1, 0.5, 1.0, 5.0, 10.0]
)

# Database metrics
food_database_queries_counter = Counter(
    'food_database_queries_total',
    'Total food database queries',
    ['source', 'status']
)

# Allergen detection metrics
allergen_detection_counter = Counter(
    'allergen_detection_total',
    'Total allergen detections',
    ['allergen', 'detected']
)
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Nutrition Analysis",
    "panels": [
      {
        "title": "Recipe Analysis Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(recipe_analysis_total[5m])",
            "legendFormat": "{{status}}"
          }
        ]
      },
      {
        "title": "Analysis Latency",
        "type": "heatmap",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(recipe_analysis_duration_seconds_bucket[5m]))",
            "legendFormat": "P95"
          }
        ]
      }
    ]
  }
}
```

### Alerting Rules

```yaml
groups:
- name: nutrition_alerts
  rules:
  - alert: HighAnalysisLatency
    expr: histogram_quantile(0.95, rate(recipe_analysis_duration_seconds_bucket[5m])) > 5
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Recipe analysis latency exceeds 5 seconds"
      
  - alert: FoodDatabaseQueryErrors
    expr: rate(food_database_queries_total{status="error"}[5m]) > 0.05
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Food database query error rate exceeds 5%"
```

## Testing Strategy

### Unit Tests

```python
import pytest
from decimal import Decimal

class TestNutritionAnalysis:
    def test_calculate_recipe_nutrition(self, nutrition_analyzer):
        recipe = Recipe(
            name="Test Recipe",
            ingredients=[
                {"food": "Chicken breast", "amount_g": 200},
                {"food": "Brown rice", "amount_g": 150},
            ],
            servings=2,
        )
        
        result = nutrition_analyzer.analyze_recipe(recipe)
        
        assert result.per_serving.calories > 0
        assert result.per_serving.protein_g > 0
        assert len(result.allergens) == 0
    
    def test_detect_allergens(self, nutrition_analyzer):
        recipe = Recipe(
            name="Peanut Butter Sandwich",
            ingredients=[
                {"food": "Peanut butter", "amount_g": 30},
                {"food": "Bread", "amount_g": 50},
            ],
            servings=1,
        )
        
        result = nutrition_analyzer.analyze_recipe(recipe)
        
        assert "peanuts" in result.allergens
        assert "wheat" in result.allergens
```

### Integration Tests

```python
class TestEndToEndNutrition:
    async def test_meal_planning_flow(self, meal_planner):
        plan = await meal_planner.generate_meal_plan(
            calorie_target=2000,
            protein_target_g=100,
            dietary_preferences=["high_protein"],
            allergies=["peanuts"],
            days=7,
        )
        
        assert len(plan.days) == 7
        assert plan.total_calories > 0
        assert plan.average_cost > 0
        
        # Verify nutritional coverage
        assert plan.nutritional_coverage > 0.8
```

### Load Testing

```python
import asyncio
from locust import HttpUser, task, between

class NutritionUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    @task(10)
    def analyze_recipe(self):
        self.client.post("/api/v1/nutrition/analyze-recipe", json={
            "name": "Test Recipe",
            "ingredients": [
                {"food": "Chicken breast", "amount_g": 200},
                {"food": "Brown rice", "amount_g": 150},
            ],
            "servings": 2,
        })
    
    @task(5)
    def search_food(self):
        self.client.get("/api/v1/nutrition/foods/search", params={
            "query": "chicken breast",
        })
```

## Versioning & Migration

### API Versioning

```python
# Version header support
@app.route("/api/v1/nutrition/analyze-recipe", methods=["POST"])
@app.route("/api/v2/nutrition/analyze-recipe", methods=["POST"])
async def analyze_recipe():
    version = request.headers.get("API-Version", "v1")
    
    if version == "v2":
        return await analyze_recipe_v2()
    return await analyze_recipe_v1()
```

### Database Migration Strategy

```bash
# Forward migration
alembic upgrade head

# Specific version
alembic upgrade ae1027a6555

# Downgrade
alembic downgrade -1
```

## Glossary

- **AI**: Adequate Intake - recommended average daily intake level
- **DRI**: Dietary Reference Intake - reference values for nutrient intake
- **FDAs**: Food and Drug Administration - US regulatory agency
- **GI**: Glycemic Index - measure of how quickly food raises blood sugar
- **GL**: Glycemic Load - GI adjusted for carbohydrate content
- **NOVA**: Food classification system by degree of processing
- **Nutri-Score**: Front-of-pack nutrition label (A-E rating)
- **RDA**: Recommended Dietary Allowance - average daily intake level
- **UL**: Tolerable Upper Intake Level - maximum daily intake unlikely to cause harm
- **USDA**: United States Department of Agriculture

## Changelog

### Version 2.0.0 (2026-07-01)
- Added EU nutrition labeling support
- Implemented glycemic index/load calculation
- Enhanced allergen detection with cross-contact risk
- Added NOVA and Nutri-Score classification

### Version 1.5.0 (2026-01-15)
- Added meal planning algorithm
- Implemented dietary assessment
- Enhanced recipe analysis with cooking losses

### Version 1.0.0 (2025-06-01)
- Initial release
- Basic nutrition analysis
- Recipe calculation

## Contributing Guidelines

### Code Style

```python
# Follow PEP 8 with Black formatter
# Line length: 88 characters
# Use type hints
# Docstrings: Google style

def analyze_recipe(
    recipe: Recipe,
    serving_size: int,
) -> NutritionResult:
    """Analyze recipe for nutritional content.
    
    Args:
        recipe: Recipe to analyze.
        serving_size: Number of servings.
    
    Returns:
        Nutrition analysis result.
    
    Raises:
        AnalysisError: If analysis fails.
    """
    pass
```

### Pull Request Process

1. Create feature branch from `main`
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation if needed
5. Request review from team lead
6. Address review comments
7. Merge after approval

## License

MIT License

Copyright (c) 2026 Nutrition Analysis Platform

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
