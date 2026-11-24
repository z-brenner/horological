"""Tests for the collection log. Run: python3 -m unittest discover -s tests"""

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "horological" / "scripts"))
import collection  # noqa: E402


class CollectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.file = str(Path(self.tmp.name) / "collection.json")

    def tearDown(self):
        self.tmp.cleanup()

    def run_cmd(self, *argv):
        buf = io.StringIO()
        with redirect_stdout(buf):
            collection.main(["--file", self.file, *argv])
        return buf.getvalue()

    def data(self):
        return json.loads(Path(self.file).read_text())

    def test_full_lifecycle(self):
        self.run_cmd("init")
        self.run_cmd("profile", "--set", "experience=enthusiast", "--set", "styles=diver,GMT")
        self.run_cmd("add", "--brand", "Seiko", "--model", "SKX007", "--movement-type", "automatic",
                     "--style", "diver", "--price", "250", "--serial", "123456")
        self.run_cmd("add", "--status", "wishlist", "--brand", "Tudor", "--model", "Black Bay 58",
                     "--price", "4000", "--priority", "high")
        self.run_cmd("acquire", "tudor", "--price", "3900")
        self.run_cmd("dispose", "seiko-skx007", "--how", "sold", "--price", "300", "--reason", "upgraded")
        self.run_cmd("service", "tudor", "--by", "Tudor", "--work", "full service")

        d = self.data()
        self.assertEqual(d["profile"]["styles"], ["diver", "GMT"])
        statuses = {w["id"]: w["status"] for w in d["watches"]}
        self.assertEqual(statuses, {"seiko-skx007": "sold", "tudor-black-bay-58": "owned"})
        types = [e["type"] for e in d["events"]]
        self.assertEqual(types, ["init", "profile", "profile", "add", "add", "acquire", "sold", "service"])

        summary = json.loads(self.run_cmd("summary"))
        self.assertEqual(summary["counts"], {"owned": 1, "sold": 1})
        self.assertEqual(summary["spent_on_owned"], {"USD": 3900})
        self.assertEqual(summary["received_from_disposals"], {"USD": 300})

    def test_serial_hidden_by_default(self):
        self.run_cmd("add", "--brand", "Omega", "--model", "Speedmaster", "--serial", "SECRET1")
        shown = self.run_cmd("show", "omega")
        self.assertNotIn("SECRET1", shown)
        self.assertNotIn("SECRET1", self.run_cmd("export", "--format", "json"))
        self.assertNotIn("SECRET1", self.run_cmd("export", "--format", "md"))
        self.assertIn("SECRET1", self.run_cmd("export", "--format", "md", "--include-serials"))

    def test_duplicate_ids(self):
        self.run_cmd("add", "--brand", "Casio", "--model", "F-91W")
        self.run_cmd("add", "--brand", "Casio", "--model", "F-91W")
        ids = [w["id"] for w in self.data()["watches"]]
        self.assertEqual(ids, ["casio-f-91w", "casio-f-91w-2"])

    def test_export_import_roundtrip(self):
        self.run_cmd("add", "--brand", "Citizen", "--model", "Promaster Diver")
        out = str(Path(self.tmp.name) / "export.json")
        self.run_cmd("export", "--format", "json", "--out", out)
        other = str(Path(self.tmp.name) / "other.json")
        buf = io.StringIO()
        with redirect_stdout(buf):
            collection.main(["--file", other, "import", out])
        imported = json.loads(Path(other).read_text())
        self.assertEqual(imported["watches"][0]["id"], "citizen-promaster-diver")

    def test_service_flag(self):
        self.run_cmd("add", "--brand", "Rolex", "--model", "Explorer", "--movement-type", "automatic")
        summary = json.loads(self.run_cmd("summary"))
        self.assertIn("rolex-explorer", summary["service_check_suggested"])

    def test_wear_and_rotation(self):
        self.run_cmd("add", "--brand", "Seiko", "--model", "Turtle", "--price", "300")
        self.run_cmd("add", "--brand", "Timex", "--model", "Marlin")
        self.run_cmd("wear", "seiko", "--date", "2026-01-01")
        self.run_cmd("wear", "seiko", "--date", "2026-01-02")
        self.run_cmd("wear", "seiko", "--date", "2026-01-02")
        rows = json.loads(self.run_cmd("rotation"))
        self.assertEqual(rows[0]["id"], "timex-marlin")
        self.assertIsNone(rows[0]["last_worn"])
        seiko = rows[1]
        self.assertEqual(seiko["times_worn"], 2)
        self.assertEqual(seiko["cost_per_wear"], 150)
        self.assertEqual(json.loads(self.run_cmd("summary"))["most_worn"], ["Seiko Turtle: 2"])

    def test_bad_experience_rejected(self):
        with self.assertRaises(SystemExit):
            self.run_cmd("profile", "--set", "experience=grandmaster")


if __name__ == "__main__":
    unittest.main()
