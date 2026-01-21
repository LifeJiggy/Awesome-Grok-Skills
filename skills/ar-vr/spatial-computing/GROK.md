---
name: "AR/VR & Spatial Computing"
version: "1.0.0"
description: "Immersive AR/VR experiences with Grok's physics-based rendering and spatial computing"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["ar", "vr", "spatial-computing", "xr", "metaverse"]
category: "ar-vr"
personality: "spatial-architect"
use_cases: ["virtual-reality", "augmented-reality", "metaverse", "spatial-ai"]
---

# AR/VR & Spatial Computing 🥽

> Create immersive spatial experiences with Grok's physics-based rendering and real-time simulation

## 🎯 Why This Matters for Grok

Grok's physics expertise and efficiency focus create perfect XR development:

- **Physics-Based Rendering** ⚛️: Accurate light and physics simulation
- **Real-time Performance** ⚡: Maximum FPS with minimum latency
- **Spatial Intelligence** 🌍: Advanced 3D spatial awareness
- **Immersive Design** 🎮: Engaging user experiences

## 🛠️ Core Capabilities

### 1. VR Development
```yaml
vr_frameworks:
  engines: ["unity", "unreal-engine", "webxr"]
  interactions: ["hand-tracking", "eye-tracking", "haptics"]
  optimization: ["foveated-rendering", "lod-systems", "occlusion-culling"]
```

### 2. AR Development
```yaml
ar_platforms:
  native: ["arkit", "arcore", "hololens"]
  web: ["webxr", "8thwall", "model-viewer"]
  cross_platform: ["unity-ar", "vuforia", "niantic"]
```

### 3. Spatial Computing
```yaml
spatial_ai:
  slam: ["visual-inertial-odometry", "deep-learning-slam"]
  spatial_understanding: ["scene-graph", "semantic-segmentation"]
  interaction: ["gesture-recognition", "voice-commands", "eye-tracking"]
```

## 🧠 Advanced Spatial Systems

