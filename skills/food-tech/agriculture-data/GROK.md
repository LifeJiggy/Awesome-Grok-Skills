---
name: "agriculture-data"
category: "food-tech"
version: "2.0.0"
tags: ["food-tech", "agriculture", "precision-farming", "crop-analytics", "farm-management"]
difficulty: "intermediate"
estimated_time: "40-55 minutes"
prerequisites: ["python", "agriculture-basics"]
---

# Agriculture Data Analytics

## Overview

Agriculture data analytics provides precision farming tools for optimizing crop production, monitoring soil health, managing irrigation, predicting yields, and tracking sustainability metrics from farm to fork. This module covers satellite imagery analysis, IoT sensor data processing, weather-based crop modeling, equipment telematics, and farm management information systems (FMIS) for data-driven agricultural decision-making.

## Core Capabilities

- **Crop Monitoring**: Satellite and drone imagery analysis for crop health assessment using NDVI, EVI, and other vegetation indices
- **Soil Analytics**: Soil composition analysis, moisture monitoring, pH tracking, and nutrient management recommendations
- **Weather Integration**: Hyperlocal weather data, frost alerts, growing degree day (GDD) calculation, and precipitation forecasting
- **Yield Prediction**: ML-based yield forecasting using historical data, satellite imagery, weather, and soil conditions
- **Irrigation Management**: Smart irrigation scheduling based on soil moisture, evapotranspiration, and weather forecasts
- **Equipment Telematics**: Farm equipment GPS tracking, utilization monitoring, and predictive maintenance alerts
- **Sustainability Metrics**: Carbon sequestration measurement, water usage tracking, and regenerative agriculture scoring
- **Supply Chain Integration**: Farm-gate data sharing with downstream supply chain partners for traceability
- **Financial Analytics**: Farm profitability analysis, input cost tracking, and commodity price hedging tools
- **Pest & Disease Detection**: Computer vision-based crop disease identification and treatment recommendations

## Usage Examples

### Crop Health Monitoring

```python
from food_tech.agriculture_data import CropMonitor, VegetationIndex

monitor = CropMonitor(
    data_sources=["sentinel_2", "drone_ndvi"],
    update_frequency_days=5,
)

# Analyze field health
analysis = monitor.analyze_field(
    field_id="FIELD-NORTH-40",
    geometry={"type": "Polygon", "coordinates": [[[-89.5, 43.1], [-89.4, 43.1], [-89.4, 43.0], [-89.5, 43.0]]]},
    crop_type="corn",
)

print(f"Field: {analysis.field_id}")
print(f"NDVI Average: {analysis.ndvi_mean:.3f}")
print(f"Health Status: {analysis.health_status}")
print(f"Stress Areas: {analysis.stress_percentage:.1%}")
print(f"Recommended Action: {analysis.recommended_action}")
```

### Yield Prediction

```python
from food_tech.agriculture_data import YieldPredictor

predictor = YieldPredictor(
    model="random_forest",
    crop_types=["corn", "soybeans", "wheat"],
)

# Predict yield
prediction = predictor.predict(
    field_id="FIELD-NORTH-40",
    crop_type="corn",
    planting_date="2026-04-15",
    historical_yields=[180, 195, 175, 200, 185],  # bu/acre last 5 years
    soil_data={"organic_matter": 3.5, "ph": 6.5, "nitrogen_ppm": 45},
    weather_season="normal",
)

print(f"Predicted Yield: {prediction.yield_bu_per_acre:.0f} bu/acre")
print(f"Confidence: {prediction.confidence:.1%}")
print(f"Range: {prediction.ci_lower:.0f} - {prediction.ci_upper:.0f} bu/acre")
print(f"Revenue Estimate: ${prediction.estimated_revenue_per_acre:.2f}/acre")
```

### Soil Management

