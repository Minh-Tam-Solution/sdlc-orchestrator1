"""
=========================================================================
Unit Tests for GrafanaDashboardService
SDLC Orchestrator - Sprint 110 (CEO Dashboard & Observability)

Version: 1.0.0
Date: January 28, 2026
Coverage Target: 80%+ isolated unit tests

Test Categories:
1. Enums (9 tests)
2. Constants (6 tests)
3. Data Classes (18 tests)
4. Helper Functions (18 tests)
5. CEO Dashboard Generation (8 tests)
6. Tech Dashboard Generation (6 tests)
7. Ops Dashboard Generation (6 tests)
8. GrafanaDashboardService (12 tests)
9. Edge Cases (6 tests)

Zero Mock Policy: Real configuration generation testing
=========================================================================
"""

import json
import pytest
import os
import tempfile
from typing import Dict, Any

from app.services.governance.grafana_dashboards import (
    # Enums
    DashboardType,
    PanelType,
    ThresholdMode,
    # Constants
    VIBECODING_COLORS,
    GRAFANA_COLORS,
    # Data Classes
    ThresholdStep,
    GrafanaPanel,
    GrafanaRow,
    GrafanaDashboard,
    # Helper Functions
    create_prometheus_target,
    create_thresholds,
    create_stat_panel,
    create_gauge_panel,
    create_piechart_panel,
    create_timeseries_panel,
    create_barchart_panel,
    create_table_panel,
    # Dashboard Factories
    create_ceo_dashboard,
    create_tech_dashboard,
    create_ops_dashboard,
    # Service Class
    GrafanaDashboardService,
)


# =============================================================================
# CATEGORY 1: ENUMS
# =============================================================================

class TestDashboardTypeEnum:
    """Tests for DashboardType enum."""

    def test_enum_001_ceo_value(self):
        """Should have CEO dashboard type."""
        assert DashboardType.CEO == "ceo"
        assert DashboardType.CEO.value == "ceo"

    def test_enum_002_tech_value(self):
        """Should have TECH dashboard type."""
        assert DashboardType.TECH == "tech"
        assert DashboardType.TECH.value == "tech"

    def test_enum_003_ops_value(self):
        """Should have OPS dashboard type."""
        assert DashboardType.OPS == "ops"
        assert DashboardType.OPS.value == "ops"


class TestPanelTypeEnum:
    """Tests for PanelType enum."""

    def test_enum_004_stat_value(self):
        """Should have STAT panel type."""
        assert PanelType.STAT == "stat"

    def test_enum_005_gauge_value(self):
        """Should have GAUGE panel type."""
        assert PanelType.GAUGE == "gauge"

    def test_enum_006_piechart_value(self):
        """Should have PIECHART panel type."""
        assert PanelType.PIECHART == "piechart"

    def test_enum_007_timeseries_value(self):
        """Should have TIMESERIES panel type."""
        assert PanelType.TIMESERIES == "timeseries"

    def test_enum_008_table_value(self):
        """Should have TABLE panel type."""
        assert PanelType.TABLE == "table"


class TestThresholdModeEnum:
    """Tests for ThresholdMode enum."""

    def test_enum_009_absolute_value(self):
        """Should have ABSOLUTE threshold mode."""
        assert ThresholdMode.ABSOLUTE == "absolute"
        assert ThresholdMode.PERCENTAGE == "percentage"


# =============================================================================
# CATEGORY 2: CONSTANTS
# =============================================================================

class TestColorConstants:
    """Tests for color constants."""

    def test_const_001_vibecoding_colors_green(self):
        """Should have green color for Vibecoding Index 0-30."""
        assert "green" in VIBECODING_COLORS
        assert VIBECODING_COLORS["green"].startswith("#")

    def test_const_002_vibecoding_colors_yellow(self):
        """Should have yellow color for Vibecoding Index 31-60."""
        assert "yellow" in VIBECODING_COLORS
        assert VIBECODING_COLORS["yellow"].startswith("#")

    def test_const_003_vibecoding_colors_orange(self):
        """Should have orange color for Vibecoding Index 61-80."""
        assert "orange" in VIBECODING_COLORS
        assert VIBECODING_COLORS["orange"].startswith("#")

    def test_const_004_vibecoding_colors_red(self):
        """Should have red color for Vibecoding Index 81-100."""
        assert "red" in VIBECODING_COLORS
        assert VIBECODING_COLORS["red"].startswith("#")

    def test_const_005_grafana_colors_all(self):
        """Should have all standard Grafana colors."""
        expected_colors = ["green", "yellow", "orange", "red", "blue", "purple"]
        for color in expected_colors:
            assert color in GRAFANA_COLORS

    def test_const_006_hex_color_format(self):
        """Should have valid hex color format."""
        for color, hex_value in GRAFANA_COLORS.items():
            assert hex_value.startswith("#")
            assert len(hex_value) == 7  # #RRGGBB format


