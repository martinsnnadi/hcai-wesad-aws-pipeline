# WESAD Silver Data Quality Framework

**Track**: Week 12 Data Quality Framework  
**Workspace**: AWS S3 (`hcai-wesad-silver-audited`)  

---

### 1. Reusable Testing Rules
*   **Uniqueness**: Enforces 0 duplicate timestamps per subject stream through structured indexing.
*   **Completeness**: Restricts row-level missingness to a strict 0.00% null threshold.
*   **Validity**: Verifies `affect_label` stays bounded within active research classes (1=Neutral, 2=Stress, 3=Amusement).
*   **Integrity**: Confirms 0 orphaned rows exist by validation checks against subject IDs.

---

### 2. Automated Production Scorecard
*   **UNIQUENESS**: 0 duplicate key violations. Status: **PASS**.
*   **COMPLETENESS**: 0.00% row-level null rate across full cohort. Status: **PASS**.
*   **VALIDITY**: 0 out-of-bounds records. Status: **PASS**.
*   **INTEGRITY**: 0 orphaned records found. Status: **PASS**.
*   **VOLUME CHECK**: 33,152 total verified 1 Hz epoch entries indexed in cloud storage. Status: **PASS**.

---

### 3. Key Data Issues & Follow-Up Actions

#### Issue 1: Out-of-Bounds Label Leakage
*   **Finding**: Initial validation scans flagged 14,209 invalid rows breaching active research categories.
*   **Root Cause**: Raw data tracks auxiliary conditions like Meditation (Code 4) and transient rest intervals (Codes 5-7). Meditation is highly sparse (missing for 33% of subjects) and rest intervals contain dead-air noise.
*   **Remediation**: Deployed an in-flight filter loop using `.isin()` to prune out codes 4–7. This focused the dataset strictly on the 33,152 clean target rows to prevent model class imbalance.


