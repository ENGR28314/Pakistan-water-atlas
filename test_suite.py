"""test_suite.py - run with:  python -m unittest test_suite.py -v"""
import importlib.util
import unittest
from datetime import date

import hydraulic_model as H
import data_loader as D
import coordinates as C
import input_driven as I
import network_view as N
import simulation_engines as S
import forests_parks as FP
import geopolitics as G

HAS_PLOTLY = importlib.util.find_spec("plotly") is not None


class TestBasinStress(unittest.TestCase):
    def test_balance_and_status(self):
        r = H.calculate_basin_stress(inflow_m3s=3500, capacity_m3s=10000, installed_mw=1000)
        self.assertAlmostEqual(r["stress_index"], 0.35)
        self.assertAlmostEqual(r["baseline_flow_m3s"], 1000 / 0.35, places=1)
        self.assertEqual(r["status"], "Nominal")

    def test_thresholds(self):
        self.assertEqual(H.calculate_basin_stress(7000, 10000, 100)["status"], "Elevated")
        self.assertEqual(H.calculate_basin_stress(10000, 10000, 100)["status"], "Critical Hazard Warning")

    def test_bad_inputs(self):
        with self.assertRaises(ValueError):
            H.calculate_basin_stress(10, 0, 10)
        with self.assertRaises(ValueError):
            H.calculate_basin_stress(-1, 10, 10)


class TestWaterQuality(unittest.TestCase):
    def test_pristine_is_excellent(self):
        r = H.water_quality_index(do_mgl=9, ph=7.5, turbidity_ntu=1, salinity_dsm=0.2, bod_mgl=0.5)
        self.assertGreaterEqual(r["wqi"], 85)
        self.assertEqual(r["status"], "Excellent")

    def test_high_salinity_collapse(self):
        r = H.water_quality_index(do_mgl=8, ph=7.5, turbidity_ntu=5, salinity_dsm=6.0, bod_mgl=1)
        self.assertEqual(r["status"], "Ecosystem Collapse Warning")


class TestHazardClustering(unittest.TestCase):
    def test_extreme_boundary(self):
        flags = H.cluster_hazard_flags(flow_m3s=15001, rainfall_mm_hr=60)
        self.assertTrue(any("CRITICAL" in f for f in flags))

    def test_below_boundary(self):
        self.assertEqual(H.cluster_hazard_flags(14999, 10), [])

    def test_cloudburst_and_landslide(self):
        flags = H.cluster_hazard_flags(1000, 85, slope_deg=30)
        self.assertTrue(any("cloudburst" in f for f in flags))
        self.assertTrue(any("landslide" in f for f in flags))


class TestRainfallSlider(unittest.TestCase):
    def test_monotonic(self):
        vals = [H.flash_flood_hazard(2400, r, 12000)["peak_flow_m3s"] for r in (0, 25, 50, 75, 100)]
        self.assertEqual(vals, sorted(vals))

    def test_levels_cover_all(self):
        seen = {H.flash_flood_hazard(2400, r, 12000)["status"] for r in range(0, 101, 5)}
        self.assertEqual(seen, set(H.HAZARD_LEVELS))

    def test_range_enforced(self):
        with self.assertRaises(ValueError):
            H.flash_flood_hazard(1000, 101, 5000)


class TestTelemetry(unittest.TestCase):
    def test_shape_and_seasonality(self):
        df = D.telemetry_12_months(end=date(2026, 10, 4))
        self.assertEqual(df["month"].nunique(), 12)
        self.assertEqual(df["gauge"].nunique(), len(D.GAUGES))
        g = df[df.gauge == "Chenab @ Marala"].set_index("month")["discharge_m3s"]
        self.assertGreater(g["2026-07"], g["2026-01"] * 5)

    def test_reproducible(self):
        a = D.telemetry_12_months(end=date(2026, 10, 4), seed=1)
        b = D.telemetry_12_months(end=date(2026, 10, 4), seed=1)
        self.assertTrue(a.equals(b))


