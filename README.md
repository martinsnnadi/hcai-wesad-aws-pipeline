# 🛰️ Multimodal Biometric Ingestion Infrastructure (WESAD)
### HCAI Data Pipeline Track | Version 1.1 (Amazon AWS)

**Academic Supervisor:** Professor Solomon Sunday Oyelere  
**Project Horizon:** 24-Week Parallel Processing Research Roadmap  
**Current Milestone:** Week 8 (Bronze Layer Validation & Inventory Enforcement)

---

## 1. Project & Dataset Review

This track focuses on building a secure, high-integrity data infrastructure for the Wearable Stress Detection (WESAD) dataset under the academic supervision of Professor Solomon Sunday Oyelere.

### 1.1 Technical Profile
*   **Domain:** Digital Health / Wearable Computing & Wellbeing.
*   **Source Engine:** Multimodal biometric sensor streams from 15 human participants.
*   **Telemetry Data Scale:** High-frequency raw data capturing continuous physiological signals: RespiBan Chest Device (ECG, EDA, EMG, Respiration sampled at 700 Hz) and Empatica E4 Wristband (BVP at 64Hz, EDA at 4Hz, Temp at 4Hz, ACC at 32Hz).
*   **Verified Storage Footprint:** Uncompressed binary telemetry expands to **16,763.98 MB (16.37 GB)** safely distributed across **76 verified object blobs** within our cloud staging tier.

### 1.2 Human-Centred AI (HCAI) Risk Assessment
*   **Model Drift Safety:** Standard AI stress-prediction models suffer from critical accuracy failures due to natural, baseline physiological differences between individual human bodies. A model trained on raw variables of one subject will instantly misclassify another.
*   **The HCAI Guardrail:** This pipeline sets up the environment to enforce Individualised Baseline Standardisation. By computing the specific statistical mean and standard deviation of each subject's rest state, it normalizes sensor drifts before data passes to machine learning layers.
*   **Biometric Identity Isolation:** To prevent individual tracking fingerprinting, the raw hardware streams are completely decoupled from downstream consumption using strict AWS Identity and Access Management (IAM) bucket boundaries.

---

## 2. Ingestion Breakthrough: Zero-Disk, Low-Memory Streaming Double-Bridge

During the active ingestion execution phase, downloading and unpacking the binary telemetry package triggered severe resource bottlenecks on standard cloud compute nodes:
*   **Disk Bottleneck (Errno 28):** The container ran out of local scratch space while attempting to unzip the files onto the native drive.
*   **Memory Bottleneck (Killed):** Bypassing the disk and loading the complete uncompressed archive into system RAM instantly triggered the Linux Out-of-Memory (OOM) Killer.

### ⚙️ The Multi-Part Streaming Architecture
To resolve these hardware constraints, the pipeline was refactored into a continuous, event-driven stream processing architecture across four synchronized layers:
1.  **The 64 KB Intake Valve:** Maintains a microscopic, fixed network memory buffer, pulling binary byte fragments from the repository server to keep the overall RAM footprint near zero.
2.  **On-The-Fly De-serialization:** Dynamically parses zip archive headers sequentially, unzipping the sensor data fragments directly in mid-air as they pass through the network card interface.
3.  **The Chunk-Size Normalizer:** Intercepts unzipped streams (such as the 900 MB serialized S10.pkl arrays) and repackages them into exact byte blocks expected by the AWS SDK via a custom `FixedSizeStreamReader` wrapper class.
4.  **Direct S3 Injection:** Pipes the data immediately out of the local memory workspace and uploads it directly into our private `hcai-wesad-bronze-landing` Amazon S3 bucket tier.

---

## 📂 3. Directory Layout & File Manifest

The event-driven streaming bridge preserves full multi-modal data lineage by capturing both the serialized participant dictionaries and the primitive sensor signals organized into subject-specific partitions:

📁 hcai-wesad-bronze-landing/📁 WESAD/📄 wesad_readme.pdf — Global dataset documentation manifest📁 S10/ — Subject Partition (Repeated S2-S17)📦 S10.pkl — Serialized Subject Dictionary🤐 S10_E4_Data.zip — Raw untouched E4 Wrist Telemetry📝 S10_respiban.txt — Raw 700 Hz Chest Sensor Stream📊 S10_quest.csv — Human Ground-Truth Affect Surveys


## 🛡️ 4. Storage Architecture & Governance Manifest

### 4.1 Access Control Guardrails & Local Connection Local Client
*   **Network Privacy:** Public internet access is completely blocked. Access is heavily restricted to authorized automated pipeline accounts to ensure total security for raw biometric signatures.
*   **Local Developer Gateway (VS Code):** Local scripting connects natively using the local **AWS Credentials Provider Chain (`~/.aws/`)**. Outbound requests are signed locally via **AWS Signature Version 4 (SigV4)**, allowing internal catalog queries without exposing secrets to the open web or pushing keys to GitHub repositories.

### 4.2 Automated S3 Lifecycle Retention Policy (Storage Liability Control)
To enforce strict compliance boundaries matching DAMA-DMBOK data governance pillars, the `hcai-wesad-bronze-landing` container utilizes an automated bucket lifecycle rule:
*   **Glacier Transition:** Moves high-volume raw text streams to cold storage after **180 days** to minimize continuous active cloud storage overhead.
*   **Permanent Expiration:** Automatically purges records completely after **365 days** to comply with standard HIPAA and GDPR biological data liabilities.

### 4.3 Provenance Tracking & Week 8 Validation
Ingestion runs automatically generate explicit cloud metadata trails tracking `pipeline_execution_id`, `file_byte_size`, and `ingestion_timestamp`. 

Our automated Week 8 python audit script (`validate_s3_inventory.py`) verifies our multi-modal deployment state and validates our total asset breakdown:
```python
import boto3
s3_client = boto3.client('s3')
# Audits multi-modal extensions (.pkl, .zip, .csv, .txt), verifies byte scales, and maps folder structures.
response = s3_client.list_objects_v2(Bucket='hcai-wesad-bronze-landing')
```

---

## 5. References

1.  Schmidt, P., et al. (2018). 'Introducing WESAD, a Multimodal Dataset for Wearable Stress Detection in the Wild', *Proceedings of the 20th ACM International Conference on Multimodal Interaction*, pp. 400-408.
2.  Oyelere, S. S., et al. (2024). 'A Scoping Review of Hybrid Intelligence Systems for Human-Centred AI in Education', *Computers in Human Behavior*, 150, p. 107995.
3.  Shneiderman, B. (2021). 'Human-Centered Artificial Intelligence: Reliable, Sa
