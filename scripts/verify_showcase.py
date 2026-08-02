#!/usr/bin/env python3
"""No-dependency integrity checks for the public showcase."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import hashlib
import re
import struct
import sys


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "index.html",
    "404.html",
    "styles.css",
    "favicon.svg",
    "robots.txt",
    "sitemap.xml",
    ".nojekyll",
    "README.md",
    "SECURITY.md",
    "NOTICE.md",
    "docs/ARCHITECTURE.md",
    "docs/QUALITY-AND-TESTING.md",
    "docs/PRIVACY.md",
    "docs/PRODUCT-DECISIONS.md",
    "assets/screenshots/today-desktop.png",
    "assets/screenshots/first-run-mobile.png",
    "assets/screenshots/verification-mobile.png",
}

FORBIDDEN_MARKERS = (
    "cloudflareaccess.com",
    "googletagmanager",
    "google-analytics",
    "cloudflareinsights",
    "posthog",
    "mixpanel",
    "segment.com",
    "hotjar",
    "fullstory",
    "clarity.ms",
    "sentry.io",
    "@gmail.com",
)

# Fingerprints prevent the public checker from publishing sensitive discovery
# strings while still rejecting them if they appear in showcase content.
PRIVATE_MARKER_FINGERPRINTS = (
    (34, "9840a0366e376f6c0e29062404e45b27e2f0d78f1f2150846ada623419399c46"),
    (7, "1bc3cd759a28d0bc99076d994335587202eb9995ba369a778765bd691b49af30"),
)


class ShowcaseParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[tuple[str, str]] = []
        self.lang = ""
        self.has_main = False
        self.has_h1 = False
        self.has_viewport = False
        self.has_description = False
        self.has_skip_link = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name: value or "" for name, value in attrs}
        if tag == "html":
            self.lang = values.get("lang", "")
        if tag == "main":
            self.has_main = True
        if tag == "h1":
            self.has_h1 = True
        if tag == "meta" and values.get("name") == "viewport":
            self.has_viewport = True
        if tag == "meta" and values.get("name") == "description":
            self.has_description = True
        if tag == "a" and values.get("href") == "#main-content":
            self.has_skip_link = True
        for attribute in ("href", "src"):
            if values.get(attribute):
                self.refs.append((attribute, values[attribute]))


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as image:
        header = image.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path.relative_to(ROOT)} is not a PNG")
    return struct.unpack(">II", header[16:24])


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_required_files() -> None:
    missing = sorted(item for item in REQUIRED if not (ROOT / item).is_file())
    if missing:
        fail(f"missing required files: {', '.join(missing)}")


def check_public_boundary() -> None:
    allowed_suffixes = {".html", ".css", ".md", ".txt", ".xml", ".svg", ".py", ".yml", ".yaml", ".png"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in {".git", "__pycache__"} for part in path.parts):
            continue
        relative = path.relative_to(ROOT)
        if path.suffix and path.suffix.lower() not in allowed_suffixes:
            fail(f"unexpected public file type: {relative}")
        if re.search(r"(?:backup|journal|evidence).*(?:\.json|\.zip)$", path.name, re.I):
            fail(f"private learner artifact detected: {relative}")
        if path == Path(__file__).resolve():
            continue
        if path.suffix.lower() in {".html", ".css", ".md", ".txt", ".xml", ".svg", ".py", ".yml", ".yaml"}:
            content = path.read_text(encoding="utf-8").lower()
            for marker in FORBIDDEN_MARKERS:
                if marker in content:
                    fail(f"forbidden public marker {marker!r} in {relative}")
            for size, fingerprint in PRIVATE_MARKER_FINGERPRINTS:
                if any(
                    hashlib.sha256(content[index : index + size].encode()).hexdigest() == fingerprint
                    for index in range(max(0, len(content) - size + 1))
                ):
                    fail(f"private marker fingerprint detected in {relative}")


def check_html() -> None:
    for name in ("index.html", "404.html"):
        parser = ShowcaseParser()
        parser.feed((ROOT / name).read_text(encoding="utf-8"))
        if parser.lang != "en":
            fail(f"{name} must declare lang=en")
        if not parser.has_main or not parser.has_h1 or not parser.has_viewport:
            fail(f"{name} is missing main, h1 or viewport semantics")
        if name == "index.html" and (not parser.has_description or not parser.has_skip_link):
            fail("index.html needs a description and skip link")
        for attribute, value in parser.refs:
            parsed = urlparse(value)
            if parsed.scheme:
                if parsed.scheme != "https":
                    fail(f"non-HTTPS {attribute} in {name}: {value}")
                continue
            if value.startswith("#"):
                continue
            if value.startswith("/"):
                base = "/builders-engineering-hub-showcase/"
                if not parsed.path.startswith(base):
                    fail(f"unexpected root-relative {attribute} in {name}: {value}")
                target = (ROOT / parsed.path.removeprefix(base)).resolve()
                if not target.is_file() and target != ROOT:
                    fail(f"broken root-relative reference in {name}: {value}")
                continue
            target = (ROOT / parsed.path).resolve()
            if parsed.path and ROOT not in target.parents and target != ROOT:
                fail(f"reference escapes repository in {name}: {value}")
            if parsed.path and not target.is_file():
                fail(f"broken local reference in {name}: {value}")


def check_screenshots() -> None:
    expected = {
        "assets/screenshots/today-desktop.png": (1440, 900),
        "assets/screenshots/first-run-mobile.png": (375, 812),
        "assets/screenshots/verification-mobile.png": (375, 812),
    }
    for name, dimensions in expected.items():
        actual = png_dimensions(ROOT / name)
        if actual != dimensions:
            fail(f"unexpected screenshot dimensions for {name}: {actual}")


def main() -> None:
    check_required_files()
    check_public_boundary()
    check_html()
    check_screenshots()
    print("PASS: public showcase boundary, links, semantics and screenshots verified")


if __name__ == "__main__":
    main()
