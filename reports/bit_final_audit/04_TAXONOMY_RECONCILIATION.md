# BIT AUDIT PHASE 4: TEMPORAL TAXONOMY AND "LOVE" LABEL RECONCILIATION REPORT

**Audit Date:** 2026-10-13T18:10:45+07:00  
**Target Corpora:** 
1. Longitudinal Surveillance Timeline Corpus ($N = 9,360$, Jan – Oct 2026)
2. Master IndoBERT NLP Classification Corpus ($N = 5,272$, Full Fine-Tuning)

---

## 1. Provenance of the Longitudinal 9,360 Corpus

The 9,360 dataset represents an out-of-sample longitudinal temporal tracking stream harvested across 10 months (January – October 2026) to map crisis evolution and the Double-Peak Crisis phenomenon:
- **Peak I (May 2026):** 3,157 tweets (Suspension of 4,581 SPPG catering kitchens).
- **Peak II (September 2026):** 4,661 tweets (National outbreak of 43,838 poisoned students).
- **Inter-crisis Monitoring (Other Months):** 1,542 tweets.
- **Total Accumulation:** $3,157 + 4,661 + 1,542 = 9,360$ posts.

---

## 2. Origin and Meaning of the "Love" (*Cinta*) Label

In the longitudinal surveillance breakdown, the 9,360 tweets were categorized under a 3-way operational crisis surveillance schema:
- **Jijik (Moral Disgust):** 9,189 tweets (**98.17%**)
- **Cinta (Love / Gratitude):** 162 tweets (**1.73%**)
- **Netral (Neutral / Objective):** 9 tweets (**0.10%**)
- **Total Mathematical Reconciliation:** $9,189 + 162 + 9 = \mathbf{9,360}$ (**100.00%**).

### Theoretical Origin:
* **Linguistic Indicators of Love ($n=162$):** *"terima kasih", "relawan dapur", "ibu kantin", "berkah", "senang", "lezat", "alhamdulillah"*.
* **Pragmatic Context:** Civic expressions of genuine appreciation toward grassroots volunteers and school kitchen cooks who served meals diligently despite institutional budget constraints.
* **Why "Love" is Absent from the 9-Emotion Master Set ($N=5,272$):**
  * Under **Plutchik's (1980) Psychoevolutionary Wheel of Emotions**, "Love" is a **Secondary Dyad** formed by the fusion of **Joy (*Bahagia*) + Trust (*Percaya*)**.
  * When constructing the master NLP classification taxonomy ($N=5,272$), rigorous psychological ontology required decomposing secondary dyads into primary affective vectors:
    - Civic program endorsements were mapped to **Percaya (Trust, $n=1,059$)**.
    - Explicit celebratory statements were mapped to **Bahagia (Joy, $n=76$)**.
* **Integrity Directive:** "Love" was **NOT** retroactively or silently renamed to "Bahagia" without justification; rather, the surveillance monitoring used a vernacular tag (*Cinta/Gratitude*), whereas the formal transformer pipeline strictly adheres to Plutchik's primary emotion taxonomy.

---

## 3. Taxonomy Separation Summary

| Dimension | Longitudinal Surveillance Corpus | Master NLP Classification Corpus |
| :--- | :---: | :---: |
| **Sample Size ($N$)** | **9,360** | **5,272** |
| **Observation Period** | Jan 1 – Oct 10, 2026 | Oct 2024 – Oct 2026 |
| **Taxonomy Model** | 3-Way Crisis Surveillance (Disgust, Love, Neutral) | 9-Emotion Plutchik Primary Taxonomy |
| **Handling of Affection** | Standalone category `Cinta` ($n=162, 1.73\%$) | Decomposed into `Percaya` ($20.09\%$) & `Bahagia` ($1.44\%$) |
| **Primary Scientific Role** | Epidemiological & temporal timeline modeling | Contextual language model fine-tuning & evaluation |

---

## 4. Audit Status
* **Provenance Status:** **`VERIFIED`**
* **Cross-Taxonomy Contamination:** **`NONE`** (Both corpora serve distinct, documented methodological objectives).
