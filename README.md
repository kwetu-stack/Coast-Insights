# Coast Insights™

**Executive Sales Intelligence & Decision Support System**

---

## Overview

Coast Insights™ is a Flask-based Executive Decision Support System (EDSS) designed to transform field sales activities into actionable business intelligence.

The platform enables executives to monitor market performance, customer activity, competitor intelligence, merchandising standards, opportunities, and strategic recommendations from a single dashboard.

Unlike traditional CRM systems, Coast Insights focuses on executive visibility and decision support rather than transaction processing.

---

## Project Goals

- Capture valuable market intelligence
- Improve executive decision making
- Track customer opportunities
- Monitor competitor activities
- Record trade visit findings
- Generate management reports
- Build an organizational knowledge base

---

## Technology Stack

- Python 3.12
- Flask
- SQLAlchemy
- Flask-Migrate
- Flask-Login
- SQLite (Development)
- Bootstrap 5
- HTML5
- CSS3
- JavaScript

---

## Architecture

The application follows the Flask Application Factory pattern.

```
app.py
│
├── config.py
├── extensions.py
├── blueprints/
├── models/
├── templates/
├── static/
├── instance/
├── uploads/
├── exports/
└── docs/
```

---

## Security Philosophy

Coast Insights is designed around an administrator-first security model.

### System Owner

- Full control
- System configuration
- User management
- Create/Edit/Delete records
- Approve recommendations
- Access audit logs

### Executive Users

- Read-only access
- Dashboard viewing
- Report downloads
- Market intelligence viewing

No public registration is provided.

---

## Development Principles

- One responsibility per file
- Blueprint-driven architecture
- Decorator-based authorization
- Auditability by design
- Incremental development
- Git version control

---

## Current Status

✅ Flask Foundation Complete

Current milestone:

Version 0.1 Foundation

---

## Roadmap

- Authentication
- User Management
- Dashboard
- Trade Visits
- Customers
- Opportunities
- Competitor Intelligence
- Market Intelligence
- Recommendations
- Reports
- Knowledge Base

---

## Developer

**KWETU PARTNERS LTD**

Project: Coast Insights™

Copyright © 2026