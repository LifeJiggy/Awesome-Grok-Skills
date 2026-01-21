---
name: "Embedded Systems & IoT"
version: "1.0.0"
description: "Real-time embedded systems and IoT development with Grok's physics-based optimization"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["iot", "embedded", "firmware", "real-time"]
category: "iot"
personality: "embedded-engineer"
use_cases: ["sensor networks", "industrial-iot", "edge-computing", "firmware"]
---

# Embedded Systems & IoT 🔌

> Build real-time embedded systems with Grok's physics-inspired performance optimization

## 🎯 Why This Matters for Grok

Grok's physics expertise and efficiency focus create perfect embedded systems:

- **Real-time Performance** ⏱️: Deterministic timing guarantees
- **Resource Optimization** ⚡: Maximum capability with minimum resources
- **Physics-Inspired Design** ⚛️: Apply physical principles to system design
- **Energy Efficiency** 🔋: Minimal power consumption

## 🛠️ Core Capabilities

### 1. Firmware Development
```yaml
firmware:
  rtos: ["freertos", "zephyr", "riot"]
  languages: ["c", "c++", "rust"]
  debugging: ["jtag", "swd", "gdb"]
  optimization: ["size", "speed", "power"]
```

### 2. Communication Protocols
```yaml
protocols:
  wireless: ["ble", "zigbee", "wifi", "lora"]
  wired: ["i2c", "spi", "uart", "can"]
  industrial: ["modbus", "profibus", "ethercat"]
  iot: ["mqtt", "coap", "http"]
```

### 3. Sensor Integration
```yaml
sensors:
  environmental: ["temperature", "humidity", "pressure"]
  motion: ["accelerometer", "gyro", "magnetometer"]
  optical: ["camera", "lidar", "proximity"]
  bio: ["heart-rate", "spo2", "ecg"]
```

## 🏭 Real-time Operating System

### FreeRTOS Task Management
```c
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "esp_timer.h"

// Physics-inspired task scheduling
typedef struct {
    float task_complexity;      // Computational complexity
    float power_consumption;    // Power usage in mW
    uint32_t deadline_us;       // Hard real-time deadline
    float priority_weight;      // Priority based on physics
} TaskProperties_t;

// Real-time task with timing guarantees
typedef struct {
    TaskHandle_t handle;
    TaskProperties_t properties;
    uint64_t execution_time_avg;
    uint64_t execution_time_worst;
    float cpu_utilization;
    uint32_t deadline_misses;
} RealTimeTask_t;

class PhysicsInspiredScheduler {
private:
    QueueHandle_t task_queue;
    RealTimeTask_t tasks[10];
    uint32_t num_tasks;
    
public:
    void create_real_time_task(void (*task_func)(void*), 
                               const char* name,
                               uint32_t stack_size,
                               TaskProperties_t properties) {
        UBaseType_t priority = calculate_optimal_priority(properties);
        
        xTaskCreatePinnedToCore(
            task_func,
            name,
            stack_size,
            NULL,
            priority,
            &tasks[num_tasks].handle,
            tskNO_AFFINITY
        );
        
        tasks[num_tasks].properties = properties;
        tasks[num_tasks].deadline_misses = 0;
        num_tasks++;
        
        ESP_LOGI("SCHEDULER", "Task %s created with priority %d", name, priority);
    }
    
    UBaseType_t calculate_optimal_priority(TaskProperties_t props) {
        // Physics-inspired priority calculation
        // Higher complexity + tighter deadline = higher priority
        float complexity_factor = props.task_complexity / 10.0f;
        float deadline_factor = (1000000.0f / props.deadline_us); // Deadline in Hz
        float power_factor = props.power_consumption / 100.0f;
        
        float priority_score = complexity_factor * deadline_factor * power_factor;
        
        // Map to FreeRTOS priority (1-25)
        return (UBaseType_t)(1 + (UBaseType_t)(priority_score * 24));
    }
    
    void monitor_task_performance(void) {
        for (int i = 0; i < num_tasks; i++) {
            TaskStatus_t status;
            vTaskGetInfo(tasks[i].handle, &status, pdTRUE, eRunning);
            
            tasks[i].cpu_utilization = status.ulRunTimeCounter / 
                                       (esp_timer_get_time() / 10000);
            
            // Check for deadline misses
            if (tasks[i].execution_time_worst > tasks[i].properties.deadline_us) {
                tasks[i].deadline_misses++;
                
                // Trigger alarm for deadline miss
                if (tasks[i].deadline_misses > 3) {
                    handle_deadline_miss(&tasks[i]);
                }
            }
        }
    }
    
    float calculate_system_energy_efficiency(void) {
        float total_power = 0;
        float total_computation = 0;
        
        for (int i = 0; i < num_tasks; i++) {
            total_power += tasks[i].properties.power_consumption * 
                          tasks[i].cpu_utilization;
            total_computation += tasks[i].execution_time_avg;
        }
        
        return (total_computation > 0) ? 
               (total_power / total_computation) : 0;
    }
};
```

