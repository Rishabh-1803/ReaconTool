import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Load the correlation matrix data
correlation_data = [
    {"osint_type": "Domain Records", "HTTP": 0.9, "HTTPS": 0.8, "SSH": 0.2, "MySQL": 0.1, "FTP": 0.3},
    {"osint_type": "Subdomains", "HTTP": 0.7, "HTTPS": 0.6, "SSH": 0.8, "MySQL": 0.9, "FTP": 0.4},
    {"osint_type": "Email Addresses", "HTTP": 0.3, "HTTPS": 0.2, "SSH": 0.6, "MySQL": 0.4, "FTP": 0.1},
    {"osint_type": "IP Ranges", "HTTP": 0.8, "HTTPS": 0.7, "SSH": 0.5, "MySQL": 0.6, "FTP": 0.5},
    {"osint_type": "Technology Stack", "HTTP": 0.95, "HTTPS": 0.9, "SSH": 0.3, "MySQL": 0.7, "FTP": 0.2},
    {"osint_type": "Breach Data", "HTTP": 0.4, "HTTPS": 0.3, "SSH": 0.8, "MySQL": 0.9, "FTP": 0.2}
]

# Convert to DataFrame
df = pd.DataFrame(correlation_data)
df.set_index('osint_type', inplace=True)

# Prepare data for heatmap
z_values = df.values
x_labels = df.columns.tolist()
y_labels = df.index.tolist()

# Abbreviate long labels to meet 15 character limit
y_labels_short = []
for label in y_labels:
    if len(label) > 15:
        if label == "Domain Records":
            y_labels_short.append("Domain Rec")
        elif label == "Email Addresses":
            y_labels_short.append("Email Addr")
        elif label == "Technology Stack":
            y_labels_short.append("Tech Stack")
        elif label == "Breach Data":
            y_labels_short.append("Breach Data")
        else:
            y_labels_short.append(label[:15])
    else:
        y_labels_short.append(label)

# Create text annotations for correlation values
text_values = []
for i in range(len(z_values)):
    row = []
    for j in range(len(z_values[i])):
        row.append(f"{z_values[i][j]:.2f}")
    text_values.append(row)

# Create heatmap
fig = go.Figure(data=go.Heatmap(
    z=z_values,
    x=x_labels,
    y=y_labels_short,
    text=text_values,
    texttemplate="%{text}",
    textfont={"size": 12},
    colorscale='Viridis',
    showscale=True,
    colorbar=dict(title="Correlation"),
    hoverongaps=False
))

# Update layout
fig.update_layout(
    title="OSINT vs Network Service Correlations",
    xaxis_title="Network Svc",
    yaxis_title="OSINT Type"
)

# Update axes
fig.update_xaxes(side="bottom")
fig.update_yaxes(side="left")

# Save the chart
fig.write_image("osint_nmap_correlation_heatmap.png")