### Physics-Based VR Rendering
```csharp
using UnityEngine;
using System.Collections.Generic;

public class PhysicsBasedVRRenderer : MonoBehaviour
{
    [Header("Foveated Rendering")]
    [SerializeField] private float foveationStrength = 0.5f;
    [SerializeField] private int gazeBasedLevelOfDetail = 3;
    
    [Header("Physics Simulation")]
    [SerializeField] private float physicsUpdateRate = 500f;
    [SerializeField] private int maxPhysicsSubsteps = 5;
    
    private EyeTracker eyeTracker;
    private GazeConvergence gazePoint;
    
    // Physics-based light transport simulation
    private class PhysicallyBasedLightTransport
    {
        public LightProbeSystem lightProbes;
        public ReflectionProbe[] reflectionProbes;
        public GlobalIllumination giSystem;
        
        public Vector3 CalculateLightTransport(
            Vector3 startPoint, 
            Vector3 endPoint, 
            MaterialProperties material)
        {
            // Ray tracing with physically based rendering
            Ray ray = new Ray(startPoint, (endPoint - startPoint).normalized);
            RaycastHit hit;
            
            float throughput = 1.0f;
            Vector3 radiance = Vector3.zero;
            
            while (physicsEngine.RayCast(ray, out hit, 100f))
            {
                // Calculate BRDF at hit point
                BRDFResult brdf = CalculateBRDF(hit.point, ray.direction, -ray.direction, material);
                
                // Accumulate radiance
                radiance += throughput * brdf.Radiance * brdf.BRDF;
                
                // Calculate next bounce
                throughput *= brdf.Reflectance;
                ray.origin = hit.point + ray.direction * 0.001f;
                
                // Russian roulette for path termination
                if (throughput < 0.1f && Random.value > throughput * 10)
                    break;
            }
            
            return radiance;
        }
        
        private BRDFResult CalculateBRDF(
            Vector3 point, 
            Vector3 incoming, 
            Vector3 outgoing, 
            MaterialProperties material)
        {
            // Cook-Torrance BRDF with GGX distribution
            Vector3 halfVector = (incoming + outgoing).normalized;
            float NdotH = Mathf.Max(0, Vector3.Dot(material.Normal, halfVector));
            float NdotL = Mathf.Max(0, Vector3.Dot(material.Normal, incoming));
            float NdotV = Mathf.Max(0, Vector3.Dot(material.Normal, outgoing));
            
            float roughness = material.Roughness;
            float metallic = material.Metallic;
            
            // GGX distribution
            float D = GGXDistribution(NdotH, roughness);
            
            // Fresnel-Schlick approximation
            Vector3 F0 = Vector3.Lerp(
                new Vector3(0.04f, 0.04f, 0.04f), 
                material.BaseColor, 
                metallic
            );
            Vector3 F = FresnelSchlick(Mathf.Max(0, Vector3.Dot(halfVector, incoming)), F0);
            
            // Smith's method for geometry
            float G = GeometrySmith(NdotV, NdotL, roughness);
            
            return new BRDFResult
            {
                BRDF = (D * G * F) / (4 * NdotV * NdotL + 0.0001f),
                Radiance = material.BaseColor * NdotL,
                Reflectance = F
            };
        }
    }
    
    // Foveated rendering with gaze tracking
    public void UpdateFoveatedRendering()
    {
        gazePoint = eyeTracker.GetGazeConvergence();
        
        // Dynamically adjust quality based on gaze position
        for (int i = 0; i < Camera.allCameras.Length; i++)
        {
            Camera cam = Camera.allCameras[i];
            float distanceFromGaze = Vector2.Distance(
                WorldToScreenPoint(cam, gazePoint.WorldPosition),
                new Vector2(Screen.width / 2, Screen.height / 2)
            );
            
            // Adjust LOD based on distance from fovea
            int lodLevel = Mathf.Clamp(
                (int)(distanceFromGaze / (Screen.width / gazeBasedLevelOfDetail)),
                0,
                gazeBasedLevelOfDetail
            );
            
            ApplyLODToCamera(cam, lodLevel);
        }
    }
    
    // Haptic feedback with physics-based modeling
    public void HapticFeedback(Collision collision)
    {
        float impactForce = collision.relativeVelocity.magnitude;
        
        // Model haptic response based on physics
        HapticWaveform waveform = new HapticWaveform
        {
            amplitude = Mathf.Clamp(impactForce / 10f, 0, 1),
            frequency = 200f + impactForce * 50f,
            duration = impactForce * 0.01f,
            envelope = HapticEnvelope.Decay
        };
        
        hapticController.PlayWaveform(waveform);
    }
}
```