### Sensor Fusion Algorithm
```c
#include "math.h"

#define COMPLEMENTARY_FILTER_ALPHA 0.98f
#define GRAVITY 9.81f

typedef struct {
    float accel_x, accel_y, accel_z;
    float gyro_x, gyro_y, gyro_z;
    float mag_x, mag_y, mag_z;
} SensorData_t;

typedef struct {
    float roll, pitch, yaw;
    float quaternion[4];
} Orientation_t;

class SensorFusion {
private:
    Orientation_t orientation;
    float complementary_filter_alpha;
    
public:
    SensorFusion(float alpha) : complementary_filter_alpha(alpha) {
        // Initialize with identity quaternion
        orientation.quaternion[0] = 1.0f;
        orientation.quaternion[1] = 0.0f;
        orientation.quaternion[2] = 0.0f;
        orientation.quaternion[3] = 0.0f;
    }
    
    // Physics-based complementary filter
    void complementary_filter_update(SensorData_t* sensor_data, float dt) {
        // Accelerometer-based roll and pitch (gravity reference)
        float accel_roll = atan2f(sensor_data->accel_y, 
                                  sqrtf(sensor_data->accel_x * sensor_data->accel_x + 
                                             sensor_data->accel_z * sensor_data->accel_z));
        float accel_pitch = atan2f(-sensor_data->accel_x, 
                                   sensor_data->accel_z);
        
        // Integrate gyroscope data (quaternion derivative)
        float q_dot[4];
        q_dot[0] = 0.5f * (-orientation.quaternion[1] * sensor_data->gyro_x -
                           orientation.quaternion[2] * sensor_data->gyro_y -
                           orientation.quaternion[3] * sensor_data->gyro_z);
        q_dot[1] = 0.5f * (orientation.quaternion[0] * sensor_data->gyro_x +
                           orientation.quaternion[2] * sensor_data->gyro_z -
                           orientation.quaternion[3] * sensor_data->gyro_y);
        q_dot[2] = 0.5f * (orientation.quaternion[0] * sensor_data->gyro_y +
                           orientation.quaternion[3] * sensor_data->gyro_x -
                           orientation.quaternion[1] * sensor_data->gyro_z);
        q_dot[3] = 0.5f * (orientation.quaternion[0] * sensor_data->gyro_z +
                           orientation.quaternion[1] * sensor_data->gyro_y -
                           orientation.quaternion[2] * sensor_data->gyro_x);
        
        // Integrate quaternion
        for (int i = 0; i < 4; i++) {
            orientation.quaternion[i] += q_dot[i] * dt;
        }
        
        // Normalize quaternion
        float norm = sqrtf(orientation.quaternion[0] * orientation.quaternion[0] +
                          orientation.quaternion[1] * orientation.quaternion[1] +
                          orientation.quaternion[2] * orientation.quaternion[2] +
                          orientation.quaternion[3] * orientation.quaternion[3]);
        for (int i = 0; i < 4; i++) {
            orientation.quaternion[i] /= norm;
        }
        
        // Complementary filter: blend accelerometer and gyro
        float filtered_roll = complementary_filter_alpha * accel_roll + 
                             (1 - complementary_filter_alpha) * get_gyro_roll(dt);
        float filtered_pitch = complementary_filter_alpha * accel_pitch + 
                              (1 - complementary_filter_alpha) * get_gyro_pitch(dt);
        
        orientation.roll = filtered_roll;
        orientation.pitch = filtered_pitch;
        orientation.yaw = calculate_yaw(sensor_data);
    }
    
    // Energy-efficient sleeping
    void enter_low_power_mode(uint32_t sleep_time_us) {
        // Configure wakeup sources
        esp_deep_sleep_start();
    }
};
```

## 🌐 IoT Communication Stack