# =============================================================================
# CATEGORY 3: DATA CLASSES
# =============================================================================

class TestThresholdStep:
    """Tests for ThresholdStep data class."""

    def test_dataclass_001_create_threshold_step(self):
        """Should create ThresholdStep with value and color."""
        step = ThresholdStep(value=50.0, color="#FF0000")
        assert step.value == 50.0
        assert step.color == "#FF0000"

    def test_dataclass_002_threshold_step_zero(self):
        """Should allow zero threshold value."""
        step = ThresholdStep(value=0, color="#00FF00")
        assert step.value == 0

    def test_dataclass_003_threshold_step_negative(self):
        """Should allow negative threshold value."""
        step = ThresholdStep(value=-10, color="#0000FF")
        assert step.value == -10


class TestGrafanaPanel:
    """Tests for GrafanaPanel data class."""

    def test_dataclass_004_create_panel_minimal(self):
        """Should create panel with required fields."""
        panel = GrafanaPanel(
            id=1,
            title="Test Panel",
            type=PanelType.STAT,
            gridPos={"x": 0, "y": 0, "w": 6, "h": 4},
            targets=[{"expr": "test_metric"}],
        )
        assert panel.id == 1
        assert panel.title == "Test Panel"
        assert panel.type == PanelType.STAT
        assert panel.fieldConfig == {}
        assert panel.options == {}
        assert panel.description == ""

    def test_dataclass_005_create_panel_full(self):
        """Should create panel with all fields."""
        panel = GrafanaPanel(
            id=1,
            title="Full Panel",
            type=PanelType.GAUGE,
            gridPos={"x": 0, "y": 0, "w": 6, "h": 4},
            targets=[{"expr": "test_metric"}],
            fieldConfig={"defaults": {"unit": "percent"}},
            options={"showThresholdLabels": True},
            description="Test description",
        )
        assert panel.fieldConfig == {"defaults": {"unit": "percent"}}
        assert panel.options == {"showThresholdLabels": True}
        assert panel.description == "Test description"

    def test_dataclass_006_panel_to_dict(self):
        """Should convert panel to dictionary."""
        panel = GrafanaPanel(
            id=1,
            title="Test",
            type=PanelType.STAT,
            gridPos={"x": 0, "y": 0, "w": 6, "h": 4},
            targets=[{"expr": "test"}],
        )
        result = panel.to_dict()
        assert result["id"] == 1
        assert result["title"] == "Test"
        assert result["type"] == "stat"
        assert result["gridPos"] == {"x": 0, "y": 0, "w": 6, "h": 4}

    def test_dataclass_007_panel_to_dict_with_description(self):
        """Should include description in dict when present."""
        panel = GrafanaPanel(
            id=1,
            title="Test",
            type=PanelType.STAT,
            gridPos={"x": 0, "y": 0, "w": 6, "h": 4},
            targets=[],
            description="My description",
        )
        result = panel.to_dict()
        assert "description" in result
        assert result["description"] == "My description"

    def test_dataclass_008_panel_to_dict_without_description(self):
        """Should exclude description from dict when empty."""
        panel = GrafanaPanel(
            id=1,
            title="Test",
            type=PanelType.STAT,
            gridPos={"x": 0, "y": 0, "w": 6, "h": 4},
            targets=[],
            description="",
        )
        result = panel.to_dict()
        assert "description" not in result


