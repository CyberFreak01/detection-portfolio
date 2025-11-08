# 🌐 Network Detection Engineering – Part 1: Zeek as My Network Detective in the Cloud

**By [Sujal Chauhan](https://github.com/CyberFreak01)**  
🎯 *Detection Engineering | Threat Hunting | Network Security | Elastic SIEM*

---

## 🧠 Overview

From **host-level telemetry to full network visibility**, this project marks **Part 1** of my *Network Detection Engineering* journey — where I deploy **Zeek** as a network security monitor within my hybrid cloud detection lab.

This lab extends my [Sysmon Deep Dive Project](../01-Cloud-Lab-Sysmon-DeepDive/) by adding a **network-layer perspective**, enabling behavioral analysis and network-based detections powered by **Elastic SIEM**.

> 📖 **Read the full article on Medium:**  
> [Network Detection Engineering Part 1 – Zeek as My Network Detective in the Cloud](https://medium.com/@sujalchauhan921/network-detection-engineering-part-1-zeek-as-my-network-detective-in-the-cloud-ebf9281b6d37)

---

## ⚙️ Why Zeek?

As I transitioned from endpoint detections (Sysmon) to network-level insights, I realized a crucial gap — *what's happening on the wire?*

Zeek fills that gap by providing:

- **Protocol-aware visibility** (HTTP, DNS, SSL/TLS, SMB, etc.)
- **File extraction and hashing** for malware detection
- **Behavioral detections** beyond static signatures
- **Rich metadata** for deeper forensic correlation

Unlike traditional IDS tools, Zeek focuses on **transforming packets into intelligence**, forming the foundation for advanced threat hunting and behavioral analytics.

---

## 🏗️ Updated Lab Architecture

Zeek operates as a **network sensor** within my **Azure VPC**, alongside Snort (used in Part 2).  
All logs are shipped via **Elastic Agent/Filebeat** to an **Elastic SIEM instance on GCP**.

### **Components:**

- 🧱 **Azure** → Windows endpoint (Sysmon + Winlogbeat), Zeek sensor
- ☁️ **GCP** → Elastic SIEM + Kibana dashboards
- 🎯 **Kali Linux** → Attacker VM for generating traffic (Nmap, Nikto, malicious downloads)

---

## 🔗 Zeek Installation and Configuration

### Prerequisites

- Debian-based Linux system (Kali Linux, Ubuntu, Debian)
- Root or sudo access
- Active network interface

### Step 1: Add Zeek's Official Repository and Key

```bash
# Add Zeek repository GPG key
wget -qO - https://download.zeek.org/zeek.gpg | sudo apt-key add -

# Add Zeek repository (Debian Testing)
echo 'deb http://download.zeek.org/debian testing main' | sudo tee /etc/apt/sources.list.d/zeek.list

# Update package list
sudo apt update
```

### Step 2: Install Zeek

```bash
sudo apt install -y zeek
```

### Step 3: Add Zeek to PATH

```bash
echo 'export PATH=/opt/zeek/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### Step 4: Verify Installation

```bash
zeek --version
```

---

## ⚙️ Initial Configuration

### Configure Network Interface

Edit `/opt/zeek/etc/node.cfg`:

```ini
[zeek]
type=standalone
host=localhost
interface=eth0  # replace with your active interface
```

### Define Network Ranges

Edit `/opt/zeek/etc/networks.cfg`:

```
10.0.1.0/24     Private-Network
192.168.1.0/24  Home-Network
```

### Deploy Zeek

```bash
sudo zeekctl deploy
```

✅ **Zeek now begins capturing and logging network activity in `/opt/zeek/logs/current/`.**

---

## 🚀 Elastic SIEM Integration

1. **Deployed Elastic Agent** on the Zeek host
2. **Added the Zeek Integration** within Elastic Fleet
3. **Shipped logs** (e.g., `http.log`, `dns.log`, `ssl.log`, `files.log`) to Elastic SIEM
4. **Built detection rules and dashboards** for:
   - Nmap & Nikto scanning behavior
   - Malicious file download detection (hash correlation)
   - HTTP user-agent anomalies
   - Global connection heatmaps

---

## 📊 Key Learnings

- Transitioning from endpoint to network telemetry improved overall situational awareness
- Zeek's structured logs made data normalization effortless in Elastic
- Network metadata proved invaluable for correlation with Sysmon events
- Behavioral detection is more resilient than signature-based approaches

---

## 📚 References

- 🔗 [Official Zeek Documentation](https://docs.zeek.org/)
- 🔗 [Elastic Zeek Integration Guide](https://www.elastic.co/guide/en/integrations/current/zeek.html)
- ✍️ [My Medium Article](https://medium.com/@sujalchauhan921/network-detection-engineering-part-1-zeek-as-my-network-detective-in-the-cloud-ebf9281b6d37)

---

## 🤝 Connect With Me

- 🐙 **GitHub:** [@CyberFreak01](https://github.com/CyberFreak01)
- ✍️ **Medium:** [@sujalchauhan921](https://medium.com/@sujalchauhan921)
- 💼 **LinkedIn:** [Connect with me](https://www.linkedin.com/in/sujal-chauhan/)

---

## 🏷️ Tags

`Zeek` `Network Detection Engineering` `Elastic SIEM` `Threat Hunting` `Network Security Monitoring` `Kali Linux` `Azure Security` `Detection Engineering` `SOC Automation` `Network IDS` `Behavioral Detection` `Cybersecurity Projects`

---

⭐ **If you found this project helpful, please consider giving it a star!**