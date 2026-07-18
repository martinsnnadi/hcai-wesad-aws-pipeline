# WESAD Time-Alignment & Completeness Summary

**Workspace**: AWS S3 (`hcai-wesad-silver-audited`)  
**Target**: Full Cohort Matrix (S2–S17)

---

### 1. Sampling Rate Harmonisation 
*   **Assumption**: Varying frequencies (4 Hz to 700 Hz) prevent relational joins. Aggregating to 1-second (1 Hz) windows cuts memory load and saves features.
*   **Action**: Ran rolling means on 700 Hz chest sensors and matched them to 1-second wrist averages. Script loops across all subjects (S2–S17) for full cohort coverage.

### 2. Behavior Label Syncing
*   **Assumption**: Compressing 700 Hz affect labels to 1-second windows requires finding the dominant emotional state.
*   **Action**: Applied a statistical mode calculation over each 1-second grouped timestamp window to align classifications.

### 3. Data Pruning
*   **Assumption**: Label rows marked `0` are background intervals between tasks with no analytical value.
*   **Action**: Filtered out all `affect_label == 0` records. Retained only active Neutral, Stressed, and Amused human states.

### 4. Infrastructure Isolation
*   **Assumption**: Medallion standards require complete storage isolation between raw data and conformed analytics.
*   **Action**: Provisioned a distinct S3 bucket (`hcai-wesad-silver-audited`) in region `eu-west-2`. Appended `subject_id` and `pipeline_conformance_ts` to every conformed row.