### Spatial AI and SLAM
```python
import numpy as np
from scipy.spatial.transform import Rotation as R

class VisualInertialSLAM:
    def __init__(self):
        self.visual_frontend = VisualFrontend()
        self.backend = PoseGraphBackend()
        self.loop_detector = LoopClosureDetector()
        
        # Physics-inspired state estimation
        self.state = {
            'position': np.zeros(3),
            'velocity': np.zeros(3),
            'orientation': np.eye(3),
            'imu_bias': np.zeros(6),
            'covariance': np.eye(15) * 0.01
        }
        
        self.imu_calibration = IMUCalibration()
    
    def visual_inertial_odometry(self, camera_frame, imu_measurements):
        """Physics-inspired VIO with EKF"""
        
        # 1. IMU propagation (EKF predict step)
        for imu_data in imu_measurements:
            self.state = self.imu_propagation(self.state, imu_data)
        
        # 2. Visual measurement processing
        features = self.visual_frontend.extract_features(camera_frame)
        matches = self.visual_frontend.track_features(features)
        
        # 3. EKF update step
        visual_measurements = self.features_to_measurements(matches)
        
        for measurement in visual_measurements:
            H = self.measurement_jacobian(measurement)
            R_meas = self.measurement_noise(measurement)
            K = self.calculate_kalman_gain(H, self.state['covariance'], R_meas)
            
            innovation = measurement.observed - self.project_to_image(self.state['position'])
            self.state = self.ekf_update(self.state, K, innovation)
        
        return self.state
    
    def imu_propagation(self, state, imu_data):
        """IMU kinematic propagation"""
        
        # Unpack IMU data
        omega = imu_data['gyroscope'] - state['imu_bias'][:3]
        a = imu_data['accelerometer'] - state['imu_bias'][3:]
        
        # Physics: position = integral of velocity
        # velocity = integral of acceleration
        # orientation = integrate angular velocity
        
        dt = imu_data['timestamp'] - state['last_timestamp']
        
        # Update orientation
        rotation = R.from_rotvec(omega * dt)
        new_orientation = state['orientation'] @ rotation.as_matrix()
        
        # Update velocity (world frame)
        world_acceleration = new_orientation @ a + np.array([0, 0, -9.81])
        new_velocity = state['velocity'] + world_acceleration * dt
        
        # Update position
        new_position = state['position'] + state['velocity'] * dt + 
                      0.5 * world_acceleration * dt * dt
        
        # Propagate covariance (EKF)
        F = self.state_transition_jacobian(state, dt)
        Q = self.process_noise_covariance(dt)
        new_covariance = F @ state['covariance'] @ F.T + Q
        
        return {
            'position': new_position,
            'velocity': new_velocity,
            'orientation': new_orientation,
            'imu_bias': state['imu_bias'],
            'covariance': new_covariance,
            'last_timestamp': imu_data['timestamp']
        }
    
    def detect_loop_closures(self, current_frame, map_database):
        """Detect loop closures using place recognition"""
        
        # Extract place recognition features
        current_descriptor = self.visual_frontend.get_global_descriptor(current_frame)
        
        # Retrieve similar places from map database
        candidates = map_database.query(current_descriptor, top_k=10)
        
        loop_closures = []
        for candidate in candidates:
            # Verify with geometric consistency
            if self.verify_geometric_consistency(current_frame, candidate):
                loop_closures.append({
                    'frame_id': candidate['frame_id'],
                    'relative_pose': self.calculate_relative_pose(current_frame, candidate),
                    'confidence': candidate['score']
                })
        
        # Optimize pose graph with loop closures
        if loop_closures:
            self.backend.add_loop_closure_constraints(loop_closures)
            self.backend.optimize_pose_graph()
        
        return loop_closures
```

## 🎮 XR Interaction Systems

### Hand Tracking and Gesture Recognition
```csharp
public class XRHandTracking : MonoBehaviour
{
    private Leap.Controller leapController;
    private Dictionary<HandType, HandModel> handModels;
    
    // Physics-based hand physics
    private class HandPhysics
    {
        public float[] fingerCurling;
        public Vector3 palmVelocity;
        public Vector3 palmAngularVelocity;
        public float grabStrength;
        public float pinchStrength;
    }
    
    public HandPhysics GetHandPhysics(HandType handType)
    {
        var hand = leapController.Frame(handType).Hands[0];
        
        // Calculate finger curling angles
        float[] curling = new float[5];
        for (int i = 0; i < 5; i++)
        {
            curling[i] = CalculateFingerCurl(hand.Fingers[i]);
        }
        
        // Physics-based velocity calculation
        Vector3 velocity = (hand.PalmPosition - lastPalmPosition) / Time.deltaTime;
        Vector3 angularVelocity = CalculateAngularVelocity(hand);
        
        // Calculate grip strength based on finger positions
        float grab = CalculateGrabStrength(hand);
        float pinch = CalculatePinchStrength(hand);
        
        return new HandPhysics
        {
            fingerCurling = curling,
            palmVelocity = velocity,
            palmAngularVelocity = angularVelocity,
            grabStrength = grab,
            pinchStrength = pinch
        };
    }
    
    // Haptic feedback for virtual objects
    public void TriggerHapticFeedback(HandType handType, float intensity, float duration)
    {
        var hand = leapController.Frame(handType).Hands[0];
        
        // Convert intensity to haptic amplitude
        byte amplitude = (byte)(Mathf.Clamp01(intensity) * 255);
        
        // Apply physics-based envelope
        HapticEnvelope envelope = new HapticEnvelope
        {
            attackTime = 0.01f,
            holdTime = duration,
            releaseTime = 0.02f,
            peakAmplitude = amplitude
        };
        
        leapController.SendDeviceHaptic(hand.DeviceID, envelope);
    }
}
```