class TestGrafanaRow:
    """Tests for GrafanaRow data class."""

    def test_dataclass_009_create_row_minimal(self):
        """Should create row with title."""
        row = GrafanaRow(title="Test Row")
        assert row.title == "Test Row"
        assert row.collapsed == False
        assert row.panels == []

    def test_dataclass_010_create_row_with_panels(self):
        """Should create row with panels."""
        panel = GrafanaPanel(
            id=1,
            title="Test",
            type=PanelType.STAT,
            gridPos={"x": 0, "y": 0, "w": 6, "h": 4},
            targets=[],
        )
        row = GrafanaRow(title="Test Row", panels=[panel])
        assert len(row.panels) == 1


class TestGrafanaDashboard:
    """Tests for GrafanaDashboard data class."""

    def test_dataclass_011_create_dashboard_minimal(self):
        """Should create dashboard with required fields."""
        dashboard = GrafanaDashboard(
            uid="test-uid",
            title="Test Dashboard",
            description="Test description",
            tags=["test"],
            panels=[],
        )
        assert dashboard.uid == "test-uid"
        assert dashboard.title == "Test Dashboard"
        assert dashboard.refresh == "5s"
        assert dashboard.time_from == "now-24h"

    def test_dataclass_012_dashboard_to_dict(self):
        """Should convert dashboard to dictionary."""
        dashboard = GrafanaDashboard(
            uid="test-uid",
            title="Test",
            description="Desc",
            tags=["t1", "t2"],
            panels=[],
        )
        result = dashboard.to_dict()
        assert result["uid"] == "test-uid"
        assert result["title"] == "Test"
        assert result["tags"] == ["t1", "t2"]
        assert "time" in result
        assert "timepicker" in result
        assert result["schemaVersion"] == 39

    def test_dataclass_013_dashboard_to_dict_with_panels(self):
        """Should include panels in dict."""
        panel = GrafanaPanel(
            id=1,
            title="Test Panel",
            type=PanelType.STAT,
            gridPos={"x": 0, "y": 0, "w": 6, "h": 4},
            targets=[],
        )
        dashboard = GrafanaDashboard(
            uid="test-uid",
            title="Test",
            description="Desc",
            tags=[],
            panels=[panel],
        )
        result = dashboard.to_dict()
        assert len(result["panels"]) == 1
        assert result["panels"][0]["id"] == 1

    def test_dataclass_014_dashboard_to_json(self):
        """Should export dashboard as JSON string."""
        dashboard = GrafanaDashboard(
            uid="test-uid",
            title="Test",
            description="Desc",
            tags=[],
            panels=[],
        )
        json_str = dashboard.to_json()
        parsed = json.loads(json_str)
        assert parsed["uid"] == "test-uid"

    def test_dataclass_015_dashboard_to_json_indent(self):
        """Should export JSON with specified indent."""
        dashboard = GrafanaDashboard(
            uid="test-uid",
            title="Test",
            description="Desc",
            tags=[],
            panels=[],
        )
        json_str = dashboard.to_json(indent=4)
        # Should have newlines for readability
        assert "\n" in json_str

    def test_dataclass_016_dashboard_time_settings(self):
        """Should include time settings in dict."""
        dashboard = GrafanaDashboard(
            uid="test",
            title="Test",
            description="Desc",
            tags=[],
            panels=[],
            time_from="now-1h",
            time_to="now",
        )
        result = dashboard.to_dict()
        assert result["time"]["from"] == "now-1h"
        assert result["time"]["to"] == "now"

    def test_dataclass_017_dashboard_refresh_intervals(self):
        """Should include refresh intervals in timepicker."""
        dashboard = GrafanaDashboard(
            uid="test",
            title="Test",
            description="Desc",
            tags=[],
            panels=[],
        )
        result = dashboard.to_dict()
        assert "5s" in result["timepicker"]["refresh_intervals"]

    def test_dataclass_018_dashboard_editable_flag(self):
        """Should include editable flag."""
        dashboard = GrafanaDashboard(
            uid="test",
            title="Test",
            description="Desc",
            tags=[],
            panels=[],
            editable=False,
        )
        result = dashboard.to_dict()
        assert result["editable"] == False


# =============================================================================
# CATEGORY 4: HELPER FUNCTIONS
# =============================================================================

