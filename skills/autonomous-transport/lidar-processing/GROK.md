---
name: "lidar-processing"
category: "autonomous-transport"
version: "1.0.0"
tags: ["autonomous-transport", "lidar-processing"]
---

# Lidar Processing

## Overview

Comprehensive lidar-processing capabilities within the autonomous-transport domain. This module provides tools, frameworks, and best practices for lidar-processing operations. LiDAR (Light Detection and Ranging) is a remote sensing method that uses light in the form of a pulsed laser to measure ranges to the Earth. These light pulses—combined with other data recorded by the airborne system— generate precise, three-dimensional information about the shape of the Earth and its surface characteristics. In autonomous transport, LiDAR is critical for real-time 3D mapping, obstacle detection, localization, and path planning.

## Core Capabilities

- Configuration and setup
- Data processing and analysis
- Integration with related systems
- Monitoring and observability
- Best practices and patterns

## Usage

```python
from lidar_processing import LidarPipeline, PointCloudProcessor

# Initialize LiDAR pipeline
pipeline = LidarPipeline(
    sensor_config="velodyne_vls128",
    processing_mode="real_time",
    output_format="pcd"
)

# Configure processing parameters
pipeline.configure(
    voxel_size=0.1,
    ground_removal=True,
    clustering_method="dbscan"
)

# Process incoming point cloud data
processor = PointCloudProcessor(pipeline)
results = processor.run(input_stream="tcp://localhost:7331")
print(f"Detected {len(results.objects)} objects")
```

## Best Practices

- Follow security guidelines
- Implement proper error handling
- Use configuration management
- Monitor performance metrics
- Document API interfaces

## Related Modules

- Other modules in autonomous-transport domain
- Integration points with external systems

## Advanced Configuration

### LiDAR Sensor Configuration

LiDAR sensors come in various configurations—mechanical spinning, solid-state, and flash LiDAR. Each has different field-of-view, range, and resolution characteristics that must be tuned for the specific autonomous vehicle platform.

```python
# Velodyne VLP-16 configuration
sensor_config = {
    "sensor_type": "velodyne_vlp16",
    "channels": 16,
    "range": 100,  # meters
    "rotation_rate": 5,  # Hz
    "field_of_view": {
        "vertical": 30,  # degrees (-15 to +15)
        "horizontal": 360  # degrees
    },
    "distance_accuracy": 0.03,  # meters
    "return_mode": "dual",  # dual return mode
    "calibration_file": "/etc/lidar/calibration_vlp16.yaml"
}

# Real-time processing pipeline configuration
processing_config = {
    "frame_rate": 20,  # Hz
    "downsampling": {
        "method": "voxel_grid",
        "leaf_size": 0.1  # meters
    },
    "ground_removal": {
        "enabled": True,
        "algorithm": "ransac",
        "plane_threshold": 0.15,
        "max_iterations": 1000
    },
    "object_detection": {
        "clustering": "dbscan",
        "min_cluster_size": 10,
        "max_cluster_size": 10000,
        "epsilon": 0.4  # DBSCAN epsilon
    }
}
```

### Point Cloud Filtering Pipeline

The filtering pipeline is crucial for removing noise, outliers, and irrelevant points before object detection and classification.

```python
import numpy as np
from point_cloud_library import FilterChain, PassThroughFilter, StatisticalOutlierRemoval

class PointCloudFilter:
    def __init__(self, config):
        self.config = config
        self.filter_chain = FilterChain()
    
    def build_pipeline(self):
        # Remove points outside vehicle bounding box
        passthrough_x = PassThroughFilter("x", -10.0, 50.0)
        passthrough_y = PassThroughFilter("y", -20.0, 20.0)
        passthrough_z = PassThroughFilter("z", -2.0, 5.0)
        
        # Statistical outlier removal
        sor = StatisticalOutlierRemoval(
            mean_k=50,
            std_dev_threshold=1.0
        )
        
        # Radius-based outlier removal
        ror = RadiusOutlierRemoval(
            min_neighbors=3,
            search_radius=0.5
        )
        
        self.filter_chain.add(passthrough_x)
        self.filter_chain.add(passthrough_y)
        self.filter_chain.add(passthrough_z)
        self.filter_chain.add(sor)
        self.filter_chain.add(ror)
        
        return self.filter_chain
    
    def process(self, point_cloud):
        """Process a single point cloud frame."""
        filtered = self.filter_chain.apply(point_cloud)
        return filtered
```

## Architecture Patterns

### LiDAR Processing Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     LiDAR Processing Pipeline                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────────┐    ┌────────────────────┐    │
│  │ LiDAR    │───▶│ Point Cloud  │───▶│ Preprocessing      │    │
│  │ Sensor   │    │ Acquisition  │    │ (Filtering,        │    │
│  │ Array    │    │              │    │  Downsampling)     │    │
│  └──────────┘    └──────────────┘    └────────────────────┘    │
│        │                                      │                 │
│        │                                      ▼                 │
│        │                              ┌────────────────────┐    │
│        │                              │ Ground Removal     │    │
│        │                              │ (RANSAC, Height    │    │
│        │                              │  Map)              │    │
│        │                              └────────────────────┘    │
│        │                                      │                 │
│        │                                      ▼                 │
│        │                              ┌────────────────────┐    │
│        │                              │ Object Detection   │    │
│        │                              │ (Clustering,       │    │
│        │                              │  Classification)   │    │
│        │                              └────────────────────┘    │
│        │                                      │                 │
│        │                                      ▼                 │
│        │                              ┌────────────────────┐    │
│        │                              │ Object Tracking    │    │
│        │                              │ (Kalman Filter,    │    │
│        │                              │  Hungarian Algo)   │    │
│        │                              └────────────────────┘    │
│        │                                      │                 │
│        │                                      ▼                 │
│        │                              ┌────────────────────┐    │
│        └──────────────────────────────│ Fusion & Output    │    │
│                                       │ (Multi-sensor      │    │
│                                       │  Integration)      │    │
│                                       └────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Real-time Processing Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Real-time LiDAR Processing                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Hardware Layer:                                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                │
│  │  LiDAR      │  │  GPU        │  │  FPGA       │                │
│  │  Sensor     │  │  (CUDA)     │  │  (Preproc)  │                │
│  │  (128-ch)   │  │  Accelerat  │  │  Offload    │                │
│  └─────────────┘  └─────────────┘  └─────────────┘                │
│         │                │                │                        │
│         ▼                ▼                ▼                        │
│  ┌─────────────────────────────────────────────────┐              │
│  │              Data Ingestion Layer                │              │
│  │  • Zero-copy shared memory transfer             │              │
│  │  • Hardware timestamp synchronization           │              │
│  │  • UDP packet reassembly & ordering             │              │
│  └─────────────────────────────────────────────────┘              │
│         │                                                         │
│         ▼                                                         │
│  ┌─────────────────────────────────────────────────┐              │
│  │           Processing Pipeline (GPU)             │              │
│  │  • CUDA kernels for voxel filtering             │              │
│  │  • Parallel ground segmentation                 │              │
│  │  • GPU-accelerated Euclidean clustering         │              │
│  └─────────────────────────────────────────────────┘              │
│         │                                                         │
│         ▼                                                         │
│  ┌─────────────────────────────────────────────────┐              │
│  │           Perception Output (ROS2)              │              │
│  │  • DetectedObjects (BoundingBox3D)              │              │
│  │  • PredictedTrajectories (3-5s horizon)         │              │
│  │  • OccupancyGrid (costmap for planner)          │              │
│  └─────────────────────────────────────────────────┘              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Point Cloud Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Point Cloud Data Flow                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Raw Point Cloud                                                │
│  ┌─────────────────────────────────────┐                       │
│  │ [x1, y1, z1, intensity1, ring1]    │                       │
│  │ [x2, y2, z2, intensity2, ring2]    │                       │
│  │ ...                                 │                       │
│  │ [xN, yN, zN, intensityN, ringN]    │                       │
│  │ Points: ~300,000 per frame          │                       │
│  └─────────────────────────────────────┘                       │
│           │                                                     │
│           ▼                                                     │
│  ┌─────────────────────────────────────┐                       │
│  │  Voxel Grid Downsampling            │                       │
│  │  • Leaf size: 0.1m                  │                       │
│  │  • Output: ~50,000 points           │                       │
│  │  • Latency: 2ms                     │                       │
│  └─────────────────────────────────────┘                       │
│           │                                                     │
│           ▼                                                     │
│  ┌─────────────────────────────────────┐                       │
│  │  Statistical Outlier Removal        │                       │
│  │  • Mean neighbors: 50               │                       │
│  │  • Std dev threshold: 1.0           │                       │
│  │  • Output: ~48,000 points           │                       │
│  │  • Latency: 3ms                     │                       │
│  └─────────────────────────────────────┘                       │
│           │                                                     │
│           ▼                                                     │
│  ┌─────────────────────────────────────┐                       │
│  │  Ground Segmentation (RANSAC)       │                       │
│  │  • Plane threshold: 0.15m           │                       │
│  │  • Max iterations: 1000             │                       │
│  │  • Ground points: ~20,000           │                       │
│  │  • Non-ground: ~28,000              │                       │
│  │  • Latency: 5ms                     │                       │
│  └─────────────────────────────────────┘                       │
│           │                                                     │
│           ▼                                                     │
│  ┌─────────────────────────────────────┐                       │
│  │  DBSCAN Clustering                  │                       │
│  │  • Epsilon: 0.4m                    │                       │
│  │  • Min cluster size: 10             │                       │
│  │  • Max cluster size: 10000          │                       │
│  │  • Detected clusters: 5-20          │                       │
│  │  • Latency: 8ms                     │                       │
│  └─────────────────────────────────────┘                       │
│                                                                 │
│  Total Pipeline Latency: ~18ms (55 Hz effective)               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Integration Guide

