---
id: odoo-task-321
type: Project Task
project: "Prototypes DEVOPS : Odoo ERP"
stage: "Sprint Complete"
assignees: "Rohit Thumu"
last_updated: 2026-06-06 06:03:34
sync_date: 2026-08-15 21:08:36
tags:
  - odoo/task
  - project/prototypes-devops-:-odoo-erp
  - status/sprint-complete
---
# Task: Odoo Industry  Consultant

- **Project:** [[Prototypes DEVOPS : Odoo ERP]]
- **Odoo Stage:** Sprint Complete
- **Assignees:** Rohit Thumu
- **Last Sync:** 2026-08-15 21:08:36

## Description
This document contains proprietary and confidential information of SystemaOps. It is intended solely for authorized personnel involved in this project. Any unauthorized review, use, disclosure, or distribution of its contents is strictly prohibited. Recipients must maintain the confidentiality of this information and may not copy, share, or use it for purposes outside the scope of this project without prior written permission from SystemaOps.https://consultant.systemaops.com/Tip: Use Chatgpt , Claude Code, Gemini Pro, Perplexity Pro, Cursor Free or Codeium Free for AI suggestions.OverviewGoal: Create industry-specific Odoo modules for Odoo 18 (stable) and Odoo 19 (latest), containerized with Docker for sales demos.Reference Repository (for ideas only): https://github.com/odoo/industryWorkflow: Customize Docker → Test Locally → Demo → Approve → Push to GitLab (when ready) → DeployNote: GitLab is not yet deployed. Initial development will be done locally, and GitLab integration will be set up once ready.1. Task BreakdownSetup
 Install Docker, Git, Python 3.10+, IDE
 Clone reference repo for ideas: git clone https://github.com/odoo/industry
 Study existing industry modules from reference repo
 Create base docker-compose template
 Set up local Git repository (GitLab to be configured later)
