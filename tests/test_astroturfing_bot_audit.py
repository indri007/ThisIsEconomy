"""
test_astroturfing_bot_audit.py
==============================
Unit tests for Point 4: Astroturfing Detection & Coordinated Inauthentic Behavior (CIB) Audit.
Verifies the 5 forensic pillars establishing authentic grassroots civic discourse:
  1. Lexical Diversity & Zero Verbatim Scripted Copypasta (Ferrara et al., 2016)
  2. Grassroots Long-Tail User Distribution (Cresci et al., 2017)
  3. Biological Circadian Diurnal Activity Cycle (Keller et al., 2020)
  4. Network Structural Incompatibility with Astroturfing Rings (Giglietto et al., 2020)
  5. Machine Agent Profiling & Transparent AI Isolation
"""

import os
import json
import pytest

BASE_DIR = "/Users/jevin/ThisIsEconomy"
RESULTS_DIR = os.path.join(BASE_DIR, "results")
JSON_REPORT = os.path.join(RESULTS_DIR, "ASTROTURFING_AND_BOT_AUDIT_REPORT.json")
MD_REPORT = os.path.join(RESULTS_DIR, "ASTROTURFING_AND_BOT_AUDIT_REPORT.md")


def test_audit_reports_exist():
    assert os.path.exists(JSON_REPORT), f"Missing JSON report at {JSON_REPORT}"
    assert os.path.exists(MD_REPORT), f"Missing Markdown report at {MD_REPORT}"


def test_pillar_1_copypasta_and_lexical_diversity():
    with open(JSON_REPORT, "r", encoding="utf-8") as f:
        data = json.load(f)
    p1 = data["pillar_1_copypasta_test"]
    assert p1["verbatim_duplicates_clean_text"] == 0, "Expected 0 duplicate cleaned tweets"
    assert p1["duplicate_rate_percent"] == 0.0, "Duplicate rate must be 0.0%"
    assert p1["type_token_ratio_ttr"] > 0.15, "TTR should demonstrate rich lexical diversity (> 0.15)"
    assert "PASSED" in p1["verdict"]


def test_pillar_2_grassroots_participation():
    with open(JSON_REPORT, "r", encoding="utf-8") as f:
        data = json.load(f)
    p2 = data["pillar_2_participation_distribution"]
    assert p2["single_post_percentage"] > 80.0, "Single post users must exceed 80% (grassroots long-tail)"
    assert p2["median_posts_per_author"] == 1.0, "Median posts per author must be 1.0"
    assert "PASSED" in p2["verdict"]


def test_pillar_3_circadian_rhythm():
    with open(JSON_REPORT, "r", encoding="utf-8") as f:
        data = json.load(f)
    p3 = data["pillar_3_circadian_rhythm"]
    assert p3["nocturnal_sleep_rate_percent"] < 15.0, "Nighttime activity (00:00-05:00) should be low (< 15%)"
    assert p3["daytime_peak_rate_percent"] > 40.0, "Daytime activity (11:00-18:00) should peak (> 40%)"
    assert p3["diurnal_contrast_ratio"] > 3.0, "Day/night ratio must show human circadian sleep rhythm (> 3x)"
    assert "PASSED" in p3["verdict"]


def test_pillar_4_network_incompatibility():
    with open(JSON_REPORT, "r", encoding="utf-8") as f:
        data = json.load(f)
    p4 = data["pillar_4_network_incompatibility"]
    assert p4["density"] < 0.005, "Graph density must be sparse (< 0.005)"
    assert p4["reciprocity"] < 0.05, "Reciprocity must be minimal (< 5%, refuting astroturfing retweet rings)"
    assert p4["louvain_modularity"] > 0.90, "Modularity must be high (> 0.90, decentralized communities)"


def test_pillar_5_machine_agent_profiling():
    with open(JSON_REPORT, "r", encoding="utf-8") as f:
        data = json.load(f)
    p5 = data["pillar_5_machine_agent_profiling"]
    assert p5["covert_political_botnets_detected"] == 0, "No covert political botnets allowed"
    assert p5["grok_corpus_share_percent"] < 2.0, "@grok share must be limited (< 2%)"
    assert "PASSED" in p5["verdict"]
    assert "AUTHENTIC ORGANIC PUBLIC DISSENT" in data["overall_forensic_verdict"]