### ROS2 Integration

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from perception_msgs.msg import DetectedObjects, Object3D
import numpy as np
from lidar_processor import PointCloudProcessor

class LidarPerceptionNode(Node):
    def __init__(self):
        super().__init__('lidar_perception')
        
        # Publisher for detected objects
        self.object_pub = self.create_publisher(
            DetectedObjects,
            '/perception/objects',
            10
        )
        
        # Subscriber for raw point clouds
        self.pointcloud_sub = self.create_subscription(
            PointCloud2,
            '/lidar/points',
            self.pointcloud_callback,
            10
        )
        
        # Initialize processor
        self.processor = PointCloudProcessor(
            config_file="/config/lidar_processor.yaml"
        )
        
        self.get_logger().info('LiDAR Perception Node initialized')
    
    def pointcloud_callback(self, msg):
        """Process incoming point cloud and publish detected objects."""
        try:
            # Convert ROS2 PointCloud2 to numpy array
            points = self.pointcloud2_to_numpy(msg)
            
            # Process with LiDAR pipeline
            detections = self.processor.process(points)
            
            # Convert to ROS2 message
            objects_msg = self.detections_to_msg(detections)
            objects_msg.header = msg.header
            
            # Publish
            self.object_pub.publish(objects_msg)
            
        except Exception as e:
            self.get_logger().error(f'Processing failed: {e}')
    
    def pointcloud2_to_numpy(self, cloud_msg):
        """Convert PointCloud2 message to numpy array."""
        points = []
        for p in cloud_msg.points:
            points.append([p.x, p.y, p.z])
        return np.array(points, dtype=np.float32)
    
    def detections_to_msg(self, detections):
        """Convert detection results to ROS2 message."""
        msg = DetectedObjects()
        for det in detections:
            obj = Object3D()
            obj.position.x = det['centroid'][0]
            obj.position.y = det['centroid'][1]
            obj.position.z = det['centroid'][2]
            obj.dimensions.x = det['bbox_size'][0]
            obj.dimensions.y = det['bbox_size'][1]
            obj.dimensions.z = det['bbox_size'][2]
            obj.classification = det['label']
            obj.confidence = det['confidence']
            msg.objects.append(obj)
        return msg

def main(args=None):
    rclpy.init(args=args)
    node = LidarPerceptionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Point Cloud Library Integration (PCL)

```cpp
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/segmentation/sac_segmentation.h>
#include <pcl/segmentation/extract_clusters.h>
#include <pcl/features/normal_3d.h>

class LidarProcessor {
public:
    using PointT = pcl::PointXYZI;
    using Cloud = pcl::PointCloud<PointT>;
    
    LidarProcessor(const LidarConfig& config) : config_(config) {
        initialize_filters();
    }
    
    void process(Cloud::Ptr input, std::vector<Object3D>& output) {
        Cloud::Ptr filtered(new Cloud);
        Cloud::Ptr ground(new Cloud);
        Cloud::Ptr non_ground(new Cloud);
        
        // Step 1: Voxel grid downsampling
        voxel_filter_.setInputCloud(input);
        voxel_filter_.filter(*filtered);
        
        // Step 2: Ground removal using RANSAC
        ground_segmentation(filtered, ground, non_ground);
        
        // Step 3: Euclidean cluster extraction
        std::vector<Cloud::Ptr> clusters;
        euclidean_clustering(non_ground, clusters);
        
        // Step 4: Extract object properties
        for (const auto& cluster : clusters) {
            Object3D obj;
            compute_bounding_box(cluster, obj);
            compute_centroid(cluster, obj);
            compute_velocity(cluster, obj);
            output.push_back(obj);
        }
    }
    
private:
    void ground_segmentation(Cloud::Ptr input, Cloud::Ptr ground, Cloud::Ptr non_ground) {
        pcl::SACSegmentation<PointT> seg;
        pcl::PointIndices::Ptr inliers(new pcl::PointIndices);
        pcl::ModelCoefficients::Ptr coefficients(new pcl::ModelCoefficients);
        
        seg.setOptimizeCoefficients(true);
        seg.setModelType(pcl::SACMODEL_PLANE);
        seg.setMethodType(pcl::SAC_RANSAC);
        seg.setDistanceThreshold(config_.ground_threshold);
        seg.setMaxIterations(config_.max_iterations);
        
        seg.setInputCloud(input);
        seg.segment(*inliers, *coefficients);
        
        // Extract ground and non-ground points
        pcl::ExtractIndices<PointT> extract;
        extract.setInputCloud(input);
        extract.setIndices(inliers);
        extract.setNegative(false);
        extract.filter(*ground);
        
        extract.setNegative(true);
        extract.filter(*non_ground);
    }
    
    void euclidean_clustering(Cloud::Ptr input, std::vector<Cloud::Ptr>& clusters) {
        pcl::search::KdTree<PointT>::Ptr tree(new pcl::search::KdTree<PointT>);
        tree->setInputCloud(input);
        
        std::vector<pcl::PointIndices> cluster_indices;
        pcl::EuclideanClusterExtraction<PointT> ec;
        ec.setClusterTolerance(config_.cluster_tolerance);
        ec.setMinClusterSize(config_.min_cluster_size);
        ec.setMaxClusterSize(config_.max_cluster_size);
        ec.setSearchMethod(tree);
        ec.setInputCloud(input);
        ec.extract(cluster_indices);
        
        for (const auto& indices : cluster_indices) {
            Cloud::Ptr cluster(new Cloud);
            for (const auto& idx : indices.indices) {
                cluster->push_back((*input)[idx]);
            }
            clusters.push_back(cluster);
        }
    }
    
    LidarConfig config_;
    pcl::VoxelGrid<PointT> voxel_filter_;
};
```

## Performance Optimization

### GPU Acceleration with CUDA

```cuda
// CUDA kernel for parallel voxel grid downsampling
__global__ void voxel_grid_kernel(
    const float4* input_points,
    float4* output_points,
    int* voxel_indices,
    float voxel_size,
    int num_points,
    int* output_count
) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= num_points) return;
    
    float4 point = input_points[idx];
    
    // Compute voxel indices
    int vx = __float2int_rd(point.x / voxel_size);
    int vy = __float2int_rd(point.y / voxel_size);
    int vz = __float2int_rd(point.z / voxel_size);
    
    // Hash voxel to unique index
    int voxel_hash = vx * 1000000 + vy * 1000 + vz;
    
    // Use atomic operation to get unique output index
    int output_idx = atomicAdd(output_count, 1);
    
    if (output_idx < MAX_POINTS) {
        output_points[output_idx] = point;
        voxel_indices[output_idx] = voxel_hash;
    }
}

// CUDA kernel for parallel DBSCAN clustering
__global__ void dbscan_kernel(
    const float4* points,
    int* labels,
    int num_points,
    float epsilon,
    int min_points
) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= num_points) return;
    
    float4 point = points[idx];
    int neighbors = 0;
    
    // Count neighbors within epsilon radius
    for (int i = 0; i < num_points; i++) {
        float4 other = points[i];
        float dist = sqrtf(
            (point.x - other.x) * (point.x - other.x) +
            (point.y - other.y) * (point.y - other.y) +
            (point.z - other.z) * (point.z - other.z)
        );
        
        if (dist <= epsilon) {
            neighbors++;
        }
    }
    
    // Label point as core, border, or noise
    if (neighbors >= min_points) {
        labels[idx] = CORE_POINT;
    } else {
        labels[idx] = NOISE;
    }
}
```

### Multi-threaded Processing Pipeline

