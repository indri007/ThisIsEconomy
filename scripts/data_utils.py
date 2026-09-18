import os
import sys

# Compute project root dynamically: directory containing 'scripts', 'data', 'dashboard'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Automatically add PROJECT_ROOT to sys.path so modules can be imported from anywhere
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def get_data_path(filename_or_relative_path):
    """
    Universally resolves dataset file paths regardless of the current working directory.
    Searches PROJECT_ROOT, data/, results/, and common subdirectories.
    """
    candidates = [
        os.path.join(PROJECT_ROOT, filename_or_relative_path),
        filename_or_relative_path,
        os.path.join(PROJECT_ROOT, "data", filename_or_relative_path),
        os.path.join(PROJECT_ROOT, "results", filename_or_relative_path),
        os.path.join(PROJECT_ROOT, "data", "results", filename_or_relative_path),
        os.path.join(PROJECT_ROOT, "data", "emotion", filename_or_relative_path),
        os.path.join(PROJECT_ROOT, "data", "sarcasm", filename_or_relative_path),
        os.path.join(PROJECT_ROOT, "data", "sna", filename_or_relative_path),
        os.path.join(PROJECT_ROOT, "data", "processed", filename_or_relative_path),
        os.path.join("..", filename_or_relative_path),
        os.path.join("..", "data", filename_or_relative_path),
        os.path.join("..", "results", filename_or_relative_path),
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    # Default to project root join if not yet created
    return os.path.abspath(os.path.join(PROJECT_ROOT, filename_or_relative_path))

def get_result_path(filename_or_relative_path):
    """
    Resolves output result paths inside the results/ directory.
    """
    candidates = [
        os.path.join(PROJECT_ROOT, "results", filename_or_relative_path),
        os.path.join(PROJECT_ROOT, "results", "storytelling", filename_or_relative_path),
        filename_or_relative_path,
        os.path.join("results", filename_or_relative_path),
        os.path.join("..", "results", filename_or_relative_path),
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    return os.path.abspath(os.path.join(PROJECT_ROOT, "results", filename_or_relative_path))

# Ensure current working directory is PROJECT_ROOT if run directly
def ensure_project_root():
    if os.getcwd() != PROJECT_ROOT:
        os.chdir(PROJECT_ROOT)
