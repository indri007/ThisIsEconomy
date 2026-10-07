import os
import sys
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class TestDashboardImports(unittest.TestCase):
    def test_import_config(self):
        from dashboard.modules.config import (
            PROJECT_ROOT as CFG_ROOT,
            get_data_path,
            get_result_path,
            get_journal_docx_path,
        )
        self.assertTrue(os.path.exists(CFG_ROOT))
        docx_path = get_journal_docx_path()
        self.assertTrue(os.path.exists(docx_path), f"Journal docx path not found: {docx_path}")

    def test_import_data_loader(self):
        from dashboard.modules.data_loader import (
            load_emotion_data,
            load_network_data,
            load_final_evaluation,
        )
        self.assertTrue(callable(load_emotion_data))
        self.assertTrue(callable(load_network_data))
        self.assertTrue(callable(load_final_evaluation))

    def test_import_ui_components(self):
        from dashboard.modules.ui_components import (
            render_thesis_stepper,
            render_submission_checklist_70_points,
            render_author_biography,
            render_downloads_footer,
        )
        self.assertTrue(callable(render_thesis_stepper))
        self.assertTrue(callable(render_submission_checklist_70_points))
        self.assertTrue(callable(render_author_biography))
        self.assertTrue(callable(render_downloads_footer))

    def test_import_views(self):
        from dashboard.modules.views_bab1 import render_bab1_page
        from dashboard.modules.views_bab2 import render_bab2_page
        from dashboard.modules.views_bab3 import render_bab3_page
        from dashboard.modules.views_bab4 import render_bab4_page
        from dashboard.modules.views_bab5 import render_bab5_page
        from dashboard.modules.views_storytelling import render_storytelling_page
        from dashboard.modules.views_audit import render_audit_page
        from dashboard.modules.views_ews import (
            render_journal_page,
            render_twitter_ai_page,
            render_big_data_page,
            render_ews_page,
            render_brand24_page,
        )
        self.assertTrue(callable(render_bab1_page))
        self.assertTrue(callable(render_bab2_page))
        self.assertTrue(callable(render_bab3_page))
        self.assertTrue(callable(render_bab4_page))
        self.assertTrue(callable(render_bab5_page))
        self.assertTrue(callable(render_storytelling_page))
        self.assertTrue(callable(render_audit_page))
        self.assertTrue(callable(render_journal_page))
        self.assertTrue(callable(render_twitter_ai_page))
        self.assertTrue(callable(render_big_data_page))
        self.assertTrue(callable(render_ews_page))
        self.assertTrue(callable(render_brand24_page))


if __name__ == "__main__":
    unittest.main()