class TestCreatePrometheusTarget:
    """Tests for create_prometheus_target helper."""

    def test_helper_001_basic_target(self):
        """Should create basic Prometheus target."""
        target = create_prometheus_target("test_metric")
        assert target["expr"] == "test_metric"
        assert target["refId"] == "A"
        assert target["instant"] == False
        assert target["range"] == True

    def test_helper_002_target_with_legend(self):
        """Should create target with legend format."""
        target = create_prometheus_target("test_metric", legend_format="{{label}}")
        assert target["legendFormat"] == "{{label}}"

    def test_helper_003_instant_target(self):
        """Should create instant query target."""
        target = create_prometheus_target("test_metric", instant=True)
        assert target["instant"] == True
        assert target["range"] == False

    def test_helper_004_target_custom_refid(self):
        """Should create target with custom refId."""
        target = create_prometheus_target("test_metric", ref_id="B")
        assert target["refId"] == "B"


class TestCreateThresholds:
    """Tests for create_thresholds helper."""

    def test_helper_005_single_threshold(self):
        """Should create single threshold."""
        steps = [ThresholdStep(0, "#00FF00")]
        result = create_thresholds(steps)
        assert result["mode"] == "absolute"
        assert len(result["steps"]) == 1

    def test_helper_006_multiple_thresholds(self):
        """Should create multiple thresholds."""
        steps = [
            ThresholdStep(0, "#00FF00"),
            ThresholdStep(50, "#FFFF00"),
            ThresholdStep(80, "#FF0000"),
        ]
        result = create_thresholds(steps)
        assert len(result["steps"]) == 3
        assert result["steps"][1]["value"] == 50

    def test_helper_007_percentage_mode(self):
        """Should create thresholds with percentage mode."""
        steps = [ThresholdStep(0, "#00FF00")]
        result = create_thresholds(steps, mode=ThresholdMode.PERCENTAGE)
        assert result["mode"] == "percentage"


class TestCreateStatPanel:
    """Tests for create_stat_panel helper."""

    def test_helper_008_basic_stat_panel(self):
        """Should create basic stat panel."""
        panel = create_stat_panel(
            id=1,
            title="Test Stat",
            query="test_metric",
            x=0, y=0, w=6, h=4,
        )
        assert panel.id == 1
        assert panel.title == "Test Stat"
        assert panel.type == PanelType.STAT
        assert panel.gridPos == {"x": 0, "y": 0, "w": 6, "h": 4}

    def test_helper_009_stat_panel_with_thresholds(self):
        """Should create stat panel with thresholds."""
        thresholds = [
            ThresholdStep(0, "#00FF00"),
            ThresholdStep(50, "#FF0000"),
        ]
        panel = create_stat_panel(
            id=1,
            title="Test",
            query="test",
            x=0, y=0, w=6, h=4,
            thresholds=thresholds,
        )
        assert "thresholds" in panel.fieldConfig["defaults"]


class TestCreateGaugePanel:
    """Tests for create_gauge_panel helper."""

    def test_helper_010_basic_gauge_panel(self):
        """Should create basic gauge panel."""
        panel = create_gauge_panel(
            id=1,
            title="Test Gauge",
            query="test_metric",
            x=0, y=0, w=6, h=4,
        )
        assert panel.type == PanelType.GAUGE

    def test_helper_011_gauge_with_min_max(self):
        """Should create gauge with min/max values."""
        panel = create_gauge_panel(
            id=1,
            title="Test",
            query="test",
            x=0, y=0, w=6, h=4,
            min_val=-10,
            max_val=100,
        )
        assert panel.fieldConfig["defaults"]["min"] == -10
        assert panel.fieldConfig["defaults"]["max"] == 100


class TestCreatePiechartPanel:
    """Tests for create_piechart_panel helper."""

    def test_helper_012_basic_piechart_panel(self):
        """Should create basic pie chart panel."""
        panel = create_piechart_panel(
            id=1,
            title="Test Pie",
            query="test_metric",
            x=0, y=0, w=6, h=4,
        )
        assert panel.type == PanelType.PIECHART
        assert panel.options["pieType"] == "donut"


