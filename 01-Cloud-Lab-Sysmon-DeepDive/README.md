# ☁️ Building the Foundation: My Cloud-Based Detection Engineering Lab

**By [Sujal Chauhan](#)**  
🎯 *Detection Engineering | Threat Hunting | Cloud Security*

---

## 🧠 TL;DR

I built an **Azure-hosted, VPC-isolated detection lab** that sends **host and network telemetry** to an **Elastic SIEM** instance running on **GCP**.  
This repository contains my **architecture**, **Sysmon configuration**, **Elastic detections**, and **alert dashboard** setup.

> The goal: Simulate real-world attacker behaviors and write detections from raw telemetry — just like an enterprise SOC would.

---

## 🏗️ Lab Architecture

![Architecture Diagram](architecture/cloud-architecture.png)

| Layer | Platform | Purpose |
|-------|-----------|----------|
| Endpoint | Azure VM | Collect host telemetry with Sysmon |
| SIEM | Elastic Stack on GCP | Log aggregation, alerting, dashboards |
| Network | Azure VNet | Isolated environment for safe simulations |
| Future | Snort / Zeek | Network-layer detection sources |

### **Overview**
- **Azure (Host Layer):** Windows VM running Sysmon & Beats  
- **GCP (SIEM Layer):** Elastic Stack for storage, analysis, and visualization  
- **Connectivity:** Encrypted channels (HTTPS/TLS) between Beats → Elastic  
- **Integrations:** Sysmon, Windows Event Logs, Snort (upcoming), Zeek (upcoming)

---

## ⚙️ Sysmon Configuration

Sysmon provides rich telemetry for process creation, registry modifications, and network activity.

> ⚠️ *Lesson Learned:* The first time I installed Sysmon, I forgot to load the `sysmonconfig.xml` file — only Event ID 1 (process creation) was logged.  
> After applying SwiftOnSecurity’s config, I unlocked events like:
> - **Event ID 3** – Network connections  
> - **Event ID 7** – Image loads  
> - **Event ID 13** – Registry modifications  

📁 **Files:**
- Config: [`sysmon/sysmonconfig.xml`](sysmon/sysmonconfig.xml)  
- Sample Events: [`sysmon/sample-sysmon-events.json`](sysmon/sample-sysmon-events.json)

![Sysmon Installation Screenshot](sysmon/sysmon-install.png)

---

## 🔍 Detections

All detections were written in **KQL** and tested on **Elastic SIEM** using the ingested Sysmon telemetry.

---

### 🧩 **1. RDP Login Failures**
Detects brute-force or repeated failed login attempts.

**Query:**
```kql
event.action: "log_on" 
AND event.outcome: "failure" 
AND event.code: "4625"
