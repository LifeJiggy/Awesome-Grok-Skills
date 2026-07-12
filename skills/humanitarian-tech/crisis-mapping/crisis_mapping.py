"""
Crisis Mapping Module
Part of the humanitarian-tech skill domain

Comprehensive crisis mapping system combining satellite imagery analysis,
crowd-sourced mapping, and situation reporting.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import json
import math
import random
import uuid


# =============================================================================
# Enums
# =============================================================================

class ImageryType(Enum):
    """Types of satellite imagery."""
    OPTICAL = "optical"
    SAR = "sar"
    THERMAL = "thermal"
    MULTISPECTRAL = "multispectral"
    HYPERSPECTRAL = "hyperspectral"
    LIDAR = "lidar"


class DamageClassification(Enum):
    """Building damage classification levels."""
    NO_DAMAGE = "no_damage"
    POSSIBLE_DAMAGE = "possible_damage"
    MODERATE_DAMAGE = "moderate_damage"
    SEVERE_DAMAGE = "severe_damage"
    DESTROYED = "destroyed"
    UNKNOWN = "unknown"


class IncidentCategory(Enum):
    """Crowd-sourced incident categories."""
    INFRASTRUCTURE_DAMAGE = "infrastructure_damage"
    DISPLACEMENT = "displacement"
    HUMANITARIAN_NEED = "humanitarian_need"
    ACCESSIBILITY = "accessibility"
    SECURITY_INCIDENT = "security_incident"
    HEALTH_EMERGENCY = "health_emergency"
    ENVIRONMENTAL_HAZARD = "environmental_hazard"
    SERVICE_DISRUPTION = "service_disruption"


class IncidentStatus(Enum):
    """Status of crowd-sourced incidents."""
    REPORTED = "reported"
    VERIFIED = "verified"
    VALIDATED = "validated"
    RESOLVED = "resolved"
    FALSE_REPORT = "false_report"
    DUPLICATE = "duplicate"


class ValidationLevel(Enum):
    """Data validation levels for crowd-sourced data."""
    UNVERIFIED = "unverified"
    SINGLE_SOURCE = "single_source"
    MULTI_SOURCE = "multi_source"
    GROUND_TRUTH = "ground_truth"
    OFFICIAL = "official"


class ReportType(Enum):
    """Types of situation reports."""
    SITREP = "sitrep"
    DAMAGE_ASSESSMENT = "damage_assessment"
    NEEDS_ASSESSMENT = "needs_assessment"
    MAPPING_UPDATE = "mapping_update"
    FLASH_REPORT = "flash_report"
    WEEKLY_SUMMARY = "weekly_summary"


class MapLayerType(Enum):
    """Types of map layers."""
    VECTOR_POINT = "vector_point"
    VECTOR_LINE = "vector_line"
    VECTOR_POLYGON = "vector_polygon"
    RASTER = "raster"
    HEATMAP = "heatmap"
    CLUSTER = "cluster"


class SatelliteSource(Enum):
    """Satellite imagery providers."""
    SENTINEL_2 = "sentinel_2"
    SENTINEL_1 = "sentinel_1"
    LANDSAT_8 = "landsat_8"
    LANDSAT_9 = "landsat_9"
    MAXAR = "maxar"
    PLANET = "planet"
    AIRBUS = "airbus"
    SPOT = "spot"


# =============================================================================
# Dataclasses
# =============================================================================

@dataclass
class GeoCoordinate:
    """Geographic coordinate."""
    longitude: float
    latitude: float
    altitude: float = 0.0

    def to_dict(self) -> Dict[str, float]:
        return {"longitude": self.longitude, "latitude": self.latitude, "altitude": self.altitude}

    def distance_to(self, other: 'GeoCoordinate') -> float:
        """Calculate distance in meters using Haversine formula."""
        R = 6371000  # Earth's radius in meters
        lat1, lat2 = math.radians(self.latitude), math.radians(other.latitude)
        dlat = math.radians(other.latitude - self.latitude)
        dlon = math.radians(other.longitude - self.longitude)
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


@dataclass
class BoundingBox:
    """Geographic bounding box."""
    min_lon: float
    min_lat: float
    max_lon: float
    max_lat: float

    @property
    def center(self) -> GeoCoordinate:
        return GeoCoordinate(
            longitude=(self.min_lon + self.max_lon) / 2,
            latitude=(self.min_lat + self.max_lat) / 2
        )

    @property
    def width_km(self) -> float:
        center_lat = (self.min_lat + self.max_lat) / 2
        return abs(self.max_lon - self.min_lon) * 111.32 * math.cos(math.radians(center_lat))

    @property
    def height_km(self) -> float:
        return abs(self.max_lat - self.min_lat) * 111.32

    def contains(self, coord: GeoCoordinate) -> bool:
        return (self.min_lon <= coord.longitude <= self.max_lon and
                self.min_lat <= coord.latitude <= self.max_lat)

    def to_dict(self) -> Dict[str, float]:
        return {"min_lon": self.min_lon, "min_lat": self.min_lat,
                "max_lon": self.max_lon, "max_lat": self.max_lat}


@dataclass
class SatelliteScene:
    """Satellite imagery scene metadata."""
    scene_id: str
    source: SatelliteSource
    acquisition_date: datetime
    cloud_cover_percent: float
    bounding_box: BoundingBox
    bands: List[str] = field(default_factory=list)
    resolution_meters: float = 10.0
    processing_level: str = "L1C"
    file_size_mb: float = 0.0
    is_processed: bool = False

    def quality_score(self) -> float:
        """Calculate scene quality score based on cloud cover and resolution."""
        cloud_score = max(0, 1 - self.cloud_cover_percent / 100)
        resolution_score = max(0, 1 - self.resolution_meters / 30)
        return (cloud_score * 0.7 + resolution_score * 0.3)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scene_id": self.scene_id,
            "source": self.source.value,
            "acquisition_date": self.acquisition_date.isoformat(),
            "cloud_cover_percent": self.cloud_cover_percent,
            "bounding_box": self.bounding_box.to_dict(),
            "resolution_meters": self.resolution_meters,
            "quality_score": self.quality_score(),
            "is_processed": self.is_processed
        }


@dataclass
class DamageAssessmentResult:
    """Result of satellite-based damage assessment."""
    assessment_id: str
    scene_before: str
    scene_after: str
    area_of_interest: BoundingBox
    total_buildings: int = 0
    damage_summary: Dict[DamageClassification, int] = field(default_factory=dict)
    confidence_score: float = 0.0
    assessment_date: datetime = field(default_factory=datetime.now)
    method: str = "change_detection"
    notes: str = ""

    @property
    def damage_percentage(self) -> float:
        if self.total_buildings == 0:
            return 0.0
        damaged = sum(v for k, v in self.damage_summary.items()
                      if k in (DamageClassification.MODERATE_DAMAGE, DamageClassification.SEVERE_DAMAGE, DamageClassification.DESTROYED))
        return (damaged / self.total_buildings) * 100

    def to_dict(self) -> Dict[str, Any]:
        return {
            "assessment_id": self.assessment_id,
            "scene_before": self.scene_before,
            "scene_after": self.scene_after,
            "area_of_interest": self.area_of_interest.to_dict(),
            "total_buildings": self.total_buildings,
            "damage_summary": {k.value: v for k, v in self.damage_summary.items()},
            "damage_percentage": self.damage_percentage,
            "confidence_score": self.confidence_score,
            "assessment_date": self.assessment_date.isoformat()
        }


@dataclass
class Incident:
    """Crowd-sourced incident report."""
    incident_id: str
    category: IncidentCategory
    location: GeoCoordinate
    title: str
    description: str
    reported_at: datetime
    reporter_id: str = "anonymous"
    status: IncidentStatus = IncidentStatus.REPORTED
    validation_level: ValidationLevel = ValidationLevel.UNVERIFIED
    upvotes: int = 0
    downvotes: int = 0
    media_urls: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    affected_population: int = 0
    priority_score: float = 0.0

    def credibility_score(self) -> float:
        """Calculate credibility based on votes and validation."""
        total_votes = self.upvotes + self.downvotes
        if total_votes == 0:
            base = 0.5
        else:
            base = self.upvotes / total_votes

        validation_bonus = {
            ValidationLevel.UNVERIFIED: 0.0,
            ValidationLevel.SINGLE_SOURCE: 0.1,
            ValidationLevel.MULTI_SOURCE: 0.2,
            ValidationLevel.GROUND_TRUTH: 0.3,
            ValidationLevel.OFFICIAL: 0.4
        }.get(self.validation_level, 0.0)

        return min(base + validation_bonus, 1.0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "incident_id": self.incident_id,
            "category": self.category.value,
            "location": self.location.to_dict(),
            "title": self.title,
            "description": self.description,
            "reported_at": self.reported_at.isoformat(),
            "status": self.status.value,
            "validation_level": self.validation_level.value,
            "credibility_score": self.credibility_score(),
            "upvotes": self.upvotes,
            "downvotes": self.downvotes,
            "affected_population": self.affected_population
        }


@dataclass
class MapLayer:
    """Geographic map layer."""
    layer_id: str
    name: str
    layer_type: MapLayerType
    data: List[Dict[str, Any]]
    source: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    is_visible: bool = True
    opacity: float = 1.0
    min_zoom: int = 0
    max_zoom: int = 18
    style: Dict[str, Any] = field(default_factory=dict)

    def feature_count(self) -> int:
        return len(self.data)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "layer_id": self.layer_id,
            "name": self.name,
            "layer_type": self.layer_type.value,
            "feature_count": self.feature_count(),
            "source": self.source,
            "is_visible": self.is_visible,
            "opacity": self.opacity,
            "style": self.style
        }


@dataclass
class SituationReport:
    """Crisis situation report."""
    report_id: str
    report_type: ReportType
    title: str
    event_id: str
    prepared_by: str
    prepared_at: datetime
    valid_from: datetime
    valid_until: Optional[datetime] = None
    affected_area: Optional[BoundingBox] = None
    summary: str = ""
    key_findings: List[str] = field(default_factory=list)
    data_sources: List[str] = field(default_factory=list)
    maps_included: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    contact_info: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "report_type": self.report_type.value,
            "title": self.title,
            "event_id": self.event_id,
            "prepared_by": self.prepared_by,
            "prepared_at": self.prepared_at.isoformat(),
            "valid_from": self.valid_from.isoformat(),
            "valid_until": self.valid_until.isoformat() if self.valid_until else None,
            "summary": self.summary,
            "key_findings": self.key_findings,
            "data_sources": self.data_sources,
            "recommendations": self.recommendations
        }


@dataclass
class MappingTask:
    """Task for volunteer mappers."""
    task_id: str
    title: str
    description: str
    area_of_interest: BoundingBox
    priority: int  # 1-5, 5 highest
    status: str = "open"
    created_at: datetime = field(default_factory=datetime.now)
    assigned_to: Optional[str] = None
    completed_at: Optional[datetime] = None
    estimated_duration_minutes: int = 30
    required_skills: List[str] = field(default_factory=list)
    validation_required: bool = True

    def is_overdue(self) -> bool:
        if self.status != "in_progress" or not self.assigned_to:
            return False
        expected_end = self.created_at + timedelta(minutes=self.estimated_duration_minutes * 2)
        return datetime.now() > expected_end

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "area_of_interest": self.area_of_interest.to_dict(),
            "priority": self.priority,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "estimated_duration_minutes": self.estimated_duration_minutes,
            "is_overdue": self.is_overdue()
        }


# =============================================================================
# Core Systems
# =============================================================================

class SatelliteAnalyzer:
    """Satellite imagery analysis and change detection system."""

    def __init__(self, data_source: str = "sentinel_hub", api_key: str = ""):
        self.data_source = data_source
        self.api_key = api_key
        self.scenes: Dict[str, SatelliteScene] = {}
        self.assessments: List[DamageAssessmentResult] = []
        self.processing_queue: List[str] = []

    def ingest_scene(self, source: SatelliteSource, acquisition_date: datetime,
                     cloud_cover: float, bounding_box: BoundingBox,
                     **kwargs) -> SatelliteScene:
        """Ingest a new satellite scene."""
        scene_id = f"SCN-{uuid.uuid4().hex[:10].upper()}"
        scene = SatelliteScene(
            scene_id=scene_id,
            source=source,
            acquisition_date=acquisition_date,
            cloud_cover_percent=cloud_cover,
            bounding_box=bounding_box,
            bands=kwargs.get("bands", ["B02", "B03", "B04", "B08"]),
            resolution_meters=kwargs.get("resolution", 10.0),
            processing_level=kwargs.get("processing_level", "L1C"),
            file_size_mb=kwargs.get("file_size_mb", 0.0)
        )
        self.scenes[scene_id] = scene
        return scene

    def detect_changes(self, scene_before_id: str, scene_after_id: str,
                       area_of_interest: BoundingBox) -> DamageAssessmentResult:
        """Perform change detection between two scenes."""
        scene_before = self.scenes.get(scene_before_id)
        scene_after = self.scenes.get(scene_after_id)

        if not scene_before or not scene_after:
            raise ValueError("Scene not found")

        # Simulate damage assessment
        total_buildings = random.randint(500, 2000)
        damage_summary = {
            DamageClassification.NO_DAMAGE: int(total_buildings * 0.6),
            DamageClassification.POSSIBLE_DAMAGE: int(total_buildings * 0.15),
            DamageClassification.MODERATE_DAMAGE: int(total_buildings * 0.12),
            DamageClassification.SEVERE_DAMAGE: int(total_buildings * 0.08),
            DamageClassification.DESTROYED: int(total_buildings * 0.05),
        }

        assessment = DamageAssessmentResult(
            assessment_id=f"DAM-{uuid.uuid4().hex[:8].upper()}",
            scene_before=scene_before_id,
            scene_after=scene_after_id,
            area_of_interest=area_of_interest,
            total_buildings=total_buildings,
            damage_summary=damage_summary,
            confidence_score=random.uniform(0.75, 0.95),
            method="change_detection"
        )

        self.assessments.append(assessment)
        return assessment

    def extract_building_footprints(self, scene_id: str,
                                    area: BoundingBox) -> List[Dict[str, Any]]:
        """Extract building footprints from satellite imagery."""
        scene = self.scenes.get(scene_id)
        if not scene:
            return []

        # Simulate building footprint extraction
        buildings = []
        num_buildings = random.randint(50, 200)
        for i in range(num_buildings):
            buildings.append({
                "building_id": f"BLD-{uuid.uuid4().hex[:8].upper()}",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [area.min_lon + random.uniform(0, area.max_lon - area.min_lon),
                         area.min_lat + random.uniform(0, area.max_lat - area.min_lat)]
                        for _ in range(5)
                    ]]
                },
                "area_sqm": random.uniform(50, 500),
                "classification": random.choice(["residential", "commercial", "industrial", "public"]),
                "confidence": random.uniform(0.7, 0.99)
            })
        return buildings

    def analyze_flood_extent(self, scene_id: str,
                             water_threshold: float = 0.3) -> Dict[str, Any]:
        """Analyze flood extent from SAR or optical imagery."""
        scene = self.scenes.get(scene_id)
        if not scene:
            return {"error": "Scene not found"}

        # Simulate flood analysis
        flooded_area_km2 = random.uniform(10, 500)
        return {
            "scene_id": scene_id,
            "water_threshold": water_threshold,
            "flooded_area_km2": flooded_area_km2,
            "affected_buildings": random.randint(100, 2000),
            "affected_population_estimate": random.randint(1000, 20000),
            "confidence_score": random.uniform(0.8, 0.95),
            "analysis_date": datetime.now().isoformat()
        }

    def get_scene_statistics(self) -> Dict[str, Any]:
        """Get statistics on available satellite scenes."""
        by_source = {}
        for scene in self.scenes.values():
            source = scene.source.value
            if source not in by_source:
                by_source[source] = {"count": 0, "avg_cloud_cover": 0, "total_area_km2": 0}
            by_source[source]["count"] += 1
            by_source[source]["avg_cloud_cover"] += scene.cloud_cover_percent
            by_source[source]["total_area_km2"] += scene.bounding_box.width_km * scene.bounding_box.height_km

        for source in by_source:
            if by_source[source]["count"] > 0:
                by_source[source]["avg_cloud_cover"] /= by_source[source]["count"]

        return {
            "total_scenes": len(self.scenes),
            "by_source": by_source,
            "total_assessments": len(self.assessments),
            "processing_queue": len(self.processing_queue)
        }


class CrowdSourcedMapper:
    """Crowd-sourced crisis mapping and incident management."""

    def __init__(self, platform: str = "ushahidi"):
        self.platform = platform
        self.incidents: Dict[str, Incident] = {}
        self.categories: Dict[IncidentCategory, int] = {cat: 0 for cat in IncidentCategory}
        self.volunteers: Dict[str, Dict[str, Any]] = {}
        self.tasks: Dict[str, MappingTask] = {}
        self.validation_log: List[Dict[str, Any]] = []

    def report_incident(self, category: IncidentCategory, location: GeoCoordinate,
                        title: str, description: str, reporter_id: str = "anonymous",
                        **kwargs) -> Incident:
        """Report a new crowd-sourced incident."""
        incident_id = f"INC-{uuid.uuid4().hex[:10].upper()}"
        incident = Incident(
            incident_id=incident_id,
            category=category,
            location=location,
            title=title,
            description=description,
            reported_at=datetime.now(),
            reporter_id=reporter_id,
            media_urls=kwargs.get("media_urls", []),
            tags=kwargs.get("tags", []),
            affected_population=kwargs.get("affected_population", 0),
            priority_score=self._calculate_priority(category, kwargs.get("affected_population", 0))
        )
        self.incidents[incident_id] = incident
        self.categories[category] += 1
        return incident

    def _calculate_priority(self, category: IncidentCategory,
                            affected_population: int) -> float:
        """Calculate incident priority score."""
        category_weights = {
            IncidentCategory.HEALTH_EMERGENCY: 1.0,
            IncidentCategory.SECURITY_INCIDENT: 0.9,
            IncidentCategory.INFRASTRUCTURE_DAMAGE: 0.8,
            IncidentCategory.HUMANITARIAN_NEED: 0.7,
            IncidentCategory.DISPLACEMENT: 0.6,
            IncidentCategory.ACCESSIBILITY: 0.5,
            IncidentCategory.ENVIRONMENTAL_HAZARD: 0.4,
            IncidentCategory.SERVICE_DISRUPTION: 0.3,
        }
        base_weight = category_weights.get(category, 0.5)
        population_factor = min(affected_population / 1000, 1.0)
        return (base_weight * 0.7 + population_factor * 0.3) * 10

    def vote_incident(self, incident_id: str, vote: str) -> bool:
        """Vote on an incident (upvote or downvote)."""
        if incident_id not in self.incidents:
            return False
        incident = self.incidents[incident_id]
        if vote == "up":
            incident.upvotes += 1
        elif vote == "down":
            incident.downvotes += 1
        else:
            return False
        return True

    def validate_incident(self, incident_id: str, validation_level: ValidationLevel,
                          validator_id: str, notes: str = "") -> bool:
        """Update incident validation level."""
        if incident_id not in self.incidents:
            return False
        incident = self.incidents[incident_id]
        incident.validation_level = validation_level
        if validation_level in (ValidationLevel.VERIFIED, ValidationLevel.GROUND_TRUTH, ValidationLevel.OFFICIAL):
            incident.status = IncidentStatus.VERIFIED

        self.validation_log.append({
            "incident_id": incident_id,
            "validation_level": validation_level.value,
            "validator_id": validator_id,
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        })
        return True

    def register_volunteer(self, volunteer_id: str, name: str,
                           skills: List[str], availability: str = "full") -> Dict[str, Any]:
        """Register a volunteer mapper."""
        volunteer = {
            "volunteer_id": volunteer_id,
            "name": name,
            "skills": skills,
            "availability": availability,
            "registered_at": datetime.now().isoformat(),
            "tasks_completed": 0,
            "accuracy_score": 0.0,
            "status": "active"
        }
        self.volunteers[volunteer_id] = volunteer
        return volunteer

    def create_mapping_task(self, title: str, description: str,
                            area: BoundingBox, priority: int,
                            required_skills: Optional[List[str]] = None) -> MappingTask:
        """Create a new mapping task for volunteers."""
        task_id = f"TASK-{uuid.uuid4().hex[:8].upper()}"
        task = MappingTask(
            task_id=task_id,
            title=title,
            description=description,
            area_of_interest=area,
            priority=priority,
            required_skills=required_skills or []
        )
        self.tasks[task_id] = task
        return task

    def assign_task(self, task_id: str, volunteer_id: str) -> bool:
        """Assign a task to a volunteer."""
        if task_id not in self.tasks or volunteer_id not in self.volunteers:
            return False
        task = self.tasks[task_id]
        if task.status != "open":
            return False
        task.assigned_to = volunteer_id
        task.status = "in_progress"
        return True

    def complete_task(self, task_id: str) -> bool:
        """Mark a task as completed."""
        if task_id not in self.tasks:
            return False
        task = self.tasks[task_id]
        if task.status != "in_progress":
            return False
        task.status = "completed"
        task.completed_at = datetime.now()
        if task.assigned_to and task.assigned_to in self.volunteers:
            self.volunteers[task.assigned_to]["tasks_completed"] += 1
        return True

    def get_incidents_by_category(self, category: IncidentCategory,
                                  status: Optional[IncidentStatus] = None) -> List[Incident]:
        """Get incidents filtered by category and status."""
        results = []
        for incident in self.incidents.values():
            if incident.category == category:
                if status is None or incident.status == status:
                    results.append(incident)
        return sorted(results, key=lambda i: i.priority_score, reverse=True)

    def get_incidents_in_area(self, bounding_box: BoundingBox) -> List[Incident]:
        """Get all incidents within a bounding box."""
        return [inc for inc in self.incidents.values()
                if bounding_box.contains(inc.location)]

    def get_statistics(self) -> Dict[str, Any]:
        """Get crowd-mapping statistics."""
        status_counts = {}
        for incident in self.incidents.values():
            status = incident.status.value
            status_counts[status] = status_counts.get(status, 0) + 1

        return {
            "total_incidents": len(self.incidents),
            "by_category": {k.value: v for k, v in self.categories.items() if v > 0},
            "by_status": status_counts,
            "total_volunteers": len(self.volunteers),
            "active_tasks": sum(1 for t in self.tasks.values() if t.status == "in_progress"),
            "completed_tasks": sum(1 for t in self.tasks.values() if t.status == "completed"),
            "total_validations": len(self.validation_log)
        }


class SituationReportGenerator:
    """Automated situation report generation system."""

    def __init__(self, templates: Optional[List[str]] = None):
        self.templates = templates or ["sitrep", "damage_assessment"]
        self.reports: List[SituationReport] = []
        self.report_counter = 0

    def generate_sitrep(self, event_id: str, title: str,
                        prepared_by: str, affected_area: BoundingBox,
                        summary: str, key_findings: List[str],
                        **kwargs) -> SituationReport:
        """Generate a situation report."""
        self.report_counter += 1
        report_id = f"SITREP-{event_id}-{self.report_counter:03d}"

        report = SituationReport(
            report_id=report_id,
            report_type=ReportType.SITREP,
            title=title,
            event_id=event_id,
            prepared_by=prepared_by,
            prepared_at=datetime.now(),
            valid_from=datetime.now(),
            valid_until=kwargs.get("valid_until", datetime.now() + timedelta(hours=24)),
            affected_area=affected_area,
            summary=summary,
            key_findings=key_findings,
            data_sources=kwargs.get("data_sources", []),
            maps_included=kwargs.get("maps_included", []),
            recommendations=kwargs.get("recommendations", []),
            contact_info=kwargs.get("contact_info", "")
        )
        self.reports.append(report)
        return report

    def generate_damage_assessment_report(self, event_id: str,
                                          assessment: DamageAssessmentResult,
                                          prepared_by: str) -> SituationReport:
        """Generate a damage assessment report from satellite analysis."""
        summary_parts = []
        for damage_level, count in assessment.damage_summary.items():
            if count > 0:
                summary_parts.append(f"{damage_level.value}: {count}")

        summary = f"Satellite-based damage assessment of {assessment.total_buildings} buildings. "
        summary += f"Damage distribution: {', '.join(summary_parts)}. "
        summary += f"Overall damage rate: {assessment.damage_percentage:.1f}%."

        key_findings = [
            f"Total buildings analyzed: {assessment.total_buildings}",
            f"Buildings destroyed: {assessment.damage_summary.get(DamageClassification.DESTROYED, 0)}",
            f"Buildings severely damaged: {assessment.damage_summary.get(DamageClassification.SEVERE_DAMAGE, 0)}",
            f"Confidence score: {assessment.confidence_score:.1%}"
        ]

        return self.generate_sitrep(
            event_id=event_id,
            title=f"Damage Assessment Report - {event_id}",
            prepared_by=prepared_by,
            affected_area=assessment.area_of_interest,
            summary=summary,
            key_findings=key_findings,
            data_sources=[assessment.scene_before, assessment.scene_after]
        )

    def generate_mapping_update(self, event_id: str, incident_count: int,
                                validated_count: int, prepared_by: str,
                                area: BoundingBox) -> SituationReport:
        """Generate a mapping update report."""
        summary = f"Crisis mapping update: {incident_count} incidents reported, "
        summary += f"{validated_count} validated ({validated_count/max(incident_count,1)*100:.1f}% validation rate)."

        key_findings = [
            f"Total incidents mapped: {incident_count}",
            f"Validated incidents: {validated_count}",
            f"Validation rate: {validated_count/max(incident_count,1)*100:.1f}%",
            f"Mapping coverage area: {area.width_km:.1f} x {area.height_km:.1f} km"
        ]

        return self.generate_sitrep(
            event_id=event_id,
            title=f"Crisis Mapping Update - {event_id}",
            prepared_by=prepared_by,
            affected_area=area,
            summary=summary,
            key_findings=key_findings
        )

    def get_reports_by_event(self, event_id: str) -> List[SituationReport]:
        """Get all reports for a specific event."""
        return [r for r in self.reports if r.event_id == event_id]

    def get_latest_report(self, event_id: str) -> Optional[SituationReport]:
        """Get the most recent report for an event."""
        reports = self.get_reports_by_event(event_id)
        if not reports:
            return None
        return max(reports, key=lambda r: r.prepared_at)

    def get_statistics(self) -> Dict[str, Any]:
        """Get report generation statistics."""
        by_type = {}
        for report in self.reports:
            rtype = report.report_type.value
            by_type[rtype] = by_type.get(rtype, 0) + 1

        return {
            "total_reports": len(self.reports),
            "by_type": by_type,
            "unique_events": len(set(r.event_id for r in self.reports)),
            "reports_with_recommendations": sum(1 for r in self.reports if r.recommendations)
        }


class SpatialAnalyzer:
    """Spatial analysis and geoprocessing system."""

    def __init__(self, reference_system: str = "WGS84"):
        self.reference_system = reference_system
        self.analysis_results: List[Dict[str, Any]] = []

    def kernel_density(self, incidents: List[Incident], bandwidth: float = 500,
                       grid_resolution: float = 100) -> Dict[str, Any]:
        """Calculate kernel density estimation for incident hotspots."""
        if not incidents:
            return {"error": "No incidents provided", "hotspots": []}

        # Calculate centroid
        avg_lat = sum(i.location.latitude for i in incidents) / len(incidents)
        avg_lon = sum(i.location.longitude for i in incidents) / len(incidents)

        # Simulate hotspot calculation
        hotspots = []
        for i in range(min(5, len(incidents))):
            hotspots.append({
                "hotspot_id": f"HS-{uuid.uuid4().hex[:6].upper()}",
                "latitude": avg_lat + random.uniform(-0.01, 0.01),
                "longitude": avg_lon + random.uniform(-0.01, 0.01),
                "density_score": random.uniform(0.5, 1.0),
                "incident_count": random.randint(3, 20),
                "radius_meters": bandwidth
            })

        result = {
            "analysis_type": "kernel_density",
            "bandwidth_meters": bandwidth,
            "grid_resolution_meters": grid_resolution,
            "input_incidents": len(incidents),
            "hotspots": sorted(hotspots, key=lambda h: h["density_score"], reverse=True),
            "analysis_date": datetime.now().isoformat()
        }
        self.analysis_results.append(result)
        return result

    def proximity_analysis(self, points: List[GeoCoordinate],
                           reference_points: List[GeoCoordinate],
                           max_distance_meters: float = 1000) -> Dict[str, Any]:
        """Calculate proximity of points to reference locations."""
        results = []
        for point in points:
            distances = [point.distance_to(ref) for ref in reference_points]
            nearest_idx = distances.index(min(distances))
            results.append({
                "point": point.to_dict(),
                "nearest_reference": reference_points[nearest_idx].to_dict(),
                "distance_meters": min(distances),
                "within_range": min(distances) <= max_distance_meters
            })

        return {
            "analysis_type": "proximity",
            "max_distance_meters": max_distance_meters,
            "points_analyzed": len(points),
            "reference_points": len(reference_points),
            "within_range_count": sum(1 for r in results if r["within_range"]),
            "results": results
        }

    def interpolate_values(self, known_points: List[Tuple[GeoCoordinate, float]],
                           target_points: List[GeoCoordinate],
                           method: str = "idw") -> Dict[str, Any]:
        """Interpolate values at target points using known data points."""
        interpolated = []
        for target in target_points:
            weighted_sum = 0
            weight_sum = 0
            for known_coord, known_value in known_points:
                distance = target.distance_to(known_coord)
                if distance < 1:
                    weight = 1000  # Very close
                else:
                    weight = 1 / (distance ** 2) if method == "idw" else 1 / distance
                weighted_sum += known_value * weight
                weight_sum += weight

            interpolated_value = weighted_sum / weight_sum if weight_sum > 0 else 0
            interpolated.append({
                "location": target.to_dict(),
                "interpolated_value": round(interpolated_value, 2),
                "method": method
            })

        return {
            "analysis_type": "interpolation",
            "method": method,
            "known_points": len(known_points),
            "target_points": len(target_points),
            "results": interpolated
        }

    def calculate_accessibility(self, origin: GeoCoordinate,
                                destinations: List[GeoCoordinate],
                                road_network_factor: float = 1.3) -> Dict[str, Any]:
        """Calculate accessibility scores for destinations from an origin."""
        accessibility = []
        for dest in destinations:
            direct_distance = origin.distance_to(dest)
            road_distance = direct_distance * road_network_factor
            travel_time_hours = road_distance / (40 * 1000)  # Assuming 40 km/h average
            accessibility.append({
                "destination": dest.to_dict(),
                "direct_distance_meters": round(direct_distance),
                "estimated_road_distance_meters": round(road_distance),
                "estimated_travel_time_hours": round(travel_time_hours, 2),
                "accessibility_score": max(0, 1 - travel_time_hours / 24)  # Normalized to 24h
            })

        return {
            "analysis_type": "accessibility",
            "origin": origin.to_dict(),
            "road_network_factor": road_network_factor,
            "destinations_analyzed": len(destinations),
            "results": sorted(accessibility, key=lambda a: a["accessibility_score"], reverse=True)
        }

    def generate_heatmap_data(self, incidents: List[Incident],
                              grid_size: float = 0.01) -> Dict[str, Any]:
        """Generate heatmap data grid from incidents."""
        if not incidents:
            return {"error": "No incidents"}

        lats = [i.location.latitude for i in incidents]
        lons = [i.location.longitude for i in incidents]

        min_lat, max_lat = min(lats), max(lats)
        min_lon, max_lon = min(lons), max(lons)

        grid = {}
        for incident in incidents:
            grid_lat = round(incident.location.latitude / grid_size) * grid_size
            grid_lon = round(incident.location.longitude / grid_size) * grid_size
            key = f"{grid_lat},{grid_lon}"
            grid[key] = grid.get(key, 0) + 1

        return {
            "analysis_type": "heatmap",
            "grid_size_degrees": grid_size,
            "bounds": {"min_lat": min_lat, "max_lat": max_lat,
                       "min_lon": min_lon, "max_lon": max_lon},
            "grid_cells": len(grid),
            "max_intensity": max(grid.values()) if grid else 0,
            "grid_data": [{"lat": float(k.split(",")[0]), "lon": float(k.split(",")[1]),
                           "intensity": v} for k, v in grid.items()]
        }


# =============================================================================
# Main Demo Function
# =============================================================================

def main() -> None:
    """Demonstrate the crisis mapping system capabilities."""
    print("=" * 70)
    print("  CRISIS MAPPING SYSTEM - DEMONSTRATION")
    print("=" * 70)

    # --- Satellite Analysis ---
    print("\n[1] SATELLITE IMAGERY ANALYSIS")
    print("-" * 40)
    sat_analyzer = SatelliteAnalyzer(data_source="sentinel_hub")

    # Ingest scenes
    aoi = BoundingBox(min_lon=-118.30, min_lat=34.00, max_lon=-118.20, max_lat=34.10)

    scene_before = sat_analyzer.ingest_scene(
        source=SatelliteSource.SENTINEL_2,
        acquisition_date=datetime(2024, 1, 1),
        cloud_cover=5.2,
        bounding_box=aoi,
        resolution=10.0
    )
    print(f"  Ingested scene: {scene_before.scene_id} (quality: {scene_before.quality_score():.2f})")

    scene_after = sat_analyzer.ingest_scene(
        source=SatelliteSource.SENTINEL_2,
        acquisition_date=datetime(2024, 1, 15),
        cloud_cover=12.5,
        bounding_box=aoi,
        resolution=10.0
    )
    print(f"  Ingested scene: {scene_after.scene_id} (quality: {scene_after.quality_score():.2f})")

    # Change detection
    damage = sat_analyzer.detect_changes(scene_before.scene_id, scene_after.scene_id, aoi)
    print(f"\n  Damage Assessment: {damage.assessment_id}")
    print(f"    Total buildings: {damage.total_buildings}")
    print(f"    Damage rate: {damage.damage_percentage:.1f}%")
    print(f"    Confidence: {damage.confidence_score:.1%}")
    print(f"    Damage summary:")
    for level, count in damage.damage_summary.items():
        if count > 0:
            print(f"      {level.value}: {count}")

    # Flood analysis
    flood = sat_analyzer.analyze_flood_extent(scene_after.scene_id)
    print(f"\n  Flood Analysis:")
    print(f"    Flooded area: {flood['flooded_area_km2']:.1f} km²")
    print(f"    Affected buildings: {flood['affected_buildings']}")
    print(f"    Affected population: {flood['affected_population_estimate']}")

    print(f"\n  Satellite Statistics: {json.dumps(sat_analyzer.get_scene_statistics(), indent=2)}")

    # --- Crowd-Sourced Mapping ---
    print("\n\n[2] CROWD-SOURCED MAPPING")
    print("-" * 40)
    crowd_mapper = CrowdSourcedMapper(platform="ushahidi")

    # Register volunteers
    volunteers = [
        ("VOL-001", "Alice Chen", ["osm", "satellite"], "full"),
        ("VOL-002", "Bob Smith", ["mobile_mapping", "verification"], "partial"),
        ("VOL-003", "Carol Davis", ["data_entry", "translation"], "full"),
    ]
    for vid, name, skills, avail in volunteers:
        crowd_mapper.register_volunteer(vid, name, skills, avail)
        print(f"  Registered volunteer: {name} ({', '.join(skills)})")

    # Report incidents
    incidents_data = [
        (IncidentCategory.INFRASTRUCTURE_DAMAGE, GeoCoordinate(-118.25, 34.05), "Bridge collapsed", "Major bridge on Highway 101 collapsed", 150),
        (IncidentCategory.DISPLACEMENT, GeoCoordinate(-118.24, 34.06), "Mass displacement", "Thousands displaced from downtown area", 5000),
        (IncidentCategory.HEALTH_EMERGENCY, GeoCoordinate(-118.26, 34.04), "Hospital damaged", "Main hospital sustained severe damage", 200),
        (IncidentCategory.ACCESSIBILITY, GeoCoordinate(-118.23, 34.07), "Road blocked", "Primary evacuation route blocked by debris", 0),
        (IncidentCategory.HUMANITARIAN_NEED, GeoCoordinate(-118.27, 34.05), "Water shortage", "No clean water access for 3 days", 800),
    ]

    reported_incidents = []
    for cat, loc, title, desc, pop in incidents_data:
        incident = crowd_mapper.report_incident(cat, loc, title, desc, affected_population=pop)
        reported_incidents.append(incident)
        print(f"  Reported: {incident.title} (priority: {incident.priority_score:.1f})")

    # Validate some incidents
    crowd_mapper.validate_incident(reported_incidents[0].incident_id,
                                   ValidationLevel.MULTI_SOURCE, "VOL-001", "Confirmed by 3 independent reports")
    crowd_mapper.validate_incident(reported_incidents[1].incident_id,
                                   ValidationLevel.GROUND_TRUTH, "VOL-002", "Verified on ground")

    # Create and assign tasks
    task = crowd_mapper.create_mapping_task(
        title="Map damaged buildings in Sector B",
        description="Identify and map all damaged buildings in Sector B",
        area=BoundingBox(-118.26, 34.04, -118.24, 34.06),
        priority=4,
        required_skills=["osm", "satellite"]
    )
    crowd_mapper.assign_task(task.task_id, "VOL-001")
    crowd_mapper.complete_task(task.task_id)
    print(f"\n  Task created and completed: {task.title}")

    print(f"\n  Crowd Mapping Statistics: {json.dumps(crowd_mapper.get_statistics(), indent=2)}")

    # --- Situation Reports ---
    print("\n\n[3] SITUATION REPORTS")
    print("-" * 40)
    reporter = SituationReportGenerator(templates=["sitrep", "damage_assessment"])

    sitrep = reporter.generate_sitrep(
        event_id="EARTHQUAKE-2024-001",
        title="Earthquake Situation Report - Day 3",
        prepared_by="OCHA Mapping Team",
        affected_area=aoi,
        summary="A 6.8 magnitude earthquake struck the greater LA area on January 12, 2024. "
                "As of Day 3, significant damage has been reported across multiple districts.",
        key_findings=[
            "Over 2,000 buildings assessed via satellite imagery",
            "15% showing moderate to severe damage",
            "Estimated 15,000 people displaced",
            "3 major roads impassable"
        ],
        recommendations=[
            "Prioritize search and rescue in areas with highest building collapse",
            "Establish temporary shelters for displaced populations",
            "Clear primary evacuation routes"
        ]
    )
    print(f"  Generated: {sitrep.title}")
    print(f"    Report ID: {sitrep.report_id}")
    print(f"    Key findings: {len(sitrep.key_findings)}")
    print(f"    Recommendations: {len(sitrep.recommendations)}")

    damage_report = reporter.generate_damage_assessment_report(
        event_id="EARTHQUAKE-2024-001",
        assessment=damage,
        prepared_by="Satellite Analysis Unit"
    )
    print(f"\n  Generated: {damage_report.title}")

    print(f"\n  Report Statistics: {json.dumps(reporter.get_statistics(), indent=2)}")

    # --- Spatial Analysis ---
    print("\n\n[4] SPATIAL ANALYSIS")
    print("-" * 40)
    spatial = SpatialAnalyzer(reference_system="WGS84")

    # Kernel density
    hotspot_result = spatial.kernel_density(reported_incidents, bandwidth=1000)
    print(f"  Kernel Density Analysis:")
    print(f"    Hotspots identified: {len(hotspot_result['hotspots'])}")
    for hs in hotspot_result['hotspots'][:3]:
        print(f"      Density: {hs['density_score']:.2f}, Incidents: {hs['incident_count']}")

    # Proximity analysis
    shelters = [
        GeoCoordinate(-118.22, 34.08),
        GeoCoordinate(-118.28, 34.02),
        GeoCoordinate(-118.25, 34.10),
    ]
    proximity = spatial.proximity_analysis(
        points=[i.location for i in reported_incidents],
        reference_points=shelters,
        max_distance_meters=5000
    )
    print(f"\n  Proximity Analysis:")
    print(f"    Points within range: {proximity['within_range_count']}/{proximity['points_analyzed']}")

    # Heatmap
    heatmap = spatial.generate_heatmap_data(reported_incidents, grid_size=0.005)
    print(f"\n  Heatmap Generation:")
    print(f"    Grid cells: {heatmap['grid_cells']}")
    print(f"    Max intensity: {heatmap['max_intensity']}")

    # Accessibility
    origin = GeoCoordinate(-118.25, 34.05)
    accessibility = spatial.calculate_accessibility(origin, shelters)
    print(f"\n  Accessibility Analysis:")
    for result in accessibility['results']:
        print(f"    To {result['destination']}: {result['estimated_travel_time_hours']:.1f}h, "
              f"score: {result['accessibility_score']:.2f}")

    # --- Summary ---
    print("\n\n" + "=" * 70)
    print("  DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\n  Components demonstrated:")
    print("    1. Satellite Analysis - scene ingestion, change detection, flood mapping")
    print("    2. Crowd-Sourced Mapping - incident reporting, validation, volunteer tasks")
    print("    3. Situation Reports - automated report generation")
    print("    4. Spatial Analysis - kernel density, proximity, heatmaps, accessibility")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()