```python
import concurrent.futures
import threading
from queue import Queue
import time

class ParallelLiDARProcessor:
    def __init__(self, num_workers=4):
        self.num_workers = num_workers
        self.input_queue = Queue(maxsize=10)
        self.output_queue = Queue(maxsize=10)
        self.running = False
        self.processors = []
    
    def start(self):
        self.running = True
        
        # Start worker threads
        for i in range(self.num_workers):
            processor = threading.Thread(
                target=self._worker_loop,
                args=(i,),
                daemon=True
            )
            processor.start()
            self.processors.append(processor)
        
        # Start output aggregator
        self.aggregator = threading.Thread(
            target=self._aggregator_loop,
            daemon=True
        )
        self.aggregator.start()
    
    def _worker_loop(self, worker_id):
        """Worker thread that processes point clouds."""
        while self.running:
            try:
                frame = self.input_queue.get(timeout=1.0)
                if frame is None:
                    break
                
                # Process the frame
                start_time = time.time()
                result = self._process_frame(frame)
                processing_time = time.time() - start_time
                
                # Add metadata
                result['worker_id'] = worker_id
                result['processing_time'] = processing_time
                result['timestamp'] = time.time()
                
                self.output_queue.put(result)
                
            except Exception as e:
                print(f"Worker {worker_id} error: {e}")
    
    def _process_frame(self, frame):
        """Process a single point cloud frame."""
        points = frame['points']
        timestamp = frame['timestamp']
        
        # Perform processing steps
        filtered = self.voxel_filter(points, voxel_size=0.1)
        ground, non_ground = self.ground_removal(filtered)
        clusters = self.clustering(non_ground)
        objects = self.extract_objects(clusters)
        
        return {
            'objects': objects,
            'point_count': len(points),
            'filtered_count': len(filtered)
        }
    
    def submit_frame(self, points, timestamp):
        """Submit a frame for processing."""
        frame = {'points': points, 'timestamp': timestamp}
        self.input_queue.put(frame)
    
    def get_results(self, timeout=1.0):
        """Get processed results."""
        try:
            return self.output_queue.get(timeout=timeout)
        except:
            return None
```

### Memory-Efficient Point Cloud Processing

```python
import numpy as np
from numba import cuda
import cupy as cp

class MemoryEfficientProcessor:
    def __init__(self, max_points=500000, voxel_size=0.1):
        self.max_points = max_points
        self.voxel_size = voxel_size
        
        # Pre-allocate GPU memory
        self.gpu_points = cp.zeros((max_points, 4), dtype=cp.float32)
        self.gpu_filtered = cp.zeros((max_points, 4), dtype=cp.float32)
        self.gpu_labels = cp.zeros(max_points, dtype=cp.int32)
    
    def process_frame(self, points):
        """Process a frame with minimal memory allocation."""
        num_points = len(points)
        
        if num_points > self.max_points:
            # Downsample before GPU transfer
            indices = np.random.choice(num_points, self.max_points, replace=False)
            points = points[indices]
            num_points = self.max_points
        
        # Transfer to GPU (zero-copy if possible)
        self.gpu_points[:num_points] = cp.asarray(points)
        
        # Process on GPU
        filtered_count = self._gpu_voxel_filter(num_points)
        ground_count = self._gpu_ground_removal(filtered_count)
        cluster_count = self._gpu_clustering(ground_count)
        
        # Transfer results back to CPU
        results = cp.asnumpy(self.gpu_labels[:cluster_count])
        
        return results
    
    @cp.fuse()
    def _gpu_voxel_filter(self, num_points):
        """GPU-accelerated voxel grid filter."""
        # Compute voxel indices
        voxel_indices = cp.floor(
            self.gpu_points[:num_points, :3] / self.voxel_size
        ).astype(cp.int32)
        
        # Create unique voxel IDs
        voxel_ids = (
            voxel_indices[:, 0] * 1000000 +
            voxel_indices[:, 1] * 1000 +
            voxel_indices[:, 2]
        )
        
        # Find unique voxels
        unique_voxels, inverse = cp.unique(voxel_ids, return_inverse=True)
        
        # For each voxel, keep the centroid
        for i, voxel in enumerate(unique_voxels):
            mask = inverse == i
            centroid = cp.mean(self.gpu_points[:num_points][mask], axis=0)
            self.gpu_filtered[i] = centroid
        
        return len(unique_voxels)
```

## Security Considerations

### LiDAR Data Security

```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hashlib
import json

class LiDARSecurityManager:
    def __init__(self, encryption_key=None):
        if encryption_key:
            self.cipher = Fernet(encryption_key)
        else:
            self.cipher = Fernet(Fernet.generate_key())
    
    def encrypt_point_cloud(self, point_cloud):
        """Encrypt point cloud data for secure transmission."""
        # Serialize to bytes
        data_bytes = point_cloud.tobytes()
        
        # Compress
        compressed = self._compress(data_bytes)
        
        # Encrypt
        encrypted = self.cipher.encrypt(compressed)
        
        return encrypted
    
    def decrypt_point_cloud(self, encrypted_data, shape):
        """Decrypt point cloud data."""
        # Decrypt
        decrypted = self.cipher.decrypt(encrypted_data)
        
        # Decompress
        decompressed = self._decompress(decrypted)
        
        # Reshape to original
        point_cloud = np.frombuffer(decompressed, dtype=np.float32).reshape(shape)
        
        return point_cloud
    
    def sign_frame(self, frame_data, private_key):
        """Sign a LiDAR frame for integrity verification."""
        import ecdsa
        
        # Hash the frame data
        frame_hash = hashlib.sha256(frame_data.tobytes()).digest()
        
        # Sign with private key
        signing_key = ecdsa.SigningKey.from_string(
            private_key, curve=ecdsa.SECP256k1
        )
        signature = signing_key.sign(frame_hash)
        
        return signature
    
    def verify_frame(self, frame_data, signature, public_key):
        """Verify frame integrity using signature."""
        import ecdsa
        
        # Hash the frame data
        frame_hash = hashlib.sha256(frame_data.tobytes()).digest()
        
        # Verify signature
        verifying_key = ecdsa.VerifyingKey.from_string(
            public_key, curve=ecdsa.SECP256k1
        )
        
        try:
            return verifying_key.verify(signature, frame_hash)
        except ecdsa.BadSignatureError:
            return False
    
    def authenticate_sensor(self, sensor_id, challenge):
        """Authenticate LiDAR sensor using challenge-response."""
        # Pre-shared key for sensor
        psk = self._get_sensor_psk(sensor_id)
        
        # Compute response
        response = hmac.new(
            psk.encode(),
            challenge.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return response
    
    def detect_spoofing(self, point_cloud, expected_pattern):
        """Detect potential LiDAR spoofing attacks."""
        # Check for regular patterns (potential spoofing)
        distances = np.linalg.norm(point_cloud[:, :3], axis=1)
        
        # Statistical analysis
        mean_dist = np.mean(distances)
        std_dist = np.std(distances)
        
        # Check for anomalies
        anomalies = np.sum(np.abs(distances - mean_dist) > 3 * std_dist)
        anomaly_ratio = anomalies / len(distances)
        
        # Check for temporal consistency
        temporal_score = self._check_temporal_consistency(point_cloud)
        
        # Check for geometric consistency
        geometric_score = self._check_geometric_consistency(point_cloud)
        
        # Combine scores
        spoofing_risk = 0.4 * anomaly_ratio + 0.3 * temporal_score + 0.3 * geometric_score
        
        return {
            'spoofing_detected': spoofing_risk > 0.7,
            'risk_score': spoofing_risk,
            'anomaly_ratio': anomaly_ratio,
            'temporal_score': temporal_score,
            'geometric_score': geometric_score
        }
    
    def _compress(self, data):
        """Compress data using LZ4."""
        import lz4.frame
        return lz4.frame.compress(data)
    
    def _decompress(self, data):
        """Decompress LZ4 compressed data."""
        import lz4.frame
        return lz4.frame.decompress(data)
    
    def _get_sensor_psk(self, sensor_id):
        """Get pre-shared key for sensor authentication."""
        # In production, retrieve from secure key management
        keys = {
            "lidar_front": "secret_key_1",
            "lidar_rear": "secret_key_2",
            "lidar_left": "secret_key_3",
            "lidar_right": "secret_key_4"
        }
        return keys.get(sensor_id, None)
    
    def _check_temporal_consistency(self, point_cloud):
        """Check temporal consistency across frames."""
        # Compare with previous frame
        if not hasattr(self, 'prev_frame'):
            self.prev_frame = point_cloud
            return 1.0
        
        # Compute frame-to-frame difference
        diff = np.abs(point_cloud - self.prev_frame)
        mean_diff = np.mean(diff)
        
        self.prev_frame = point_cloud
        
        # Lower difference means more consistent (less likely spoofing)
        return 1.0 - min(1.0, mean_diff / 10.0)
    
    def _check_geometric_consistency(self, point_cloud):
        """Check geometric consistency of point cloud."""
        # Check for expected geometric patterns
        # (e.g., road surface, building facades)
        
        # Simple check: verify points form expected shapes
        distances = np.linalg.norm(point_cloud[:, :3], axis=1)
        
        # Check if distances follow expected distribution
        # (e.g., road points should be within certain range)
        expected_range = (0.5, 50.0)
        in_range = np.sum(
            (distances >= expected_range[0]) & 
            (distances <= expected_range[1])
        )
        
        return in_range / len(distances)
```

