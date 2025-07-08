import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import numpy as np
import json

# Load the data
data = {
  "nodes": [
    {"id": "DNS_Record", "label": "DNS Record (192.168.1.10)", "type": "spiderfoot", "risk": "Low", "category": "Domain"},
    {"id": "admin_subdomain", "label": "admin.example.com", "type": "spiderfoot", "risk": "Medium", "category": "Subdomain"},
    {"id": "admin_email", "label": "admin@example.com", "type": "spiderfoot", "risk": "High", "category": "Email"},
    {"id": "ip_range", "label": "192.168.1.0/24", "type": "spiderfoot", "risk": "Medium", "category": "IP Range"},
    {"id": "apache_tech", "label": "Apache 2.4.41", "type": "spiderfoot", "risk": "Medium", "category": "Technology"},
    {"id": "nmap_80_10", "label": "192.168.1.10:80 (HTTP)", "type": "nmap", "risk": "Low", "service": "HTTP"},
    {"id": "nmap_443_10", "label": "192.168.1.10:443 (HTTPS)", "type": "nmap", "risk": "Low", "service": "HTTPS"},
    {"id": "nmap_22_15", "label": "192.168.1.15:22 (SSH)", "type": "nmap", "risk": "Medium", "service": "SSH"},
    {"id": "nmap_80_15", "label": "192.168.1.15:80 (HTTP)", "type": "nmap", "risk": "Medium", "service": "HTTP"},
    {"id": "nmap_3306_15", "label": "192.168.1.15:3306 (MySQL)", "type": "nmap", "risk": "High", "service": "MySQL"}
  ],
  "edges": [
    {"source": "DNS_Record", "target": "nmap_80_10", "weight": 1.5, "type": "Direct IP + Infrastructure"},
    {"source": "DNS_Record", "target": "nmap_443_10", "weight": 1.5, "type": "Direct IP + Infrastructure"},
    {"source": "admin_subdomain", "target": "nmap_22_15", "weight": 1.1, "type": "Direct IP Match"},
    {"source": "admin_subdomain", "target": "nmap_80_15", "weight": 1.1, "type": "Direct IP Match"},
    {"source": "admin_subdomain", "target": "nmap_3306_15", "weight": 1.1, "type": "Direct IP Match"},
    {"source": "apache_tech", "target": "nmap_80_10", "weight": 1.2, "type": "Technology Match"},
    {"source": "apache_tech", "target": "nmap_80_15", "weight": 1.2, "type": "Technology Match"},
    {"source": "ip_range", "target": "nmap_80_10", "weight": 0.7, "type": "Network Range"},
    {"source": "ip_range", "target": "nmap_443_10", "weight": 0.7, "type": "Network Range"},
    {"source": "ip_range", "target": "nmap_80_15", "weight": 0.7, "type": "Network Range"}
  ]
}

# Create NetworkX graph for layout
G = nx.Graph()

# Add nodes to the graph
for node in data['nodes']:
    G.add_node(node['id'], **node)

# Add edges to the graph
for edge in data['edges']:
    G.add_edge(edge['source'], edge['target'], weight=edge['weight'], type=edge['type'])

# Use spring layout for positioning with more spacing
pos = nx.spring_layout(G, k=4, iterations=100)

# Define colors for different types
color_map = {
    'spiderfoot': '#1FB8CD',  # Strong cyan
    'nmap': '#FFC185'         # Light orange
}

# Define size mapping for risk levels - more distinct sizes
size_map = {
    'Low': 25,
    'Medium': 40,
    'High': 55
}

# Create edge traces with varying thickness based on weight
edge_traces = []
for edge in data['edges']:
    x0, y0 = pos[edge['source']]
    x1, y1 = pos[edge['target']]
    
    # Scale line width based on weight (multiply by 3 for visibility)
    line_width = edge['weight'] * 3
    
    edge_trace = go.Scatter(
        x=[x0, x1, None], y=[y0, y1, None],
        line=dict(width=line_width, color='#888'),
        hoverinfo='text',
        hovertext=f"Weight: {edge['weight']}<br>Type: {edge['type'][:15]}",
        mode='lines',
        showlegend=False
    )
    edge_traces.append(edge_trace)

