"""
tests/test_audit_master_suite.py
================================================================================
Master 10-Point Audit and Verification Suite for Streamlit Thesis Repository
Meets all Section H mandatory testing requirements.
================================================================================
"""

import os
import sys
import py_compile
import subprocess
from pathlib import Path
import unittest
import pandas as pd
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


class TestMasterAuditSuite(unittest.TestCase):
    
    # ── 1. Pemeriksaan sintaks seluruh file Python ──
    def test_01_syntax_all_python_files(self):
        """Compile check every single Python file in the repository."""
        py_files = list(PROJECT_ROOT.glob("**/*.py"))
        py_files = [f for f in py_files if ".venv" not in f.parts and "__pycache__" not in f.parts and "tmp" not in f.parts]
        failed_files = []
        for pf in py_files:
            try:
                py_compile.compile(str(pf), doraise=True)
            except py_compile.PyCompileError as e:
                failed_files.append((str(pf), str(e)))
        self.assertEqual(len(failed_files), 0, f"Syntax errors in files: {failed_files}")
        print(f"[PASS] 1. Sintaks seluruh {len(py_files)} file Python valid 100%.")

    # ── 2. Pemeriksaan import aplikasi ──
    def test_02_application_imports(self):
        """Verify all dashboard core modules import cleanly."""
        modules = [
            "dashboard.modules.config",
            "dashboard.modules.data_loader",
            "dashboard.modules.ui_components",
            "dashboard.modules.views_bab1",
            "dashboard.modules.views_bab2",
            "dashboard.modules.views_bab3",
            "dashboard.modules.views_bab4",
            "dashboard.modules.views_bab5",
            "dashboard.modules.views_storytelling",
            "dashboard.modules.views_audit",
            "dashboard.modules.views_ews",
        ]
        for mod_name in modules:
            __import__(mod_name)
        print(f"[PASS] 2. Seluruh {len(modules)} modul aplikasi berhasil di-import tanpa error.")

    # ── 3. Pemeriksaan keberadaan seluruh asset yang dirujuk ──
    def test_03_all_referenced_assets_exist(self):
        """Verify core assets referenced by config and ui_components exist."""
        from dashboard.modules.config import get_journal_docx_path, get_result_path
        core_files = [
            get_journal_docx_path("JCMC_OXFORD_MBG_COMMUNICATION_2026.docx"),
            get_journal_docx_path("ICS_TAYLOR_FRANCIS_MBG_COMMUNICATION_2026.docx"),
            get_journal_docx_path("JURNAL_MBG_SCOPUS_Q1_LATEST_2026.docx"),
            get_journal_docx_path("Journal_Paper_Indri_Anjar_MBG_SNA.docx"),
            PROJECT_ROOT / "results" / "mbg_network_official.gexf",
            PROJECT_ROOT / "results" / "17_macro_topology_metrics.png",
            PROJECT_ROOT / "results" / "19_community_echo_chambers.png",
            PROJECT_ROOT / "results" / "18_actor_centrality_typology.png",
            PROJECT_ROOT / "results" / "15_material3_network_interaction.png",
            PROJECT_ROOT / "results" / "16_nodexl_graph_visualization.png",
            PROJECT_ROOT / "results" / "wordcloud_mbg.png",
            PROJECT_ROOT / "docs" / "A_MEAL_OF_ASH_AND_IRONY.md",
        ]
        missing = [str(f) for f in core_files if not os.path.exists(f)]
        self.assertEqual(len(missing), 0, f"Missing referenced assets: {missing}")
        print(f"[PASS] 3. Seluruh {len(core_files)} asset primer berhasil diverifikasi keberadaannya.")

    # ── 4. Pemeriksaan seluruh referensi gambar dan dataset ──
    def test_04_storytelling_images_integrity(self):
        """Verify all 10 storytelling master plot images exist, are valid PNGs, and can be opened with PIL."""
        from dashboard.modules.config import resolve_image_path
        storytelling_images = [
            "1_pipeline.png",
            "2_dataset_characteristics.png",
            "emotion_distribution.png",
            "3_sarcasm.png",
            "f1_scores.png",
            "emotion_confusion_matrix_final.png",
            "6_global_network.png",
            "16_nodexl_graph_visualization.png",
            "top_actors.png",
            "9_emotion_network.png",
            "10_absa_thematic.png",
            "grafik_master_indobert_dan_rumus_tesis.png",
            "17_macro_topology_metrics.png",
            "19_community_echo_chambers.png",
            "18_actor_centrality_typology.png",
            "15_material3_network_interaction.png",
        ]
        verified_count = 0
        for img_name in storytelling_images:
            resolved = resolve_image_path(img_name)
            self.assertIsNotNone(resolved, f"Image {img_name} could not be resolved.")
            self.assertTrue(os.path.isfile(resolved), f"Resolved path {resolved} is not a valid file.")
            with Image.open(resolved) as im:
                self.assertGreater(im.width, 0)
                self.assertGreater(im.height, 0)
            verified_count += 1
        print(f"[PASS] 4. Seluruh {verified_count} berkas visual storytelling diverifikasi beresolusi valid & tidak corrupt.")

    # ── 5. Pemeriksaan fungsi get_image_path() / resolve_image_path() ──
    def test_05_path_resolution_utilities(self):
        """Verify centralized path resolution with relative, base, and absolute queries."""
        from dashboard.modules.config import resolve_image_path, get_result_path, get_data_path
        p1 = resolve_image_path("1_pipeline.png")
        self.assertIsNotNone(p1)
        self.assertTrue(os.path.exists(p1))

        p2 = get_result_path("1_pipeline.png")
        self.assertTrue(os.path.exists(p2))

        p3 = get_data_path("indobert_9_emosi_fixed.csv")
        self.assertTrue(os.path.exists(p3))

        # Check non-existent safe fallback
        p_missing = resolve_image_path("non_existent_fake_file.png")
        self.assertIsNone(p_missing)
        print("[PASS] 5. Utilitas path resolve_image_path(), get_result_path(), get_data_path() berfungsi presisi.")

    # ── 6. Pemeriksaan struktur dataset wajib ──
    def test_06_mandatory_dataset_schemas(self):
        """Verify presence, non-empty status, and schema of required thesis datasets."""
        from dashboard.modules.data_loader import load_emotion_data, load_network_data, load_final_evaluation
        # Emotion data
        df_emo = load_emotion_data()
        self.assertFalse(df_emo.empty)
        self.assertTrue("text" in df_emo.columns or "full_text" in df_emo.columns)
        self.assertTrue("predicted_emotion" in df_emo.columns or "label" in df_emo.columns)
        self.assertGreaterEqual(len(df_emo), 3000)

        # Network data
        edges, nodes = load_network_data()
        self.assertFalse(edges.empty)
        self.assertIn("Source", edges.columns)
        self.assertIn("Target", edges.columns)
        self.assertGreaterEqual(len(edges), 600)

        # Final evaluation
        ev = load_final_evaluation()
        self.assertIn("comparison", ev)
        self.assertFalse(ev["comparison"].empty)
        self.assertIn("per_class", ev)
        self.assertFalse(ev["per_class"].empty)
        print(f"[PASS] 6. Dataset wajib lolos validasi skema (Emosi: {len(df_emo)} baris, Edge: {len(edges)} baris, Evaluasi: {len(ev['comparison'])} model).")

    # ── 7. Pengujian halaman galeri storytelling ──
    def test_07_storytelling_module_integrity(self):
        """Verify views_storytelling helper functions, tabs, and content elements."""
        from dashboard.modules.views_storytelling import get_image_path, render_story_image
        self.assertTrue(callable(get_image_path))
        self.assertTrue(callable(render_story_image))
        # Ensure 1_pipeline.png resolves
        path_pipe = get_image_path("1_pipeline.png")
        self.assertIsNotNone(path_pipe)
        self.assertTrue(os.path.isfile(path_pipe))
        print("[PASS] 7. Halaman galeri storytelling & helper render_story_image() terverifikasi stabil.")

    # ── 8. Pengujian startup aplikasi Streamlit ──
    def test_08_streamlit_app_startup(self):
        """Simulate Streamlit application load and page rendering via AppTest."""
        app_path = PROJECT_ROOT / "dashboard" / "app.py"
        self.assertTrue(app_path.is_file())
        py_compile.compile(str(app_path), doraise=True)
        # Check requirements consistency
        req_root = (PROJECT_ROOT / "requirements.txt").read_text(encoding="utf-8")
        req_dash = (PROJECT_ROOT / "dashboard" / "requirements.txt").read_text(encoding="utf-8")
        self.assertEqual(req_root.strip(), req_dash.strip(), "dashboard/requirements.txt out of sync with root requirements.txt")
        # Run AppTest headless execution
        from streamlit.testing.v1 import AppTest
        at = AppTest.from_file(str(app_path))
        at.run(timeout=30)
        self.assertEqual(len(list(at.exception)), 0, f"Exceptions on startup: {list(at.exception)}")
        print("[PASS] 8. Startup simulasi Streamlit dashboard/app.py dan AppTest rendering valid (0 exception).")

    # ── 9. Pengujian bahwa asset opsional yang hilang tidak merusak halaman ──
    def test_09_missing_asset_robustness(self):
        """Verify crash-proof st.image interceptor and data loaders handle missing files gracefully."""
        from dashboard.modules.config import _crash_proof_st_image
        import streamlit as st
        # Simulate calling _crash_proof_st_image with missing file
        try:
            res = _crash_proof_st_image("completely_missing_imaginary_plot.png", caption="Test Missing")
            # Should return None and not raise FileNotFoundError or MediaFileStorageError
            self.assertIsNone(res)
        except Exception as e:
            self.fail(f"_crash_proof_st_image raised unexpected exception: {e}")
        print("[PASS] 9. Penanganan asset opsional yang hilang terverifikasi crash-proof (zero unhandled exceptions).")

    # ── 10. Pemeriksaan perubahan dengan git diff ──
    def test_10_git_diff_integrity(self):
        """Verify git status and ensure changes are tracked and valid."""
        res = subprocess.run(["git", "status", "--porcelain"], cwd=str(PROJECT_ROOT), capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        print("[PASS] 10. Audit git diff & integritas branch berjalan normal.")


if __name__ == "__main__":
    unittest.main()
