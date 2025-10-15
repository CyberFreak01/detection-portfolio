☁️ Cloud-Based Detection Engineering Lab
By Sujal Chauhan
Detection Engineering | Threat Hunting | Cloud Security

🧠 TL;DR
Built an Azure-hosted detection lab that sends host and network telemetry to Elastic SIEM on GCP. Contains architecture, Sysmon config, Elastic detections, and alert dashboard.

🏗️ Lab Architecture
Layer	Platform	Purpose
Endpoint	Azure VM	Collect host telemetry with Sysmon
SIEM	Elastic Stack on GCP	Log aggregation, alerting, dashboards
Network	Azure VNet	Isolated environment
Future	Snort / Zeek	Network-layer detection
⚙️ Sysmon Configuration
Used SwiftOnSecurity's config to capture:

Event ID 3 – Network connections

Event ID 7 – Image loads

Event ID 13 – Registry modifications

📁 Files: sysmon/sysmonconfig.xml

🔍 Detections
1. RDP Login Failures
kql
event.action: "log_on" 
AND event.outcome: "failure" 
AND event.code: "4625"
2. PowerShell Obfuscation
kql
event.code: "1"
AND process.name: "powershell.exe"
AND process.command_line: (*-EncodedCommand* OR *-enc*)
3. Registry Persistence
kql
event.code: "1"
AND process.name: "reg.exe" 
AND process.command_line: (*add* AND *CurrentVersion\\Run*)
🛠️ Tech Stack
Cloud: Azure, GCP

SIEM: Elastic Stack

Telemetry: Sysmon, Winlogbeat

Detection: KQL

🚀 Roadmap
Snort IDS integration

Zeek network analysis

Cross-correlation rules

Elastic Canvas visualizations

"Detection Engineering is about understanding the story behind alerts."