Module Development
 Identify industries from reference repo (use as inspiration)
 Create module scaffolding (models, views, security)
 Develop Odoo 18 modules (don't copy directly - create your own)
 Port to Odoo 19 (add latest features)
Dockerization (Using docker-compose)
 Copy base docker-compose.yml template for each industry
 Customize docker-compose.yml per industry (ports, volumes, services)
 Configure .env files with industry-specific variables
 Set up persistent volumes for data retention
 No custom Dockerfile needed - use official Odoo images
Testing
 Test each module locally
 Verify containers start correctly
 Test all CRUD operations
 Performance testing
Demo & Deployment
 Prepare demo data and scripts
 Conduct internal demo
 Get approval
 [Future] Set up GitLab repositories
 [Future] Push code to GitLab
 [Future] Deploy to sales demo environment
2. Architecture DiagramsSystem OverviewSales Demo Environment
├── Industry 1 (Odoo 18) ─┐
├── Industry 1 (Odoo 19)  │
├── Industry 2 (Odoo 18)  ├─→ Nginx Proxy ─→ Sales Team
├── Industry 2 (Odoo 19)  │
└── Industry N (...)      ┘Docker Stack (Per Industry)┌─────────────────────┐
│ Odoo Container      │
│ - Custom modules    │
│ - Port 8069        │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ PostgreSQL          │
│ - Industry DB       │
│ - Port 5432        │
└─────────────────────┘3. Module Structureindustry-[name]/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── [industry]_model.py
├── views/
│   ├── [industry]_views.xml
│   └── [industry]_menus.xml
├── security/
│   ├── ir.model.access.csv
│   └── security_groups.xml
├── data/
│   └── demo_data.xml
├── tests/
│   └── test_[industry].py
├── docker/
│   ├── docker-compose.yml
│   ├── .env
│   └── odoo.conf
└── README.md4. Docker Configurationdocker-compose.yml Templateyamlversion: '3.8'

services:
  web:
    image: odoo:${ODOO_VERSION}
    container_name: odoo-${INDUSTRY_NAME}-${ODOO_VERSION}
    depends_on:
      - db
    ports:
      - "${ODOO_PORT}:8069"
    volumes:
      - ./addons:/mnt/extra-addons
      - odoo-data:/var/lib/odoo
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=odoo

  db:
    image: postgres:15
    container_name: postgres-${INDUSTRY_NAME}
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=odoo
      - POSTGRES_PASSWORD=odoo
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  odoo-data:
  db-data:.env Templateenv# Odoo Configuration
ODOO_VERSION=18.0
INDUSTRY_NAME=healthcare
ODOO_PORT=8069

# Database Configuration
POSTGRES_VERSION=15
POSTGRES_DB=odoo
POSTGRES_USER=odoo
POSTGRES_PASSWORD=odoo

# Optional: Multi-instance setup
# ODOO_PORT=8069  # For Odoo 18
# ODOO_PORT=8070  # For Odoo 19 (different port)odoo.conf Templateini[options]
addons_path = /mnt/extra-addons
data_dir = /var/lib/odoo
admin_passwd = admin
db_host = db
db_port = 5432
db_user = odoo
db_password = odoo5. Git Workflow (For Future GitLab Setup)Note: GitLab is not yet deployed. Use local Git for now.Current: Local Git Onlybash# Initialize local repository
git init
git add .
git commit -m "Initial commit: [industry] module"

# Keep commits organized for future GitLab push
git log --onelineFuture: GitLab Branch Strategymain
├── develop
│   ├── feature/industry-[name]-odoo18
│   └── feature/industry-[name]-odoo19Future: GitLab Commandsbash# When GitLab is ready:
# Add remote
git remote add origin https://gitlab.com/yourproject/industry-[name].git

# Create branch
git checkout -b feature/industry-healthcare-odoo18

# Commit
git add .
git commit -m "feat(healthcare): Add patient module"

# Push to GitLab
git push origin feature/industry-healthcare-odoo18Commit Message Convention (Use Now)feat(scope): subject         # New feature
fix(scope): subject          # Bug fix
docs(scope): subject         # Documentation
refactor(scope): subject     # Code refactoringExample:feat(healthcare): Add patient management module for Odoo 18

- Implemented patient model with demographics
- Added appointment scheduling views
- Configured security groups6. Testing ChecklistModule Testing
 Module installs without errors
 All menu items visible
 Create/Read/Update/Delete works
 Security groups enforced
 Demo data loads correctly
Docker Testing
 docker-compose up -d starts all services
 Access http://localhost:8069 (or configured port)
 Database connection successful
 Custom modules visible in Apps menu
 Data persists after docker-compose restart
 No errors in docker-compose logs
 Volumes created: docker volume ls
7. DeploymentLocal Testingbash# Navigate to industry docker folder
cd industry-[name]/docker

# Configure environment
cp .env.example .env
# Edit .env with your settings (ODOO_VERSION, INDUSTRY_NAME, ports)

# Start containers using docker-compose
docker-compose up -d

# Watch logs
docker-compose logs -f

# Access Odoo
# Browser: http://localhost:8069
# Create database and install modulesProduction Deploybash# NOTE: This is for future when GitLab and demo server are ready

# Push to GitLab (when available)
git push origin main

# SSH to demo server (when available)
ssh user@demo-server.com

# Navigate to project
cd /opt/industries/industry-[name]/docker

# Pull latest changes
git pull origin main

# Deploy with docker-compose
docker-compose -f docker-compose.prod.yml up -d

# Verify deployment
docker-compose ps
docker-compose logs -f web8. Quick ReferenceEssential docker-compose Commandsbash# Start all services (detached mode)
docker-compose up -d

# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v

# View logs (all services)
docker-compose logs -f

# View logs (specific service)
docker-compose logs -f web

# Restart specific service
docker-compose restart web

# Check service status
docker-compose ps

# Execute command in running container
docker-compose exec web bash

# Pull latest images
docker-compose pull

# Rebuild and restart
docker-compose up -d --build

# Scale a service (for load testing)
docker-compose up -d --scale web=3Essential Odoo Commands (Inside Container)bashodoo -d dbname -i module_name --stop-after-init    # Install
odoo -d dbname -u module_name --stop-after-init    # Update
odoo -d dbname --test-enable                       # TestEssential Git Commandsbashgit status                        # Check status
git add .                         # Stage changes
git commit -m "message"           # Commit
git push origin branch-name       # Push
git pull origin develop           # Pull latest9. Development StagesStage 1: Environment Setup
Install: Docker, Git, Python, VS Code
Clone reference repo: git clone https://github.com/odoo/industry
Study the reference modules - understand structure, don't copy directly
Read Odoo docs: https://www.odoo.com/documentation/18.0/developer/
Set up local Git repository
Stage 2: First Module
Pick an industry (get ideas from reference repo)
Create your own module structure (don't copy directly)
Add basic model and view
Test locally with docker-compose
Commit to local Git repository
Stage 3: Full Development
Complete Odoo 18 module
Port to Odoo 19
Write tests
Create docker-compose.yml for the industry
Configure .env file with proper ports
Stage 4: Testing & Validation
Test locally with docker-compose
Verify all services running with docker-compose ps
Run all test cases
Fix any issues found
Stage 5: Demo & Deployment
Prepare demo data and presentation
Demo to team
Get approval
Commit final version to local Git
[Future] Push to GitLab when available
[Future] Deploy to demo server
10. Common Industries (Reference)Based on https://github.com/odoo/industry (use for inspiration only):
Healthcare
Retail
Manufacturing
Real Estate
Education
Hospitality
Construction
Automotive
Agriculture
Financial Services
Important Notes:
The GitHub repository is for reference only - study the structure and patterns
Create your own modules - don't copy directly from the reference
Adapt ideas to your specific business requirements
Check the reference repo to understand industry-specific needs
11. TroubleshootingContainer won't startbash# Check logs for errors
docker-compose logs -f

# Clean restart
docker-compose down -v
docker-compose up -d

# Check which ports are in use
docker-compose ps
netstat -tuln | grep 8069Module not appearingbash# Enter Odoo container
docker-compose exec web bash

# Update module list
odoo -d dbname -u base --stop-after-init

# Or restart Odoo service
docker-compose restart webPermission errors on volumesbash# Fix ownership of addon directory
sudo chown -R $USER:$USER ./addons

# Or run with proper permissions in docker-compose.yml
# user: "${UID}:${GID}"Database connection issuesbash# Check if database container is running
docker-compose ps

# Recreate database
docker-compose down
docker volume rm $(docker volume ls -q | grep db-data)
docker-compose up -dPort already in usebash# Find what's using the port
sudo lsof -i :8069

# Change port in .env file
# ODOO_PORT=8070

# Restart with new port
docker-compose down
docker-compose up -dChanges not reflectingbash# Restart Odoo service
docker-compose restart web

# Or force recreation
docker-compose up -d --force-recreate web
