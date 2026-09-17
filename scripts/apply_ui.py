import sys

def inject_css(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Check if already injected
    if "def apply_material3_theme():" in content:
        print("CSS already injected.")
        return

    css_code = """
def apply_material3_theme():
    st.markdown('''
    <style>
    /* Google Fonts: Roboto (Material 3 standard) */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif !important;
    }
    
    /* Material 3 Card Elevation & Radius for Images */
    img {
        border-radius: 16px !important;
        box-shadow: 0 4px 8px 3px rgba(0,0,0,0.15) !important;
        transition: transform 0.3s cubic-bezier(0.2, 0, 0, 1) !important;
        margin-bottom: 20px !important;
    }
    img:hover {
        transform: scale(1.02) !important;
    }
    
    /* Material 3 Buttons (Filled tonal / Primary) */
    .stButton>button {
        border-radius: 100px !important;
        border: none !important;
        background-color: #6750A4 !important;
        color: #FFFFFF !important;
        padding: 10px 24px !important;
        font-weight: 500 !important;
        box-shadow: 0 1px 3px 1px rgba(0,0,0,0.15), 0 1px 2px 0 rgba(0,0,0,0.3) !important;
        transition: all 0.2s cubic-bezier(0.2, 0, 0, 1) !important;
    }
    .stButton>button:hover {
        background-color: #4F378B !important;
        box-shadow: 0 2px 6px 2px rgba(0,0,0,0.15), 0 1px 2px 0 rgba(0,0,0,0.3) !important;
    }
    
    /* Info boxes (Alerts) styled as M3 Surface Containers */
    div[data-testid="stMarkdownContainer"] > div.stAlert {
        border-radius: 16px !important;
        border: none !important;
        background-color: #F4EFF4 !important;
        color: #1C1B1F !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
    }
    
    /* Header Typography M3 styling */
    h1, h2, h3 {
        color: #1C1B1F !important;
        letter-spacing: -0.02em !important;
    }
    
    /* Main Background & Sidebar */
    .stApp {
        background-color: #FFFBFE !important;
    }
    [data-testid="stSidebar"] {
        background-color: #F4EFF4 !important;
        border-right: none !important;
    }
    </style>
    ''', unsafe_allow_html=True)
"""
    
    # Insert right after st.set_page_config
    parts = content.split("st.set_page_config(")
    if len(parts) > 1:
        part2 = parts[1].split(")\n", 1)
        if len(part2) > 1:
            new_content = parts[0] + "st.set_page_config(" + part2[0] + ")\n" + css_code + "\napply_material3_theme()\n" + part2[1]
            with open(filepath, 'w') as f:
                f.write(new_content)
            print("Successfully injected Material 3 CSS.")
            return

    print("Could not find insertion point.")

inject_css('dashboard/app.py')
