#!/usr/bin/env python3
"""
scripts/run_and_log_all_tests.py
================================
Menjalankan seluruh rangkaian tes (pytest) secara komprehensif,
merekam log eksekusi aktual, stempel waktu, dan ringkasan terstruktur
untuk membuktikan kelulusan sistem secara ilmiah dan dapat direproduksi.
"""

import sys
import time
import subprocess
import json
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"
REPORTS_DIR = PROJECT_ROOT / "reports" / "scientific_validation"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

log_file = LOGS_DIR / "TEST_EXECUTION_AUDIT_RUN.log"
summary_json = REPORTS_DIR / "TEST_EXECUTION_SUMMARY.json"

print("=" * 80)
print(f"🔬 MENJALANKAN AUDIT EKSEKUSI PENGUJIAN UNIT (PYTEST RUNNER)")
print(f"Stempel Waktu : {datetime.now().isoformat()} WIB")
print(f"Log Output    : {log_file}")
print("=" * 80)

t0 = time.time()
cmd = [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"]

res = subprocess.run(
    cmd,
    cwd=str(PROJECT_ROOT),
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)
duration = time.time() - t0

output_text = res.stdout

with open(log_file, "w", encoding="utf-8") as f:
    f.write(f"=== PYTEST AUDIT EXECUTION LOG ===\n")
    f.write(f"Timestamp : {datetime.now().isoformat()}\n")
    f.write(f"Command   : {' '.join(cmd)}\n")
    f.write(f"Exit Code : {res.returncode}\n")
    f.write(f"Duration  : {duration:.2f} seconds\n")
    f.write("=" * 60 + "\n\n")
    f.write(output_text)

# Parse passed count from output
passed_count = 0
for line in output_text.splitlines():
    if "passed" in line and ("=" in line or "short test summary" in line):
        print(line)

summary_data = {
    "execution_timestamp_iso": datetime.now().isoformat(),
    "command": " ".join(cmd),
    "exit_code": res.returncode,
    "success": res.returncode == 0,
    "duration_seconds": round(duration, 2),
    "log_file": str(log_file.relative_to(PROJECT_ROOT)),
    "environment": {
        "python_version": sys.version.split()[0],
        "platform": sys.platform
    }
}

with open(summary_json, "w", encoding="utf-8") as f:
    json.dump(summary_data, f, indent=2)

print(f"\n[OK] Log eksekusi berhasil disimpan: {log_file} ({log_file.stat().st_size} bytes)")
print(f"[OK] Ringkasan audit JSON disimpan: {summary_json}")

if res.returncode == 0:
    print("✅ SEMUA PENGUJIAN LULUS 100% SECARA AKTUAL!")
    sys.exit(0)
else:
    print("❌ DITEMUKAN KEGAGALAN DALAM PENGUJIAN!")
    sys.exit(1)