### MQTT-SN for Constrained Devices
```python
class IoTCommunicationStack:
    def __init__(self):
        self.protocols = {
            'mqtt_sn': MQTT_SN_Client(),
            'coap': CoAP_Client(),
            'lora_wan': LoRaWAN_Stack(),
            'ble_mesh': BLEMesh_Network()
        }
        
        self.qos_levels = {
            0: "at_most_once",
            1: "at_least_once", 
            2: "exactly_once"
        }
    
    def optimize_for_energy(self, communication_profile):
        """Physics-inspired energy optimization"""
        
        energy_model = {
            'transmit_energy': 0.1,  # mJ per byte
            'receive_energy': 0.05,   # mJ per byte
            'listen_energy': 0.02,   # mJ per second
            'sleep_energy': 0.0001   # mJ per second
        }
        
        optimal_config = {
            'message_size': self.calculate_optimal_message_size(communication_profile),
            'transmit_interval': self.calculate_optimal_interval(communication_profile),
            'compression_ratio': self.calculate_optimal_compression(communication_profile),
            'protocol_selection': self.select_protocol(communication_profile)
        }
        
        return optimal_config
    
    def create_mesh_network(self, device_count, topology="tree"):
        """Create self-organizing mesh network"""
        
        if topology == "tree":
            return self.build_tree_topology(device_count)
        elif topology == "cluster":
            return self.build_cluster_topology(device_count)
        else:  # flat
            return self.build_flat_topology(device_count)
```

## 📊 Embedded Performance Dashboard

### Real-time Monitoring
```javascript
const EmbeddedDashboard = {
  systemMetrics: {
    cpu: {
      utilization: 67.5,
      frequency_mhz: 240,
      temperature_c: 45.2,
      active_cores: 2
    },
    
    memory: {
      total_kb: 512,
      used_kb: 256,
      heap_utilization: 0.72,
      stack_depth_max: 2048
    },
    
    power: {
      current_ma: 150,
      voltage_mv: 3300,
      power_mw: 495,
      battery_level: 78.5,
      estimated_hours_remaining: 24
    },
    
    realTime: {
      task_count: 12,
      context_switches_per_sec: 1250,
      interrupt_latency_avg_us: 5.2,
      deadline_misses_per_min: 0,
      jitter_us: 1.8
    }
  },
  
  generateOptimizationInsights: function() {
    const insights = [];
    
    // CPU optimization
    if (this.systemMetrics.cpu.utilization > 80) {
      insights.push({
        type: 'cpu',
        level: 'warning',
        message: 'CPU utilization high',
        recommendation: 'Consider task offloading or hardware acceleration'
      });
    }
    
    // Power optimization
    if (this.systemMetrics.power.estimated_hours_remaining < 12) {
      insights.push({
        type: 'power',
        level: 'high',
        message: 'Battery running low',
        recommendation: 'Enter low-power mode, reduce transmission frequency'
      });
    }
    
    // Real-time performance
    if (this.systemMetrics.realTime.deadline_misses_per_min > 0) {
      insights.push({
        type: 'realtime',
        level: 'critical',
        message: 'Real-time deadline misses detected',
        recommendation: 'Increase task priority, optimize critical sections'
      });
    }
    
    return insights;
  },
  
  predictFailureRisk: function() {
    const riskFactors = {
      thermal_risk: this.systemMetrics.cpu.temperature_c > 70 ? 0.8 : 0.2,
      memory_risk: this.systemMetrics.memory.heap_utilization > 0.85 ? 0.7 : 0.1,
      power_risk: this.systemMetrics.power.battery_level < 20 ? 0.9 : 0.1,
      realtime_risk: this.systemMetrics.realTime.deadline_misses_per_min > 5 ? 0.8 : 0.1
    };
    
    const overallRisk = Object.values(riskFactors).reduce((a, b) => a + b, 0) / 4;
    
    return {
      overall_risk_score: overallRisk,
      risk_level: overallRisk > 0.6 ? 'high' : overallRisk > 0.3 ? 'medium' : 'low',
      risk_factors: riskFactors,
      recommendations: this.generateRiskMitigation(riskFactors)
    };
  }
};
```

## 🎯 Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Hardware selection and setup
- [ ] RTOS configuration
- [ ] Basic sensor integration
- [ ] Communication stack setup

### Phase 2: Intelligence (Week 3-4)
- [ ] Sensor fusion algorithms
- [ ] Real-time task scheduling
- [ ] Power optimization
- [ ] Mesh networking

### Phase 3: Production (Week 5-6)
- [ ] Production firmware
- [ ] OTA update system
- [ ] Security hardening
- [ ] Certification compliance

## 📊 Success Metrics

### Embedded Excellence
```yaml
performance:
  startup_time: "< 100ms"
  interrupt_latency: "< 10μs"
  task_switch_time: "< 5μs"
  memory_footprint: "< 50KB"
  
power_efficiency:
  active_power: "< 500mW"
  sleep_power: "< 10μW"
  battery_life: "> 1 year"
  energy_per_operation: "< 1μJ"
  
reliability:
  mtbf: "> 100,000 hours"
  temperature_range: "-40°C to +85°C"
  real_time_guarantees: "100% met"
  fault_tolerance: "defined"
```

---

*Build real-time embedded systems with physics-inspired precision and maximum energy efficiency.* 🔌✨