```python
from food_tech.agriculture_data import SoilAnalyzer

analyzer = SoilAnalyzer(
    sampling_grid="2.5 acre",
    lab_analysis="comprehensive",
)

# Analyze soil samples
soil = analyzer.analyze(
    field_id="FIELD-NORTH-40",
    samples=[
        {"lat": 43.05, "lon": -89.45, "depth_cm": 30, "ph": 6.5, "organic_matter_pct": 3.5,
         "nitrogen_ppm": 45, "phosphorus_ppm": 32, "potassium_ppm": 180},
        {"lat": 43.05, "lon": -89.44, "depth_cm": 30, "ph": 6.2, "organic_matter_pct": 2.8,
         "nitrogen_ppm": 35, "phosphorus_ppm": 28, "potassium_ppm": 150},
    ],
)

print(f"Average pH: {soil.avg_ph:.1f}")
print(f"Organic Matter: {soil.avg_organic_matter:.1f}%")
print(f"N-P-K Status: {soil.npk_status}")
for rec in soil.recommendations:
    print(f"  -> {rec}")
```

### Smart Irrigation

```python
from food_tech.agriculture_data import IrrigationManager

irrigation = IrrigationManager(
    field_id="FIELD-NORTH-40",
    system_type="center_pivot",
    flow_rate_gpm=800,
)

# Get irrigation recommendation
recommendation = irrigation.get_recommendation(
    soil_moisture_pct=35,
    crop_stage="tasseling",
    forecast_rain_mm=15,
    forecast_days=3,
    et_crop_mm=6.5,
)

print(f"Irrigation Needed: {recommendation.required}")
print(f"Amount: {recommendation.amount_mm:.1f} mm")
print(f"Duration: {recommendation.duration_hours:.1f} hours")
print(f"Timing: {recommendation.timing}")
print(f"Water Savings vs Schedule: {recommendation.savings_pct:.0%}")
```

## Best Practices

- Use satellite imagery at 5-day intervals during growing season for timely crop health assessment
- Calibrate soil sensors with lab-analyzed soil samples at least annually for accurate readings
- Integrate weather forecasts (not just historical data) for irrigation and spray timing decisions
- Track yield data at field level for at least 5 years to build reliable prediction models
- Use variable rate technology (VRT) for fertilizer and seed application based on soil zone maps
- Monitor growing degree days (GDD) for crop staging and harvest timing optimization
- Document all field operations (planting, spraying, harvesting) with GPS coordinates and timestamps
- Implement buffer zones near waterways and use integrated pest management (IPM) to reduce chemical use
- Share farm-gate data with supply chain partners to enable full traceability and premium pricing
- Maintain data ownership; use platforms that allow data export and don't lock you into single vendors

## Related Modules

- `food-tech/supply-chain` - Farm-to-fork supply chain traceability
- `food-tech/food-safety` - Agricultural product safety and compliance
- `food-tech/nutrition-analysis` - Crop nutritional quality tracking

## Advanced Configuration

### Satellite Imagery Configuration

```yaml
satellite_imagery:
  sources:
    sentinel_2:
      enabled: true
      api_key: "${SENTINEL_API_KEY}"
      resolution_meters: 10
      revisit_days: 5
      bands:
        - "B02"  # Blue
        - "B03"  # Green
        - "B04"  # Red
        - "B08"  # Near Infrared
        - "B11"  # SWIR
        - "B12"  # SWIR
        
    landsat_8:
      enabled: true
      api_key: "${LANDSAT_API_KEY}"
      resolution_meters: 30
      revisit_days: 16
      bands:
        - "B2"   # Blue
        - "B3"   # Green
        - "B4"   # Red
        - "B5"   # NIR
        - "B6"   # SWIR1
        - "B7"   # SWIR2
        
    drone_imagery:
      enabled: true
      resolution_cm: 5
      flight_altitude_m: 100
      overlap_pct: 80
      
  processing:
    atmospheric_correction: true
    cloud_masking: true
    cloud_threshold_pct: 20
    mosaic_method: "median"
    
  indices:
    ndvi:
      formula: "(NIR - Red) / (NIR + Red)"
      description: "Normalized Difference Vegetation Index"
      healthy_range: [0.3, 0.8]
      
    evi:
      formula: "2.5 * (NIR - Red) / (NIR + 6*Red - 7.5*Blue + 1)"
      description: "Enhanced Vegetation Index"
      healthy_range: [0.2, 0.7]
      
    ndwi:
      formula: "(Green - NIR) / (Green + NIR)"
      description: "Normalized Difference Water Index"
      water_threshold: 0.3
```

