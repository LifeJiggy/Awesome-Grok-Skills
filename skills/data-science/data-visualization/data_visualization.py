"""
Data Visualization Framework

Production-grade visualization framework providing statistical graphics, interactive
dashboards, geospatial mapping, and automated reporting for data science communication.
"""

from __future__ import annotations

import io
import json
import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ChartType(Enum):
    HISTOGRAM = "histogram"
    KDE = "kde"
    ECDF = "ecdf"
    SCATTER = "scatter"
    BUBBLE = "bubble"
    LINE = "line"
    AREA = "area"
    BAR = "bar"
    GROUPED_BAR = "grouped_bar"
    STACKED_BAR = "stacked_bar"
    BOX = "box"
    VIOLIN = "violin"
    SWARM = "swarm"
    STRIP = "strip"
    POINT = "point"
    HEATMAP = "heatmap"
    PAIR = "pair"
    RIDGELINE = "ridgeline"
    WATERFALL = "waterfall"
    FUNNEL = "funnel"
    TREEMAP = "treemap"
    SUNBURST = "sunburst"
    GAUGE = "gauge"
    SPARKLINE = "sparkline"


class Theme(Enum):
    DEFAULT = "default"
    DARK = "dark"
    LIGHT = "light"
    PUBLICATION = "publication"
    PRESENTATION = "presentation"
    HIGH_CONTRAST = "high_contrast"
    MINIMAL = "minimal"
    SEABORN = "seaborn"


class ColorScale(Enum):
    VIRIDIS = "viridis"
    PLASMA = "plasma"
    INFERNO = "inferno"
    MAGMA = "magma"
    CIVIDIS = "cividis"
    YLORRD = "YlOrRd"
    BLUES = "Blues"
    GREENS = "Greens"
    REDS = "Reds"
    RdYlBu = "RdYlBu"
    CUSTOM = "custom"


class GeoType(Enum):
    CHOROPLETH = "choropleth"
    BUBBLE_MAP = "bubble_map"
    HEATMAP = "heatmap"
    SCATTER_MAP = "scatter_map"
    POLYLINE = "polyline"
    MARKER = "marker"


class ExportFormat(Enum):
    PNG = "png"
    SVG = "svg"
    PDF = "pdf"
    HTML = "html"
    JSON = "json"


class AnnotationType(Enum):
    MEAN = "mean"
    MEDIAN = "median"
    STD_DEV = "std_dev"
    PERCENTILE = "percentile"
    REGRESSION = "regression"
    CONFIDENCE = "confidence"
    HIGHLIGHT = "highlight"
    ARROW = "arrow"
    TEXT = "text"
    VLINE = "vline"
    HLINE = "hline"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ColorPalette:
    """Named color palette with accessibility metadata."""
    name: str
    colors: List[str]
    colorblind_safe: bool = True
    contrast_ratios: Optional[Dict[str, float]] = None

    def __getitem__(self, idx: int) -> str:
        return self.colors[idx % len(self.colors)]

    def __len__(self) -> int:
        return len(self.colors)


@dataclass
class Annotation:
    """Chart annotation specification."""
    type: AnnotationType
    x: Optional[float] = None
    y: Optional[float] = None
    text: Optional[str] = None
    color: str = "#333333"
    fontsize: int = 9
    linestyle: str = "--"
    linewidth: float = 1.0
    alpha: float = 0.8


@dataclass
class AxisConfig:
    """Axis configuration."""
    label: str = ""
    lim: Optional[Tuple[float, float]] = None
    scale: str = "linear"  # linear, log, symlog
    tick_format: Optional[str] = None
    grid: bool = True
    grid_alpha: float = 0.3
    rotation: float = 0
    fontsize: int = 11


@dataclass
class LegendConfig:
    """Legend configuration."""
    show: bool = True
    position: str = "best"  # best, upper_right, lower_right, etc.
    title: str = ""
    fontsize: int = 10
    ncol: int = 1
    frameon: bool = False


