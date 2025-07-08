# Scan a target range and run OSINT modules
fusion scan 10.10.0.0/24 --nmap "-T4 -sC -sV" --osint all

# Import historical files
fusion import scans/example.xml intel/spiderfoot_acme.json

# Correlate & view results
fusion find --domain acme.corp
fusion find --ip 10.10.0.42 --format tree

# Export to graph DB
fusion export --neo4j neo_acme.csv
