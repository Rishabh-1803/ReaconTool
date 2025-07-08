// Data storage
const appData = {
  spiderfoot_data: [
    {
      target: "example.com",
      type: "Domain",
      finding: "DNS Record",
      value: "192.168.1.10",
      source: "Public DNS",
      risk_level: "Low",
      category: "Infrastructure"
    },
    {
      target: "example.com", 
      type: "Subdomain",
      finding: "admin.example.com",
      value: "192.168.1.15",
      source: "Certificate Transparency",
      risk_level: "Medium",
      category: "Attack Surface"
    },
    {
      target: "example.com",
      type: "Email",
      finding: "admin@example.com",
      value: "Found in breach data",
      source: "HaveIBeenPwned",
      risk_level: "High",
      category: "Credentials"
    },
    {
      target: "example.com",
      type: "IP Range",
      finding: "192.168.1.0/24",
      value: "Company network range",
      source: "WHOIS",
      risk_level: "Medium",
      category: "Infrastructure"
    },
    {
      target: "example.com",
      type: "Technology",
      finding: "Apache 2.4.41",
      value: "Web server version",
      source: "HTTP Headers",
      risk_level: "Medium",
      category: "Technology Stack"
    }
  ],
  nmap_data: [
    {
      ip: "192.168.1.10",
      port: 80,
      service: "HTTP",
      version: "Apache 2.4.41",
      state: "open",
      banner: "Apache/2.4.41 (Ubuntu)",
      risk_level: "Low",
      vulnerabilities: []
    },
    {
      ip: "192.168.1.10",
      port: 443,
      service: "HTTPS",
      version: "Apache 2.4.41",
      state: "open",
      banner: "Apache/2.4.41 SSL",
      risk_level: "Low",
      vulnerabilities: []
    },
    {
      ip: "192.168.1.15",
      port: 22,
      service: "SSH",
      version: "OpenSSH 7.6p1",
      state: "open",
      banner: "SSH-2.0-OpenSSH_7.6p1",
      risk_level: "Medium",
      vulnerabilities: ["CVE-2018-15473"]
    },
    {
      ip: "192.168.1.15",
      port: 80,
      service: "HTTP",
      version: "Apache 2.4.41",
      state: "open",
      banner: "Apache/2.4.41 (Ubuntu)",
      risk_level: "Medium",
      vulnerabilities: []
    },
    {
      ip: "192.168.1.15",
      port: 3306,
      service: "MySQL",
      version: "5.7.30",
      state: "open",
      banner: "MySQL 5.7.30",
      risk_level: "High",
      vulnerabilities: ["CVE-2019-2614", "CVE-2019-2627"]
    }
  ],
  correlations: [
    {
      osint_finding: "DNS Record",
      osint_type: "Domain",
      osint_risk: "Low",
      nmap_target: "192.168.1.10:80",
      nmap_service: "HTTP",
      nmap_risk: "Low",
      correlation_score: 1.5,
      correlation_reasons: ["Direct IP match", "Similar risk levels", "Infrastructure service match"],
      combined_risk: "Low"
    },
    {
      osint_finding: "DNS Record",
      osint_type: "Domain",
      osint_risk: "Low",
      nmap_target: "192.168.1.10:443",
      nmap_service: "HTTPS",
      nmap_risk: "Low",
      correlation_score: 1.5,
      correlation_reasons: ["Direct IP match", "Similar risk levels", "Infrastructure service match"],
      combined_risk: "Low"
    },
    {
      osint_finding: "admin.example.com",
      osint_type: "Subdomain",
      osint_risk: "Medium",
      nmap_target: "192.168.1.15:22",
      nmap_service: "SSH",
      nmap_risk: "Medium",
      correlation_score: 1.1,
      correlation_reasons: ["Direct IP match", "Similar risk levels"],
      combined_risk: "Medium"
    },
    {
      osint_finding: "admin.example.com",
      osint_type: "Subdomain",
      osint_risk: "Medium",
      nmap_target: "192.168.1.15:3306",
      nmap_service: "MySQL",
      nmap_risk: "High",
      correlation_score: 1.1,
      correlation_reasons: ["Direct IP match", "Similar risk levels"],
      combined_risk: "High"
    },
    {
      osint_finding: "Apache 2.4.41",
      osint_type: "Technology",
      osint_risk: "Medium",
      nmap_target: "192.168.1.10:80",
      nmap_service: "HTTP",
      nmap_risk: "Low",
      correlation_score: 1.2,
      correlation_reasons: ["Technology version match", "Similar risk levels"],
      combined_risk: "Medium"
    },
    {
      osint_finding: "Apache 2.4.41",
      osint_type: "Technology",
      osint_risk: "Medium",
      nmap_target: "192.168.1.15:80",
      nmap_service: "HTTP",
      nmap_risk: "Medium",
      correlation_score: 1.2,
      correlation_reasons: ["Technology version match", "Similar risk levels"],
      combined_risk: "Medium"
    }
  ]
};