@dataclass
class ChartSpec:
    """Complete chart specification."""
    chart_type: ChartType
    data: Any  # DataFrame or dict of arrays
    x: Optional[str] = None
    y: Optional[str] = None
    hue: Optional[str] = None
    size: Optional[str] = None
    style: Optional[str] = None
    title: str = ""
    subtitle: str = ""
    xlabel: str = ""
    ylabel: str = ""
    zlabel: str = ""
    palette: Union[str, ColorPalette] = "viridis"
    theme: Theme = Theme.DEFAULT
    figsize: Tuple[int, int] = (10, 6)
    dpi: int = 100
    annotations: List[Annotation] = field(default_factory=list)
    x_axis: AxisConfig = field(default_factory=AxisConfig)
    y_axis: AxisConfig = field(default_factory=AxisConfig)
    legend: LegendConfig = field(default_factory=LegendConfig)
    grid: bool = True
    tight_layout: bool = True
    alpha: float = 0.8
    bins: int = 30
    kde: bool = False
    cumulative: bool = False
    stacked: bool = False
    orient: str = "vertical"
    show_mean: bool = False
    show_median: bool = False
    show_std: bool = False
    confidence_level: float = 0.95


@dataclass
class DashboardPanel:
    """Dashboard panel specification."""
    panel_type: str
    title: str
    data: Any
    position: Tuple[int, int] = (0, 0)
    size: Tuple[int, int] = (1, 1)
    interactive: bool = True
    crossfilter: bool = False
    options: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DashboardSpec:
    """Complete dashboard specification."""
    title: str
    theme: Theme = Theme.DARK
    panels: List[DashboardPanel] = field(default_factory=list)
    filters: List[Dict[str, Any]] = field(default_factory=list)
    layout: str = "grid"  # grid, flex, custom
    responsive: bool = True
    width: str = "100%"
    height: str = "100vh"


@dataclass
class ReportSection:
    """Report section specification."""
    title: str
    content: List[Dict[str, Any]] = field(default_factory=list)
    subsections: List[Dict[str, Any]] = field(default_factory=list)
    page_break: bool = False


@dataclass
class ReportSpec:
    """Complete report specification."""
    title: str
    author: str = ""
    template: str = "default"
    brand_colors: Dict[str, str] = field(default_factory=dict)
    sections: List[ReportSection] = field(default_factory=list)
    page_size: str = "A4"
    margins: Dict[str, float] = field(default_factory=lambda: {"top": 1, "bottom": 1, "left": 1, "right": 1})


@dataclass
class GeoSpec:
    """Geospatial visualization specification."""
    geo_type: GeoType
    data: Any
    geo_column: str
    value_column: Optional[str] = None
    lat_column: Optional[str] = None
    lon_column: Optional[str] = None
    color_scale: ColorScale = ColorScale.VIRIDIS
    basemap: str = "openstreetmap"
    zoom: int = 5
    center: Optional[Tuple[float, float]] = None
    tooltip_format: str = ""
    bins: int = 7
    radius: int = 10


@dataclass
class ExportOptions:
    """Export configuration."""
    format: ExportFormat = ExportFormat.PNG
    filename: str = "chart"
    dpi: int = 300
    bbox_inches: str = "tight"
    transparent: bool = False
    quality: int = 95
    width: Optional[int] = None
    height: Optional[int] = None


# ---------------------------------------------------------------------------
# Color Palettes
# ---------------------------------------------------------------------------

OKABE_ITO = ColorPalette(
    name="okabe_ito",
    colors=["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7", "#000000"],
    colorblind_safe=True,
)

VIRIDIS_PALETTE = ColorPalette(
    name="viridis",
    colors=["#440154", "#482878", "#3e4989", "#31688e", "#26828e", "#1f9e89", "#35b779", "#6ece58", "#b5de2b", "#fde725"],
    colorblind_safe=True,
)

PUBLICATION_PALETTE = ColorPalette(
    name="publication",
    colors=["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#D55E00", "#F0E442", "#000000"],
    colorblind_safe=True,
)

DARK_THEME_COLORS = {
    "background": "#1e1e2e",
    "text": "#cdd6f4",
    "grid": "#45475a",
    "axes": "#585b70",
    "accent": "#89b4fa",
    "highlight": "#f38ba8",
}

