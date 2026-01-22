"""
Embedded Systems Pipeline
IoT and real-time embedded systems
"""

import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from collections import deque


class TaskPriority(Enum):
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3


@dataclass
class RTOSConfig:
    tick_rate: int = 1000
    max_tasks: int = 16
    stack_size: int = 256
    heap_size: int = 4096


class RTOSKernel:
    """Real-time operating system kernel"""
    
    def __init__(self, config: RTOSConfig):
        self.config = config
        self.tasks = []
        self.current_task = None
        self.tick_count = 0
        self.running = False
    
    def create_task(self, name: str, 
                   priority: TaskPriority,
                   stack_size: int = None) -> int:
        """Create new task"""
        task_id = len(self.tasks)
        self.tasks.append({
            "id": task_id,
            "name": name,
            "priority": priority,
            "stack": [0] * (stack_size or self.config.stack_size),
            "state": "ready",
            "wait_time": 0
        })
        return task_id
    
    def schedule(self):
        """Schedule next task based on priority"""
        ready_tasks = [t for t in self.tasks if t["state"] == "ready"]
        
        if not ready_tasks:
            return
        
        highest = min(ready_tasks, key=lambda t: t["priority"].value)
        self.current_task = highest
    
    def delay(self, task_id: int, milliseconds: int):
        """Delay task"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["wait_time"] = milliseconds // (1000 // self.config.tick_rate)
                task["state"] = "waiting"
                break
    
    def tick_isr(self):
        """Timer interrupt service routine"""
        self.tick_count += 1
        
        for task in self.tasks:
            if task["state"] == "waiting":
                task["wait_time"] -= 1
                if task["wait_time"] <= 0:
                    task["state"] = "ready"


class SensorInterface:
    """Sensor interface for embedded systems"""
    
    def __init__(self):
        self.sensors = {}
        self.buffers = {}
    
    def register_sensor(self, name: str, 
                       sample_rate: int,
                       resolution: int):
        """Register new sensor"""
        self.sensors[name] = {
            "sample_rate": sample_rate,
            "resolution": resolution,
            "last_reading": None,
            "last_time": 0
        }
        self.buffers[name] = deque(maxlen=100)
    
    def read_sensor(self, name: str) -> Optional[float]:
        """Read from sensor"""
        if name not in self.sensors:
            return None
        
        sensor = self.sensors[name]
        current_time = time.time()
        
        if current_time - sensor["last_time"] < 1 / sensor["sample_rate"]:
            return sensor["last_reading"]
        
        simulated_reading = self._simulate_reading(name)
        sensor["last_reading"] = simulated_reading
        sensor["last_time"] = current_time
        self.buffers[name].append(simulated_reading)
        
        return simulated_reading
    
    def _simulate_reading(self, name: str) -> float:
        """Simulate sensor reading"""
        base_values = {
            "temperature": 25.0,
            "humidity": 50.0,
            "pressure": 1013.25,
            "accelerometer_x": 0.0,
            "accelerometer_y": 0.0,
            "accelerometer_z": 1.0,
            "gyroscope_x": 0.0,
            "gyroscope_y": 0.0,
            "gyroscope_z": 0.0
        }
        return base_values.get(name, 0.0) + (hash(str(time.time())) % 100) / 1000
    
    def get_filtered_reading(self, name: str, 
                            filter_type: str = "moving_average",
                            window: int = 5) -> float:
        """Get filtered sensor reading"""
        if name not in self.buffers or len(self.buffers[name]) == 0:
            return self.read_sensor(name)
        
        if filter_type == "moving_average":
            return np.mean(list(self.buffers[name])[-window:])
        elif filter_type == "exponential":
            alpha = 2 / (window + 1)
            readings = list(self.buffers[name])[-window:]
            filtered = readings[0]
            for r in readings[1:]:
                filtered = alpha * r + (1 - alpha) * filtered
            return filtered
        
        return self.read_sensor(name)


class LowPowerManager:
    """Low power management for embedded devices"""
    
    def __init__(self):
        self.power_modes = {
            "active": {"current_ma": 50, "wake_time_us": 0},
            "sleep": {"current_ma": 1, "wake_time_us": 100},
            "deep_sleep": {"current_ma": 0.01, "wake_time_us": 1000},
            "hibernation": {"current_ma": 0.001, "wake_time_us": 5000}
        }
        self.current_mode = "active"
        self.last_wake_time = time.time()
    
    def enter_mode(self, mode: str):
        """Enter low power mode"""
        if mode in self.power_modes:
            self.current_mode = mode
            print(f"Entered {mode} mode")
    
    def estimate_battery_life(self, 
                             battery_mah: float,
                             average_current_ma: float = None) -> float:
        """Estimate battery life in hours"""
        current = average_current_ma or self.power_modes[self.current_mode]["current_ma"]
        return battery_mah / current if current > 0 else float('inf')
    
    def optimize_schedule(self, 
                         tasks: List[Dict],
                         battery_mah: float) -> List[Dict]:
        """Optimize task schedule for power efficiency"""
        optimized = []
        current_time = 0
        
        for task in sorted(tasks, key=lambda t: t.get("deadline", 0)):
            task_power = task.get("power_ma", 10)
            available_power = battery_mah / (24 - current_time / 3600)
            
            if task_power <= available_power:
                optimized.append(task)
                current_time += task.get("duration_ms", 1000) / 1000
        
        return optimized


class CommunicationStack:
    """Embedded communication protocol stack"""
    
    def __init__(self):
        self.protocols = {}
        self.buffers = {}
    
    def add_protocol(self, name: str, protocol_type: str):
        """Add communication protocol"""
        self.protocols[name] = {
            "type": protocol_type,
            "tx_buffer": [],
            "rx_buffer": [],
            "status": "idle"
        }
    
    def send(self, protocol: str, data: bytes) -> bool:
        """Send data over protocol"""
        if protocol not in self.protocols:
            return False
        
        self.protocols[protocol]["tx_buffer"].append(data)
        self.protocols[protocol]["status"] = "transmitting"
        return True
    
    def receive(self, protocol: str, max_bytes: int = 1024) -> Optional[bytes]:
        """Receive data from protocol"""
        if protocol not in self.protocols:
            return None
        
        buffer = self.protocols[protocol]["rx_buffer"]
        if not buffer:
            return None
        
        data = b"".join(buffer[:max_bytes])
        self.protocols[protocol]["rx_buffer"] = buffer[len(data):]
        return data
    
    def crc16(self, data: bytes) -> int:
        """Calculate CRC16 checksum"""
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        return crc


if __name__ == "__main__":
    import numpy as np
    
    config = RTOSConfig(tick_rate=1000)
    rtos = RTOSKernel(config)
    
    rtos.create_task("sensor_task", TaskPriority.HIGH)
    rtos.create_task("comms_task", TaskPriority.NORMAL)
    
    sensors = SensorInterface()
    sensors.register_sensor("temperature", sample_rate=10, resolution=12)
    sensors.register_sensor("humidity", sample_rate=1, resolution=8)
    
    for _ in range(10):
        temp = sensors.read_sensor("temperature")
        filtered = sensors.get_filtered_reading("temperature")
    
    power = LowPowerManager()
    power.enter_mode("deep_sleep")
    battery_life = power.estimate_battery_life(2000)
    
    comms = CommunicationStack()
    comms.add_protocol("uart", "uart")
    comms.send("uart", b"\x01\x02\x03")
    
    print(f"RTOS tasks: {len(rtos.tasks)}")
    print(f"Temperature: {temp:.2f}, Filtered: {filtered:.2f}")
    print(f"Battery life: {battery_life:.1f} hours")