# Create node traces for each type
spiderfoot_nodes = [node for node in data['nodes'] if node['type'] == 'spiderfoot']
nmap_nodes = [node for node in data['nodes'] if node['type'] == 'nmap']

# Spiderfoot nodes - truncate labels to fit better
sf_x = [pos[node['id']][0] for node in spiderfoot_nodes]
sf_y = [pos[node['id']][1] for node in spiderfoot_nodes]
sf_text = []
for node in spiderfoot_nodes:
    label = node['label']
    if len(label) > 15:
        # Smart truncation
        if 'DNS Record' in label:
            sf_text.append('DNS Rec')
        elif 'admin.example.com' in label:
            sf_text.append('admin.ex.com')
        elif 'admin@example.com' in label:
            sf_text.append('admin@ex.com')
        elif '192.168.1.0/24' in label:
            sf_text.append('192.168.1.0/24')
        elif 'Apache' in label:
            sf_text.append('Apache 2.4.41')
        else:
            sf_text.append(label[:15])
    else:
        sf_text.append(label)

sf_sizes = [size_map[node['risk']] for node in spiderfoot_nodes]
sf_hover = [f"ID: {node['id']}<br>Risk: {node['risk']}<br>Cat: {node.get('category', 'N/A')}" for node in spiderfoot_nodes]

spiderfoot_trace = go.Scatter(
    x=sf_x, y=sf_y,
    mode='markers+text',
    text=sf_text,
    textposition="bottom center",
    textfont=dict(size=10),
    hoverinfo='text',
    hovertext=sf_hover,
    marker=dict(
        size=sf_sizes,
        color=color_map['spiderfoot'],
        line=dict(width=2, color='white')
    ),
    name='Spiderfoot'
)

# Nmap nodes - truncate labels to fit better
nmap_x = [pos[node['id']][0] for node in nmap_nodes]
nmap_y = [pos[node['id']][1] for node in nmap_nodes]
nmap_text = []
for node in nmap_nodes:
    label = node['label']
    if len(label) > 15:
        # Smart truncation for nmap labels
        if '192.168.1.10:80' in label:
            nmap_text.append('10:80 HTTP')
        elif '192.168.1.10:443' in label:
            nmap_text.append('10:443 HTTPS')
        elif '192.168.1.15:22' in label:
            nmap_text.append('15:22 SSH')
        elif '192.168.1.15:80' in label:
            nmap_text.append('15:80 HTTP')
        elif '192.168.1.15:3306' in label:
            nmap_text.append('15:3306 MySQL')
        else:
            nmap_text.append(label[:15])
    else:
        nmap_text.append(label)

nmap_sizes = [size_map[node['risk']] for node in nmap_nodes]
nmap_hover = [f"ID: {node['id']}<br>Risk: {node['risk']}<br>Svc: {node.get('service', 'N/A')}" for node in nmap_nodes]

nmap_trace = go.Scatter(
    x=nmap_x, y=nmap_y,
    mode='markers+text',
    text=nmap_text,
    textposition="bottom center",
    textfont=dict(size=10),
    hoverinfo='text',
    hovertext=nmap_hover,
    marker=dict(
        size=nmap_sizes,
        color=color_map['nmap'],
        line=dict(width=2, color='white')
    ),
    name='Nmap'
)

# Create the figure
fig = go.Figure(data=edge_traces + [spiderfoot_trace, nmap_trace])

# Update layout
fig.update_layout(
    title="OSINT Findings Correlation Network",
    showlegend=True,
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
    hovermode='closest',
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    plot_bgcolor='white'
)

# Update axes to remove ticks and labels
fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False)

# Save the chart
fig.write_image("osint_correlation_network.png")