class TestCreateTimeseriesPanel:
    """Tests for create_timeseries_panel helper."""

    def test_helper_013_basic_timeseries_panel(self):
        """Should create basic time series panel."""
        queries = [{"expr": "test_metric", "legend": "Test"}]
        panel = create_timeseries_panel(
            id=1,
            title="Test Timeseries",
            queries=queries,
            x=0, y=0, w=12, h=8,
        )
        assert panel.type == PanelType.TIMESERIES
        assert len(panel.targets) == 1

    def test_helper_014_timeseries_multiple_queries(self):
        """Should create timeseries with multiple queries."""
        queries = [
            {"expr": "metric_a", "legend": "A"},
            {"expr": "metric_b", "legend": "B"},
            {"expr": "metric_c", "legend": "C"},
        ]
        panel = create_timeseries_panel(
            id=1,
            title="Multi Query",
            queries=queries,
            x=0, y=0, w=12, h=8,
        )
        assert len(panel.targets) == 3
        assert panel.targets[0]["refId"] == "A"
        assert panel.targets[1]["refId"] == "B"
        assert panel.targets[2]["refId"] == "C"


class TestCreateBarchartPanel:
    """Tests for create_barchart_panel helper."""

    def test_helper_015_basic_barchart_panel(self):
        """Should create basic bar chart panel."""
        panel = create_barchart_panel(
            id=1,
            title="Test Barchart",
            query="test_metric",
            x=0, y=0, w=6, h=4,
        )
        assert panel.type == PanelType.BARCHART

    def test_helper_016_barchart_orientation(self):
        """Should create bar chart with orientation."""
        panel = create_barchart_panel(
            id=1,
            title="Test",
            query="test",
            x=0, y=0, w=6, h=4,
            orientation="vertical",
        )
        assert panel.options["orientation"] == "vertical"


class TestCreateTablePanel:
    """Tests for create_table_panel helper."""

    def test_helper_017_basic_table_panel(self):
        """Should create basic table panel."""
        panel = create_table_panel(
            id=1,
            title="Test Table",
            query="test_metric",
            x=0, y=0, w=12, h=8,
        )
        assert panel.type == PanelType.TABLE

    def test_helper_018_table_panel_options(self):
        """Should have table-specific options."""
        panel = create_table_panel(
            id=1,
            title="Test",
            query="test",
            x=0, y=0, w=12, h=8,
        )
        assert "showHeader" in panel.options
        assert panel.options["showHeader"] == True


# =============================================================================
# CATEGORY 5: CEO DASHBOARD GENERATION
# =============================================================================

class TestCEODashboard:
    """Tests for CEO Dashboard generation."""

    def test_ceo_001_create_ceo_dashboard(self):
        """Should create CEO dashboard."""
        dashboard = create_ceo_dashboard()
        assert dashboard is not None
        assert dashboard.uid == "ceo-dashboard"
        assert dashboard.title == "CEO Dashboard - Governance Intelligence"

    def test_ceo_002_ceo_dashboard_tags(self):
        """Should have correct tags."""
        dashboard = create_ceo_dashboard()
        assert "governance" in dashboard.tags
        assert "ceo" in dashboard.tags

    def test_ceo_003_ceo_dashboard_has_panels(self):
        """Should have panels."""
        dashboard = create_ceo_dashboard()
        assert len(dashboard.panels) > 0

    def test_ceo_004_ceo_dashboard_time_saved_panel(self):
        """Should have Time Saved panel."""
        dashboard = create_ceo_dashboard()
        panel_titles = [p.title for p in dashboard.panels]
        assert any("Time Saved" in title for title in panel_titles)

    def test_ceo_005_ceo_dashboard_pending_decisions(self):
        """Should have Pending Decisions panel."""
        dashboard = create_ceo_dashboard()
        panel_titles = [p.title for p in dashboard.panels]
        assert any("Pending" in title for title in panel_titles)

    def test_ceo_006_ceo_dashboard_valid_json(self):
        """Should export valid JSON."""
        dashboard = create_ceo_dashboard()
        json_str = dashboard.to_json()
        parsed = json.loads(json_str)
        assert "panels" in parsed

    def test_ceo_007_ceo_dashboard_refresh_rate(self):
        """Should have appropriate refresh rate."""
        dashboard = create_ceo_dashboard()
        assert dashboard.refresh == "5s"

    def test_ceo_008_ceo_dashboard_panel_ids_unique(self):
        """Should have unique panel IDs."""
        dashboard = create_ceo_dashboard()
        panel_ids = [p.id for p in dashboard.panels]
        assert len(panel_ids) == len(set(panel_ids))