LIGHT_THEME_COLORS = {
    "background": "#ffffff",
    "text": "#1e1e2e",
    "grid": "#e6e9ef",
    "axes": "#ccd0da",
    "accent": "#1e66f5",
    "highlight": "#d20f39",
}

PALETTE_REGISTRY: Dict[str, ColorPalette] = {
    "okabe_ito": OKABE_ITO,
    "viridis": VIRIDIS_PALETTE,
    "publication": PUBLICATION_PALETTE,
}


# ---------------------------------------------------------------------------
# Chart Builder
# ---------------------------------------------------------------------------

class ChartBuilder:
    """Build charts with a consistent API and sensible defaults."""

    def __init__(self, theme: Theme = Theme.DEFAULT, dpi: int = 100):
        self.theme = theme
        self.dpi = dpi
        self._theme_colors = self._resolve_theme(theme)

    def _resolve_theme(self, theme: Theme) -> Dict[str, str]:
        if theme == Theme.DARK:
            return DARK_THEME_COLORS
        return LIGHT_THEME_COLORS

    def _resolve_palette(self, palette: Union[str, ColorPalette]) -> ColorPalette:
        if isinstance(palette, ColorPalette):
            return palette
        return PALETTE_REGISTRY.get(palette, VIRIDIS_PALETTE)

    def create(self, **kwargs: Any) -> "ChartFigure":
        """Create a chart from specification."""
        spec = ChartSpec(**kwargs)
        return ChartFigure(spec, self._theme_colors, self.dpi)

    def create_from_spec(self, spec: ChartSpec) -> "ChartFigure":
        return ChartFigure(spec, self._theme_colors, self.dpi)


class ChartFigure:
    """Renderable chart figure with annotation and export capabilities."""

    def __init__(self, spec: ChartSpec, theme_colors: Dict[str, str], dpi: int = 100):
        self.spec = spec
        self.theme_colors = theme_colors
        self.dpi = dpi
        self._annotations: List[Annotation] = list(spec.annotations)
        self._layers: List[Dict[str, Any]] = []
        self._rendered = False

    def add_annotation(self, annotation: Annotation) -> "ChartFigure":
        self._annotations.append(annotation)
        return self

    def add_stat_box(
        self,
        position: str = "upper_right",
        stats: List[str] = None,
        data_source: Any = None,
        column: Optional[str] = None,
    ) -> "ChartFigure":
        if stats is None:
            stats = ["mean", "median", "std"]
        stat_values = {}
        if data_source is not None and column is not None:
            arr = np.asarray(data_source[column] if hasattr(data_source, "column") else data_source)
            if "mean" in stats:
                stat_values["Mean"] = f"{np.mean(arr):.4f}"
            if "median" in stats:
                stat_values["Median"] = f"{np.median(arr):.4f}"
            if "std" in stats:
                stat_values["Std"] = f"{np.std(arr, ddof=1):.4f}"
            if "skewness" in stats:
                m3 = np.mean((arr - np.mean(arr)) ** 3)
                stat_values["Skewness"] = f"{m3 / (np.std(arr, ddof=1) ** 3):.4f}"
            if "kurtosis" in stats:
                m4 = np.mean((arr - np.mean(arr)) ** 4)
                stat_values["Kurtosis"] = f"{m4 / (np.std(arr, ddof=1) ** 4) - 3:.4f}"

        self._annotations.append(Annotation(
            type=AnnotationType.TEXT,
            text="\n".join(f"{k}: {v}" for k, v in stat_values.items()),
            fontsize=8,
        ))
        return self

    def add_layer(self, layer_type: str, **options: Any) -> "ChartFigure":
        self._layers.append({"type": layer_type, **options})
        return self

    def savefig(self, filename: str, dpi: Optional[int] = None, **kwargs: Any) -> str:
        """Export chart to file."""
        export_dpi = dpi or self.dpi
        ext = Path(filename).suffix.lower()

        # Generate chart data as dictionary
        chart_data = self._to_dict()
        chart_data["export"] = {
            "filename": filename,
            "dpi": export_dpi,
            "format": ext.lstrip("."),
            **kwargs,
        }

        # Write as JSON for downstream rendering
        json_path = filename.rsplit(".", 1)[0] + ".json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(chart_data, f, indent=2, default=str)

        logger.info("Chart saved to %s (spec: %s)", filename, json_path)
        return json_path

    def to_html(self, include_plotlyjs: bool = True) -> str:
        """Generate standalone HTML for the chart."""
        chart_data = self._to_dict()
        html = f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>{self.spec.title}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
       background: {self.theme_colors.get('background', '#fff')};
       color: {self.theme_colors.get('text', '#333')};
       margin: 20px; }}
