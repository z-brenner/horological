"""Tests for horocalc. Run: python3 -m unittest discover -s tests"""

import io
import json
import math
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "horological" / "scripts"))
import horocalc  # noqa: E402


def run(*argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        horocalc.main(["--json", *argv])
    return json.loads(buf.getvalue())


class FreqTests(unittest.TestCase):
    def test_28800(self):
        r = run("freq", "--vph", "28800", "--escape-teeth", "15")
        self.assertEqual(r["hz"], 4)
        self.assertEqual(r["beats_per_second"], 8)
        self.assertEqual(r["escape_wheel_rpm"], 16)

    def test_hz_to_vph(self):
        self.assertEqual(run("freq", "--hz", "3")["vph"], 21600)


class RateTests(unittest.TestCase):
    def test_rate_and_cosc(self):
        r = run("rate", "--gain", "21", "--days", "7", "--standard", "cosc")
        self.assertAlmostEqual(r["rate_s_per_day"], 3.0)
        self.assertIn("within", r["tolerance_checks"][0])

    def test_loss_outside_rolex(self):
        r = run("rate", "--gain", "-30", "--days", "10", "--standard", "rolex")
        self.assertIn("outside", r["tolerance_checks"][0])


class MoonTests(unittest.TestCase):
    def test_59_tooth(self):
        r = run("moonphase", "--teeth", "59")
        self.assertAlmostEqual(r["display_period_days"], 29.5)
        self.assertTrue(2.5 < r["years_until_one_day_error"] < 2.8)

    def test_135_tooth_precision(self):
        r = run("moonphase", "--period", "29.530594")
        self.assertGreater(r["years_until_one_day_error"], 10000)


class WaterTests(unittest.TestCase):
    def test_100m(self):
        r = run("water", "--m", "100")
        self.assertAlmostEqual(r["bar"], 10)
        self.assertAlmostEqual(r["iso_6425_test_pressure_bar"], 12.5)

    def test_30m_guidance(self):
        self.assertIn("Not for swimming", run("water", "--m", "30")["practical_meaning"])


class MagnetTests(unittest.TestCase):
    def test_iso_baseline(self):
        r = run("magnet", "--am", "4800")
        self.assertAlmostEqual(r["gauss"], 60.3, places=1)

    def test_master_chronometer(self):
        r = run("magnet", "--tesla", "1.5")
        self.assertEqual(r["gauss"], 15000)


class SeikoTests(unittest.TestCase):
    def test_decode(self):
        r = run("seiko-serial", "7N1234", "--from-year", "1970", "--to-year", "1989")
        self.assertEqual(r["month"], "November")
        self.assertEqual(r["candidate_years"], ["1977", "1987"])


class GoldLigneTests(unittest.TestCase):
    def test_18k(self):
        self.assertAlmostEqual(run("gold", "--karat", "18")["fineness_per_mille"], 750)

    def test_ligne(self):
        self.assertTrue(math.isclose(run("ligne", "--lignes", "11.5")["mm"], 25.9417, rel_tol=1e-4))


class BeatsReserveTests(unittest.TestCase):
    def test_beats(self):
        r = run("beats", "--vph", "28800", "--years", "1")
        self.assertAlmostEqual(r["total_beats"], 28800 * 24 * 365.2425)

    def test_reserve(self):
        r = run("reserve", "--barrel-turns", "6.5", "--hours-per-barrel-turn", "7")
        self.assertAlmostEqual(r["estimated_power_reserve_h"], 45.5)


class NewCommandTests(unittest.TestCase):
    def test_tachy(self):
        self.assertAlmostEqual(run("tachy", "--seconds", "30")["units_per_hour"], 120)
        self.assertAlmostEqual(run("tachy", "--speed", "90")["elapsed_seconds"], 40)

    def test_telemeter(self):
        self.assertAlmostEqual(run("telemeter", "--seconds", "3")["distance_m"], 1030.26, places=1)

    def test_seconds_pendulum(self):
        r = run("pendulum", "--period-s", "2")
        self.assertAlmostEqual(r["length_m"], 0.9936, places=3)
        self.assertAlmostEqual(r["beats_per_hour"], 3600)

    def test_fit(self):
        r = run("fit", "--wrist-mm", "170", "--lug-to-lug", "47")
        self.assertAlmostEqual(r["estimated_flat_wrist_width_mm"], 52.7)
        self.assertIn("comfortably", r["verdict"])
        self.assertIn("overhang", run("fit", "--wrist-mm", "150", "--lug-to-lug", "51")["verdict"])


if __name__ == "__main__":
    unittest.main()