// Application state
let currentTab = 'osint';
let currentSearch = '';
let currentRiskFilter = '';
let selectedOsintRow = null;
let selectedNmapRow = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
  initializeApp();
});

function initializeApp() {
  setupEventListeners();
  updateDashboardStats();
  renderOsintTable();
  renderNmapTable();
  renderCorrelationTable();
}

function setupEventListeners() {
  // Tab navigation
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      switchTab(this.dataset.tab);
    });
  });

  // Search functionality
  document.getElementById('search-input').addEventListener('input', function() {
    currentSearch = this.value.toLowerCase();
    renderCurrentTab();
  });

  // Risk filter
  document.getElementById('risk-filter').addEventListener('change', function() {
    currentRiskFilter = this.value;
    renderCurrentTab();
  });

  // Export functionality
  document.getElementById('export-btn').addEventListener('click', exportResults);
}

function switchTab(tabName) {
  currentTab = tabName;
  
  // Update tab buttons
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.remove('active');
  });
  document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
  
  // Update tab content
  document.querySelectorAll('.tab-pane').forEach(pane => {
    pane.classList.remove('active');
  });
  document.getElementById(`${tabName}-tab`).classList.add('active');
  
  // Clear selections when switching tabs
  clearHighlights();
}

function updateDashboardStats() {
  const totalFindings = appData.spiderfoot_data.length + appData.nmap_data.length;
  const correlationsCount = appData.correlations.length;
  
  // Calculate risk levels correctly
  const allItems = [...appData.spiderfoot_data, ...appData.nmap_data];
  const highRiskCount = allItems.filter(item => item.risk_level === 'High').length;
  const mediumRiskCount = allItems.filter(item => item.risk_level === 'Medium').length;
  
  document.getElementById('total-findings').textContent = totalFindings;
  document.getElementById('correlations-count').textContent = correlationsCount;
  document.getElementById('high-risk').textContent = highRiskCount;
  document.getElementById('medium-risk').textContent = mediumRiskCount;
}

function renderOsintTable() {
  const tbody = document.getElementById('osint-tbody');
  const filteredData = filterData(appData.spiderfoot_data);
  
  tbody.innerHTML = '';
  
  filteredData.forEach((item, index) => {
    const row = document.createElement('tr');
    row.className = 'clickable';
    row.dataset.finding = item.finding;
    row.dataset.type = 'osint';
    
    row.innerHTML = `
      <td>${item.type}</td>
      <td><strong>${item.finding}</strong></td>
      <td>${item.value}</td>
      <td>${item.source}</td>
      <td><span class="status risk-${item.risk_level.toLowerCase()}">${item.risk_level}</span></td>
      <td>${item.category}</td>
    `;
    
    row.addEventListener('click', function() {
      handleOsintRowClick(item, row);
    });
    
    tbody.appendChild(row);
  });
}

function renderNmapTable() {
  const tbody = document.getElementById('nmap-tbody');
  const filteredData = filterData(appData.nmap_data);
  
  tbody.innerHTML = '';
  
  filteredData.forEach((item, index) => {
    const row = document.createElement('tr');
    row.className = 'clickable';
    row.dataset.target = `${item.ip}:${item.port}`;
    row.dataset.type = 'nmap';
    
    const vulnerabilityDisplay = item.vulnerabilities.length > 0 
      ? item.vulnerabilities.map(vuln => `<span class="vulnerability" title="Click for CVE details">${vuln}</span>`).join(' ')
      : 'None';
    
    row.innerHTML = `
      <td>${item.ip}</td>
      <td>${item.port}</td>
      <td>${item.service}</td>
      <td>${item.version}</td>
      <td>${item.state}</td>
      <td><span class="status risk-${item.risk_level.toLowerCase()}">${item.risk_level}</span></td>
      <td class="vulnerabilities">${vulnerabilityDisplay}</td>
    `;
    
    row.addEventListener('click', function() {
      handleNmapRowClick(item, row);
    });
    
    tbody.appendChild(row);
  });
}