### Soil Sensor Configuration

```yaml
soil_sensors:
  types:
    moisture:
      sensor_type: "capacitance"
      depth_levels: [10, 30, 60, 90]  # cm
      accuracy_pct: 2
      calibration_frequency_days: 30
      
    temperature:
      sensor_type: "thermocouple"
      depth_levels: [5, 15, 30, 60]  # cm
      accuracy_celsius: 0.5
      
    ph:
      sensor_type: "ion_selective_electrode"
      depth_levels: [15, 30]  # cm
      accuracy_ph: 0.2
      calibration_frequency_days: 90
      
    ec:
      sensor_type: "conductivity"
      description: "Electrical Conductivity"
      depth_levels: [15, 30]  # cm
      accuracy_pct: 3
      
  data_collection:
    interval_minutes: 15
    storage_resolution: "hourly_average"
    transmission_protocol: "lorawan"
    
  alerts:
    low_moisture_threshold_pct: 25
    high_moisture_threshold_pct: 80
    frost_threshold_celsius: 2
```

### Weather Integration Configuration

```yaml
weather_integration:
  data_sources:
    primary:
      provider: "openweathermap"
      api_key: "${WEATHER_API_KEY}"
      update_frequency_minutes: 30
      forecast_days: 7
      
    secondary:
      provider: "weather_gov"
      api_key: "${WEATHER_GOV_API_KEY}"
      update_frequency_minutes: 60
      forecast_days: 14
      
  hyperlocal:
    enabled: true
    station_spacing_km: 5
    interpolation_method: "inverse_distance_weighting"
    
  alerts:
    frost:
      enabled: true
      threshold_celsius: 2
      advance_warning_hours: 24
      
    heat_stress:
      enabled: true
      threshold_index: 30  # Heat Index
      advance_warning_hours: 12
      
    heavy_rain:
      enabled: true
      threshold_mm_per_hour: 25
      advance_warning_hours: 6
      
  growing_degree_days:
    base_temperature_celsius: 10
    crop_coefficients:
      corn: 10
      soybeans: 10
      wheat: 5
      cotton: 15
```

### Equipment Telematics Configuration

```yaml
equipment_telematics:
  tracking:
    enabled: true
    update_frequency_seconds: 30
    geofencing_enabled: true
    
  sensors:
    engine:
      rpm: true
      temperature: true
      oil_pressure: true
      fuel_level: true
      
    hydraulic:
      pressure: true
      temperature: true
      flow_rate: true
      
    gps:
      latitude: true
      longitude: true
      speed: true
      heading: true
      
  maintenance:
    predictive_enabled: true
    alert_threshold_hours: 50
    components:
      - name: "engine_oil"
        interval_hours: 250
        alert_before_hours: 50
        
      - name: "hydraulic_filter"
        interval_hours: 500
        alert_before_hours: 100
        
      - name: "air_filter"
        interval_hours: 300
        alert_before_hours: 50
        
  utilization:
    idle_threshold_minutes: 5
    field_work_categories:
      - "planting"
      - "spraying"
      - "harvesting"
      - "tillage"
```

## Architecture Patterns

### Satellite Image Processing Pipeline

