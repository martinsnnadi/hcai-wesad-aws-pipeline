# WESAD Ingestion Infrastructure
### HCAI Parallel Cloud Pipeline Track | Amazon AWS Tier

**Supervisor:** Prof. Solomon Sunday Oyelere  
**Milestone:** Week 8 (Bronze Validation & Inventory Enforcement)

---

## 1. Project & Dataset Review

Secure, high-integrity data infrastructure for the Wearable Stress Detection (WESAD) dataset.

### 1.1 Technical Profile
*   **Domain**: Digital Health / Wearable Computing & Wellbeing.
*   **Source Stream**: Multimodal biometric sensor telemetry from 15 human participants.
*   **Data Scale**: High-frequency signals across RespiBan Chest Device (ECG, EDA, EMG, Respiration @ 700 Hz) and Empatica E4 Wristband (BVP @ 64Hz, EDA @ 4Hz, Temp @ 4Hz, ACC @ 32Hz).
*   **Storage Footprint**: Uncompressed binary telemetry expands to **16,763.98 MB (16.37 GB)** across **76 verified object blobs** in cloud storage.

### 1.2 HCAI Risk Assessment
*   **Model Drift**: Stress-prediction models fail due to individual baseline physiological differences. Pipeline sets up directory structures to calculate **Individualised Baseline Standardisation** (rest-state mean/standard deviation) to neutralize sensor drift.
*   **Identity Isolation**: Disables public access and uses strict AWS IAM bucket boundaries to decouple raw biometric hardware streams from downstream model layers.

---

## 2. Ingestion Breakthrough: Zero-Disk Streaming Double-Bridge

Unpacking the raw telemetry package on standard compute nodes triggered major resource bottlenecks:
*   **Disk Bottleneck (`Errno 28`)**: Container ran out of scratch space trying to unzip files onto the local drive.
*   **Memory Bottleneck (`Killed`)**: Bypassing the disk to unpack the full archive directly into RAM triggered the Linux Out-of-Memory (OOM) Killer.

### The Multi-Part Streaming Architecture
Refactored pipeline into a continuous, event-driven stream processing layout across four layers:
1.  **64 KB Intake Valve**: Pulls binary byte fragments from the repository server using a fixed memory buffer to keep the local RAM footprint near zero.
2.  **In-Air De-serialization**: Parses zip archive headers sequentially, unzipping data fragments inside the network card interface.
3.  **Chunk-Size Normalizer**: Intercepts unzipped streams (like the 900 MB `S10.pkl` arrays) and repackages them into exact byte blocks using a custom `FixedSizeStreamReader` class.
4.  **Direct S3 Injection**: Pipes the data immediately out of memory and uploads it straight into our private `hcai-wesad-bronze-landing` S3 bucket.

---

## 3. Directory Layout & File Manifest

The streaming bridge preserves full multi-modal lineage by separating the zipped signals, raw text streams, and survey metrics into subject-specific partitions:


<ul>
  <li>📁 <strong>hcai-wesad-bronze-landing/</strong>
    <ul>
      <li>📁 <strong>WESAD/</strong>
        <ul>
          <li>📄 <code>wesad_readme.pdf</code> — <em>Global dataset documentation manifest</em></li>
          <li>📁 <strong>S10/</strong> — <em>Subject Partition (Repeated S2-S17)</em>
            <ul>
              <li>📦 <code>S10.pkl</code> — <em>Serialized Subject Dictionary</em></li>
              <li>🤐 <code>S10_E4_Data.zip</code> — <em>Raw untouched E4 Wrist Telemetry</em></li>
              <li>📝 <code>S10_respiban.txt</code> — <em>Raw 700 Hz Chest Sensor Stream</em></li>
              <li>📊 <code>S10_quest.csv</code> — <em>Human Ground-Truth Affect Surveys</em></li>
            </ul>
          </li>
        </ul>
      </li>
    </ul>
  </li>
</ul>

---

## 4. Storage Architecture & Governance Manifest

### 4.1 Access Control & VS Code Gateway
*   **Network Privacy**: Blocks public web access. Limits visibility to authorized automated pipeline accounts to protect biometric data.
*   **Local Developer Gateway**: Connects locally in VS Code using the **AWS Credentials Provider Chain (`~/.aws/`)**. Signs outbound traffic via **AWS Signature Version 4 (SigV4)**, allowing internal catalog queries without exposing secrets or pushing keys to GitHub.

### 4.2 S3 Lifecycle Retention Policy (DAMA-DMBOK Alignment)
Applies a programmatic bucket lifecycle rule to mitigate active data liabilities:
*   **Glacier Transition**: Moves high-volume raw text streams to cold storage after **180 days** to cut active cloud storage overhead.
*   **Permanent Expiration**: Purges files completely after **365 days** to comply with standard HIPAA and GDPR biological data guidelines.

### 4.3 Provenance Tracking & Week 8 Validation
Generates automated metadata logs tracking `pipeline_execution_id`, `file_byte_size`, and `ingestion_timestamp`.

Our automated Week 8 python audit script (`validate_s3_inventory.py`) checks storage integrity and verifies the object matrix state:
```python
import boto3
s3_client = boto3.client('s3')
# Audits object extensions (.pkl, .zip, .csv, .txt), checks byte scales, and maps folder paths.
response = s3_client.list_objects_v2(Bucket='hcai-wesad-bronze-landing')
```

---

## 5. References

1. Schmidt, P. et al. (2018) 'Introducing WESAD, a Multimodal Dataset for Wearable Stress Detection in the Wild', *Proceedings of the 20th ACM ICMI*, pp. 400-408.
2. Oyelere, S. S. et al. (2024) 'A Scoping Review of Hybrid Intelligence Systems for Human-Centred AI in Education', *Computers in Human Behavior*, 150.
3. Shneiderman, B. (2021) 'Human-Centered Artificial Intelligence: Reliable, Safe
