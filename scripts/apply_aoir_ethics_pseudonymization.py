#!/usr/bin/env python3
"""
apply_aoir_ethics_pseudonymization.py
======================================
Implements Point 3: Internet Research Ethics & AoIR Pseudonymization Protocol
(Franzke et al., 2020; Zimmer, 2010).

Distinguishes:
  1. Public Institutional Entities & Machine Agents (Identified explicitly):
     - @prabowo (Head of State)
     - @grok (Autonomous AI Agent)
     - @gerindra (Ruling Political Party)
     - @kemdikbud_ri (Ministry of Education)
     - @tempodotco (Investigative Media Outlet)
     - @banten_pemprov (Provincial Government)
     - @tanyakanrl, @tanyarlfes (Public Autobase Feeds)
     - @direktoridosen (Academic Directory Hub)
     - @gibran_tweet (Vice Presidential Public Figure)

  2. Private Citizen Accounts (Pseudonymized for privacy & protection under UU ITE):
     - @4Y4NKZ -> [Citizen_Satirist_16]
     - @newIding30 -> [Citizen_Discussant_16]
     - @Capitalisborju -> [Citizen_Critic_16]
     - @dbdbidip -> [Citizen_Parent_259]
     - @greeniefloo -> [Citizen_Parent_259B]
     - @renregalia -> [Citizen_Parent_259C]
     - @Casagrande10939 -> [Citizen_Observer_08]
     - @SauloLinsFreir1 -> [Citizen_Observer_08B]
     - @luvdysh_ -> [Citizen_Student_264]
     - @helloyosh_ -> [Citizen_Student_264B]
     - @ayiurswoo -> [Citizen_Student_264C]
     - @mBg_JK -> [Citizen_Watchdog_314]
     - @regar_op0sisi -> [Citizen_Commentator_15]
     - @punishe98373138 -> [Citizen_Evaluator_15]
     - @daffiriffi -> [Citizen_Retweeter_15]
     - @ryookaasan -> [Citizen_Influencer_335]
     - @deluxe_melissa -> [Citizen_Influencer_212]
     - @multibank_io -> [Commercial_Account_56]
     - @bbiiyaya -> [Citizen_Student_05]
     - @kenzowijay46299 -> [Citizen_Observer_44]
     - @eisbedog -> [Citizen_Observer_185]
     - @Giziiii21 -> [Citizen_Observer_03]
     - @ctrlaltdel_77 -> [Citizen_Observer_37]
     - @Marshabeara9x2 -> [Citizen_Observer_261]
     - @AjuntamentVLC -> [Public_Municipality_VLC]

Outputs:
  - results/sna_canonical_pipeline/canonical_top25_actors_aoir_pseudonymized.csv
  - results/AOIR_ETHICAL_PSEUDONYMIZATION_REPORT.json
  - results/AOIR_ETHICAL_PSEUDONYMIZATION_REPORT.md
"""

import os
import json
import pandas as pd

BASE_DIR = "/Users/jevin/ThisIsEconomy"
RESULTS_DIR = os.path.join(BASE_DIR, "results")
SNA_DIR = os.path.join(RESULTS_DIR, "sna_canonical_pipeline")

PUBLIC_ENTITIES = {
    "@prabowo": "Head of State (Presidential Office)",
    "@grok": "Autonomous AI Agent (Epistemic Oracle)",
    "@gerindra": "Ruling Political Party",
    "@kemdikbud_ri": "Ministry of Education & Culture",
    "@tempodotco": "Independent Investigative News Outlet",
    "@banten_pemprov": "Provincial Government Account",
    "@tanyakanrl": "Public Automated Discussion Feed (Autobase)",
    "@tanyarlfes": "Public Automated Discussion Feed (Autobase)",
    "@direktoridosen": "Scholarly Directory Hub",
    "@gibran_tweet": "Vice Presidential Political Account",
    "@AjuntamentVLC": "Official Public Municipality Account"
}

CITIZEN_PSEUDONYM_MAP = {
    "@4Y4NKZ": "[Citizen_Satirist_16]",
    "@newIding30": "[Citizen_Discussant_16]",
    "@Capitalisborju": "[Citizen_Critic_16]",
    "@dbdbidip": "[Citizen_Parent_259]",
    "@greeniefloo": "[Citizen_Parent_259B]",
    "@renregalia": "[Citizen_Parent_259C]",
    "@Casagrande10939": "[Citizen_Observer_08]",
    "@SauloLinsFreir1": "[Citizen_Observer_08B]",
    "@luvdysh_": "[Citizen_Student_264]",
    "@helloyosh_": "[Citizen_Student_264B]",
    "@ayiurswoo": "[Citizen_Student_264C]",
    "@mBg_JK": "[Citizen_Watchdog_314]",
    "@regar_op0sisi": "[Citizen_Commentator_15]",
    "@punishe98373138": "[Citizen_Evaluator_15]",
    "@daffiriffi": "[Citizen_Retweeter_15]",
    "@ryookaasan": "[Citizen_Influencer_335]",
    "@deluxe_melissa": "[Citizen_Influencer_212]",
    "@multibank_io": "[Commercial_Account_56]",
    "@bbiiyaya": "[Citizen_Student_05]",
    "@kenzowijay46299": "[Citizen_Observer_44]",
    "@eisbedog": "[Citizen_Observer_185]",
    "@Giziiii21": "[Citizen_Observer_03]",
    "@ctrlaltdel_77": "[Citizen_Observer_37]",
    "@Marshabeara9x2": "[Citizen_Observer_261]",
    "@unmagnetism": "[Citizen_Inquirer_61]",
    "@JuanJulianto2": "[Citizen_Inquirer_61B]"
}