```python
class SatelliteImageProcessor:
    def __init__(self, data_store, index_calculator):
        self.data_store = data_store
        self.index_calc = index_calculator
    
    async def process_image(self, image: SatelliteImage) -> ProcessedImage:
        # Apply atmospheric correction
        corrected = await self.atmospheric_correction(image)
        
        # Apply cloud masking
        masked = await self.cloud_masking(corrected)
        
        # Calculate vegetation indices
        indices = await self.calculate_indices(masked)
        
        # Store results
        await self.data_store.store(masked, indices)
        
        return ProcessedImage(
            image_id=masked.id,
            indices=indices,
            metadata=masked.metadata,
        )
```

### Crop Health Assessment Engine

```python
class CropHealthEngine:
    def __init__(self, index_database, historical_data):
        self.index_db = index_database
        self.historical = historical_data
    
    async def assess_health(self, field_id: str, date: date) -> HealthAssessment:
        # Get current indices
        current = await self.index_db.get_indices(field_id, date)
        
        # Get historical baseline
        baseline = await self.historical.get_baseline(field_id, date)
        
        # Calculate anomalies
        anomalies = self.calculate_anomalies(current, baseline)
        
        # Identify stress areas
        stress_areas = self.identify_stress(current, baseline)
        
        # Generate recommendations
        recommendations = self.generate_recommendations(anomalies, stress_areas)
        
        return HealthAssessment(
            field_id=field_id,
            date=date,
            ndvi_mean=current.ndvi_mean,
            ndvi_anomaly=anomalies.ndvi,
            stress_areas=stress_areas,
            health_status=self.determine_status(anomalies),
            recommendations=recommendations,
        )
```

### Yield Prediction Model

```python
class YieldPredictionModel:
    def __init__(self, feature_store, trained_models):
        self.features = feature_store
        self.models = trained_models
    
    async def predict_yield(self, field_id: str, crop_type: str) -> YieldPrediction:
        # Get features
        features = await self.features.get_features(field_id, crop_type)
        
        # Get appropriate model
        model = await self.models.get_model(crop_type)
        
        # Generate prediction
        prediction = await model.predict(features)
        
        # Calculate confidence interval
        ci = self.calculate_confidence_interval(prediction, model.uncertainty)
        
        # Calculate revenue estimate
        revenue = await self.estimate_revenue(
            prediction.yield,
            field_id,
            crop_type,
        )
        
        return YieldPrediction(
            field_id=field_id,
            crop_type=crop_type,
            yield_bu_per_acre=prediction.yield,
            confidence=prediction.confidence,
            ci_lower=ci.lower,
            ci_upper=ci.upper,
            estimated_revenue_per_acre=revenue,
            factors=prediction.feature_importance,
        )
```

### Smart Irrigation Controller

```python
class SmartIrrigationController:
    def __init__(self, soil_sensors, weather_forecast, crop_model):
        self.soil = soil_sensors
        self.weather = weather_forecast
        self.crop = crop_model
    
    async def get_recommendation(self, field_id: str) -> IrrigationRecommendation:
        # Get soil moisture
        moisture = await self.soil.get_moisture(field_id)
        
        # Get weather forecast
        forecast = await self.weather.get_forecast(field_id, days=3)
        
        # Get crop water requirements
        crop_requirements = await self.crop.get_water_requirements(field_id)
        
        # Calculate irrigation need
        irrigation_need = self.calculate_need(
            moisture,
            forecast,
            crop_requirements,
        )
        
        # Generate recommendation
        if irrigation_need.required:
            recommendation = IrrigationRecommendation(
                required=True,
                amount_mm=irrigation_need.amount,
                duration_hours=self.calculate_duration(irrigation_need.amount),
                timing=irrigation_need.optimal_timing,
                savings_pct=self.calculate_savings(irrigation_need),
            )
        else:
            recommendation = IrrigationRecommendation(
                required=False,
                reason="Soil moisture adequate",
                next_check_hours=24,
            )
        
        return recommendation
```

