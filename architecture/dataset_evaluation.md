# WESAD Dataset Evaluation & Strategic Scoping

---

## 1. Access, Licensing & Volume Statistics

Publicly sourced via the UCI Machine Learning Repository. Openly available for academic research, education, and development under attribution guidelines. 

The raw data footprint evaluates to **~500 MB compressed, expanding to a massive 16,763.98 MB (16.37 GB) footprint across 76 uncompressed multi-modal object blobs** in cloud storage.

### Biometric HCAI Risk Assessment
While free of text-based Personally Identifiable Information (PII) like names, the dataset captures raw high-frequency human physiological telemetry. This functions as a distinct **Biometric Signature Marker**. To secure participant privacy, the pipeline enforces a strict identity isolation boundary using AWS IAM bucket rules, ensuring subject identifiers ($S2$ through $S17$) cannot be cross-referenced with external data layers.

---

## 2. Technical Profile & Multi-Sensor Scale

The telemetry dataset tracks continuous synchronised physiological streams from 15 human participants across two distinct hardware modalities:
*   **RespiBan Chest Device (700 Hz)**: 700 readings per second tracking Electrocardiogram (ECG), Electrodermal Activity (EDA), Electromyogram (EMG), Respiration, and 3-axis Accelerometer data.
*   **Empatica E4 Wristband**: Multi-frequency streams capturing Blood Volume Pulse (BVP @ 64 Hz), EDA (@ 4 Hz), Ambient Skin Temperature (@ 4 Hz), and Accelerometer (@ 32 Hz).

### Engineering Opportunities
*   **Storage Foundations**: Provisioning secure, private append-only landing zones inside Amazon S3.
*   **Memory Management**: Engineering zero-disk, low-memory streaming chunk buffers to extract heavy, nested Python Pickle files (`.pkl`) without triggering container memory crashes.
*   **Signal Alignment**: Designing down-sampling and windowing functions to reconcile 700 Hz chest sensors with 4 Hz wrist readings.
*   **Pipeline Orchestration**: Automating and scheduling ingestion workflows using Apache Airflow DAGs.

---

## 3. Research Relevance & HCAI Model Drift Guardrails

Directly supports Prof. Oyelere’s core research into hybrid intelligence, collaborative AI design, and human wellbeing. Rather than tracking digital click logs, this framework captures subconscious physical responses to stress and emotional states.

### The Model Drift Blocker & Personalisation Solution
Standard automated AI stress models frequently suffer from accuracy failures due to natural baseline physiological variations between individual human bodies. A model trained on raw sensor readings from one subject will misclassify another. 

To prevent model drift and protect user safety, this pipeline prepares the storage partitions to enforce **Individualised Baseline Standardisation**. By computing the specific statistical mean and standard deviation of each subject's rest state, the framework normalises signals before they reach machine learning layers.

---

## 4. Data Quality Challenges (The Structural Hurdles)

WESAD introduces complex, highly volatile data engineering obstacles:
*   **Serialised Binary Formats**: Core streams are locked inside nested `.pkl` arrays. These are unreadable by standard relational SQL databases and require Python/PySpark compute clusters to parse.
*   **Extreme High-Volume Noise**: Raw ECG and EMG signals capture physical movement artefacts. The infrastructure must be optimised to compute rolling window averages, smoothing filters, and signal metrics.
*   **Asynchronous Timestamps**: Mismatched sampling frequencies (4 Hz up to 700 Hz) require the pipeline to downsample streams into uniform chronological bins without dropping critical medical indicators.

---

## 5. Portfolio & Architectural Value

Moves beyond basic, generic data science code templates to demonstrate production-grade cloud data engineering:
*   **Enterprise Architecture**: Implements a highly resilient AWS data lake framework using Amazon S3, Boto3, and containerized Python streaming logic.
*   **Advanced Patterns**: Builds functional engines to handle non-relational hardware streams, parse asynchronous multi-modal time-series intervals, and map binary arrays at scale.
*   **HCAI Premium**: Showcases critical, high-demand industry competencies in data minimisation, privacy compliance, and storage lifecycle asset management.

---

## 6. References

1. Schmidt, P. et al. (2018) 'Introducing WESAD: A Multimodal Dataset for Wearable Stress and Affect Detection', *Proceedings of the 20th ACM International Conference on Multimodal Interaction (ICMI '18)*, pp. 400-408.
2. Oyelere, S. S. et al. (2026) 'A Scoping Review of Hybrid Intelligence Systems for Human-Centred AI in Education', *Computers in Human Behavior*, 150.
3. Shneiderman, B. (2021) 'Human-Centered Artificial Intelligence: Reliable, Safe & Trustworthy', *International Journal of Human–Computer Interaction*, 37(6), pp. 479-491.