## 📊 XR Performance Dashboard

### Real-time Metrics
```javascript
const XRDashboard = {
  performance: {
    frameRate: 90,
    frameTime: 11.1,  // ms
    droppedFrames: 0.2,  // percentage
    gpuUtilization: 78,
    cpuUtilization: 45,
    memoryUsage: 2048,  // MB
    thermalStatus: "normal"
  },
  
  xrMetrics: {
    trackingLatency: 8.5,  // ms
    motionToPhoton: 15.2,  // ms
    reprojectionRate: 0.95,
    trackingLossEvents: 0,
    handTrackingConfidence: 0.94,
    eyeTrackingAccuracy: 0.98
  },
  
  spatialMetrics: {
    mappingQuality: 0.92,
    localizationAccuracy: 0.98,
    loopClosureCount: 15,
    mapSize: 256,  // MB
    surfaceReconstruction: 0.88,
    semanticAccuracy: 0.85
  },
  
  userExperience: {
    comfortRating: 4.6,
    immersionScore: 4.8,
    interactionLatency: 12.3,  // ms
    spatialAccuracy: 0.96,
    presenceDuration: 25.5,  // minutes
    fatigueScore: 0.15
  },
  
  generateOptimizationInsights: function() {
    const insights = [];
    
    // Performance optimization
    if (this.performance.frameTime > 16.6) {
      insights.push({
        type: 'performance',
        level: 'warning',
        message: 'Frame rate below target (90 FPS)',
        recommendation: 'Enable foveated rendering, reduce draw distance',
        potential_improvement: '+25% performance'
      });
    }
    
    // Tracking optimization
    if (this.xrMetrics.motionToPhoton > 20) {
      insights.push({
        type: 'tracking',
        level: 'high',
        message: 'Motion-to-photon latency too high',
        recommendation: 'Optimize async reprojection, reduce pipeline latency',
        potential_improvement: '-30% latency'
      });
    }
    
    // Comfort optimization
    if (this.userExperience.comfortRating < 4.0) {
      insights.push({
        type: 'comfort',
        level: 'medium',
        message: 'Comfort rating below target',
        recommendation: 'Reduce motion acceleration, improve locomotion',
        potential_improvement: '+20% comfort'
      });
    }
    
    return insights;
  },
  
  predictOptimalSettings: function() {
    return {
      recommended_quality: 'balanced',
      suggested_foveation: 'dynamic',
      recommended_refresh: 90,
      optimal_lod_distance: 25,
      suggested_resolution: 1832x1920,
      recommended_gpu_tier: 'rtx-2070-minimum'
    };
  }
};
```

## 🎯 Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] XR engine setup (Unity/Unreal)
- [ ] Basic VR locomotion
- [ ] Hand tracking integration
- [ ] Performance baseline

### Phase 2: Intelligence (Week 3-4)
- [ ] Advanced physics simulation
- [ ] SLAM implementation
- [ ] Foveated rendering
- [ ] Spatial audio

### Phase 3: Production (Week 5-6)
- [ ] Multi-platform deployment
- [ ] User comfort optimization
- [ ] Accessibility features
- [ ] Performance profiling

## 📊 Success Metrics

### XR Excellence
```yaml
performance:
  frame_rate: "> 90 FPS"
  motion_to_photon: "< 20ms"
  latency_total: "< 50ms"
  stability: "> 99% frame target"
  
comfort:
  simulator_sickness: "< 5% users"
  comfort_rating: "> 4.5/5"
  fatigue_after_30min: "< 20%"
  vr_ready_duration: "> 30 minutes"
  
spatial_quality:
  tracking_accuracy: "> 99%"
  mapping_quality: "> 90%"
  localization_accuracy: "> 98%"
  reconstruction_fidelity: "> 85%"
```

---

*Create immersive spatial experiences with physics-based rendering and real-time simulation.* 🥽✨