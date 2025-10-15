☁️ Building the Foundation: My Cloud-Based Detection Engineering Lab
By Sujal Chauhan
🎯 Detection Engineering | Threat Hunting | Cloud Security

🧠 TL;DR
I built an Azure-hosted, VPC-isolated detection lab that sends host and network telemetry to an Elastic SIEM instance running on GCP.
This repository contains my architecture, Sysmon configuration, Elastic detections, and alert dashboard setup.

The goal: Simulate real-world attacker behaviors and write detections from raw telemetry — just like an enterprise SOC would.

🏗️ Lab Architecture
https://github.com/user-attachments/assets/00c76255-1674-488f-8aab-d9769c115cc9

Layer	Platform	Purpose
Endpoint	Azure VM	Collect host telemetry with Sysmon
SIEM	Elastic Stack on GCP	Log aggregation, alerting, dashboards
Network	Azure VNet	Isolated environment for safe simulations
Future	Snort / Zeek	Network-layer detection sources
Overview
Azure (Host Layer): Windows VM running Sysmon & Beats

GCP (SIEM Layer): Elastic Stack for storage, analysis, and visualization

Connectivity: Encrypted channels (HTTPS/TLS) between Beats → Elastic

Integrations: Sysmon, Windows Event Logs, Snort (upcoming), Zeek (upcoming)

⚙️ Sysmon Configuration
Sysmon provides rich telemetry for process creation, registry modifications, and network activity.

⚠️ Lesson Learned: The first time I installed Sysmon, I forgot to load the sysmonconfig.xml file — only Event ID 1 (process creation) was logged.
After applying SwiftOnSecurity's config, I unlocked events like:

Event ID 3 – Network connections

Event ID 7 – Image loads

Event ID 13 – Registry modifications

📁 Files:

Config: sysmon/sysmonconfig.xml

Sample Events: sysmon/sample-sysmon-events.json

https://sysmon/sysmon-install.png

🔍 Detections
All detections were written in KQL and tested on Elastic SIEM using the ingested Sysmon telemetry.

🧩 1. RDP Login Failures
Detects brute-force or repeated failed login attempts.

Query:

kql
event.action: "log_on" 
AND event.outcome: "failure" 
AND event.code: "4625"
Why: Event ID 4625 indicates failed logon attempts — early brute-force or credential spraying activity.

📁 queries/rdp_login_failures.kql

⚡ 2. PowerShell Process Chain with Obfuscation
Detects obfuscated PowerShell activity — a common attacker tradecraft.

Query:

kql
event.code: "1"
AND winlog.channel: "Microsoft-Windows-Sysmon/Operational"
AND process.name: "powershell.exe"
AND process.parent.name: "powershell.exe"
AND process.command_line: (*-EncodedCommand* OR *-enc* OR *-e*)
Why: Flags encoded or obfuscated PowerShell commands often used in malware, payload delivery, or lateral movement.

📁 queries/powershell_obfuscation.kql

🧱 3. Reg.exe Used for Persistence
Detects attempts to create persistence through Registry "Run" keys.

Query:

kql
event.code: "1"
AND winlog.channel: "Microsoft-Windows-Sysmon/Operational"
AND process.name: "reg.exe"
AND process.command_line: (*add* AND *CurrentVersion\\Run* AND */d*)
Why: Run keys allow programs to execute automatically at startup — often abused for persistence.

📁 queries/reg_persistence.kql

📊 Alerting & Dashboard
I converted each detection into Elastic alerts and visualized them on a Detection Dashboard.

📁 detections/detection-alerts.ndjson

🧩 Key Learnings
Telemetry depth depends on configuration. Sysmon without config = visibility loss.

KQL + process relationships form the foundation of host-based detection logic.

Cross-data correlation (Sysmon + Snort/Zeek) transforms raw logs into meaningful intelligence.

Elastic SIEM is a fantastic platform for learning detection development.

🛠️ Tools & Tech Stack
Category	Tool
Cloud	Microsoft Azure, Google Cloud Platform
SIEM	Elastic Stack (Elasticsearch + Kibana)
Telemetry	Sysmon, Winlogbeat, Filebeat
Detection Writing	KQL (Kibana Query Language)
Upcoming	Snort IDS, Zeek Network Analyzer
🚀 Upcoming Work
Integrate Snort IDS for network-layer detections

Add Zeek telemetry for deeper visibility (DNS, SSL, HTTP)

Build cross-correlation rules between Sysmon and network events

Publish detection visualizations using Elastic Canvas / Kibana Lens

📚 Articles & Write-Ups
Part 1: Why I Built a Detection Lab

Part 2: Cloud-Based Detection Engineering Lab (this repo)

Part 3: Network Detection with Snort & Zeek (Coming Soon)

🧾 License
MIT License – free to use, modify, and share with proper attribution.

If you build on this lab, please give credit — collaboration makes the blue team stronger 💪

👨‍💻 Author
Sujal Chauhan
📍 Cloud Detection Engineer | Threat Hunter | SOC Enthusiast

🔗 [LinkedIn] | 📰 [Medium Blog] | 🐦 [Twitter / X] | 📧 sujal@example.com

"Detection Engineering isn't about chasing alerts — it's about understanding the story behind them."