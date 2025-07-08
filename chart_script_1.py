import math, json, plotly.graph_objects as go

# Brand colors in required order
brand_colors = ["#1FB8CD", "#FFC185", "#ECEBD5", "#5D878F", "#D2BA4C"]

# Provided JSON data
data_json = {
  "phases": [
    {
      "id": 1,
      "name": "OSINT Collection",
      "tool": "Spiderfoot",
      "description": "Passive reconnaissance using public sources",
      "activities": ["DNS Records", "Subdomains", "Email Addresses", "IP Ranges", "Technology Stack"],
      "x": 1,
      "y": 5,
      "color": "#2563eb"
    },
    {
      "id": 2,
      "name": "Target Identification",
      "tool": "Analysis",
      "description": "Identify targets from OSINT findings",
      "activities": ["IP Addresses", "Domain Names", "Infrastructure Mapping"],
      "x": 3,
      "y": 5,
      "color": "#7c3aed"
    },
    {
      "id": 3,
      "name": "Network Scanning",
      "tool": "nmap",
      "description": "Active reconnaissance of identified targets",
      "activities": ["Port Scanning", "Service Detection", "Version Identification", "Vulnerability Scanning"],
      "x": 5,
      "y": 5,
      "color": "#dc2626"
    },
    {
      "id": 4,
      "name": "Correlation Analysis",
      "tool": "Combined",
      "description": "Connect OSINT and network scan findings",
      "activities": ["IP Matching", "Technology Correlation", "Risk Assessment", "Pattern Recognition"],
      "x": 3,
      "y": 3,
      "color": "#059669"
    },
    {
      "id": 5,
      "name": "Risk Assessment",
      "tool": "Analysis",
      "description": "Evaluate combined security posture",
      "activities": ["Vulnerability Prioritization", "Attack Surface Analysis", "Threat Modeling"],
      "x": 3,
      "y": 1,
      "color": "#ea580c"
    }
  ],
  "connections": [
    {"from": 1, "to": 2, "label": "Identify Targets"},
    {"from": 2, "to": 3, "label": "Scan Targets"},
    {"from": 1, "to": 4, "label": "OSINT Data"},
    {"from": 3, "to": 4, "label": "Scan Results"},
    {"from": 4, "to": 5, "label": "Correlated Findings"}
  ]
}

phases = data_json["phases"]
connections = data_json["connections"]

# Map id to phase data and assign brand colors
id_to_phase = {}
for idx, phase in enumerate(phases):
    phase_color = brand_colors[idx % len(brand_colors)]
    phase["brand_color"] = phase_color
    id_to_phase[phase["id"]] = phase

fig = go.Figure()

# Add node scatter traces (one per phase for legend entries)
legend_names = ["OSINT", "Target ID", "Net Scan", "Correlate", "Risk Assess"]
for idx, phase in enumerate(phases):
    fig.add_trace(
        go.Scatter(
            x=[phase["x"]],
            y=[phase["y"]],
            mode="markers",
            marker=dict(size=50, color=phase["brand_color"], line=dict(width=2, color="#000")),
            name=legend_names[idx],
            hoverinfo="skip"
        )
    )

# Build arrow shapes for each connection
shapes = []
arrow_size = 0.3  # length of arrowhead
arrow_angle = math.radians(25)  # arrowhead angle
for conn in connections:
    src = id_to_phase[conn["from"]]
    tgt = id_to_phase[conn["to"]]
    x0, y0 = src["x"], src["y"]
    x1, y1 = tgt["x"], tgt["y"]

    # Base line path
    path = f"M{x0},{y0} L{x1},{y1} "

    # Calculate arrowhead coordinates
    dx = x1 - x0
    dy = y1 - y0
    length = math.hypot(dx, dy)
    if length == 0:
        continue
    ux, uy = dx / length, dy / length  # unit vector

    # Rotate vectors for arrowhead sides
    left_angle = math.atan2(uy, ux) + math.pi - arrow_angle
    right_angle = math.atan2(uy, ux) + math.pi + arrow_angle

    lx = x1 + arrow_size * math.cos(left_angle)
    ly = y1 + arrow_size * math.sin(left_angle)
    rx = x1 + arrow_size * math.cos(right_angle)
    ry = y1 + arrow_size * math.sin(right_angle)

    # Add arrowhead lines to path
    path += f"M{x1},{y1} L{lx},{ly} M{x1},{y1} L{rx},{ry}"

    shapes.append(
        dict(
            type="path",
            path=path,
            line=dict(color="#666", width=2),
            layer="below",
            xref="x",
            yref="y"
        )
    )

# Add text annotations for phase names
annotations = []
phase_short_names = ["OSINT Collect", "Target ID", "Net Scan", "Correlate", "Risk Assess"]
for idx, phase in enumerate(phases):
    annotations.append(
        dict(
            x=phase["x"],
            y=phase["y"],
            text=phase_short_names[idx],
            showarrow=False,
            font=dict(size=10, color="black"),
            xanchor="center",
            yanchor="middle"
        )
    )

# Add text annotations for arrow labels
arrow_labels = ["ID Targets", "Scan Targets", "OSINT Data", "Scan Results", "Corr Findings"]
for idx, conn in enumerate(connections):
    src = id_to_phase[conn["from"]]
    tgt = id_to_phase[conn["to"]]
    mid_x = (src["x"] + tgt["x"]) / 2
    mid_y = (src["y"] + tgt["y"]) / 2
    
    annotations.append(
        dict(
            x=mid_x,
            y=mid_y,
            text=arrow_labels[idx],
            showarrow=False,
            font=dict(size=8, color="#666"),
            xanchor="center",
            yanchor="middle",
            bgcolor="white",
            bordercolor="#666",
            borderwidth=1
        )
    )

fig.update_layout(
    title="Recon Workflow",
    shapes=shapes,
    annotations=annotations,
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Hide axes and set ranges
fig.update_xaxes(showticklabels=False, range=[0,6])
fig.update_yaxes(showticklabels=False, range=[0,6])

# Disable clipping
fig.update_traces(cliponaxis=False)

# Save to PNG
fig.write_image("recon_workflow.png")