## Integration Guide

### Sentinel Hub Integration

```python
import httpx

class SentinelHubIntegration:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://services.sentinel-hub.com"
    
    async def get_image(self, bbox: BBox, date: date, bands: List[str]) -> SatelliteImage:
        # Get access token
        token = await self.get_access_token()
        
        # Request image
        headers = {"Authorization": f"Bearer {token}"}
        
        payload = {
            "input": {
                "bounds": bbox.to_dict(),
                "data": [{
                    "type": "sentinel-2-l2a",
                    "dataFilter": {
                        "timeRange": {
                            "from": date.isoformat(),
                            "to": date.isoformat()
                        }
                    }
                }]
            },
            "output": {
                "width": 512,
                "height": 512,
                "responses": [{
                    "identifier": "default",
                    "format": {"type": "image/tiff"}
                }]
            },
            "processing": {
                "bands": bands
            }
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/process",
                headers=headers,
                json=payload,
            )
        
        return self.parse_image(response.content)
```

### IoT Sensor Platform Integration

```python
class IoTSensorPlatformIntegration:
    def __init__(self, platform_url: str, api_key: str):
        self.platform_url = platform_url
        self.api_key = api_key
    
    async def get_sensor_data(self, sensor_id: str, hours: int = 24) -> List[SensorReading]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
        params = {
            "sensor_id": sensor_id,
            "hours": hours,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.platform_url}/sensors/data",
                headers=headers,
                params=params,
            )
        
        return self.parse_readings(response.json())
    
    async def send_command(self, sensor_id: str, command: str) -> CommandResult:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
        payload = {
            "sensor_id": sensor_id,
            "command": command,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.platform_url}/sensors/command",
                headers=headers,
                json=payload,
            )
        
        return self.parse_command_result(response.json())
```

### Farm Management System Integration

```python
class FMSIntegration:
    def __init__(self, fms_url: str, api_key: str):
        self.fms_url = fms_url
        self.api_key = api_key
    
    async def sync_field_data(self, field_id: str) -> SyncResult:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
        # Get field data from FMS
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.fms_url}/fields/{field_id}",
                headers=headers,
            )
        
        field_data = self.parse_field_data(response.json())
        
        # Sync to agriculture data system
        await self.sync_to_system(field_data)
        
        return SyncResult(
            field_id=field_id,
            status="synced",
            records_synced=len(field_data.operations),
        )
```

## Performance Optimization

### Database Optimization

```sql
-- Create indexes for common queries
CREATE INDEX idx_satellite_images_field_date ON satellite_images (field_id, capture_date DESC);
CREATE INDEX idx_soil_readings_sensor_date ON soil_readings (sensor_id, recorded_at DESC);
CREATE INDEX idx_yield_predictions_field ON yield_predictions (field_id, crop_type, prediction_date);

-- Create materialized view for field summaries
CREATE MATERIALIZED VIEW field_health_summary AS
SELECT 
    field_id,
    DATE(capture_date) as capture_date,
    AVG(ndvi) as avg_ndvi,
    MIN(ndvi) as min_ndvi,
    MAX(ndvi) as max_ndvi,
    STDDEV(ndvi) as std_ndvi
FROM satellite_indices
GROUP BY field_id, DATE(capture_date);
```

### Caching Strategy

```python
class AgricultureCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 3600  # 1 hour
    
    async def get_field_health(self, field_id: str) -> Optional[HealthAssessment]:
        cache_key = f"field_health:{field_id}"
        cached = await self.redis.get(cache_key)
        if cached:
            return HealthAssessment.from_json(cached)
        return None
    
    async def cache_field_health(self, field_id: str, health: HealthAssessment):
        cache_key = f"field_health:{field_id}"
        await self.redis.setex(
            cache_key,
            self.default_ttl,
            health.to_json()
        )
```

