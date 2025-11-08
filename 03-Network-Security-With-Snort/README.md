# 🧱 Network Detection Engineering (Part 2): Snort IPS — From Detection to Prevention

**By [Sujal Chauhan (CyberFreak01)](https://github.com/CyberFreak01)**  
🎯 *Detection Engineering | Threat Hunting | Network Security | Elastic SIEM*

---

## 🧠 Overview

**Part 2** of my Network Detection Engineering series focuses on deploying **Snort IPS** on a Windows Server within Azure. While Zeek (Part 1) provided deep network visibility through behavioral analysis, Snort adds **signature-based detection and prevention** capabilities to the lab.

This project demonstrates how to configure Snort in both **IDS (Intrusion Detection System)** and **IPS (Intrusion Prevention System)** modes, integrate with Elastic SIEM, and troubleshoot common cloud environment challenges.

> 📖 **Read the full article on Medium:**  
> [Network Detection Engineering Part 2 – Snort IPS: From Detection to Prevention](https://medium.com/@sujalchauhan921)

---

## ⚙️ Why Snort?

Snort complements Zeek by providing:

- **Signature-based detection** for known threats
- **Real-time traffic analysis** and packet logging
- **Active prevention** capabilities (IPS mode)
- **Flexible rule engine** for custom detections
- **Community-driven rule sets** for emerging threats

Together, Zeek's behavioral analytics and Snort's signature matching create a **defense-in-depth network security strategy**.

---

## 🏗️ Lab Architecture

### **Components:**

- 🧱 **Azure** → Windows Server (Snort IPS), Windows endpoint (Sysmon), Zeek sensor
- ☁️ **GCP** → Elastic SIEM + Kibana dashboards
- 🎯 **Kali Linux** → Attacker VM for generating malicious traffic

---

## 📦 Snort Installation on Windows Server (Azure VM)

### Prerequisites

- Windows Server 2019 or later
- Administrator access
- Active network interface
- Internet connectivity for downloads

### Step 1: Download and Install Snort

```powershell
# Create temp directory
New-Item -ItemType Directory -Force -Path "C:\Temp"

# Download Snort installer
Invoke-WebRequest -Uri "https://www.snort.org/downloads/snort/snort-2.9.20-Installer-x64.exe" -OutFile "C:\Temp\snort-installer.exe"

# Run the installer
Start-Process -FilePath "C:\Temp\snort-installer.exe" -Wait
```

**Default Installation Path:**

```
C:\Snort\
```

### Step 2: Install WinPcap / Npcap

Snort requires a packet capture driver.

```powershell
# Download WinPcap
Invoke-WebRequest -Uri "https://www.winpcap.org/install/bin/WinPcap_4_1_3.exe" -OutFile "C:\Temp\winpcap.exe"

# Install WinPcap
Start-Process -FilePath "C:\Temp\winpcap.exe" -Wait
```

💡 **Tip:** For modern Windows environments, use [Npcap](https://npcap.com/) (WinPcap successor).

**Alternative - Npcap Installation:**

```powershell
# Download Npcap
Invoke-WebRequest -Uri "https://npcap.com/dist/npcap-1.79.exe" -OutFile "C:\Temp\npcap.exe"

# Install Npcap
Start-Process -FilePath "C:\Temp\npcap.exe" -Wait
```

### Step 3: Identify Network Interface

Run the following to list available interfaces:

```bash
snort -W
```

**Example output:**

```
1. \Device\NPF_{XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX} (Ethernet)
2. \Device\NPF_{YYYYYYYY-YYYY-YYYY-YYYY-YYYYYYYYYYYY} (Wi-Fi)
```

Select the correct interface ID (e.g., `-i 1`).

---

## ⚙️ Configuration

### Step 4: Configure Snort

Edit `C:\Snort\etc\snort.conf` with your environment variables:

```bash
# Network variables
var HOME_NET [10.0.1.0/24,192.168.1.0/24]
var EXTERNAL_NET !$HOME_NET

# Rule paths
var RULE_PATH C:\Snort\rules
var SO_RULE_PATH C:\Snort\so_rules
var PREPROC_RULE_PATH C:\Snort\preproc_rules

# Output (for Elastic SIEM integration)
output alert_fast: snort.log

# Disable checksum validation (important for virtual/cloud setups)
config checksum_mode: none
```

📁 **Full configuration file:** 👉 [snort.conf](https://github.com/CyberFreak01)

### Step 5: Download Snort Community Rules

1. Sign up at [snort.org](https://www.snort.org/)
2. Navigate to **Download → Community Rules**
3. Extract the rules into:

```
C:\Snort\rules\
```

---

## 🚀 Running Snort

### Step 6: Start Snort in IDS Mode

**Basic IDS mode (quiet output):**

```bash
snort -q -c C:\Snort\etc\snort.conf -i 1
```

**View live alerts in the console:**

```bash
snort -A console -c C:\Snort\etc\snort.conf -i 1
```

**Log to file with full alerts:**

```bash
snort -A full -c C:\Snort\etc\snort.conf -i 1 -l C:\Snort\log
```

### Step 7: Start Snort in IPS (Inline) Mode

To enable prevention (active blocking):

```bash
snort -Q --daq afpacket -c C:\Snort\etc\snort.conf -i 1
```

⚠️ **Note:** IPS mode requires proper DAQ (Data Acquisition) module configuration and may need additional setup on Windows.

---

## 🧰 Troubleshooting: Checksum Offloading Issues

Cloud environments (like Azure or Hyper-V) often cause TCP checksum mismatches due to checksum offloading features.

### Method 1: Disable Checksum Validation in Snort (Recommended)

**Command-line:**

```bash
snort -A console -c C:\Snort\etc\snort.conf -i 1 -k none
```

**Configuration file (snort.conf):**

```nginx
config checksum_mode: none
```

### Method 2: Disable Checksum Offloading on Network Adapter

```powershell
# Find network adapter name
Get-NetAdapter

# Disable IPv4 checksum offload
Set-NetAdapterAdvancedProperty -Name "Ethernet0" -DisplayName "IPv4 Checksum Offload" -DisplayValue "Disabled"

# Disable TCP checksum offload
Set-NetAdapterAdvancedProperty -Name "Ethernet0" -DisplayName "TCP Checksum Offload (IPv4)" -DisplayValue "Disabled"

# Disable UDP checksum offload
Set-NetAdapterAdvancedProperty -Name "Ethernet0" -DisplayName "UDP Checksum Offload (IPv4)" -DisplayValue "Disabled"

# Restart the adapter
Restart-NetAdapter -Name "Ethernet0"
```

⚠️ **Caution:** Disabling offloading can slightly reduce network performance.

## 📊 Key Learnings

- Signature-based detection complements behavioral analytics from Zeek
- Cloud environments require checksum validation adjustments
- IPS mode provides active defense but requires careful tuning to avoid false positives
- Snort rule management is crucial for maintaining detection efficacy

---

## 📚 References

- 🔗 [Official Snort Documentation](https://www.snort.org/documents)
- 🔗 [Snort Rules Documentation](https://www.snort.org/faq/what-are-snort-rules)
- 🔗 [WinPcap Download](https://www.winpcap.org/install/)
- 🔗 [Npcap Download](https://npcap.com/)
- ✍️ [My Medium Article](https://medium.com/@sujalchauhan921)

---

## 🤝 Connect With Me

- 🐙 **GitHub:** [@CyberFreak01](https://github.com/CyberFreak01)
- ✍️ **Medium:** [@sujalchauhan921](https://medium.com/@sujalchauhan921)
- 💼 **LinkedIn:** [Connect with me](https://www.linkedin.com/in/sujal-chauhan/)

---

## 🏷️ Tags

`Snort IPS` `Snort IDS` `Detection Engineering` `Threat Hunting` `Network Intrusion Prevention` `Elastic SIEM` `Windows Server Security` `Azure Security` `Npcap` `Network Security Monitoring` `Cybersecurity` `SOC Automation` `Snort Configuration` `Inline Mode` `Signature Detection`

---

⭐ **If you found this project helpful, please consider giving it a star!**