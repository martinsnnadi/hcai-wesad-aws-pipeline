# Multimodal Biometric Ingestion Infrastructure (WESAD)
## HCAI Data Pipeline Track | Version 1.0 (Amazon AWS)

**Academic Supervisor:** Professor Solomon Sunday Oyelere  
**Project Horizon:** 24-Week Parallel Processing Research Roadmap  
**Current Milestone:** Weeks 5–8 (Bronze Layer Ingestion & Streaming)

---

## 1. Project & Dataset Review
This track focuses on building a secure, high-integrity data infrastructure for the **Wearable Stress Detection (WESAD)** dataset under the academic supervision of Professor Solomon Sunday Oyelere. 

### 1.1 Technical Profile
* **Domain:** Digital Health / Wearable Computing & Wellbeing.
* **Source Engine:** Multimodal biometric sensor streams from 15 human participants.
* **Telemetry Data Scale:** High-frequency raw data capturing continuous physiological signals: RespiBan Chest Device (ECG, EDA, EMG, Respiration sampled at 700 Hz) and Empatica E4 Wristband (BVP at 64Hz, EDA at 4Hz, Temp at 4Hz, ACC at 32Hz).
* **Storage Footprint:** Expands from a ~500 MB compressed archive to **over 2.5 GB of raw, serialized binary data (.pkl / Pickle formats)**.

### 1.2 Human-Centred AI (HCAI) Risk Assessment
* **Model Drift Safety:** Standard AI stress-prediction models suffer from critical accuracy failures due to natural, baseline physiological differences between individual human bodies. A model trained on raw variables of one subject will instantly misclassify another. 
* **The HCAI Guardrail:** This pipeline sets up the environment to enforce **Individualised Baseline Standardisation**. By computing the specific statistical mean and standard deviation of each subject's rest state, it normalizes sensor drifts *before* data passes to machine learning layers.
* **Biometric Identity Isolation:** To prevent individual tracking fingerprinting, the raw hardware streams are completely decoupled from downstream consumption using strict **AWS Identity and Access Management (IAM)** bucket boundaries.

---

## 2. Ingestion Breakthrough: Zero-Disk, Low-Memory Streaming Double-Bridge

During the active ingestion execution phase, downloading and unpacking the 2.5 GB binary telemetry package triggered severe resource bottlenecks on standard cloud compute nodes:
1. **Disk Bottleneck (Errno 28):** The container ran out of local scratch space while attempting to unzip the files onto the native drive.
2. **Memory Bottleneck (Killed):** Bypassing the disk and loading the complete uncompressed archive into system RAM instantly triggered the Linux Out-of-Memory (OOM) Killer.

### ⚙️ The Multi-Part Streaming Architecture
To resolve these hardware constraints, I refactored the pipeline into a continuous, event-driven stream processing architecture across four synchronized layers:
* **The 64 KB Intake Valve:** Maintains a microscopic, fixed network memory buffer, pulling binary byte fragments from the repository server to keep the overall RAM footprint near zero.
* **On-The-Fly De-serialization:** Dynamically parses zip archive headers sequentially, unzipping the sensor data fragments directly in mid-air as they pass through the network card interface.
* **The Chunk-Size Normalizer:** Intercepts unzipped streams (such as the 900 MB serialized `S10.pkl` arrays) and repackages them into exact byte blocks expected by the AWS SDK via a custom `FixedSizeStreamReader` wrapper class.
* **Direct S3 Injection:** Pipes the data immediately out of the local memory workspace and uploads it directly into our private **`hcai-wesad-bronze-landing`** Amazon S3 bucket tier.

## 3. Storage Architecture & Governance Manifest
* **Storage Framework:** Data lands in an append-only, fully private Amazon S3 bucket tier (`hcai-wesad-bronze-landing`). 
* **Access Control Guardrails:** Public internet access is completely blocked [1]. Access is heavily restricted to authorized automated pipeline accounts to ensure total security for raw biometric signatures [1].
* **Provenance Tracking:** Ingestion runs automatically generate explicit cloud metadata trails tracking `pipeline_execution_id`, `file_byte_size`, and `ingestion_timestamp`.

----

  ## 4. References
 Schmidt, P., et al. (2018). 'Introducing WESAD, a Multimodal Dataset for Wearable Stress Detection in the Wild', *Proceedings of the 20th ACM International Conference on Multimodal Interaction*, pp. 400-408.  
 Oyelere, S. S., et al. (2024). 'A Scoping Review of Hybrid Intelligence Systems for Human-Centred AI in Education', *Computers in Human Behavior*, 150, p. 107995.  
 Shneiderman, B. (2021). 'Human-Centered Artificial Intelligence: Reliable, Safe & Trustworthy', *International Journal of Human–Computer Interaction*, 37(6), pp. 479-491.