### Batch Processing

```python
class AgricultureBatchProcessor:
    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size
    
    async def process_batch(self, items: List, processor: Callable):
        batches = [
            items[i:i+self.batch_size]
            for i in range(0, len(items), self.batch_size)
        ]
        
        results = []
        for batch in batches:
            batch_results = await asyncio.gather(*[
                processor(item) for item in batch
            ])
            results.extend(batch_results)
        
        return results
```

## Security Considerations

### Data Encryption

```python
from cryptography.fernet import Fernet

class AgricultureDataEncryption:
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive agriculture data"""
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted: str) -> str:
        """Decrypt sensitive agriculture data"""
        return self.fernet.decrypt(encrypted.encode()).decode()
```

### Access Control

```python
class AgricultureAccessControl:
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
class AgricultureAuditLogger:
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

**Issue: Satellite image quality issues**
```python
async def diagnose_satellite_quality(image_id: str):
    image = await get_satellite_image(image_id)
    
    print(f"Image {image_id}:")
    print(f"  Cloud cover: {image.cloud_cover_pct:.1f}%")
    print(f"  Quality score: {image.quality_score:.2f}")
    
    if image.cloud_cover_pct > 20:
        print(f"  WARNING: High cloud cover")
        print(f"  Recommendation: Request alternative image date")
    
    if image.quality_score < 0.7:
        print(f"  WARNING: Low quality score")
        print(f"  Recommendation: Check atmospheric conditions")
```

**Issue: Soil sensor data gaps**
```python
async def diagnose_sensor_gaps(sensor_id: str, date_range: Tuple[date, date]):
    readings = await get_sensor_readings(sensor_id, date_range)
    
    # Calculate expected readings
    expected_count = (date_range[1] - date_range[0]).days * 24 * 4  # 15-min intervals
    
    gap_pct = 1 - (len(readings) / expected_count)
    
    print(f"Sensor {sensor_id}:")
    print(f"  Expected readings: {expected_count}")
    print(f"  Actual readings: {len(readings)}")
    print(f"  Gap percentage: {gap_pct:.1%}")
    
    if gap_pct > 0.1:
        print(f"  WARNING: Significant data gaps")
        print(f"  Recommendation: Check sensor connectivity")
```

**Issue: Yield prediction accuracy**
```python
async def diagnose_yield_accuracy(model_name: str):
    predictions = await get_recent_predictions(model_name, days=30)
    actuals = await get_actual_yields()
    
    # Calculate accuracy metrics
    mape = calculate_mape(predictions, actuals)
    bias = calculate_bias(predictions, actuals)
    
    print(f"Model {model_name}:")
    print(f"  MAPE: {mape:.1f}%")
    print(f"  Bias: {bias:.1f}%")
    
    if mape > 20:
        print(f"  WARNING: High prediction error")
        print(f"  Recommendation: Retrain model with recent data")
```

## API Reference

### Crop Monitoring API

```python
# Analyze field health
POST /api/v1/crop/analyze
Request:
{
    "field_id": "FIELD-NORTH-40",
    "geometry": {"type": "Polygon", "coordinates": [...]},
    "crop_type": "corn",
    "date": "2026-07-01"
}

Response:
{
    "field_id": "FIELD-NORTH-40",
    "ndvi_mean": 0.65,
    "ndvi_anomaly": 0.05,
    "health_status": "good",
    "stress_areas": [
        {"location": {"lat": 43.05, "lon": -89.45}, "severity": "low"}
    ],
    "recommendations": ["Continue current management practices"]
}
```

### Yield Prediction API

```python
# Predict yield
POST /api/v1/yield/predict
Request:
{
    "field_id": "FIELD-NORTH-40",
    "crop_type": "corn",
    "planting_date": "2026-04-15",
    "historical_yields": [180, 195, 175, 200, 185]
}