def get_aoir_display_label(handle):
    if handle in PUBLIC_ENTITIES:
        return handle
    return CITIZEN_PSEUDONYM_MAP.get(handle, f"[Citizen_User_{handle.strip('@')[:4]}]")

def process_canonical_top25():
    csv_path = os.path.join(SNA_DIR, "canonical_top25_actors.csv")
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return None

    df = pd.read_csv(csv_path)
    
    df["Raw_Handle"] = df["Label"]
    df["Ethical_Entity_Type"] = df["Label"].apply(lambda h: "Public Authority / Media / AI" if h in PUBLIC_ENTITIES else "Private Citizen Account")
    df["AoIR_Pseudonym_Label"] = df["Label"].apply(get_aoir_display_label)
    
    out_csv = os.path.join(SNA_DIR, "canonical_top25_actors_aoir_pseudonymized.csv")
    df.to_csv(out_csv, index=False)
    print(f"[OK] Saved pseudonymized CSV: {out_csv}")
    
    # Generate audit report
    audit_data = {
        "protocol": "Association of Internet Researchers (AoIR) Ethical Guidelines 3.0",
        "rationale": (
            "To safeguard ordinary citizens from online harassment, doxxing, and legal retribution under "
            "restrictive speech frameworks (Indonesia's UU ITE), all private accounts are pseudonymized. "
            "Only verified institutional entities, public officials, news media, and algorithmic utilities "
            "remain explicitly identified."
        ),
        "total_top25_actors": len(df),
        "public_entities_count": int((df["Ethical_Entity_Type"] == "Public Authority / Media / AI").sum()),
        "pseudonymized_citizens_count": int((df["Ethical_Entity_Type"] == "Private Citizen Account").sum()),
        "mapping_table": df[["Label", "AoIR_Pseudonym_Label", "Ethical_Entity_Type", "Communication_Role"]].to_dict(orient="records")
    }
    
    json_path = os.path.join(RESULTS_DIR, "AOIR_ETHICAL_PSEUDONYMIZATION_REPORT.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(audit_data, f, indent=2)
    print(f"[OK] Saved JSON report: {json_path}")
    
    md_path = os.path.join(RESULTS_DIR, "AOIR_ETHICAL_PSEUDONYMIZATION_REPORT.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# 🛡️ AOIR ETHICAL PSEUDONYMIZATION AUDIT REPORT\n")
        f.write("### Research Ethics & Internet Privacy Compliance (AoIR 3.0 & GDPR Principles)\n\n")
        f.write(f"- **Protocol:** {audit_data['protocol']}\n")
        f.write(f"- **Public Entities Retained:** {audit_data['public_entities_count']} accounts (Public accountability justification)\n")
        f.write(f"- **Private Citizens Pseudonymized:** {audit_data['pseudonymized_citizens_count']} accounts (Privacy & legal protection)\n\n")
        f.write("## 📋 Mapping Table: Raw Handles vs. Ethical Pseudonyms\n\n")
        f.write("| Rank | Raw Handle | AoIR Pseudonym Label | Ethical Entity Type | Communicative Function |\n")
        f.write("|:---:|:---|:---|:---|:---|\n")
        for i, item in enumerate(audit_data["mapping_table"], 1):
            f.write(f"| {i} | `{item['Label']}` | **`{item['AoIR_Pseudonym_Label']}`** | {item['Ethical_Entity_Type']} | {item['Communication_Role']} |\n")
        f.write("\n---\n")
        f.write("### Ethical References:\n")
        f.write("- Franzke, A. S., Bechmann, A., Zimmer, M., Ess, C., & AoIR. (2020). *Internet research: Ethical guidelines 3.0*. Association of Internet Researchers.\n")
        f.write("- Zimmer, M. (2010). 'But the data is already public': On the ethics of research in Facebook and social computing. *Ethics and Information Technology*, 12(4), 313–325.\n")
    print(f"[OK] Saved Markdown report: {md_path}")
    
    return audit_data

if __name__ == "__main__":
    process_canonical_top25()