# =============================================================================
# CATEGORY 6: TECH DASHBOARD GENERATION
# =============================================================================

class TestTechDashboard:
    """Tests for Tech Dashboard generation."""

    def test_tech_001_create_tech_dashboard(self):
        """Should create Tech dashboard."""
        dashboard = create_tech_dashboard()
        assert dashboard is not None
        assert dashboard.uid == "tech-dashboard"
        assert dashboard.title == "Tech Dashboard - Developer Experience & Performance"

    def test_tech_002_tech_dashboard_tags(self):
        """Should have correct tags."""
        dashboard = create_tech_dashboard()
        assert "governance" in dashboard.tags
        assert "tech" in dashboard.tags

    def test_tech_003_tech_dashboard_has_panels(self):
        """Should have panels."""
        dashboard = create_tech_dashboard()
        assert len(dashboard.panels) > 0

    def test_tech_004_tech_dashboard_developer_friction(self):
        """Should have Developer Friction panel."""
        dashboard = create_tech_dashboard()
        panel_titles = [p.title for p in dashboard.panels]
        # Check for friction-related panel
        assert any("Friction" in title or "Developer" in title for title in panel_titles)

    def test_tech_005_tech_dashboard_valid_json(self):
        """Should export valid JSON."""
        dashboard = create_tech_dashboard()
        json_str = dashboard.to_json()
        parsed = json.loads(json_str)
        assert "panels" in parsed

    def test_tech_006_tech_dashboard_panel_ids_unique(self):
        """Should have unique panel IDs."""
        dashboard = create_tech_dashboard()
        panel_ids = [p.id for p in dashboard.panels]
        assert len(panel_ids) == len(set(panel_ids))


# =============================================================================
# CATEGORY 7: OPS DASHBOARD GENERATION
# =============================================================================

class TestOpsDashboard:
    """Tests for Ops Dashboard generation."""

    def test_ops_001_create_ops_dashboard(self):
        """Should create Ops dashboard."""
        dashboard = create_ops_dashboard()
        assert dashboard is not None
        assert dashboard.uid == "ops-dashboard"
        assert dashboard.title == "Ops Dashboard - System Health & Kill Switch"

    def test_ops_002_ops_dashboard_tags(self):
        """Should have correct tags."""
        dashboard = create_ops_dashboard()
        assert "governance" in dashboard.tags
        assert "ops" in dashboard.tags

    def test_ops_003_ops_dashboard_has_panels(self):
        """Should have panels."""
        dashboard = create_ops_dashboard()
        assert len(dashboard.panels) > 0

    def test_ops_004_ops_dashboard_kill_switch(self):
        """Should have Kill Switch panel."""
        dashboard = create_ops_dashboard()
        panel_titles = [p.title for p in dashboard.panels]
        assert any("Kill Switch" in title for title in panel_titles)

    def test_ops_005_ops_dashboard_valid_json(self):
        """Should export valid JSON."""
        dashboard = create_ops_dashboard()
        json_str = dashboard.to_json()
        parsed = json.loads(json_str)
        assert "panels" in parsed

    def test_ops_006_ops_dashboard_panel_ids_unique(self):
        """Should have unique panel IDs."""
        dashboard = create_ops_dashboard()
        panel_ids = [p.id for p in dashboard.panels]
        assert len(panel_ids) == len(set(panel_ids))


# =============================================================================
# CATEGORY 8: GRAFANA DASHBOARD SERVICE
# =============================================================================