function renderCorrelationTable() {
  const tbody = document.getElementById('correlation-tbody');
  const filteredData = filterCorrelationData(appData.correlations);
  
  tbody.innerHTML = '';
  
  filteredData.forEach((item, index) => {
    const row = document.createElement('tr');
    row.dataset.index = index;
    
    const scoreClass = getCorrelationScoreClass(item.correlation_score);
    const reasonsDisplay = item.correlation_reasons.join(', ');
    
    row.innerHTML = `
      <td><strong>${item.osint_finding}</strong></td>
      <td>${item.osint_type}</td>
      <td>${item.nmap_target}</td>
      <td>${item.nmap_service}</td>
      <td><span class="correlation-score ${scoreClass}" title="Correlation strength indicator">${item.correlation_score.toFixed(1)}</span></td>
      <td><span class="status risk-${item.combined_risk.toLowerCase()}">${item.combined_risk}</span></td>
      <td title="${reasonsDisplay}">${reasonsDisplay}</td>
    `;
    
    tbody.appendChild(row);
  });
}

function filterData(data) {
  return data.filter(item => {
    const matchesSearch = !currentSearch || 
      Object.values(item).some(value => {
        if (value === null || value === undefined) return false;
        return value.toString().toLowerCase().includes(currentSearch);
      });
    
    const matchesRiskFilter = !currentRiskFilter || 
      item.risk_level === currentRiskFilter;
    
    return matchesSearch && matchesRiskFilter;
  });
}

function filterCorrelationData(data) {
  return data.filter(item => {
    const matchesSearch = !currentSearch || 
      Object.values(item).some(value => {
        if (value === null || value === undefined) return false;
        if (Array.isArray(value)) {
          return value.some(v => v.toString().toLowerCase().includes(currentSearch));
        }
        return value.toString().toLowerCase().includes(currentSearch);
      });
    
    const matchesRiskFilter = !currentRiskFilter || 
      item.combined_risk === currentRiskFilter;
    
    return matchesSearch && matchesRiskFilter;
  });
}

function getCorrelationScoreClass(score) {
  if (score >= 1.2) return 'strong';
  if (score >= 1.0) return 'moderate';
  return 'weak';
}

function handleOsintRowClick(osintItem, row) {
  clearHighlights();
  selectedOsintRow = row;
  row.classList.add('highlighted');
  
  // Find and highlight related nmap findings
  const relatedCorrelations = appData.correlations.filter(corr => 
    corr.osint_finding === osintItem.finding
  );
  
  // Highlight related nmap rows
  relatedCorrelations.forEach(corr => {
    const nmapRows = document.querySelectorAll('#nmap-tbody tr');
    nmapRows.forEach(nmapRow => {
      const target = nmapRow.dataset.target;
      if (target === corr.nmap_target) {
        nmapRow.classList.add('highlighted');
      }
    });
  });
  
  // Show notification
  showNotification(`Found ${relatedCorrelations.length} related network scan result(s)`);
}

function handleNmapRowClick(nmapItem, row) {
  clearHighlights();
  selectedNmapRow = row;
  row.classList.add('highlighted');
  
  // Find and highlight related OSINT findings
  const target = `${nmapItem.ip}:${nmapItem.port}`;
  const relatedCorrelations = appData.correlations.filter(corr => 
    corr.nmap_target === target
  );
  
  // Highlight related OSINT rows
  relatedCorrelations.forEach(corr => {
    const osintRows = document.querySelectorAll('#osint-tbody tr');
    osintRows.forEach(osintRow => {
      const finding = osintRow.dataset.finding;
      if (finding === corr.osint_finding) {
        osintRow.classList.add('highlighted');
      }
    });
  });
  
  // Show notification
  showNotification(`Found ${relatedCorrelations.length} related OSINT finding(s)`);
}

function clearHighlights() {
  document.querySelectorAll('.highlighted').forEach(el => {
    el.classList.remove('highlighted');
  });
  selectedOsintRow = null;
  selectedNmapRow = null;
}

function renderCurrentTab() {
  switch(currentTab) {
    case 'osint':
      renderOsintTable();
      break;
    case 'nmap':
      renderNmapTable();
      break;
    case 'correlations':
      renderCorrelationTable();
      break;
  }
}

function exportResults() {
  const data = {
    osint_findings: appData.spiderfoot_data,
    nmap_results: appData.nmap_data,
    correlations: appData.correlations,
    export_timestamp: new Date().toISOString(),
    total_findings: appData.spiderfoot_data.length + appData.nmap_data.length,
    correlations_count: appData.correlations.length
  };
  
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `correlation-analysis-${new Date().toISOString().split('T')[0]}.json`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  
  // Show export confirmation
  showNotification('Analysis results exported successfully!');
}

