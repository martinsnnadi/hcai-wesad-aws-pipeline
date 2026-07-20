# WESAD Time-Alignment & Completeness Summary

**Workspace**: AWS S3 (`hcai-wesad-silver-audited`)  
**Target**: Full Cohort Matrix (S2–S17)

---

### 1. Sampling Rate Harmonisation & Production Outputs
*   **Assumption**: Varying frequencies (4 Hz to 700 Hz) prevent relational joins. Aggregating to 1-second (1 Hz) windows cuts memory load and preserves medical tracking features.
*   **Action**: Ran rolling means on 700 Hz chest sensors and matched them to 1-second wrist averages. Script looped across all valid subjects to write clean `.csv` matrices directly to the Silver S3 layer.

### 📊 Verified Production Ingestion Scorecard
The scale-out pipeline successfully processed and conformed the full dataset:
*   **S2**: 3,018 conformed rows
*   **S3**: 3,142 conformed rows
*   **S4**: 3,117 conformed rows
*   **S5**: 3,197 conformed rows
*   **S6**: 3,166 conformed rows
*   **S7**: 3,135 conformed rows
*   **S8**: 3,157 conformed rows
*   **S9**: 3,172 conformed rows
*   **S10**: 3,226 conformed rows *(Testing baseline marker)*
*   **S11**: 3,171 conformed rows
*   **S13**: 3,124 conformed rows
*   **S14**: 3,212 conformed rows
*   **S15**: 3,115 conformed rows
*   **S16**: 3,153 conformed rows
*   **S17**: 3,181 conformed rows
*   **S1, S12**: Excluded entirely due to hardware drops and sensor calibration failures.

---

### 2. Behavior Label Syncing
*   **Assumption**: Compressing 700 Hz affect labels to 1-second windows requires isolating the dominant emotional state within that timeframe.
*   **Action**: Applied a statistical mode calculation over each 1-second grouped timestamp window to lock down true alignment states.

### 3. Data Pruning
*   **Assumption**: Label rows marked `0` are transient background intervals between tasks with no analytical value.
*   **Action**: Filtered out all `affect_label == 0` records. Retained only active Neutral (1), Stressed (2), and Amused (3) human behavioral states.

### 4. Infrastructure Isolation
*   **Assumption**: Medallion standards require complete storage isolation between raw files and conformed analytics tables.
*   **Action**: Provisioned a distinct S3 bucket (`hcai-wesad-silver-audited`) in region `eu-west-2`. Appended `subject_id` and `pipeline_conformance_ts` lineage tokens to every row.
