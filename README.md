## 🚀 Ingestion Breakthrough: Zero-Disk, Low-Memory Streaming Double-Bridge

During the active Week 5/6 ingestion phase, downloading and unzipping the multimodal 2.5 GB WESAD binary data package triggered critical resource bottlenecks on standard cloud compute nodes:
1. **Disk Bottleneck (Errno 28):** The environment ran out of scratch disk space while attempting to unpack the massive files locally.
2. **Memory Bottleneck (Killed):** Bypassing the disk and reading raw blocks into system RAM instantly triggered the Linux Out-of-Memory (OOM) Killer.

### ⚙️ The Multi-Part Streaming Architecture
To resolve these hardware constraints, I refactored the pipeline into a continuous, event-driven stream processing architecture across four synchronized layers:
* **The 64 KB Intake Valve:** Maintains a microscopic, fixed network memory buffer, pulling binary byte fragments from the repository server to keep the overall RAM footprint near zero.
* **On-The-Fly De-serialization:** Dynamically parses zip archive headers sequentially, unzipping the sensor data fragments directly in mid-air as they pass through the network card interface.
* **The Chunk-Size Normalizer:** Intercepts unzipped streams (such as the 900 MB serialized `S10.pkl` arrays) and repackages them into exact byte blocks expected by the AWS SDK via a custom `FixedSizeStreamReader` wrapper class.
* **Direct S3 Injection:** Pipes the data immediately out of the local memory workspace and uploads it directly into our private **`hcai-wesad-bronze-landing`** Amazon S3 bucket tier.
