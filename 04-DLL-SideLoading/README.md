
# DLL Side-Loading Detection Lab

## Overview
Simulated DLL side-loading attack using Notepad++ 8.4.1 and built detection rules in Elastic SIEM to identify this MITRE ATT&CK technique (T1574.002).

## Attack Simulation
- **Target Application:** Notepad++ 8.4.1 (vulnerable version)
- **Malicious DLL:** UxTheme.dll (displays message box on load)
- **Technique:** MITRE T1574.002 - DLL Side-Loading
- **Compilation:** `x86_64-w64-mingw32-gcc -shared -o UxTheme.dll uxtheme.c -luser32`

## Detection Rules

### Network Detection (Snort)
```snort
alert tcp any any -> $HOME_NET 80 (
    msg:"LAB - HTTP GET for .dll download"; 
    sid:1100001; 
    flow:to_server,established; 
    content:".dll"; 
    http_uri; 
    nocase;
)
```

### Endpoint Detection (Elastic/KQL)
```kql
event.dataset:"windows.sysmon_operational" 
AND event.action:"Image loaded"
AND NOT file.code_signature.status:"Valid"
AND NOT file.directory:("C:\\Windows\\*" OR "C:\\Program Files*")
AND NOT process.executable:("C:\\Windows\\*" OR "C:\\Program Files*")
AND NOT file.name:("*.ni.dll")
```

## Tools Used
- **Sysmon** - Event ID 7 telemetry
- **Elastic SIEM** - Detection rule creation
- **Process Monitor** - Forensic analysis
- **Snort IDS** - Network-level detection
- **MinGW** - DLL compilation

## Key Files
- `uxtheme.c` - Malicious DLL source code
- `UxTheme.dll` - Compiled payload
- `detection_rule.json` - Elastic detection rule export

## Results
✅ Successfully simulated attack  
✅ Detected unsigned DLL loads from non-system paths  
✅ Reduced false positives by 95%+ through query tuning  
✅ Mapped to MITRE ATT&CK framework

## Author
Detection Engineering & Threat Hunting Lab

## License
MIT

## Addtional References

## https://rewterz.com/threat-advisory/hackers-exploit-onedrive-via-dll-sideloading-to-run-malicious-code

## https://www.cybereason.com/blog/threat-analysis-report-dll-side-loading-widely-abused