function showNotification(message) {
  // Create notification element
  const notification = document.createElement('div');
  notification.className = 'notification';
  notification.textContent = message;
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: #4fd1c7;
    color: #1a202c;
    padding: 16px 24px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    font-weight: 500;
    animation: slideIn 0.3s ease-out;
  `;
  
  document.body.appendChild(notification);
  
  // Remove notification after 3 seconds
  setTimeout(() => {
    notification.style.animation = 'slideOut 0.3s ease-in';
    setTimeout(() => {
      document.body.removeChild(notification);
    }, 300);
  }, 3000);
}

// Add notification animations to CSS
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from {
      transform: translateX(100%);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }
  
  @keyframes slideOut {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(100%);
      opacity: 0;
    }
  }
`;
document.head.appendChild(style);

// Add tooltip functionality
document.addEventListener('mouseover', function(event) {
  const element = event.target;
  
  if (element.classList.contains('vulnerability')) {
    const cve = element.textContent;
    showTooltip(element, `Vulnerability: ${cve} - Security issue requiring attention`);
  } else if (element.classList.contains('correlation-score')) {
    const score = parseFloat(element.textContent);
    let description = '';
    
    if (score >= 1.2) {
      description = 'Strong correlation - High confidence in relationship between OSINT and network findings';
    } else if (score >= 1.0) {
      description = 'Moderate correlation - Some relationship indicators present';
    } else {
      description = 'Weak correlation - Limited relationship evidence';
    }
    
    showTooltip(element, description);
  } else if (element.classList.contains('status')) {
    const riskLevel = element.textContent;
    let description = '';
    
    switch(riskLevel) {
      case 'High':
        description = 'High risk - Requires immediate attention and remediation';
        break;
      case 'Medium':
        description = 'Medium risk - Should be addressed during next maintenance window';
        break;
      case 'Low':
        description = 'Low risk - Monitor and address as resources permit';
        break;
    }
    
    showTooltip(element, description);
  }
});

document.addEventListener('mouseout', function() {
  hideTooltip();
});

function showTooltip(element, text) {
  let tooltip = document.getElementById('tooltip');
  if (!tooltip) {
    tooltip = document.createElement('div');
    tooltip.id = 'tooltip';
    tooltip.className = 'tooltip';
    document.body.appendChild(tooltip);
  }
  
  tooltip.textContent = text;
  tooltip.classList.remove('hidden');
  tooltip.style.display = 'block';
  
  const rect = element.getBoundingClientRect();
  tooltip.style.left = `${rect.left + window.scrollX}px`;
  tooltip.style.top = `${rect.top + window.scrollY - tooltip.offsetHeight - 10}px`;
  
  // Adjust position if tooltip goes off screen
  if (rect.left + tooltip.offsetWidth > window.innerWidth) {
    tooltip.style.left = `${window.innerWidth - tooltip.offsetWidth - 10}px`;
  }
  
  if (rect.top - tooltip.offsetHeight < 0) {
    tooltip.style.top = `${rect.bottom + window.scrollY + 10}px`;
  }
}

function hideTooltip() {
  const tooltip = document.getElementById('tooltip');
  if (tooltip) {
    tooltip.style.display = 'none';
    tooltip.classList.add('hidden');
  }
}

// Add click handlers for CVE links
document.addEventListener('click', function(event) {
  if (event.target.classList.contains('vulnerability')) {
    const cve = event.target.textContent;
    const url = `https://cve.mitre.org/cgi-bin/cvename.cgi?name=${cve}`;
    window.open(url, '_blank');
  }
});

// Performance optimization
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Initialize tooltips and help system
function initializeHelp() {
  const helpElements = document.querySelectorAll('.help-text');
  helpElements.forEach(element => {
    element.addEventListener('click', function() {
      const helpContent = this.getAttribute('data-help') || this.textContent;
      showNotification(helpContent);
    });
  });
}

// Call help initialization
document.addEventListener('DOMContentLoaded', function() {
  setTimeout(initializeHelp, 100);
});

// Add keyboard navigation
document.addEventListener('keydown', function(event) {
  if (event.key === 'Escape') {
    clearHighlights();
    hideTooltip();
  }
  
  if (event.ctrlKey && event.key === 'e') {
    event.preventDefault();
    exportResults();
  }
});

// Add focus management for accessibility
document.addEventListener('focus', function(event) {
  if (event.target.classList.contains('clickable')) {
    event.target.style.outline = '2px solid #4fd1c7';
  }
}, true);

document.addEventListener('blur', function(event) {
  if (event.target.classList.contains('clickable')) {
    event.target.style.outline = 'none';
  }
}, true);