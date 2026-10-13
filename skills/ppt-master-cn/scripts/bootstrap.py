#!/usr/bin/env python3
"""Verified installation of official PPT Master inside a single Codex Skill."""
from __future__ import annotations

import argparse
import hashlib
import shutil
import stat
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

VERSION = "v6.7.0"
SOURCE = f"https://github.com/hugohe3/ppt-master/releases/download/{VERSION}/ppt-master-skill-{VERSION}.zip"
SHA256 = "40424d9784fa25f771da8b312258c3c67a168925122aa6bb7faf6848e77ceee9"
ROOT = Path(__file__).resolve().parent.parent
ENGINE = ROOT / "vendor" / "ppt-master"
MAX_DOWNLOAD = 80 * 1024 * 1024
MAX_UNPACKED = 700 * 1024 * 1024
MAX_FILES = 12000


def check_installed(path: Path = ENGINE) -> None:
    required = (
        "SKILL.md", "LICENSE", "SPONSORS.md", "SPONSORS_CN.md",
        "requirements.txt", "workflows/routing.md", "scripts/attribution_guard.py",
    )
    absent = [x for x in required if not (path / x).is_file()]
    if absent:
        raise RuntimeError("上游引擎文件缺失：" + ", ".join(absent))
    subprocess.run([sys.executable, str(path / "scripts" / "attribution_guard.py")], check=True)


def locate_root(zf: zipfile.ZipFile) -> str:
    names = {item.filename for item in zf.infolist() if not item.is_dir()}
    roots = {
        name[:-len("SKILL.md")]
        for name in names
        if name.endswith("SKILL.md")
        and name[:-len("SKILL.md")] + "scripts/attribution_guard.py" in names
    }
    if len(roots) != 1:
        raise ValueError("无法唯一识别官方 Skill 目录")
    return roots.pop()


def unpack_verified(zf: zipfile.ZipFile, target: Path) -> None:
    prefix = locate_root(zf)
    members = zf.infolist()
    if len(members) > MAX_FILES or sum(m.file_size for m in members) > MAX_UNPACKED:
        raise ValueError("压缩包超过大小限制")
    for member in members:
        name = member.filename
        path = PurePosixPath(name)
        if name.startswith("/") or "\\" in name or ".." in path.parts or not path.parts:
            raise ValueError(f"不安全的 ZIP 路径：{name}")
        kind = (member.external_attr >> 16) & 0o170000
        if kind == stat.S_IFLNK:
            raise ValueError(f"不允许符号链接：{name}")
        if not name.startswith(prefix) or member.is_dir():
            continue
        relative = name[len(prefix):]
        if not relative:
            continue
        output = target.joinpath(*PurePosixPath(relative).parts)
        output.parent.mkdir(parents=True, exist_ok=True)
        with zf.open(member) as src, output.open("wb") as dst:
            shutil.copyfileobj(src, dst)


def download(archive_path: Path) -> None:
    request = urllib.request.Request(SOURCE, headers={"User-Agent": "ppt-master-cn-bootstrap/1.0"})
    total = 0
    with urllib.request.urlopen(request, timeout=120) as src, archive_path.open("wb") as dst:
        while chunk := src.read(1024 * 1024):
            total += len(chunk)
            if total > MAX_DOWNLOAD:
                raise ValueError("下载超过大小限制")
            dst.write(chunk)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def install(archive: Path | None, skip_deps: bool, force: bool) -> None:
    if ENGINE.exists() and not force:
        check_installed()
        print(f"校验通过：{ENGINE}")
        return
    vendor = ENGINE.parent
    vendor.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ppt-cn-download-") as tmp:
        archive_path = archive or Path(tmp) / "release.zip"
        if archive is None:
            download(archive_path)
        digest = sha256_file(archive_path)
        if digest != SHA256:
            raise RuntimeError(f"SHA-256 不匹配：{digest}")
        staged = Path(tempfile.mkdtemp(prefix=".ppt-master-stage-", dir=vendor))
        try:
            with zipfile.ZipFile(archive_path) as zf:
                unpack_verified(zf, staged)
            check_installed(staged)
            if not skip_deps:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", str(staged / "requirements.txt")],
                    check=True,
                )
            if ENGINE.exists():
                shutil.rmtree(ENGINE)
            staged.rename(ENGINE)
            print(f"安装成功：{ENGINE}")
        finally:
            if staged.exists():
                shutil.rmtree(staged)


def main() -> int:
    parser = argparse.ArgumentParser(description="初始化 PPT Master CN 官方引擎")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--skip-deps", action="store_true")
    parser.add_argument("--archive", type=Path)
    args = parser.parse_args()
    if sys.version_info < (3, 10):
        parser.error("需要 Python 3.10+")
    try:
        if args.check:
            check_installed()
            print("上游引擎完整性验证通过")
        else:
            install(args.archive, args.skip_deps, args.force)
    except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError, zipfile.BadZipFile) as exc:
        print(f"安装/验证失败：{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
