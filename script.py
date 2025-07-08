import json
import pandas as pd

# Create sample data showing correlation between Spiderfoot and nmap findings
# This represents how OSINT data (Spiderfoot) correlates with network scanning (nmap)

# Sample Spiderfoot OSINT data
spiderfoot_data = [
    {
        "target": "example.com",
        "type": "Domain",
        "finding": "DNS Record",
        "value": "192.168.1.10",
        "source": "Public DNS",
        "risk_level": "Low",
        "category": "Infrastructure"
    },
    {
        "target": "example.com", 
        "type": "Subdomain",
        "finding": "admin.example.com",
        "value": "192.168.1.15",
        "source": "Certificate Transparency",
        "risk_level": "Medium",
        "category": "Attack Surface"
    },
    {
        "target": "example.com",
        "type": "Email",
        "finding": "admin@example.com",
        "value": "Found in breach data",
        "source": "HaveIBeenPwned",
        "risk_level": "High",
        "category": "Credentials"
    },
    {
        "target": "example.com",
        "type": "IP Range",
        "finding": "192.168.1.0/24",
        "value": "Company network range",
        "source": "WHOIS",
        "risk_level": "Medium",
        "category": "Infrastructure"
    },
    {
        "target": "example.com",
        "type": "Technology",
        "finding": "Apache 2.4.41",
        "value": "Web server version",
        "source": "HTTP Headers",
        "risk_level": "Medium",
        "category": "Technology Stack"
    }
]

# Sample nmap network scanning data
nmap_data = [
    {
        "ip": "192.168.1.10",
        "port": 80,
        "service": "HTTP",
        "version": "Apache 2.4.41",
        "state": "open",
        "banner": "Apache/2.4.41 (Ubuntu)",
        "risk_level": "Low",
        "vulnerabilities": []
    },
    {
        "ip": "192.168.1.10",
        "port": 443,
        "service": "HTTPS",
        "version": "Apache 2.4.41",
        "state": "open",
        "banner": "Apache/2.4.41 SSL",
        "risk_level": "Low",
        "vulnerabilities": []
    },
    {
        "ip": "192.168.1.15",
        "port": 22,
        "service": "SSH",
        "version": "OpenSSH 7.6p1",
        "state": "open",
        "banner": "SSH-2.0-OpenSSH_7.6p1",
        "risk_level": "Medium",
        "vulnerabilities": ["CVE-2018-15473"]
    },
    {
        "ip": "192.168.1.15",
        "port": 80,
        "service": "HTTP",
        "version": "Apache 2.4.41",
        "state": "open",
        "banner": "Apache/2.4.41 (Ubuntu)",
        "risk_level": "Medium",
        "vulnerabilities": []
    },
    {
        "ip": "192.168.1.15",
        "port": 3306,
        "service": "MySQL",
        "version": "5.7.30",
        "state": "open",
        "banner": "MySQL 5.7.30",
        "risk_level": "High",
        "vulnerabilities": ["CVE-2019-2614", "CVE-2019-2627"]
    }
]

# Create correlation analysis between Spiderfoot and nmap data
correlations = []

# Find correlations between OSINT findings and network scan results
for osint in spiderfoot_data:
    for scan in nmap_data:
        correlation_score = 0
        correlation_reasons = []
        
        # IP correlation
        if osint["value"] == scan["ip"]:
            correlation_score += 0.8
            correlation_reasons.append("Direct IP match")
        
        # Technology/Version correlation
        if osint["type"] == "Technology" and osint["finding"] in scan["version"]:
            correlation_score += 0.9
            correlation_reasons.append("Technology version match")
        
        # Risk level correlation
        risk_weights = {"Low": 1, "Medium": 2, "High": 3}
        if abs(risk_weights[osint["risk_level"]] - risk_weights[scan["risk_level"]]) <= 1:
            correlation_score += 0.3
            correlation_reasons.append("Similar risk levels")
        
        # Service correlation
        if osint["category"] == "Infrastructure" and scan["service"] in ["HTTP", "HTTPS"]:
            correlation_score += 0.4
            correlation_reasons.append("Infrastructure service match")
        
        if correlation_score > 0.5:
            correlations.append({
                "osint_finding": osint["finding"],
                "osint_type": osint["type"],
                "osint_risk": osint["risk_level"],
                "nmap_target": f"{scan['ip']}:{scan['port']}",
                "nmap_service": scan["service"],
                "nmap_risk": scan["risk_level"],
                "correlation_score": round(correlation_score, 2),
                "correlation_reasons": correlation_reasons,
                "combined_risk": "High" if max(risk_weights[osint["risk_level"]], risk_weights[scan["risk_level"]]) >= 3 else "Medium" if max(risk_weights[osint["risk_level"]], risk_weights[scan["risk_level"]]) >= 2 else "Low"
            })

# Convert to DataFrames
df_spiderfoot = pd.DataFrame(spiderfoot_data)
df_nmap = pd.DataFrame(nmap_data)
df_correlations = pd.DataFrame(correlations)

print("Spiderfoot OSINT Data:")
print(df_spiderfoot.to_string(index=False))
print("\n" + "="*80 + "\n")

print("Nmap Network Scan Data:")
print(df_nmap.to_string(index=False))
print("\n" + "="*80 + "\n")

print("Correlation Analysis:")
print(df_correlations.to_string(index=False))

# Save data for the web application
spiderfoot_json = json.dumps(spiderfoot_data, indent=2)
nmap_json = json.dumps(nmap_data, indent=2)
correlations_json = json.dumps(correlations, indent=2)

print(f"\nData prepared for web application with {len(correlations)} correlations found.")