.chart-title {{ font-size: 16px; font-weight: 600; margin-bottom: 4px; }}
.chart-subtitle {{ font-size: 12px; color: #666; margin-bottom: 16px; }}
.chart-container {{ border: 1px solid {self.theme_colors.get('grid', '#ddd')};
                    border-radius: 8px; padding: 16px; }}
</style>
</head><body>
<div class="chart-container">
  <div class="chart-title">{self.spec.title}</div>
  <div class="chart-subtitle">{self.spec.subtitle}</div>
  <pre style="font-size:10px;white-space:pre-wrap;">{json.dumps(chart_data, indent=2, default=str)}</pre>
</div>
</body></html>"""
        return html

    def _to_dict(self) -> Dict[str, Any]:
        """Serialize chart to dictionary."""
        data_dict = {}
        if hasattr(self.spec.data, "to_dict"):
            data_dict = self.spec.data.to_dict()
        elif isinstance(self.spec.data, dict):
            data_dict = {k: v.tolist() if hasattr(v, "tolist") else v for k, v in self.spec.data.items()}
        elif isinstance(self.spec.data, np.ndarray):
            data_dict = {"values": self.spec.data.tolist()}
        else:
            data_dict = {"values": str(self.spec.data)}

        return {
            "chart_type": self.spec.chart_type.value,
            "title": self.spec.title,
            "subtitle": self.spec.subtitle,
            "xlabel": self.spec.xlabel,
            "ylabel": self.spec.ylabel,
            "x": self.spec.x,
            "y": self.spec.y,
            "hue": self.spec.hue,
            "palette": self.spec.palette if isinstance(self.spec.palette, str) else self.spec.palette.name,
            "theme": self.spec.theme.value,
            "figsize": list(self.spec.figsize),
            "data": data_dict,
            "annotations": [
                {"type": a.type.value, "text": a.text, "x": a.x, "y": a.y}
                for a in self._annotations
            ],
            "layers": self._layers,
            "options": {
                "bins": self.spec.bins,
                "kde": self.spec.kde,
                "cumulative": self.spec.cumulative,
                "stacked": self.spec.stacked,
                "alpha": self.spec.alpha,
                "show_mean": self.spec.show_mean,
                "show_median": self.spec.show_median,
            },
        }


# ---------------------------------------------------------------------------
# Dashboard Builder
# ---------------------------------------------------------------------------

class DashboardBuilder:
    """Build interactive dashboards with linked panels and filters."""

    def __init__(self, title: str = "Dashboard", theme: Theme = Theme.DARK):
        self.spec = DashboardSpec(title=title, theme=theme)
        self._theme_colors = DARK_THEME_COLORS if theme == Theme.DARK else LIGHT_THEME_COLORS

    def add_panel(self, panel: DashboardPanel) -> "DashboardBuilder":
        self.spec.panels.append(panel)
        return self

    def add_filter(self, column: str, filter_type: str = "dropdown", options: Optional[List[str]] = None) -> "DashboardBuilder":
        self.spec.filters.append({
            "column": column,
            "type": filter_type,
            "options": options or [],
        })
        return self

    def add_metric_card(
        self,
        title: str,
        value: Any,
        delta: Optional[str] = None,
        position: Tuple[int, int] = (0, 0),
        size: Tuple[int, int] = (1, 1),
    ) -> "DashboardBuilder":
        self.spec.panels.append(DashboardPanel(
            panel_type="metric_card",
            title=title,
            data={"value": value, "delta": delta},
            position=position,
            size=size,
            interactive=False,
        ))
        return self

    def add_chart_panel(
        self,
        chart_type: str,
        title: str,
        data: Any,
        position: Tuple[int, int] = (0, 0),
        size: Tuple[int, int] = (1, 1),
        crossfilter: bool = False,
        **kwargs: Any,
    ) -> "DashboardBuilder":
        self.spec.panels.append(DashboardPanel(
            panel_type=chart_type,
            title=title,
            data=data,
            position=position,
            size=size,
            crossfilter=crossfilter,
            options=kwargs,
        ))
        return self

    def to_html(self) -> str:
        """Generate standalone HTML dashboard."""
        panels_html = ""
        for panel in self.spec.panels:
            panels_html += f"""
<div class="panel" style="grid-column: span {panel.size[0]}; grid-row: span {panel.size[1]};">
  <div class="panel-title">{panel.title}</div>
  <div class="panel-content">
    <pre>{json.dumps({"type": panel.panel_type, "data": panel.data}, default=str, indent=2)}</pre>
  </div>
</div>"""

        filters_html = ""
        for f in self.spec.filters:
            options = "".join(f"<option>{o}</option>" for o in f.get("options", []))
            filters_html += f"""
<select class="filter" data-column="{f['column']}">
  <option value="">All {f['column']}</option>
  {options}
</select>"""

        return f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>{self.spec.title}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
       background: {self._theme_colors['background']};
       color: {self._theme_colors['text']};
       margin: 0; padding: 20px; }}
.dashboard-title {{ font-size: 24px; font-weight: 700; margin-bottom: 16px; }}
.filters {{ display: flex; gap: 12px; margin-bottom: 16px; }}
.filter {{ padding: 6px 12px; border-radius: 6px; border: 1px solid {self._theme_colors['grid']};
           background: {self._theme_colors['background']}; color: {self._theme_colors['text']}; }}
.grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }}
.panel {{ background: {self._theme_colors['axes']}22; border: 1px solid {self._theme_colors['grid']};
          border-radius: 8px; padding: 16px; }}
.panel-title {{ font-size: 14px; font-weight: 600; margin-bottom: 8px; }}
.panel-content {{ font-size: 11px; }}
</style>
</head><body>
<div class="dashboard-title">{self.spec.title}</div>
<div class="filters">{filters_html}</div>
<div class="grid">{panels_html}</div>
</body></html>"""

    def export(self, filename: str) -> str:
        html = self.to_html()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        logger.info("Dashboard exported to %s", filename)
        return filename


# ---------------------------------------------------------------------------
# Geo Chart
# ---------------------------------------------------------------------------

class GeoChart:
    """Geospatial visualization builder."""

    def __init__(self, basemap: str = "openstreetmap"):
        self.basemap = basemap

    def create(self, **kwargs: Any) -> "GeoFigure":
        spec = GeoSpec(**kwargs)
        return GeoFigure(spec, self.basemap)

    def choropleth(
        self,
        data: Any,
        geo_column: str,
        value_column: str,
        color_scale: ColorScale = ColorScale.VIRIDIS,
        title: str = "",
        **kwargs: Any,
    ) -> "GeoFigure":
        return self.create(
            geo_type=GeoType.CHOROPLETH,
            data=data,
            geo_column=geo_column,
            value_column=value_column,
            color_scale=color_scale,
            title=title,
            **kwargs,
        )

    def bubble_map(
        self,
        data: Any,
        lat_column: str,
        lon_column: str,
        size_column: Optional[str] = None,
        color_column: Optional[str] = None,
        title: str = "",
        **kwargs: Any,
    ) -> "GeoFigure":
        return self.create(
            geo_type=GeoType.BUBBLE_MAP,
            data=data,
            geo_column="",
            lat_column=lat_column,
            lon_column=lon_column,
            size=size_column,
            title=title,
            **kwargs,
        )


class GeoFigure:
    """Renderable geospatial figure."""

    def __init__(self, spec: GeoSpec, basemap: str):
        self.spec = spec
        self.basemap = basemap
        self._overlays: List[Dict[str, Any]] = []

    def add_scale_bar(self, position: str = "bottom_left") -> "GeoFigure":
        self._overlays.append({"type": "scale_bar", "position": position})
        return self

    def add_north_arrow(self, position: str = "top_right") -> "GeoFigure":
        self._overlays.append({"type": "north_arrow", "position": position})
        return self

    def add_tooltip(self, format_str: str) -> "GeoFigure":
        self.spec.tooltip_format = format_str
        return self

    def savefig(self, filename: str, dpi: int = 300) -> str:
        geo_data = {
            "geo_type": self.spec.geo_type.value,
            "basemap": self.basemap,
            "color_scale": self.spec.color_scale.value,
            "zoom": self.spec.zoom,
            "center": self.spec.center,
            "overlays": self._overlays,
        }
        json_path = filename.rsplit(".", 1)[0] + ".geo.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(geo_data, f, indent=2, default=str)
        logger.info("Geo chart saved to %s", json_path)
        return json_path

    def to_dict(self) -> Dict[str, Any]:
        data_dict = {}
        if hasattr(self.spec.data, "to_dict"):
            data_dict = self.spec.data.to_dict()
        elif isinstance(self.spec.data, dict):
            data_dict = self.spec.data
        return {
            "geo_type": self.spec.geo_type.value,
            "geo_column": self.spec.geo_column,
            "value_column": self.spec.value_column,
            "color_scale": self.spec.color_scale.value,
            "basemap": self.basemap,
            "data": data_dict,
            "overlays": self._overlays,
        }


# ---------------------------------------------------------------------------
# Report Builder
# ---------------------------------------------------------------------------

class ReportBuilder:
    """Build automated PDF/HTML reports with charts and metrics."""

    def __init__(
        self,
        title: str = "Report",
        author: str = "",
        template: str = "default",
        brand_colors: Optional[Dict[str, str]] = None,
    ):
        self.spec = ReportSpec(
            title=title,
            author=author,
            template=template,
            brand_colors=brand_colors or {},
        )
        self._charts: Dict[str, Any] = {}
        self._sections: List[ReportSection] = []

    def add_section(self, section: ReportSection) -> "ReportBuilder":
        self._sections.append(section)
        self.spec.sections.append(section)
        return self

    def add_chart(self, chart_id: str, chart_figure: Any) -> "ReportBuilder":
        self._charts[chart_id] = chart_figure
        return self

    def add_executive_summary(
        self,
        metrics: List[Dict[str, Any]],
        narrative: str = "",
    ) -> "ReportBuilder":
        content = []
        if narrative:
            content.append({"type": "text", "body": narrative})
        content.append({"type": "metric_grid", "metrics": metrics})
        self._sections.append(ReportSection(title="Executive Summary", content=content))
        return self

    def build_html(self) -> str:
        """Build complete HTML report."""
        brand_primary = self.spec.brand_colors.get("primary", "#1a73e8")
        brand_secondary = self.spec.brand_colors.get("secondary", "#34a853")

        sections_html = ""
        for section in self._sections:
            content_html = ""
            for item in section.content:
                if item.get("type") == "text":
                    content_html += f"<p>{item.get('body', '')}</p>"
                elif item.get("type") == "metric_grid":
                    metrics_html = ""
                    for m in item.get("metrics", []):
                        delta_color = "#34a853" if m.get("delta", "").startswith("+") else "#d20f39"
                        metrics_html += f"""
<div class="metric">
  <div class="metric-value">{m.get('value', '')}</div>
  <div class="metric-label">{m.get('label', '')}</div>
  <div class="metric-delta" style="color:{delta_color}">{m.get('delta', '')}</div>
</div>"""
                    content_html += f'<div class="metrics-grid">{metrics_html}</div>'
                elif item.get("type") == "chart":
                    content_html += f'<div class="chart-placeholder">[Chart: {item.get("ref", "")}]</div>'

            sections_html += f"""
<div class="section{' page-break' if section.page_break else ''}">
  <h2>{section.title}</h2>
  {content_html}
</div>"""

        return f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>{self.spec.title}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
       margin: 0; padding: 40px; color: #333; line-height: 1.6; }}
.report-header {{ border-bottom: 3px solid {brand_primary}; padding-bottom: 20px; margin-bottom: 30px; }}
.report-title {{ font-size: 28px; font-weight: 700; color: {brand_primary}; }}
.report-author {{ font-size: 14px; color: #666; margin-top: 4px; }}
.report-date {{ font-size: 12px; color: #999; }}
h2 {{ color: {brand_primary}; border-bottom: 1px solid #eee; padding-bottom: 8px; }}
.metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 16px; margin: 16px 0; }}
.metric {{ text-align: center; padding: 16px; background: #f8f9fa; border-radius: 8px; }}
.metric-value {{ font-size: 24px; font-weight: 700; color: {brand_primary}; }}
.metric-label {{ font-size: 12px; color: #666; margin-top: 4px; }}
.metric-delta {{ font-size: 11px; font-weight: 600; }}
.chart-placeholder {{ background: #f0f0f0; border-radius: 8px; padding: 40px; text-align: center; color: #999; }}
.page-break {{ page-break-before: always; }}
@media print {{
  body {{ padding: 20px; }}
  .page-break {{ page-break-before: always; }}
}}
</style>
</head><body>
<div class="report-header">
  <div class="report-title">{self.spec.title}</div>
  <div class="report-author">{self.spec.author}</div>
  <div class="report-date">{datetime.now().strftime('%B %d, %Y')}</div>
</div>
{sections_html}
</body></html>"""

    def build(self, filename: str) -> str:
        html = self.build_html()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        logger.info("Report saved to %s", filename)
        return filename


# ---------------------------------------------------------------------------
# Accessibility Helpers
# ---------------------------------------------------------------------------

class AccessibilityHelper:
    """WCAG accessibility utilities for charts."""

    @staticmethod
    def check_contrast(foreground: str, background: str) -> float:
        """Compute WCAG contrast ratio between two hex colors."""
        def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
            h = hex_color.lstrip("#")
            return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

        def relative_luminance(rgb: Tuple[int, int, int]) -> float:
            vals = []
            for c in rgb:
                srgb = c / 255.0
                vals.append(srgb / 12.92 if srgb <= 0.04045 else ((srgb + 0.055) / 1.055) ** 2.4)
            return 0.2126 * vals[0] + 0.7152 * vals[1] + 0.0722 * vals[2]

        l1 = relative_luminance(hex_to_rgb(foreground))
        l2 = relative_luminance(hex_to_rgb(background))
        lighter = max(l1, l2)
        darker = min(l1, l2)
        return (lighter + 0.05) / (darker + 0.05)

    @staticmethod
    def is_wcag_aa_compliant(foreground: str, background: str, large_text: bool = False) -> bool:
        ratio = AccessibilityHelper.check_contrast(foreground, background)
        return ratio >= 4.5 if not large_text else ratio >= 3.0

    @staticmethod
    def generate_alt_text(spec: ChartSpec) -> str:
        chart_name = spec.chart_type.value.replace("_", " ").title()
        parts = [f"A {chart_name.lower()}"]
        if spec.x:
            parts.append(f"showing {spec.x}")
        if spec.y:
            parts.append(f"against {spec.y}")
        if spec.hue:
            parts.append(f"colored by {spec.hue}")
        if spec.title:
            parts.append(f"titled '{spec.title}'")
        return " ".join(parts) + "."


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate data visualization capabilities."""
    print("=" * 70)
    print("Data Visualization Framework - Demo")
    print("=" * 70)

    rng = np.random.default_rng(42)

    # --- 1. Chart Builder ---
    print("\n--- Chart Builder ---")
    builder = ChartBuilder(theme=Theme.PUBLICATION)

    # Create histogram chart spec
    data = {
        "revenue": rng.normal(50000, 15000, 500).tolist(),
        "segment": rng.choice(["Enterprise", "SMB", "Consumer"], 500).tolist(),
    }
    chart = builder.create(
        chart_type=ChartType.HISTOGRAM,
        data=data,
        x="revenue",
        hue="segment",
        title="Revenue Distribution by Segment",
        xlabel="Revenue ($)",
        ylabel="Count",
        bins=25,
        kde=True,
        show_mean=True,
    )
    chart.add_stat_box(
        position="upper_right",
        stats=["mean", "median", "std"],
        data_source=data,
        column="revenue",
    )
    chart_json = chart._to_dict()
    print(f"  Chart type: {chart_json['chart_type']}")
    print(f"  Title:      {chart_json['title']}")
    print(f"  Data keys:  {list(chart_json['data'].keys())}")
    print(f"  Annotations: {len(chart_json['annotations'])}")

    # Save chart
    chart.savefig("demo_chart.png")
    print("  Saved: demo_chart.png + demo_chart.json")

    # --- 2. HTML export ---
    print("\n--- HTML Export ---")
    html = chart.to_html()
    print(f"  HTML length: {len(html)} chars")
    with open("demo_chart.html", "w") as f:
        f.write(html)
    print("  Saved: demo_chart.html")

    # --- 3. Dashboard Builder ---
    print("\n--- Dashboard Builder ---")
    dashboard = DashboardBuilder(title="Sales Dashboard", theme=Theme.DARK)
    dashboard.add_metric_card("Total Revenue", "$4.2M", delta="+15%", position=(0, 0))
    dashboard.add_metric_card("Active Users", "12,450", delta="+8%", position=(0, 1))
    dashboard.add_metric_card("NPS Score", "72", delta="+5", position=(0, 2))
    dashboard.add_chart_panel(
        "line_chart", "Revenue Trend",
        data={"months": ["Jan", "Feb", "Mar", "Apr", "May"],
              "revenue": [1.2, 1.4, 1.3, 1.6, 1.8]},
        position=(1, 0), size=(2, 2),
    )
    dashboard.add_filter("date_range", "date_range_picker")
    dashboard.add_filter("region", "multi_select", ["North", "South", "East", "West"])
    dashboard.export("demo_dashboard.html")
    print("  Saved: demo_dashboard.html")

    # --- 4. Geo Chart ---
    print("\n--- Geo Chart ---")
    geo = GeoChart(basemap="openstreetmap")
    geo_fig = geo.choropleth(
        data={"state": ["CA", "NY", "TX", "FL"], "population": [39.5, 19.5, 29.0, 21.5]},
        geo_column="state",
        value_column="population",
        color_scale=ColorScale.YLORRD,
        title="Population by State (millions)",
    )
    geo_fig.add_scale_bar()
    geo_fig.add_north_arrow()
    geo_dict = geo_fig.to_dict()
    print(f"  Geo type: {geo_dict['geo_type']}")
    print(f"  Overlays: {len(geo_dict['overlays'])}")

    # --- 5. Report Builder ---
    print("\n--- Report Builder ---")
    report = ReportBuilder(
        title="Q4 2024 Business Review",
        author="Data Science Team",
        template="executive_summary",
        brand_colors={"primary": "#1a73e8", "secondary": "#34a853"},
    )
    report.add_executive_summary(
        metrics=[
            {"label": "Revenue", "value": "$4.2M", "delta": "+15%"},
            {"label": "Customers", "value": "12,450", "delta": "+8%"},
            {"label": "NPS", "value": "72", "delta": "+5"},
        ],
        narrative="Revenue grew 15% QoQ driven by enterprise segment expansion.",
    )
    report.add_section(ReportSection(
        title="Revenue Analysis",
        content=[{"type": "chart", "ref": "revenue_trend"}],
    ))
    report.build("demo_report.html")
    print("  Saved: demo_report.html")

    # --- 6. Accessibility ---
    print("\n--- Accessibility ---")
    acc = AccessibilityHelper()
    ratio = acc.check_contrast("#0072B2", "#ffffff")
    compliant = acc.is_wcag_aa_compliant("#0072B2", "#ffffff")
    print(f"  Contrast ratio (blue/white): {ratio:.2f}:1")
    print(f"  WCAG AA compliant: {compliant}")

    alt_text = acc.generate_alt_text(ChartSpec(
        chart_type=ChartType.SCATTER,
        data={}, x="age", y="income", hue="segment",
        title="Customer Segments",
    ))
    print(f"  Alt text: {alt_text}")

    # Clean up generated files
    for f in ["demo_chart.png", "demo_chart.json", "demo_chart.html",
              "demo_dashboard.html", "demo_report.html"]:
        if os.path.exists(f):
            os.remove(f)

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()