---
name: health-monitoring
category: health-tech
version: 1.0.0
tags:
  - wearables
  - vital-signs
  - anomaly-detection
  - chronic-disease
  - iot-health
  - continuous-monitoring
difficulty: intermediate
estimated_time: 90 minutes
prerequisites:
  - python-programming
  - statistics-basics
  - physiology-fundamentals
---

# Health Monitoring

Health monitoring encompasses the continuous or intermittent collection of physiological data from wearable devices, implantable sensors, and home health equipment. Data is analyzed for anomaly detection, trend analysis, and chronic disease management.

## Core Concepts

### Wearable Data
Consumer and medical-grade devices (smartwatches, fitness trackers, CGMs, smart rings) that capture continuous physiological signals — heart rate, HRV, SpO2, skin temperature, activity patterns, sleep architecture.

### Vital Signs Monitoring
Systematic tracking of core physiological parameters: heart rate, blood pressure, respiratory rate, temperature, oxygen saturation, and blood glucose. Each has age/sex-specific normal ranges and clinical alert thresholds.

### Anomaly Detection
Statistical and ML-based identification of deviations from baseline physiology. Approaches include Z-score thresholds, moving average control charts, LSTM autoencoders, and isolation forests. Critical for early detection of deterioration.

### Chronic Disease Management
Structured monitoring protocols for conditions like diabetes, heart failure, COPD, and hypertension. Combines device data with patient-reported outcomes, medication adherence tracking, and clinical intervention triggers.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Health Monitoring Pipeline                  │
├────────────────┬──────────────────┬─────────────────────┤
│  Data Sources  │  Analytics Core  │  Clinical Output    │
│                │                  │                     │
│ • Wearables    │ • Time-series DB │ • Dashboards        │
│ • Home Devices │ • Anomaly Engine │ • Clinical Alerts   │
│ • CGMs         │ • Trend Analysis │ • Risk Scores       │
│ • Implants     │ • ML Models      │ • Recommendations   │
│ • Patient HR   │ • Rule Engine    │ • Reports           │
└────────────────┴──────────────────┴─────────────────────┘
```

## Data Types by Device

| Device | Metrics | Frequency | Clinical Use |
|--------|---------|-----------|-------------|
| Smartwatch | HR, HRV, SpO2, Steps | Continuous | AFib detection, activity |
| CGM | Interstitial glucose | Every 5 min | Diabetes management |
| BP Cuff | Systolic/Diastolic, Pulse | 2-4x daily | Hypertension control |
| Smart Scale | Weight, BMI, Body comp | Daily | Heart failure monitoring |
| Pulse Oximeter | SpO2, PR | Spot check | Respiratory monitoring |
| Spirometer | FEV1, FVC | Daily | COPD/asthma management |
| ECG Monitor | Rhythm, intervals | On-demand | Arrhythmia detection |

## Normal Vital Sign Ranges

| Vital Sign | Adult Normal | Alert Low | Alert High |
|------------|-------------|-----------|------------|
| Heart Rate | 60-100 bpm | <50 | >120 |
| Systolic BP | 90-120 mmHg | <90 | >180 |
| Diastolic BP | 60-80 mmHg | <60 | >110 |
| SpO2 | 95-100% | <92% | — |
| Respiratory Rate | 12-20 /min | <8 | >28 |
| Temperature | 97.8-99.1 F | <96 | >101.3 |
| Blood Glucose | 70-140 mg/dL | <54 | >400 |

## Anomaly Detection Methods

| Method | Complexity | Best For |
|--------|-----------|----------|
| Z-Score | Low | Single-parameter thresholds |
| Moving Average | Low | Trend shifts |
| EWMA | Low | Gradual drift detection |
| Isolation Forest | Medium | Multi-parameter anomalies |
| LSTM Autoencoder | High | Complex temporal patterns |
| Clinical Rules | Low | Known pathophysiology |

## Common Pitfalls

1. **Motion artifacts**: Wearable data corrupted by movement — filter before analysis
2. **Baseline drift**: Individual baselines shift over time — personalize thresholds
3. **Alert fatigue**: Too many false positives desensitize clinicians
4. **Data gaps**: Intermittent connectivity creates missing data windows
5. **Confounding**: Exercise, stress, caffeine affect vital signs — context matters
6. **Device variance**: Consumer devices may have ±5 bpm accuracy limitations

## References

- Dunn, J., et al. (2018). Wearable Sensors for Remote Patient Monitoring. *JMIR mHealth*
- Steinhubl, S. R., et al. (2015). The Emerging Field of Mobile Health. *Science Translational Medicine*
- ADA Standards of Medical Care in Diabetes (2024)
- AHA Guidelines for Home Monitoring of Heart Failure