## Troubleshooting Guide

| Symptom | Possible Cause | Diagnostic Steps | Solution |
|---------|---------------|------------------|----------|
| No point cloud data | Sensor connection issue | 1. Check USB/Ethernet connection<br>2. Verify sensor power<br>3. Check network configuration | 1. Reconnect cables<br>2. Restart sensor<br>3. Verify IP configuration |
| High latency | Processing bottleneck | 1. Profile CPU/GPU usage<br>2. Check memory allocation<br>3. Analyze pipeline timing | 1. Optimize CUDA kernels<br>2. Increase buffer size<br>3. Parallelize processing |
| Poor object detection | Calibration drift | 1. Check calibration file<br>2. Compare with reference data<br>3. Verify sensor alignment | 1. Recalibrate sensor<br>2. Update calibration parameters<br>3. Check mounting |
| Memory leaks | Resource management issue | 1. Monitor memory usage<br>2. Check for unclosed resources<br>3. Profile allocation patterns | 1. Implement RAII patterns<br>2. Use memory pools<br>3. Add cleanup routines |
| High CPU usage | Inefficient algorithms | 1. Profile code execution<br>2. Identify hot loops<br>3. Check algorithm complexity | 1. Optimize algorithms<br>2. Use GPU acceleration<br>3. Implement caching |
| Data corruption | Network/packet loss | 1. Check network statistics<br>2. Verify packet integrity<br>3. Monitor error rates | 1. Use reliable transport<br>2. Implement error correction<br>3. Add checksums |
| Sensor calibration errors | Environmental factors | 1. Check temperature conditions<br>2. Verify mounting stability<br>3. Compare with known references | 1. Recalibrate in stable environment<br>2. Add thermal compensation<br>3. Use reference targets |
| Processing queue overflow | Insufficient throughput | 1. Monitor queue depth<br>2. Check processing rate<br>3. Analyze bottleneck | 1. Increase worker threads<br>2. Optimize processing pipeline<br>3. Implement backpressure |
| Inconsistent detection | Sensor noise | 1. Analyze point cloud statistics<br>2. Check for outliers<br>3. Verify sensor specifications | 1. Apply noise filtering<br>2. Use multiple returns<br>3. Implement sensor fusion |
| High memory usage | Large point clouds | 1. Monitor memory consumption<br>2. Check point density<br>3. Analyze voxel sizes | 1. Implement voxel downsampling<br>2. Use spatial indexing<br>3. Add memory limits |

## API Reference

### PointCloudProcessor

```python
class PointCloudProcessor:
    """
    Main processor for LiDAR point cloud data.
    
    Attributes:
        config (dict): Processing configuration
        statistics (dict): Processing statistics
    
    Methods:
        process(points: np.ndarray) -> dict
            Process a single point cloud frame.
        
        process_batch(frames: list) -> list
            Process multiple point cloud frames.
        
        configure(config: dict) -> None
            Update processing configuration.
        
        get_statistics() -> dict
            Get processing statistics.
    """
    
    def __init__(self, config_path: str = None):
        """
        Initialize the PointCloudProcessor.
        
        Args:
            config_path: Path to configuration file (YAML/JSON)
        
        Raises:
            ValueError: If configuration is invalid
            FileNotFoundError: If config file not found
        """
        pass
    
    def process(self, points: np.ndarray, timestamp: float = None) -> dict:
        """
        Process a single point cloud frame.
        
        Args:
            points: Point cloud as numpy array (N x 4: x, y, z, intensity)
            timestamp: Optional timestamp for the frame
        
        Returns:
            dict with keys:
                - objects: List of detected objects
                - ground_points: Ground plane points
                - processing_time: Processing duration in seconds
                - metadata: Additional processing metadata
        
        Raises:
            ProcessingError: If processing fails
            ValidationError: If input is invalid
        """
        pass
    
    def process_batch(self, frames: list, parallel: bool = True) -> list:
        """
        Process multiple point cloud frames.
        
        Args:
            frames: List of (points, timestamp) tuples
            parallel: Whether to process in parallel
        
        Returns:
            List of processing results
        """
        pass
    
    def configure(self, config: dict) -> None:
        """
        Update processing configuration.
        
        Args:
            config: Configuration dictionary
        
        Raises:
            ValueError: If configuration is invalid
        """
        pass
    
    def get_statistics(self) -> dict:
        """
        Get processing statistics.
        
        Returns:
            dict with keys:
                - frames_processed: Number of frames processed
                - average_processing_time: Average processing time
                - peak_memory_usage: Peak memory usage in MB
                - error_count: Number of errors
        """
        pass
    
    def reset_statistics(self) -> None:
        """Reset processing statistics."""
        pass
```

### LidarSensorManager

```python
class LidarSensorManager:
    """
    Manager for multiple LiDAR sensors.
    
    Attributes:
        sensors (dict): Dictionary of connected sensors
        calibration (dict): Sensor calibration data
    
    Methods:
        connect(sensor_id: str, config: dict) -> bool
            Connect to a LiDAR sensor.
        
        disconnect(sensor_id: str) -> bool
            Disconnect from a sensor.
        
        calibrate(sensor_id: str, method: str = 'auto') -> dict
            Calibrate a sensor.
        
        get_synchronized_data(timeout: float = 1.0) -> dict
            Get synchronized data from all sensors.
    """
    
    def __init__(self):
        """Initialize the sensor manager."""
        pass
    
    def connect(self, sensor_id: str, config: dict) -> bool:
        """
        Connect to a LiDAR sensor.
        
        Args:
            sensor_id: Unique sensor identifier
            config: Sensor configuration
        
        Returns:
            True if connection successful
        
        Raises:
            ConnectionError: If connection fails
            SensorNotFoundError: If sensor not found
        """
        pass
    
    def disconnect(self, sensor_id: str) -> bool:
        """
        Disconnect from a sensor.
        
        Args:
            sensor_id: Sensor to disconnect
        
        Returns:
            True if disconnection successful
        """
        pass
    
    def calibrate(self, sensor_id: str, method: str = 'auto') -> dict:
        """
        Calibrate a sensor.
        
        Args:
            sensor_id: Sensor to calibrate
            method: Calibration method ('auto', 'manual', 'reference')
        
        Returns:
            Calibration results with transformation matrix
        
        Raises:
            CalibrationError: If calibration fails
        """
        pass
    
    def get_synchronized_data(self, timeout: float = 1.0) -> dict:
        """
        Get synchronized data from all sensors.
        
        Args:
            timeout: Maximum wait time in seconds
        
        Returns:
            dict with sensor_id as keys and point clouds as values
        
        Raises:
            TimeoutError: If synchronization times out
        """
        pass
```

## Data Models

### Point Cloud Data Structure