class TestEngines(unittest.TestCase):
    def test_monte_carlo_reproducible(self):
        a = S.FloodMonteCarlo(9000).run(2000)["p_exceed"]
        b = S.FloodMonteCarlo(9000).run(2000)["p_exceed"]
        self.assertEqual(a, b)
        self.assertTrue(0 <= a <= 1)

    def test_scenarios_ordered(self):
        df = S.ClimateScenarioEngine().project(10000, 30)
        self.assertEqual(list(df.scenario), ["Baseline", "Medium", "Worst-case"])
        self.assertTrue(df.peak_flow_m3s.is_monotonic_increasing)

    def test_water_share(self):
        df = S.WaterShareEngine().share(80, {"Punjab": 60, "Sindh": 40})
        self.assertAlmostEqual(df.allocated_maf.sum(), 80, places=2)

    def test_pondage_gap(self):
        r = S.TreatyDisputeEngine().pondage_gap(24, 8, 600)
        self.assertEqual(r["ratio"], 3.0)
        self.assertGreater(r["india_hours"], r["pakistan_hours"])

    def test_lcoe_positive(self):
        e = S.HydropowerEconomics()
        self.assertGreater(e.lcoe_usd_mwh(1700, 720, 0.55), 0)
        self.assertAlmostEqual(e.annual_gwh(100, 0.5), 438.0)

    def test_reservoir_clipped(self):
        df = S.ReservoirSimulator(100, 10, 60).run([5000] * 5, [0] * 5)
        self.assertLessEqual(df.storage_mcm.max(), 110)


class TestData(unittest.TestCase):
    def test_all_seven_provinces(self):
        self.assertEqual(len(C.PROVINCES), 7)

    def test_links_reference_structures(self):
        for a, b in C.LINK_CANALS.values():
            self.assertIn(a, C.STRUCTURES)
            self.assertIn(b, C.STRUCTURES)

    def test_every_park_has_coordinates(self):
        self.assertEqual(set(FP.NATIONAL_PARKS.park), set(C.PARKS))

    def test_coordinates_inside_pakistan_bbox(self):
        for name, (la, lo) in C.PARKS.items():
            self.assertTrue(23 <= la <= 37.5 and 60 <= lo <= 78, name)
        for name, s in C.STRUCTURES.items():
            self.assertTrue(23 <= s["lat"] <= 37.5 and 60 <= s["lon"] <= 78, name)

    def test_upstream_downstream_order(self):
        order = D.upstream_downstream("Indus")
        self.assertLess(order.index("Tarbela Dam"), order.index("Kotri Barrage"))

    def test_dispute_tables(self):
        self.assertEqual(float(D.PONDAGE_TABLE.set_index("project").loc["Ratle", "india_design_mcm"]), 24.0)
        self.assertEqual(len(D.NEUTRAL_EXPERT_SCHEDULE), 4)
        self.assertEqual(len(G.PCA_TIMELINE) >= 8, True)


class TestInputDriven(unittest.TestCase):
    def test_validate_clips_and_coerces(self):
        df = I.default_data().astype({"honey_production_t": object})
        df.loc[0, "honey_production_t"] = "bad"
        df.loc[1, "employment_persons"] = -5
        out = I.validate(df)
        self.assertEqual(out.loc[0, "honey_production_t"], 0)
        self.assertEqual(out.loc[1, "employment_persons"], 0)

    def test_missing_column(self):
        with self.assertRaises(ValueError):
            I.validate(I.default_data().drop(columns=["employment_persons"]))

    def test_summary(self):
        s = I.summary(I.default_data(), "Cultivated area (ha)")
        self.assertEqual(s["top"], "Punjab")

    @unittest.skipUnless(HAS_PLOTLY, "plotly not installed")
    def test_all_chart_combinations(self):
        df = I.default_data()
        for m in I.METRICS:
            for g in I.GRAPH_TYPES:
                self.assertIsNotNone(I.build_chart(df, m, g))


class TestNetwork(unittest.TestCase):
    def test_graph_is_dag_and_connected(self):
        import networkx as nx
        g = N.irrigation_graph()
        self.assertTrue(nx.is_directed_acyclic_graph(g))
        self.assertIn("Kotri", N.downstream_of(g, "Tarbela"))
        self.assertIn("Tarbela", N.upstream_of(g, "Kotri"))

    def test_confluence_graph(self):
        g = N.confluence_graph()
        self.assertIn("Indus (lower)", N.downstream_of(g, "Chenab R."))


@unittest.skipUnless(HAS_PLOTLY, "plotly not installed")
class TestMaps(unittest.TestCase):
    def test_all_maps_build(self):
        import map_view as M
        for f in (M.province_map, M.water_system_map, M.link_canal_map, M.climate_map, M.ranges_map, M.lakes_map,
                  M.geopolitics_map, M.pakal_ratle_map, M.china_map, M.forests_parks_map):
            self.assertGreater(len(f().data), 0, f.__name__)
        self.assertGreater(len(M.hazards_map(D.HISTORICAL_EVENTS).data), 0)
        for p in C.PARKS:
            self.assertGreater(len(M.park_map(p).data), 0, p)


if __name__ == "__main__":
    unittest.main()
