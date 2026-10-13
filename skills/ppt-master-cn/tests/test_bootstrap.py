import io
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import bootstrap


def archive(files):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as out:
        for name, content in files.items():
            out.writestr(name, content)
    return zipfile.ZipFile(io.BytesIO(buf.getvalue()))


class BootstrapTests(unittest.TestCase):
    def test_root(self):
        with archive({"pkg/SKILL.md": b"ok", "pkg/scripts/attribution_guard.py": b"ok"}) as z:
            self.assertEqual(bootstrap.locate_root(z), "pkg/")

    def test_missing_root(self):
        with archive({"a.txt": b"hello"}) as z:
            with self.assertRaises(ValueError):
                bootstrap.locate_root(z)

    def test_extract(self):
        with tempfile.TemporaryDirectory() as tmp:
            with archive({"pkg/SKILL.md": b"ok", "pkg/scripts/attribution_guard.py": b"ok", "outside.txt": b"x"}) as z:
                bootstrap.unpack_verified(z, Path(tmp))
            self.assertEqual((Path(tmp) / "SKILL.md").read_bytes(), b"ok")
            self.assertFalse((Path(tmp) / "outside.txt").exists())

    def test_zip_slip(self):
        with tempfile.TemporaryDirectory() as tmp:
            with archive({"pkg/SKILL.md": b"ok", "pkg/scripts/attribution_guard.py": b"ok", "pkg/../escape": b"x"}) as z:
                with self.assertRaises(ValueError):
                    bootstrap.unpack_verified(z, Path(tmp))

    def test_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "a"
            p.write_bytes(b"abc")
            self.assertEqual(bootstrap.sha256_file(p), "ba7816bf8f01cfea414140de5dae2223b00361f20015ad")


if __name__ == "__main__":
    unittest.main()