```python
from dataclasses import dataclass
from typing import List, Optional
import numpy as np
from enum import Enum

class PointType(Enum):
    """Point type enumeration."""
    XYZ = 0
    XYZI = 1
    XYZIR = 2  # Ring number
    XYZIRG = 3  # Gray value

@dataclass
class PointCloud:
    """Point cloud data structure."""
    points: np.ndarray  # N x (3, 4, or 5) array
    timestamp: float
    frame_id: str
    point_type: PointType
    intensity: Optional[np.ndarray] = None
    ring: Optional[np.ndarray] = None
    
    @property
    def num_points(self) -> int:
        return len(self.points)
    
    @property
    def bounds(self) -> tuple:
        """Get bounding box (min, max) for each dimension."""
        min_vals = np.min(self.points[:, :3], axis=0)
        max_vals = np.max(self.points[:, :3], axis=0)
        return (min_vals, max_vals)
    
    @property
    def centroid(self) -> np.ndarray:
        """Get centroid of point cloud."""
        return np.mean(self.points[:, :3], axis=0)
    
    def downsample(self, voxel_size: float) -> 'PointCloud':
        """Downsample using voxel grid filter."""
        # Implementation here
        pass
    
    def transform(self, matrix: np.ndarray) -> 'PointCloud':
        """Apply transformation matrix."""
        # Implementation here
        pass
    
    def crop(self, min_bound: np.ndarray, max_bound: np.ndarray) -> 'PointCloud':
        """Crop to bounding box."""
        # Implementation here
        pass

@dataclass
class Object3D:
    """3D object detection result."""
    centroid: np.ndarray  # 3D position
    dimensions: np.ndarray  # length, width, height
    orientation: float  # yaw angle in radians
    velocity: Optional[np.ndarray] = None
    classification: Optional[str] = None
    confidence: float = 0.0
    tracking_id: Optional[int] = None
    points: Optional[np.ndarray] = None  # Points belonging to object
    
    @property
    def bounding_box(self) -> np.ndarray:
        """Get 8 corners of bounding box."""
        l, w, h = self.dimensions
        corners = np.array([
            [-l/2, -w/2, -h/2],
            [l/2, -w/2, -h/2],
            [l/2, w/2, -h/2],
            [-l/2, w/2, -h/2],
            [-l/2, -w/2, h/2],
            [l/2, -w/2, h/2],
            [l/2, w/2, h/2],
            [-l/2, w/2, h/2]
        ])
        
        # Apply rotation
        rotation = np.array([
            [np.cos(self.orientation), -np.sin(self.orientation), 0],
            [np.sin(self.orientation), np.cos(self.orientation), 0],
            [0, 0, 1]
        ])
        
        corners = corners @ rotation.T + self.centroid
        return corners
    
    def iou(self, other: 'Object3D') -> float:
        """Compute IoU with another object."""
        # Implementation here
        pass

@dataclass
class GroundPlane:
    """Ground plane model."""
    normal: np.ndarray  # Plane normal vector
    distance: float  # Distance from origin
    inlier_count: int
    confidence: float
    
    def project_point(self, point: np.ndarray) -> np.ndarray:
        """Project point onto ground plane."""
        # Implementation here
        pass
    
    def distance_to_point(self, point: np.ndarray) -> float:
        """Compute signed distance from point to plane."""
        return np.dot(self.normal, point) + self.distance

@dataclass
class Trajectory:
    """Object trajectory prediction."""
    object_id: int
    positions: List[np.ndarray]  # History of positions
    timestamps: List[float]
    predicted_positions: Optional[List[np.ndarray]] = None
    prediction_horizon: float = 3.0  # seconds
    
    @property
    def velocity(self) -> np.ndarray:
        """Compute current velocity."""
        if len(self.positions) < 2:
            return np.zeros(3)
        
        dt = self.timestamps[-1] - self.timestamps[-2]
        if dt <= 0:
            return np.zeros(3)
        
        return (self.positions[-1] - self.positions[-2]) / dt
    
    @property
    def acceleration(self) -> np.ndarray:
        """Compute current acceleration."""
        if len(self.positions) < 3:
            return np.zeros(3)
        
        v1 = (self.positions[-2] - self.positions[-3]) / \
             (self.timestamps[-2] - self.timestamps[-3])
        v2 = (self.positions[-1] - self.positions[-2]) / \
             (self.timestamps[-1] - self.timestamps[-2])
        
        dt = self.timestamps[-1] - self.timestamps[-2]
        if dt <= 0:
            return np.zeros(3)
        
        return (v2 - v1) / dt
```

### Configuration Data Models

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum

class SensorType(str, Enum):
    """Supported LiDAR sensor types."""
    VELODYNE_VLP16 = "velodyne_vlp16"
    VELODYNE_VLP32 = "velodyne_vlp32"
    VELODYNE_HDL64 = "velodyne_hdl64"
    VELODYNE_VLS128 = "velodyne_vls128"
    OUST_OS1_16 = "oust_os1_16"
    OUST_OS1_32 = "oust_os1_32"
    OUST_OS1_64 = "oust_os1_64"
    LIVOX_MID_70 = "livox_mid_70"
    LIVOX_AVIA = "livox_avia"
    GENERIC = "generic"

class ProcessingMode(str, Enum):
    """Processing mode enumeration."""
    REAL_TIME = "real_time"
    OFFLINE = "offline"
    BATCH = "batch"

class ClusteringMethod(str, Enum):
    """Clustering algorithm enumeration."""
    DBSCAN = "dbscan"
    EUCLIDEAN = "euclidean"
    REGION_GROWING = "region_growing"
    RANSAC = "ransac"

class SensorConfig(BaseModel):
    """LiDAR sensor configuration."""
    sensor_type: SensorType
    channels: int = Field(..., ge=1, le=128)
    range: float = Field(..., gt=0)
    rotation_rate: float = Field(..., gt=0)
    field_of_view: Dict[str, float]
    distance_accuracy: float = Field(..., gt=0)
    return_mode: str = "single"
    calibration_file: Optional[str] = None
    
    class Config:
        use_enum = True

class ProcessingConfig(BaseModel):
    """LiDAR processing pipeline configuration."""
    frame_rate: int = Field(20, ge=1, le=100)
    processing_mode: ProcessingMode = ProcessingMode.REAL_TIME
    
    downsampling: Dict[str, any] = {
        "method": "voxel_grid",
        "leaf_size": 0.1
    }
    
    ground_removal: Dict[str, any] = {
        "enabled": True,
        "algorithm": "ransac",
        "plane_threshold": 0.15,
        "max_iterations": 1000
    }
    
    object_detection: Dict[str, any] = {
        "clustering": "dbscan",
        "min_cluster_size": 10,
        "max_cluster_size": 10000,
        "epsilon": 0.4
    }
    
    tracking: Dict[str, any] = {
        "algorithm": "kalman",
        "max_age": 3.0,
        "min_hits": 3,
        "distance_threshold": 2.0
    }
    
    class Config:
        use_enum = True

class OutputConfig(BaseModel):
    """Output configuration."""
    format: str = "pcd"
    compression: bool = True
    path: str = "/output/lidar"
    publish_ros: bool = True
    ros_topic: str = "/perception/objects"
    max_file_size_mb: int = 100

class SecurityConfig(BaseModel):
    """Security configuration."""
    encryption_enabled: bool = False
    authentication_enabled: bool = False
    spoofing_detection: bool = True
    max_frame_rate: int = 100
    anomaly_threshold: float = 0.7
```

## Deployment Guide

### Docker Deployment

```dockerfile
# Multi-stage build for LiDAR processing
FROM nvidia/cuda:11.8.0-devel-ubuntu22.04 AS builder

# Install dependencies
RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    libpcl-dev \
    libopencv-dev \
    libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

# Build application
WORKDIR /app
COPY . .
RUN mkdir build && cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release .. && \
    make -j$(nproc)

# Runtime stage
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpcl-dev \
    libopencv-dev \
    libboost-all-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy built application
COPY --from=builder /app/build /app
COPY config/ /app/config

# Set environment variables
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
ENV CUDA_VISIBLE_DEVICES=0

# Expose ports
EXPOSE 7331/udp  # LiDAR data
EXPOSE 8080      # REST API