Response:
{
    "field_id": "FIELD-NORTH-40",
    "yield_bu_per_acre": 192,
    "confidence": 0.85,
    "ci_lower": 175,
    "ci_upper": 210,
    "estimated_revenue_per_acre": 864.00,
    "factors": {
        "weather": 0.35,
        "soil": 0.30,
        "management": 0.35
    }
}
```

### Soil Management API

```python
# Analyze soil samples
POST /api/v1/soil/analyze
Request:
{
    "field_id": "FIELD-NORTH-40",
    "samples": [
        {"lat": 43.05, "lon": -89.45, "depth_cm": 30, "ph": 6.5, "organic_matter_pct": 3.5}
    ]
}

Response:
{
    "field_id": "FIELD-NORTH-40",
    "avg_ph": 6.4,
    "avg_organic_matter": 3.2,
    "npk_status": "adequate",
    "recommendations": [
        "Apply 50 lbs/acre nitrogen",
        "Consider lime application to raise pH"
    ]
}
```

## Data Models

### Satellite Image Model

```python
class SatelliteImage:
    image_id: str
    source: str  # sentinel_2, landsat_8, drone
    field_id: str
    capture_date: date
    bbox: BBox
    resolution_meters: float
    cloud_cover_pct: float
    bands: List[str]
    file_path: str
    metadata: Dict[str, Any]
    created_at: datetime
```

### Soil Sample Model

```python
class SoilSample:
    sample_id: str
    field_id: str
    location: Point
    depth_cm: float
    ph: float
    organic_matter_pct: float
    nitrogen_ppm: float
    phosphorus_ppm: float
    potassium_ppm: float
    moisture_pct: float
    ec_dsm: float  # Electrical Conductivity
    collected_at: datetime
    lab_analysis: Optional[LabAnalysis]
```

### Yield Prediction Model

```python
class YieldPrediction:
    prediction_id: str
    field_id: str
    crop_type: str
    yield_bu_per_acre: float
    confidence: float
    ci_lower: float
    ci_upper: float
    estimated_revenue_per_acre: float
    factors: Dict[str, float]
    model_version: str
    prediction_date: datetime
    created_at: datetime
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agriculture-data-service
  namespace: agriculture-production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: agriculture-data-service
  template:
    metadata:
      labels:
        app: agriculture-data-service
    spec:
      containers:
      - name: agriculture-data
        image: your-registry/agriculture-data-service:2.0.0
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

# Satellite imagery metrics
satellite_images_counter = Counter(
    'agriculture_satellite_images_total',
    'Total satellite images processed',
    ['source', 'status']
)

satellite_processing_duration = Histogram(
    'agriculture_satellite_processing_duration_seconds',
    'Satellite image processing duration',
    ['source'],
    buckets=[10, 30, 60, 120, 300]
)

# Soil sensor metrics
soil_readings_counter = Counter(
    'agriculture_soil_readings_total',
    'Total soil readings',
    ['sensor_id', 'parameter']
)

