import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

print("ROOT =", ROOT)

from ews import ews_engine

print("EWS_IMPORT=PASS")
print("EWS_MODULE =", ews_engine.__file__)