# Run application
CMD ["/app/lidar_processor", "--config", "/app/config/default.yaml"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: lidar-processor
  namespace: autonomous-transport
  labels:
    app: lidar-processor
    tier: perception
spec:
  replicas: 3
  selector:
    matchLabels:
      app: lidar-processor
  template:
    metadata:
      labels:
        app: lidar-processor
    spec:
      containers:
      - name: lidar-processor
        image: registry.example.com/lidar-processor:latest
        resources:
          limits:
            memory: "8Gi"
            cpu: "4"
            nvidia.com/gpu: 1
          requests:
            memory: "4Gi"
            cpu: "2"
            nvidia.com/gpu: 1
        ports:
        - containerPort: 7331
          protocol: UDP
          name: lidar-data
        - containerPort: 8080
          protocol: TCP
          name: api
        volumeMounts:
        - name: config
          mountPath: /app/config
        - name: shared-memory
          mountPath: /dev/shm
        env:
        - name: CUDA_VISIBLE_DEVICES
          value: "0"
        - name: PROCESSING_MODE
          value: "real_time"
        - name: LOG_LEVEL
          value: "INFO"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: config
        configMap:
          name: lidar-processor-config
      - name: shared-memory
        emptyDir:
          medium: Memory
          sizeLimit: 2Gi
      nodeSelector:
        hardware: gpu
        nvidia.com/gpu.product: "NVIDIA-RTX-A6000"
---
apiVersion: v1
kind: Service
metadata:
  name: lidar-processor-service
  namespace: autonomous-transport
spec:
  selector:
    app: lidar-processor
  ports:
  - name: lidar-data
    port: 7331
    targetPort: 7331
    protocol: UDP
  - name: api
    port: 8080
    targetPort: 8080
  type: ClusterIP
```

### Systemd Service

```ini
# /etc/systemd/system/lidar-processor.service
[Unit]
Description=LiDAR Point Cloud Processor
After=network.target
Wants=nvidia-persistenced.service

[Service]
Type=simple
User=autonomous
Group=autonomous
WorkingDirectory=/opt/lidar-processor
ExecStart=/opt/lidar-processor/bin/lidar_processor --config /etc/lidar/config.yaml
Restart=always
RestartSec=5
LimitNOFILE=65536

# Environment
Environment=CUDA_VISIBLE_DEVICES=0
Environment=LD_LIBRARY_PATH=/usr/local/lib
Environment=ROS_DOMAIN_ID=42

# Resource limits
LimitMEMLOCK=infinity
LimitRTTIME=infinity
Nice=-20
IOSchedulingClass=realtime
IOSchedulingPriority=0

# Security hardening
ProtectSystem=strict
ProtectHome=true
NoNewPrivileges=true
ReadWritePaths=/var/lib/lidar-processor /var/log/lidar-processor

[Install]
WantedBy=multi-user.target
```

## Monitoring & Observability

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge, Summary
from prometheus_client import start_http_server
import time

class LidarMetrics:
    """Prometheus metrics for LiDAR processing."""
    
    # Counters
    frames_processed = Counter(
        'lidar_frames_processed_total',
        'Total number of frames processed',
        ['sensor_id', 'status']
    )
    
    objects_detected = Counter(
        'lidar_objects_detected_total',
        'Total number of objects detected',
        ['classification']
    )
    
    errors = Counter(
        'lidar_processing_errors_total',
        'Total number of processing errors',
        ['error_type']
    )
    
    # Histograms
    processing_latency = Histogram(
        'lidar_processing_latency_seconds',
        'LiDAR processing latency',
        ['stage'],
        buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0]
    )
    
    point_count = Histogram(
        'lidar_point_count',
        'Number of points per frame',
        buckets=[1000, 5000, 10000, 50000, 100000, 200000, 300000]
    )
    
    # Gauges
    queue_depth = Gauge(
        'lidar_queue_depth',
        'Current processing queue depth'
    )
    
    gpu_memory_usage = Gauge(
        'lidar_gpu_memory_usage_bytes',
        'GPU memory usage in bytes',
        ['device']
    )
    
    active_sensors = Gauge(
        'lidar_active_sensors',
        'Number of active LiDAR sensors'
    )
    
    # Summaries
    detection_confidence = Summary(
        'lidar_detection_confidence',
        'Object detection confidence scores',
        ['classification']
    )
    
    def __init__(self, port=9090):
        """Initialize metrics and start HTTP server."""
        start_http_server(port)
    
    def record_frame(self, sensor_id, num_points, processing_time, status='success'):
        """Record metrics for a processed frame."""
        self.frames_processed.labels(sensor_id=sensor_id, status=status).inc()
        self.point_count.observe(num_points)
        self.processing_latency.labels(stage='total').observe(processing_time)
    
    def record_detection(self, classification, confidence):
        """Record object detection metrics."""
        self.objects_detected.labels(classification=classification).inc()
        self.detection_confidence.labels(classification=classification).observe(confidence)
    
    def record_error(self, error_type):
        """Record error metrics."""
        self.errors.labels(error_type=error_type).inc()
    
    def update_gpu_usage(self, device, usage_bytes):
        """Update GPU memory usage."""
        self.gpu_memory_usage.labels(device=device).set(usage_bytes)
    
    def update_queue_depth(self, depth):
        """Update queue depth."""
        self.queue_depth.set(depth)
```

### Grafana Dashboard Configuration

```json
{
  "dashboard": {
    "title": "LiDAR Processing Dashboard",
    "panels": [
      {
        "title": "Frame Processing Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(lidar_frames_processed_total[5m])",
            "legendFormat": "{{sensor_id}}"
          }
        ]
      },
      {
        "title": "Processing Latency",
        "type": "heatmap",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(lidar_processing_latency_seconds_bucket[5m]))",
            "legendFormat": "p95"
          }
        ]
      },
      {
        "title": "Object Detection Count",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(rate(lidar_objects_detected_total[5m])) by (classification)"
          }
        ]
      },
      {
        "title": "GPU Memory Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "lidar_gpu_memory_usage_bytes / 1024 / 1024 / 1024",
            "legendFormat": "{{device}}"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(lidar_processing_errors_total[5m])",
            "legendFormat": "{{error_type}}"
          }
        ]
      },
      {
        "title": "Queue Depth",
        "type": "gauge",
        "targets": [
          {
            "expr": "lidar_queue_depth"
          }
        ]
      }
    ],
    "refresh": "5s",
    "time": {
      "from": "now-1h",
      "to": "now"
    }
  }
}
```

### Logging Configuration

```python
import logging
import logging.handlers
import json
from datetime import datetime

class StructuredFormatter(logging.Formatter):
    """Structured JSON formatter for LiDAR logs."""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add extra fields
        if hasattr(record, 'sensor_id'):
            log_entry['sensor_id'] = record.sensor_id
        
        if hasattr(record, 'frame_id'):
            log_entry['frame_id'] = record.frame_id
        
        if hasattr(record, 'processing_time'):
            log_entry['processing_time'] = record.processing_time
        
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry)

def setup_logging(log_file='/var/log/lidar-processor/lidar.log'):
    """Configure structured logging for LiDAR processor."""
    
    # Create logger
    logger = logging.getLogger('lidar')
    logger.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(StructuredFormatter())
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=100*1024*1024,  # 100MB
        backupCount=10
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(StructuredFormatter())
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger
```

## Testing Strategy

### Unit Tests

```python
import pytest
import numpy as np
from lidar_processor import PointCloudProcessor, Object3D, PointCloud

class TestPointCloudProcessor:
    """Unit tests for PointCloudProcessor."""
    
    @pytest.fixture
    def processor(self):
        """Create a processor instance for testing."""
        return PointCloudProcessor(
            config={
                'voxel_size': 0.1,
                'ground_removal': True,
                'clustering_method': 'dbscan'
            }
        )
    
    @pytest.fixture
    def sample_point_cloud(self):
        """Generate a sample point cloud."""
        num_points = 10000
        points = np.random.randn(num_points, 4).astype(np.float32)
        points[:, 3] = np.random.uniform(0, 255, num_points)  # intensity
        return points
    
    def test_initialization(self, processor):
        """Test processor initialization."""
        assert processor is not None
        assert processor.config is not None
    
    def test_process_frame(self, processor, sample_point_cloud):
        """Test frame processing."""
        result = processor.process(sample_point_cloud)
        
        assert 'objects' in result
        assert 'processing_time' in result
        assert isinstance(result['objects'], list)
    
    def test_empty_point_cloud(self, processor):
        """Test processing empty point cloud."""
        empty_cloud = np.array([]).reshape(0, 4)
        result = processor.process(empty_cloud)
        
        assert len(result['objects']) == 0
    
    def test_ground_removal(self, processor):
        """Test ground plane removal."""
        # Create point cloud with clear ground plane
        ground_points = np.array([
            [x, y, 0.0, 100] 
            for x in np.arange(-10, 10, 0.1)
            for y in np.arange(-10, 10, 0.1)
        ])
        
        # Add some non-ground points
        non_ground_points = np.array([
            [5, 5, 2.0, 200],
            [5, 5, 3.0, 200],
            [-5, -5, 2.5, 200]
        ])
        
        points = np.vstack([ground_points, non_ground_points])
        result = processor.process(points)
        
        # Should detect objects above ground
        assert len(result['objects']) > 0
    
    def test_clustering(self, processor):
        """Test object clustering."""
        # Create point cloud with distinct clusters
        cluster1 = np.random.randn(100, 4).astype(np.float32)
        cluster1[:, :3] += np.array([10, 10, 1])
        
        cluster2 = np.random.randn(100, 4).astype(np.float32)
        cluster2[:, :3] += np.array([-10, -10, 1])
        
        points = np.vstack([cluster1, cluster2])
        result = processor.process(points)
        
        # Should detect at least 2 objects
        assert len(result['objects']) >= 2
    
    def test_performance(self, processor, sample_point_cloud):
        """Test processing performance."""
        import time
        
        start_time = time.time()
        for _ in range(10):
            processor.process(sample_point_cloud)
        total_time = time.time() - start_time
        
        avg_time = total_time / 10
        
        # Should process at least 10 Hz
        assert avg_time < 0.1

class TestObject3D:
    """Unit tests for Object3D data model."""
    
    def test_bounding_box(self):
        """Test bounding box calculation."""
        obj = Object3D(
            centroid=np.array([0, 0, 0]),
            dimensions=np.array([2, 1, 1.5]),
            orientation=0.0,
            confidence=0.9
        )
        
        bbox = obj.bounding_box
        assert bbox.shape == (8, 3)
    
    def test_iou(self):
        """Test IoU calculation."""
        obj1 = Object3D(
            centroid=np.array([0, 0, 0]),
            dimensions=np.array([2, 1, 1.5]),
            orientation=0.0,
            confidence=0.9
        )
        
        obj2 = Object3D(
            centroid=np.array([0.5, 0, 0]),
            dimensions=np.array([2, 1, 1.5]),
            orientation=0.0,
            confidence=0.85
        )
        
        iou = obj1.iou(obj2)
        assert 0 < iou < 1

class TestPointCloud:
    """Unit tests for PointCloud data model."""
    
    def test_bounds(self):
        """Test bounding box calculation."""
        points = np.array([
            [0, 0, 0, 100],
            [1, 1, 1, 150],
            [2, 2, 2, 200]
        ])
        
        cloud = PointCloud(
            points=points,
            timestamp=0.0,
            frame_id='test',
            point_type=0
        )
        
        min_vals, max_vals = cloud.bounds
        np.testing.assert_array_equal(min_vals, [0, 0, 0])
        np.testing.assert_array_equal(max_vals, [2, 2, 2])
    
    def test_centroid(self):
        """Test centroid calculation."""
        points = np.array([
            [1, 0, 0, 100],
            [0, 1, 0, 150],
            [0, 0, 1, 200]
        ])
        
        cloud = PointCloud(
            points=points,
            timestamp=0.0,
            frame_id='test',
            point_type=0
        )
        
        centroid = cloud.centroid
        np.testing.assert_array_almost_equal(centroid, [1/3, 1/3, 1/3])
```

### Integration Tests

```python
import pytest
import asyncio
from lidar_processor import LidarSystem, SensorManager

class TestLidarIntegration:
    """Integration tests for complete LiDAR system."""
    
    @pytest.fixture
    def system(self):
        """Create a complete LiDAR system for testing."""
        return LidarSystem(
            config={
                'sensors': ['sensor_1'],
                'processing': {
                    'frame_rate': 10,
                    'mode': 'test'
                }
            }
        )
    
    @pytest.mark.asyncio
    async def test_end_to_end_processing(self, system):
        """Test complete processing pipeline."""
        # Generate test data
        test_data = np.random.randn(50000, 4).astype(np.float32)
        
        # Process through system
        result = await system.process_frame(test_data, timestamp=0.0)
        
        # Verify result structure
        assert 'objects' in result
        assert 'metadata' in result
        assert 'timestamp' in result
    
    @pytest.mark.asyncio
    async def test_multi_sensor_fusion(self):
        """Test fusion of multiple sensor inputs."""
        system = LidarSystem(
            config={
                'sensors': ['sensor_front', 'sensor_rear'],
                'fusion': {
                    'method': 'weighted_average',
                    'weights': [0.6, 0.4]
                }
            }
        )
        
        # Simulate data from two sensors
        front_data = np.random.randn(30000, 4).astype(np.float32)
        rear_data = np.random.randn(30000, 4).astype(np.float32)
        
        # Process both
        front_result = await system.process_frame(front_data, sensor_id='sensor_front')
        rear_result = await system.process_frame(rear_data, sensor_id='sensor_rear')
        
        # Fuse results
        fused = await system.fuse_results()
        
        assert 'objects' in fused
        assert len(fused['objects']) > 0
    
    @pytest.mark.asyncio
    async def test_real_time_performance(self, system):
        """Test real-time processing capability."""
        import time
        
        # Process 100 frames
        frame_times = []
        for i in range(100):
            test_data = np.random.randn(50000, 4).astype(np.float32)
            
            start = time.time()
            await system.process_frame(test_data, timestamp=i * 0.05)
            frame_times.append(time.time() - start)
        
        # Verify real-time performance (10 Hz = 100ms per frame)
        avg_time = np.mean(frame_times)
        p95_time = np.percentile(frame_times, 95)
        
        assert avg_time < 0.1  # 100ms
        assert p95_time < 0.15  # 150ms

class TestSensorManager:
    """Integration tests for sensor management."""
    
    @pytest.mark.asyncio
    async def test_sensor_discovery(self):
        """Test automatic sensor discovery."""
        manager = SensorManager()
        
        # Discover sensors
        sensors = await manager.discover_sensors()
        
        assert len(sensors) > 0
        assert all(hasattr(s, 'sensor_id') for s in sensors)
    
    @pytest.mark.asyncio
    async def test_sensor_calibration(self):
        """Test sensor calibration workflow."""
        manager = SensorManager()
        
        # Connect to sensor
        sensor = await manager.connect('sensor_1')
        
        # Calibrate
        calibration_result = await sensor.calibrate(method='auto')
        
        assert calibration_result['success'] is True
        assert 'transformation_matrix' in calibration_result
    
    @pytest.mark.asyncio
    async def test_sensor_health_monitoring(self):
        """Test sensor health monitoring."""
        manager = SensorManager()
        
        # Connect sensors
        await manager.connect('sensor_1')
        await manager.connect('sensor_2')
        
        # Get health status
        health = await manager.get_health_status()
        
        assert 'sensor_1' in health
        assert 'sensor_2' in health
        assert health['sensor_1']['status'] == 'healthy'
```

### Load Testing

```python
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from lidar_processor import PointCloudProcessor, LoadTester

class LiDARLoadTester:
    """Load testing for LiDAR processing system."""
    
    def __init__(self, config):
        self.config = config
        self.processor = PointCloudProcessor(config)
        self.results = []
    
    async def run_load_test(self, num_frames=1000, concurrent=10):
        """Run load test with specified parameters."""
        print(f"Starting load test: {num_frames} frames, {concurrent} concurrent")
        
        start_time = time.time()
        
        # Create tasks
        tasks = []
        for i in range(num_frames):
            task = self._process_frame(i)
            tasks.append(task)
        
        # Run with concurrency limit
        semaphore = asyncio.Semaphore(concurrent)
        
        async def bounded_task(task):
            async with semaphore:
                return await task
        
        results = await asyncio.gather(
            *[bounded_task(task) for task in tasks],
            return_exceptions=True
        )
        
        total_time = time.time() - start_time
        
        # Analyze results
        successful = [r for r in results if not isinstance(r, Exception)]
        failed = [r for r in results if isinstance(r, Exception)]
        
        return {
            'total_frames': num_frames,
            'successful': len(successful),
            'failed': len(failed),
            'total_time': total_time,
            'frames_per_second': num_frames / total_time,
            'average_latency': np.mean([r['processing_time'] for r in successful]),
            'p95_latency': np.percentile([r['processing_time'] for r in successful], 95),
            'p99_latency': np.percentile([r['processing_time'] for r in successful], 99),
            'errors': [str(e) for e in failed]
        }
    
    async def _process_frame(self, frame_id):
        """Process a single frame for load testing."""
        # Generate test data
        points = np.random.randn(50000, 4).astype(np.float32)
        
        # Process
        start = time.time()
        result = self.processor.process(points, timestamp=frame_id * 0.05)
        processing_time = time.time() - start
        
        result['processing_time'] = processing_time
        result['frame_id'] = frame_id
        
        return result
    
    def run_memory_leak_test(self, iterations=1000):
        """Test for memory leaks."""
        import tracemalloc
        
        tracemalloc.start()
        
        initial_memory = tracemalloc.get_traced_memory()[0]
        
        for i in range(iterations):
            points = np.random.randn(50000, 4).astype(np.float32)
            self.processor.process(points, timestamp=i * 0.05)
        
        final_memory = tracemalloc.get_traced_memory()[0]
        
        tracemalloc.stop()
        
        memory_growth = final_memory - initial_memory
        memory_growth_percent = (memory_growth / initial_memory) * 100
        
        return {
            'iterations': iterations,
            'initial_memory_mb': initial_memory / 1024 / 1024,
            'final_memory_mb': final_memory / 1024 / 1024,
            'memory_growth_mb': memory_growth / 1024 / 1024,
            'memory_growth_percent': memory_growth_percent,
            'leak_detected': memory_growth_percent > 10  # 10% threshold
        }
```

## Versioning & Migration

### Semantic Versioning

```yaml
# versioning.yaml
versioning:
  scheme: "semver"
  current_version: "1.0.0"
  
  version_history:
    - version: "1.0.0"
      date: "2024-01-15"
      changes:
        - "Initial release"
        - "Support for Velodyne VLP-16, VLP-32, HDL-64"
        - "Real-time processing pipeline"
        - "DBSCAN clustering"
    
    - version: "1.1.0"
      date: "2024-03-20"
      changes:
        - "Added support for OUST OS1 sensors"
        - "GPU acceleration with CUDA"
        - "Multi-sensor fusion"
        - "Performance improvements (2x faster)"
    
    - version: "1.2.0"
      date: "2024-06-10"
      changes:
        - "Added Livox sensor support"
        - "ROS2 integration"
        - "Enhanced security features"
        - "Spoofing detection"
    
    - version: "2.0.0"
      date: "2024-09-01"
      changes:
        - "Breaking API changes"
        - "New configuration format"
        - "Improved object tracking"
        - "3D bounding box estimation"
        - "Trajectory prediction"

  migration_notes:
    v1_to_v2:
      - "Update configuration file format"
      - "Replace deprecated methods"
      - "Update ROS message definitions"
      - "Recalibrate sensors"
```

### Migration Scripts

```python
#!/usr/bin/env python3
"""Migration script for LiDAR processor configuration."""

import yaml
import json
import sys
from pathlib import Path

def migrate_v1_to_v2(config_path):
    """Migrate configuration from v1 to v2 format."""
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Check if already v2
    if config.get('version') == '2.0.0':
        print("Configuration is already v2.0.0")
        return config
    
    # Migrate
    new_config = {
        'version': '2.0.0',
        'sensors': {},
        'processing': {},
        'output': {},
        'security': {}
    }
    
    # Migrate sensor configuration
    if 'sensor_type' in config:
        sensor_id = 'default_sensor'
        new_config['sensors'][sensor_id] = {
            'type': config['sensor_type'],
            'channels': config.get('channels', 16),
            'range': config.get('range', 100),
            'calibration': config.get('calibration_file', None)
        }
    
    # Migrate processing configuration
    if 'processing' in config:
        new_config['processing'] = {
            'frame_rate': config['processing'].get('frame_rate', 20),
            'mode': config['processing'].get('mode', 'real_time'),
            'downsampling': config['processing'].get('downsampling', {
                'method': 'voxel_grid',
                'leaf_size': 0.1
            }),
            'ground_removal': config['processing'].get('ground_removal', {
                'enabled': True,
                'algorithm': 'ransac'
            }),
            'clustering': config['processing'].get('clustering', {
                'method': 'dbscan',
                'epsilon': 0.4
            })
        }
    
    # Migrate output configuration
    if 'output' in config:
        new_config['output'] = {
            'format': config['output'].get('format', 'pcd'),
            'path': config['output'].get('path', '/output'),
            'ros': config['output'].get('publish_ros', True)
        }
    
    # Add new v2 fields
    new_config['security'] = {
        'encryption_enabled': False,
        'authentication_enabled': False,
        'spoofing_detection': True
    }
    
    # Save migrated configuration
    output_path = Path(config_path).with_suffix('.v2.yaml')
    with open(output_path, 'w') as f:
        yaml.dump(new_config, f, default_flow_style=False)
    
    print(f"Migrated configuration saved to: {output_path}")
    
    return new_config

def validate_config(config, version='2.0.0'):
    """Validate configuration against schema."""
    
    required_fields = {
        '2.0.0': ['version', 'sensors', 'processing', 'output']
    }
    
    fields = required_fields.get(version, [])
    
    missing = [f for f in fields if f not in config]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")
    
    # Validate sensor types
    valid_sensor_types = [
        'velodyne_vlp16', 'velodyne_vlp32', 'velodyne_hdl64',
        'oust_os1_16', 'oust_os1_32', 'oust_os1_64',
        'livox_mid_70', 'livox_avia', 'generic'
    ]
    
    for sensor_id, sensor_config in config.get('sensors', {}).items():
        if sensor_config.get('type') not in valid_sensor_types:
            raise ValueError(f"Invalid sensor type: {sensor_config.get('type')}")
    
    # Validate processing settings
    processing = config.get('processing', {})
    if 'frame_rate' in processing:
        if not 1 <= processing['frame_rate'] <= 100:
            raise ValueError("Frame rate must be between 1 and 100")
    
    return True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: migrate.py <config_path>")
        sys.exit(1)
    
    config_path = sys.argv[1]
    migrated_config = migrate_v1_to_v2(config_path)
    
    if validate_config(migrated_config):
        print("Migration and validation successful!")
    else:
        print("Migration failed validation!")
        sys.exit(1)
```

## Glossary

| Term | Definition |
|------|------------|
| **LiDAR** | Light Detection and Ranging - a remote sensing method using pulsed laser light |
| **Point Cloud** | A set of data points in 3D space, typically representing the external surface of objects |
| **Voxel** | A 3D pixel, used for spatial partitioning of point clouds |
| **DBSCAN** | Density-Based Spatial Clustering of Applications with Noise - a clustering algorithm |
| **RANSAC** | Random Sample Consensus - an iterative method for fitting models to data with outliers |
| **Euclidean Clustering** | Grouping points based on spatial proximity using Euclidean distance |
| **Ground Segmentation** | The process of separating ground plane points from non-ground objects |
| **Object Detection** | Identifying and classifying objects within point cloud data |
| **Tracking** | Following objects across multiple frames to maintain identity |
| **Kalman Filter** | An algorithm for estimating system state from noisy measurements |
| **Bounding Box** | The smallest rectangular prism enclosing an object |
| **Centroid** | The geometric center of a point cluster |
| **Intensity** | The strength of the laser return signal |
| **Ring** | The channel number for multi-return LiDAR sensors |
| **Frame** | A single scan or sweep from the LiDAR sensor |
| **Frame Rate** | The number of complete scans per second (Hz) |
| **FOV** | Field of View - the angular extent of the observable area |
| **Resolution** | The minimum distance between distinguishable points |
| **Calibration** | The process of aligning sensor data with vehicle coordinates |
| **Transformation Matrix** | A 4x4 matrix representing rotation and translation |
| **ROS** | Robot Operating System - middleware for robotics applications |
| **PCL** | Point Cloud Library - an open-source library for point cloud processing |
| **CUDA** | Compute Unified Device Architecture - NVIDIA's parallel computing platform |
| **GPU** | Graphics Processing Unit - hardware for parallel computation |
| **FPGA** | Field-Programmable Gate Array - reconfigurable hardware for acceleration |
| **Zero-copy** | Data transfer without intermediate copying |
| **Backpressure** | Mechanism to slow down data producers when consumers can't keep up |
| **Latency** | Time delay between data acquisition and processing completion |
| **Throughput** | Amount of data processed per unit time |
| **Spoofing** | Malicious injection of false LiDAR data |
| **Fusion** | Combining data from multiple sensors for improved accuracy |

## Changelog

### v2.0.0 (2024-09-01)
- Breaking API changes for improved consistency
- New YAML-based configuration format
- Enhanced object tracking with trajectory prediction
- 3D bounding box estimation
- Multi-sensor fusion improvements
- Security features and spoofing detection

### v1.2.0 (2024-06-10)
- Added Livox Mid-70 and Avia sensor support
- ROS2 integration
- Enhanced security features
- Improved error handling and logging

### v1.1.0 (2024-03-20)
- Added OUST OS1 sensor support
- GPU acceleration with CUDA kernels
- Multi-sensor fusion capability
- Performance improvements (2x faster processing)
- Memory optimization

### v1.0.0 (2024-01-15)
- Initial release
- Support for Velodyne VLP-16, VLP-32, HDL-64
- Real-time processing pipeline
- DBSCAN clustering
- Ground removal with RANSAC
- Basic object detection

### v0.9.0 (2023-11-01)
- Beta release
- Core point cloud processing
- Basic filtering and downsampling
- Unit and integration tests

### v0.8.0 (2023-09-15)
- Alpha release
- Proof of concept implementation
- Basic sensor connectivity
- Initial documentation

## Contributing Guidelines

### Development Setup

```bash
# Clone the repository
git clone https://github.com/example/lidar-processor.git
cd lidar-processor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/

# Run linting
flake8 src/
mypy src/

# Run formatting
black src/
isort src/
```

### Code Style

- Follow PEP 8 for Python code
- Use type hints for all function signatures
- Write docstrings for public functions and classes
- Keep functions under 50 lines
- Keep files under 500 lines
- Use meaningful variable names

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Testing Requirements

- All new code must have unit tests
- Maintain minimum 80% code coverage
- All tests must pass before merging
- Include integration tests for new features
- Performance tests for critical paths

### Documentation

- Update README.md for new features
- Add API documentation for new endpoints
- Include usage examples
- Update configuration documentation

## License

MIT License

Copyright (c) 2024 LiDAR Processing Team

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