# Yield prediction metrics
yield_predictions_counter = Counter(
    'agriculture_yield_predictions_total',
    'Total yield predictions',
    ['crop_type', 'model']
)
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Agriculture Data Analytics",
    "panels": [
      {
        "title": "Satellite Image Processing",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(agriculture_satellite_images_total[5m])",
            "legendFormat": "{{source}} - {{status}}"
          }
        ]
      },
      {
        "title": "Soil Moisture Levels",
        "type": "gauge",
        "targets": [
          {
            "expr": "agriculture_soil_readings_total{parameter='moisture'}",
            "legendFormat": "{{sensor_id}}"
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
- name: agriculture_alerts
  rules:
  - alert: LowSoilMoisture
    expr: agriculture_soil_readings_total{parameter="moisture"} < 25
    for: 1h
    labels:
      severity: warning
    annotations:
      summary: "Soil moisture below threshold"
      
  - alert: SatelliteImageProcessingFailed
    expr: rate(agriculture_satellite_images_total{status="failed"}[5m]) > 0.1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Satellite image processing failure rate high"
```

## Testing Strategy

### Unit Tests

```python
import pytest
from decimal import Decimal

class TestCropMonitoring:
    def test_calculate_ndvi(self, crop_monitor):
        # Test NDVI calculation
        nir = 0.45
        red = 0.15
        
        ndvi = crop_monitor.calculate_ndvi(nir, red)
        
        assert abs(ndvi - 0.50) < 0.01  # (0.45-0.15)/(0.45+0.15) = 0.50
    
    def test_health_status(self, crop_monitor):
        # Test health status determination
        ndvi_anomaly = 0.05
        
        status = crop_monitor.determine_health_status(ndvi_anomaly)
        
        assert status == "good"
```

### Integration Tests

```python
class TestEndToEndAgriculture:
    async def test_yield_prediction_flow(self, agriculture_system):
        # Analyze field
        health = await agriculture_system.analyze_field(
            field_id="FIELD-NORTH-40",
            crop_type="corn",
        )
        
        assert health.ndvi_mean > 0
        assert health.health_status in ["poor", "fair", "good", "excellent"]
        
        # Predict yield
        prediction = await agriculture_system.predict_yield(
            field_id="FIELD-NORTH-40",
            crop_type="corn",
        )
        
        assert prediction.yield_bu_per_acre > 0
        assert prediction.confidence > 0.5
```

### Load Testing

```python
import asyncio
from locust import HttpUser, task, between

class AgricultureUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    @task(10)
    def analyze_field(self):
        self.client.post("/api/v1/crop/analyze", json={
            "field_id": f"FIELD-{self.field_counter}",
            "crop_type": "corn",
        })
        self.field_counter += 1
    
    @task(5)
    def predict_yield(self):
        self.client.post("/api/v1/yield/predict", json={
            "field_id": f"FIELD-{self.field_counter}",
            "crop_type": "corn",
        })
```

## Versioning & Migration

### API Versioning

```python
# Version header support
@app.route("/api/v1/crop/analyze", methods=["POST"])
@app.route("/api/v2/crop/analyze", methods=["POST"])
async def analyze_field():
    version = request.headers.get("API-Version", "v1")
    
    if version == "v2":
        return await analyze_field_v2()
    return await analyze_field_v1()
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

- **NDVI**: Normalized Difference Vegetation Index - measure of crop health
- **EVI**: Enhanced Vegetation Index - improved vegetation measurement
- **GDD**: Growing Degree Days - heat units for crop development
- **VRT**: Variable Rate Technology - precision application of inputs
- **IPM**: Integrated Pest Management - sustainable pest control
- **ET**: Evapotranspiration - water loss from soil and plants
- **FMIS**: Farm Management Information System - farm data platform
- **BBox**: Bounding Box - geographic area definition
- **LAI**: Leaf Area Index - measure of canopy cover

## Changelog

### Version 2.0.0 (2026-07-01)
- Added drone imagery processing
- Implemented predictive maintenance for equipment
- Enhanced sustainability metrics tracking
- Added pest and disease detection

### Version 1.5.0 (2026-01-15)
- Added soil sensor integration
- Implemented smart irrigation
- Enhanced weather integration

### Version 1.0.0 (2025-06-01)
- Initial release
- Basic satellite monitoring
- Yield prediction

## Contributing Guidelines

### Code Style

```python
# Follow PEP 8 with Black formatter
# Line length: 88 characters
# Use type hints
# Docstrings: Google style

def analyze_field(
    field_id: str,
    crop_type: str,
) -> HealthAssessment:
    """Analyze field crop health.
    
    Args:
        field_id: Field identifier.
        crop_type: Type of crop.
    
    Returns:
        Health assessment result.
    
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

Copyright (c) 2026 Agriculture Data Analytics Platform

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