class TestGrafanaDashboardService:
    """Tests for GrafanaDashboardService class."""

    def test_service_001_initialization(self):
        """Should initialize service."""
        service = GrafanaDashboardService()
        assert service is not None
        assert service._initialized == False

    def test_service_002_initialize(self):
        """Should initialize all dashboards."""
        service = GrafanaDashboardService()
        service.initialize()
        assert service._initialized == True
        assert len(service._dashboards) == 3

    def test_service_003_get_ceo_dashboard(self):
        """Should get CEO dashboard."""
        service = GrafanaDashboardService()
        dashboard = service.get_dashboard(DashboardType.CEO)
        assert dashboard.uid == "ceo-dashboard"

    def test_service_004_get_tech_dashboard(self):
        """Should get Tech dashboard."""
        service = GrafanaDashboardService()
        dashboard = service.get_dashboard(DashboardType.TECH)
        assert dashboard.uid == "tech-dashboard"

    def test_service_005_get_ops_dashboard(self):
        """Should get Ops dashboard."""
        service = GrafanaDashboardService()
        dashboard = service.get_dashboard(DashboardType.OPS)
        assert dashboard.uid == "ops-dashboard"

    def test_service_006_auto_initialize_on_get(self):
        """Should auto-initialize when getting dashboard."""
        service = GrafanaDashboardService()
        assert service._initialized == False
        _ = service.get_dashboard(DashboardType.CEO)
        assert service._initialized == True

    def test_service_007_get_dashboard_json(self):
        """Should get dashboard as JSON string."""
        service = GrafanaDashboardService()
        json_str = service.get_dashboard_json(DashboardType.CEO)
        parsed = json.loads(json_str)
        assert parsed["uid"] == "ceo-dashboard"

    def test_service_008_get_dashboard_dict(self):
        """Should get dashboard as dictionary."""
        service = GrafanaDashboardService()
        result = service.get_dashboard_dict(DashboardType.CEO)
        assert isinstance(result, dict)
        assert result["uid"] == "ceo-dashboard"

    def test_service_009_get_all_dashboards(self):
        """Should get all dashboards."""
        service = GrafanaDashboardService()
        all_dashboards = service.get_all_dashboards()
        assert DashboardType.CEO in all_dashboards
        assert DashboardType.TECH in all_dashboards
        assert DashboardType.OPS in all_dashboards

    def test_service_010_get_all_auto_initialize(self):
        """Should auto-initialize when getting all dashboards."""
        service = GrafanaDashboardService()
        assert service._initialized == False
        _ = service.get_all_dashboards()
        assert service._initialized == True

    def test_service_011_export_all_dashboards(self):
        """Should export all dashboards to files."""
        service = GrafanaDashboardService()
        with tempfile.TemporaryDirectory() as tmpdir:
            exported = service.export_all_dashboards(tmpdir)
            assert len(exported) == 3
            for filepath in exported:
                assert os.path.exists(filepath)
                with open(filepath) as f:
                    data = json.load(f)
                    assert "uid" in data

    def test_service_012_double_initialize_safe(self):
        """Should be safe to call initialize twice."""
        service = GrafanaDashboardService()
        service.initialize()
        service.initialize()  # Should not raise
        assert service._initialized == True


# =============================================================================
# CATEGORY 9: EDGE CASES
# =============================================================================

class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_edge_001_empty_threshold_list(self):
        """Should handle empty threshold list."""
        result = create_thresholds([])
        assert result["steps"] == []

    def test_edge_002_panel_grid_position_zero(self):
        """Should handle zero grid positions."""
        panel = create_stat_panel(
            id=1,
            title="Test",
            query="test",
            x=0, y=0, w=0, h=0,
        )
        assert panel.gridPos["w"] == 0
        assert panel.gridPos["h"] == 0

    def test_edge_003_long_query_string(self):
        """Should handle long query strings."""
        long_query = "sum(rate(test_metric{" + ",".join([f'label_{i}="value"' for i in range(50)]) + "}[5m]))"
        target = create_prometheus_target(long_query)
        assert target["expr"] == long_query

    def test_edge_004_special_chars_in_title(self):
        """Should handle special characters in title."""
        panel = create_stat_panel(
            id=1,
            title="Test <Panel> & 'Quotes' \"Double\"",
            query="test",
            x=0, y=0, w=6, h=4,
        )
        assert "Test" in panel.title

    def test_edge_005_unicode_in_description(self):
        """Should handle unicode in description."""
        panel = create_stat_panel(
            id=1,
            title="Test",
            query="test",
            x=0, y=0, w=6, h=4,
            description="Vietnamese: Xin cho",
        )
        assert "Vietnamese" in panel.description

    def test_edge_006_large_panel_id(self):
        """Should handle large panel IDs."""
        panel = create_stat_panel(
            id=99999,
            title="Test",
            query="test",
            x=0, y=0, w=6, h=4,
        )
        assert panel.id == 99999
