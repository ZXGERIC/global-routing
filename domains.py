"""
40 Domain Agents Configuration for the Routing Experiment
"""

# 40 domains with their descriptions and sample queries
DOMAINS = [
    {
        "name": "travel",
        "description": "Handles all travel-related requests including flight bookings, hotel reservations, car rentals, vacation planning, trip itinerary management, travel documentation, and travel advice.",
        "keywords": ["flight", "hotel", "travel", "vacation", "trip", "booking", "airplane", "hotel", "resort", "airline", "airport"],
        "sub_agents": ["flights", "hotels", "cars", "activities"],
        "sample_queries": [
            "I need to book a flight to Tokyo",
            "Find me a hotel in Paris",
            "Rent a car for next week",
            "Plan a vacation to Hawaii"
        ]
    },
    {
        "name": "finance",
        "description": "Manages financial matters including banking transactions, investment portfolio management, expense tracking, budget planning, financial reports, salary information, and payment processing.",
        "keywords": ["bank", "payment", "expense", "salary", "invest", "budget", "finance", "money", "account", "transaction"],
        "sub_agents": ["banking", "trading", "expenses", "reports"],
        "sample_queries": [
            "Check my bank balance",
            "I want to invest in stocks",
            "Report an expense",
            "Show my financial report"
        ]
    },
    {
        "name": "hr",
        "description": "Human resources department handling employee requests, leave management, benefits administration, payroll inquiries, onboarding processes, training programs, and workplace policies.",
        "keywords": ["leave", "pto", "holiday", "payroll", "benefits", "training", "onboard", "employee", "hr", "policy"],
        "sub_agents": ["payroll", "benefits", "recruiting", "training"],
        "sample_queries": [
            "Request time off for next week",
            "Check my benefits",
            "When do I get paid?",
            "Enroll in training program"
        ]
    },
    {
        "name": "it_support",
        "description": "IT help desk for technical support including password resets, software installation, hardware issues, network connectivity, VPN access, email problems, and device management.",
        "keywords": ["password", "reset", "vpn", "wifi", "computer", "laptop", "software", "install", "network", "email"],
        "sub_agents": ["hardware", "software", "network", "access"],
        "sample_queries": [
            "Reset my password",
            "My VPN is not working",
            "Install new software",
            "Connect to WiFi"
        ]
    },
    {
        "name": "customer_service",
        "description": "Customer service for product inquiries, order status, returns and refunds, complaints, product information, account updates, and general customer assistance.",
        "keywords": ["order", "return", "refund", "complaint", "product", "delivery", "shipment", "support", "help"],
        "sub_agents": ["orders", "returns", "complaints", "info"],
        "sample_queries": [
            "Where is my order?",
            "I want to return this item",
            "File a complaint",
            "Product information"
        ]
    },
    {
        "name": "sales",
        "description": "Sales department for product inquiries, pricing information, quotes and proposals, contract discussions, demo requests, partnership opportunities, and sales-related questions.",
        "keywords": ["buy", "purchase", "price", "quote", "discount", "deal", "contract", "demo", "sales"],
        "sub_agents": ["enterprise", "smb", "partnerships", "quotations"],
        "sample_queries": [
            "I want to buy your product",
            "What's the price?",
            "Request a quote",
            "Schedule a demo"
        ]
    },
    {
        "name": "marketing",
        "description": "Marketing team handling campaign management, content creation, social media, analytics, brand guidelines, marketing materials, and promotional activities.",
        "keywords": ["campaign", "content", "social media", "analytics", "brand", "marketing", "advertise", "promote"],
        "sub_agents": ["campaigns", "content", "analytics", "creative"],
        "sample_queries": [
            "Create a marketing campaign",
            "Post on social media",
            "Show marketing analytics",
            "Review brand guidelines"
        ]
    },
    {
        "name": "legal",
        "description": "Legal department for contract review, compliance matters, intellectual property, regulatory issues, legal documentation, policy review, and legal advice.",
        "keywords": ["contract", "legal", "compliance", "regulation", "policy", "ip", "trademark", "copyright", "lawyer"],
        "sub_agents": ["contracts", "compliance", "ip", "advisory"],
        "sample_queries": [
            "Review this contract",
            "Compliance question",
            "IP registration",
            "Legal advice needed"
        ]
    },
    {
        "name": "operations",
        "description": "Operations team managing supply chain, logistics, inventory management, process optimization, vendor relations, facility management, and operational efficiency.",
        "keywords": ["supply", "chain", "logistics", "inventory", "vendor", "facility", "operations", "process", "optimize"],
        "sub_agents": ["logistics", "inventory", "vendors", "facilities"],
        "sample_queries": [
            "Check inventory levels",
            "Track shipment",
            "Vendor management",
            "Optimize processes"
        ]
    },
    {
        "name": "engineering",
        "description": "Engineering department for software development, technical architecture, code reviews, DevOps, technical documentation, bug fixes, and engineering practices.",
        "keywords": ["code", "develop", "engineer", "architecture", "devops", "bug", "feature", "technical", "api"],
        "sub_agents": ["frontend", "backend", "devops", "qa"],
        "sample_queries": [
            "Review my code",
            "Deploy to production",
            "Fix this bug",
            "API documentation"
        ]
    },
    {
        "name": "product",
        "description": "Product management for feature planning, roadmap, user research, requirements gathering, prioritization, product strategy, and go-to-market planning.",
        "keywords": ["product", "feature", "roadmap", "requirement", "user", "strategy", "backlog", "priority"],
        "sub_agents": ["discovery", "roadmap", "requirements", "growth"],
        "sample_queries": [
            "Add a new feature",
            "Show product roadmap",
            "User research results",
            "Prioritize backlog"
        ]
    },
    {
        "name": "design",
        "description": "Design team for UI/UX design, visual design, design systems, user research, prototyping, design reviews, and brand assets.",
        "keywords": ["design", "ui", "ux", "prototype", "mockup", "wireframe", "visual", "brand"],
        "sub_agents": ["ux", "visual", "research", "systems"],
        "sample_queries": [
            "Design a new feature",
            "Create mockups",
            "User experience review",
            "Design system guidelines"
        ]
    },
    {
        "name": "communications",
        "description": "Communications team for internal communications, public relations, press releases, crisis communications, employee engagement, and corporate messaging.",
        "keywords": ["announcement", "press", "news", "communication", "pr", "media", "messaging"],
        "sub_agents": ["internal", "pr", "crisis", "brand_voice"],
        "sample_queries": [
            "Send company announcement",
            "Press release",
            "Handle media inquiry",
            "Internal communication"
        ]
    },
    {
        "name": "facilities",
        "description": "Facilities management for office space, maintenance requests, room bookings, equipment, safety, security, and workplace environment.",
        "keywords": ["office", "room", "desk", "maintenance", "cleaning", "security", "parking", "facility"],
        "sub_agents": ["maintenance", "space", "security", "services"],
        "sample_queries": [
            "Book a meeting room",
            "Report maintenance issue",
            "Office access",
            "Parking information"
        ]
    },
    {
        "name": "procurement",
        "description": "Procurement department for purchasing, vendor selection, contract negotiations, procurement policies, approval workflows, and supplier management.",
        "keywords": ["purchase", "vendor", "supplier", "procure", "buy", "contract", "approval", "requisition"],
        "sub_agents": ["sourcing", "contracts", "approvals", "vendors"],
        "sample_queries": [
            "Request new purchase",
            "Vendor selection",
            "Approval status",
            "Procurement policy"
        ]
    },
    {
        "name": "data_analytics",
        "description": "Data analytics team for business intelligence, data visualization, reporting, dashboards, data analysis, insights, and analytics requests.",
        "keywords": ["data", "analytics", "report", "dashboard", "insight", "metric", "visualization", "bi"],
        "sub_agents": ["bi", "visualization", "insights", "engineering"],
        "sample_queries": [
            "Generate sales report",
            "Create dashboard",
            "Data analysis request",
            "Show key metrics"
        ]
    },
    {
        "name": "security",
        "description": "Security team for cybersecurity, access control, security audits, incident response, security policies, compliance, and threat monitoring.",
        "keywords": ["security", "cyber", "threat", "hack", "breach", "audit", "access", "compliance"],
        "sub_agents": ["incident_response", "audit", "compliance", "engineering"],
        "sample_queries": [
            "Report security incident",
            "Security audit request",
            "Access control",
            "Threat monitoring"
        ]
    },
    {
        "name": "sustainability",
        "description": "Sustainability team for environmental initiatives, carbon footprint, ESG reporting, green policies, sustainable practices, and social responsibility.",
        "keywords": ["sustainability", "environment", "green", "carbon", "esg", "eco", "climate", "sustainable"],
        "sub_agents": ["initiatives", "reporting", "compliance", "education"],
        "sample_queries": [
            "Carbon footprint report",
            "Green initiatives",
            "ESG metrics",
            "Sustainability policy"
        ]
    },
    {
        "name": "learning_development",
        "description": "Learning and development for training programs, skill development, learning resources, career growth, educational content, and development plans.",
        "keywords": ["learn", "training", "course", "skill", "development", "education", "career", "grow"],
        "sub_agents": ["programs", "resources", "certification", "mentoring"],
        "sample_queries": [
            "Enroll in training",
            "Skill assessment",
            "Career development",
            "Learning resources"
        ]
    },
    {
        "name": "innovation",
        "description": "Innovation team for R&D, new technologies, experimentation, innovation programs, idea management, prototyping, and future planning.",
        "keywords": ["innovation", "rd", "research", "experiment", "idea", "prototype", "future", "new tech"],
        "sub_agents": ["research", "incubator", "partnerships", "labs"],
        "sample_queries": [
            "Submit new idea",
            "R&D project",
            "Innovation program",
            "Technology research"
        ]
    },
    {
        "name": "quality_assurance",
        "description": "Quality assurance for testing, quality control, process improvements, standards, audits, certification, and quality metrics.",
        "keywords": ["quality", "qa", "test", "testing", "audit", "standard", "control", "inspection"],
        "sub_agents": ["testing", "automation", "compliance", "improvement"],
        "sample_queries": [
            "Quality testing request",
            "QA automation",
            "Quality audit",
            "Test coverage report"
        ]
    },
    {
        "name": "risk_management",
        "description": "Risk management for risk assessment, mitigation strategies, risk monitoring, compliance, insurance, and risk reporting.",
        "keywords": ["risk", "mitigation", "assessment", "hazard", "insurance", "compliance"],
        "sub_agents": ["assessment", "mitigation", "monitoring", "reporting"],
        "sample_queries": [
            "Risk assessment",
            "Mitigation strategies",
            "Risk report",
            "Compliance check"
        ]
    },
    {
        "name": "project_management",
        "description": "Project management for project planning, scheduling, resource allocation, progress tracking, project reporting, and coordination.",
        "keywords": ["project", "plan", "schedule", "timeline", "milestone", "resource", "progress"],
        "sub_agents": ["planning", "tracking", "resources", "reporting"],
        "sample_queries": [
            "Project status update",
            "Resource allocation",
            "Timeline planning",
            "Project roadmap"
        ]
    },
    {
        "name": "customer_success",
        "description": "Customer success for onboarding, adoption, retention, customer health, success planning, and proactive support.",
        "keywords": ["onboard", "adoption", "retention", "churn", "success", "health", "customer"],
        "sub_agents": ["onboarding", "adoption", "renewals", "advocacy"],
        "sample_queries": [
            "Customer onboarding",
            "Adoption strategies",
            "Renewal planning",
            "Customer health check"
        ]
    },
    {
        "name": "billing",
        "description": "Billing department for invoices, payments, billing inquiries, pricing adjustments, account statements, and billing disputes.",
        "keywords": ["bill", "invoice", "payment", "pricing", "charge", "fee", "statement"],
        "sub_agents": ["invoicing", "payments", "disputes", "adjustments"],
        "sample_queries": [
            "Pay my bill",
            "Invoice inquiry",
            "Billing dispute",
            "Account statement"
        ]
    },
    {
        "name": "partnerships",
        "description": "Partnerships team for alliance management, partner relationships, joint ventures, channel partnerships, and partner programs.",
        "keywords": ["partner", "alliance", "channel", "joint", "venture", "ecosystem"],
        "sub_agents": ["alliances", "channel", "programs", "integration"],
        "sample_queries": [
            "Partner request",
            "Channel partnership",
            "Alliance management",
            "Integration with partner"
        ]
    },
    {
        "name": "events",
        "description": "Events team for event planning, coordination, logistics, marketing events, conferences, and company events.",
        "keywords": ["event", "conference", "summit", "workshop", "seminar", "meetup", "gathering"],
        "sub_agents": ["planning", "logistics", "marketing", "coordination"],
        "sample_queries": [
            "Plan an event",
            "Conference details",
            "Event logistics",
            "Company gathering"
        ]
    },
    {
        "name": "content",
        "description": "Content team for content creation, editing, publishing, content strategy, copywriting, and content management.",
        "keywords": ["content", "blog", "article", "copy", "write", "edit", "publish"],
        "sub_agents": ["creation", "editing", "strategy", "distribution"],
        "sample_queries": [
            "Write a blog post",
            "Content strategy",
            "Edit content",
            "Publishing request"
        ]
    },
    {
        "name": "research",
        "description": "Research team for market research, competitive analysis, industry research, user research, and data research.",
        "keywords": ["research", "study", "survey", "analysis", "market", "competitive", "industry"],
        "sub_agents": ["market", "competitive", "user", "data"],
        "sample_queries": [
            "Market research",
            "Competitive analysis",
            "Research survey",
            "Industry report"
        ]
    },
    {
        "name": "ethics_compliance",
        "description": "Ethics and compliance for ethical guidelines, compliance programs, policy enforcement, ethics training, and regulatory compliance.",
        "keywords": ["ethics", "compliance", "regulation", "policy", "governance", "conduct"],
        "sub_agents": ["programs", "training", "monitoring", "reporting"],
        "sample_queries": [
            "Ethics question",
            "Compliance program",
            "Report concern",
            "Policy clarification"
        ]
    },
    {
        "name": "treasury",
        "description": "Treasury for cash management, investments, banking relationships, liquidity, financial risk, and treasury operations.",
        "keywords": ["treasury", "cash", "liquidity", "investment", "banking", "capital"],
        "sub_agents": ["cash", "investments", "risk", "operations"],
        "sample_queries": [
            "Cash position",
            "Investment strategy",
            "Liquidity report",
            "Treasury operations"
        ]
    },
    {
        "name": "tax",
        "description": "Tax department for tax planning, tax compliance, tax filings, tax advice, and tax reporting.",
        "keywords": ["tax", "filing", "compliance", "deduction", "irs", "revenue"],
        "sub_agents": ["planning", "compliance", "filing", "advisory"],
        "sample_queries": [
            "Tax planning",
            "File tax return",
            "Tax compliance",
            "Tax question"
        ]
    },
    {
        "name": "internal_audit",
        "description": "Internal audit for auditing, risk assessment, control evaluation, compliance checks, and audit reporting.",
        "keywords": ["audit", "internal", "control", "review", "assurance", "governance"],
        "sub_agents": ["financial", "operational", "it", "compliance"],
        "sample_queries": [
            "Internal audit request",
            "Control review",
            "Audit report",
            "Compliance check"
        ]
    },
    {
        "name": "investor_relations",
        "description": "Investor relations for shareholder communications, earnings calls, investor presentations, stock information, and financial disclosures.",
        "keywords": ["investor", "shareholder", "stock", "earnings", "disclosure", "analyst"],
        "sub_agents": ["communications", "events", "materials", "analysts"],
        "sample_queries": [
            "Investor information",
            "Earnings call",
            "Stock query",
            "Analyst inquiry"
        ]
    },
    {
        "name": "corporate_development",
        "description": "Corporate development for M&A, strategic planning, business development, due diligence, and corporate strategy.",
        "keywords": ["ma", "merger", "acquisition", "strategy", "corporate", "development"],
        "sub_agents": ["ma", "strategy", "planning", "analysis"],
        "sample_queries": [
            "M&A opportunity",
            "Strategic planning",
            "Business development",
            "Due diligence"
        ]
    },
    {
        "name": "workplace",
        "description": "Workplace team for employee experience, workplace culture, employee engagement, diversity and inclusion, and workplace programs.",
        "keywords": ["workplace", "culture", "engagement", "diversity", "inclusion", "employee"],
        "sub_agents": ["experience", "culture", "dei", "programs"],
        "sample_queries": [
            "Employee engagement",
            "Workplace culture",
            "Diversity program",
            "Employee feedback"
        ]
    },
    {
        "name": "revenue_operations",
        "description": "Revenue operations for revenue tracking, forecasting, sales operations, revenue recognition, and revenue optimization.",
        "keywords": ["revenue", "forecast", "sales ops", "recognition", "growth"],
        "sub_agents": ["forecasting", "operations", "analytics", "strategy"],
        "sample_queries": [
            "Revenue forecast",
            "Sales operations",
            "Revenue report",
            "Growth analysis"
        ]
    }
]

# Sub-agent descriptions for routing
SUB_AGENTS = {
    "flights": "Handles flight bookings, changes, cancellations, and flight status",
    "hotels": "Manages hotel search, booking, modifications, and reservations",
    "cars": "Handles car rental bookings, modifications, and vehicle selection",
    "activities": "Manages tours, activities, and experiences booking",
    "banking": "Handles bank accounts, transfers, and banking services",
    "trading": "Manages investment trading, portfolio, and market orders",
    "expenses": "Handles expense reporting, tracking, and reimbursement",
    "reports": "Generates financial reports and statements",
    "payroll": "Manages salary, payments, and compensation",
    "benefits": "Handles employee benefits, insurance, and perks",
    "recruiting": "Manages recruitment, hiring, and job applications",
    "training": "Coordinates training programs and employee development",
    "hardware": "Handles hardware issues, device management, and equipment",
    "software": "Manages software installation, updates, and troubleshooting",
    "network": "Handles network, WiFi, VPN, and connectivity issues",
    "access": "Manages user access, permissions, and authentication",
    "orders": "Handles order placement, tracking, and status",
    "returns": "Manages returns, exchanges, and refunds",
    "complaints": "Handles customer complaints and escalations",
    "info": "Provides general product and service information",
    "enterprise": "Handles enterprise sales and large accounts",
    "smb": "Manages small and medium business sales",
    "partnerships": "Handles partnership and channel sales",
    "quotations": "Creates and manages sales quotes and proposals",
    "campaigns": "Manages marketing campaigns and initiatives",
    "content": "Creates and manages marketing content",
    "analytics": "Provides marketing analytics and insights",
    "creative": "Handles creative design and marketing materials",
    "contracts": "Reviews and manages legal contracts",
    "compliance": "Handles compliance and regulatory matters",
    "ip": "Manages intellectual property and trademarks",
    "advisory": "Provides legal advice and guidance",
    "logistics": "Manages shipping, logistics, and delivery",
    "inventory": "Tracks inventory levels and stock management",
    "vendors": "Manages vendor relationships and procurement",
    "facilities": "Handles facility management and maintenance",
    "frontend": "Handles frontend development and UI",
    "backend": "Manages backend development and APIs",
    "devops": "Handles DevOps, infrastructure, and deployment",
    "qa": "Manages quality assurance and testing",
    "discovery": "Handles product discovery and research",
    "roadmap": "Manages product roadmap and planning",
    "requirements": "Gathers and manages product requirements",
    "growth": "Handles product growth and optimization",
    "ux": "Manages UX design and research",
    "visual": "Handles visual design and graphics",
    "research": "Conducts design research and testing",
    "systems": "Manages design systems and components",
    "internal": "Handles internal communications",
    "pr": "Manages public relations and media",
    "crisis": "Handles crisis communications",
    "brand_voice": "Manages brand voice and messaging",
    "maintenance": "Handles facility maintenance and repairs",
    "space": "Manages office space and desk bookings",
    "security": "Handles physical security and access",
    "services": "Manages facility services and support",
    "sourcing": "Handles vendor sourcing and selection",
    "approvals": "Manages procurement approval workflows",
    "vendors": "Manages vendor relationships",
    "bi": "Handles business intelligence and reporting",
    "visualization": "Creates data visualizations and dashboards",
    "insights": "Provides data insights and analysis",
    "engineering": "Handles data engineering and pipelines",
    "incident_response": "Handles security incident response",
    "audit": "Conducts security audits and assessments",
    "compliance": "Handles security compliance and certifications",
    "engineering": "Manages security engineering and tools",
    "initiatives": "Manages sustainability initiatives",
    "reporting": "Handles ESG and sustainability reporting",
    "compliance": "Ensures environmental compliance",
    "education": "Provides sustainability education and awareness",
    "programs": "Manages training programs and courses",
    "resources": "Provides learning resources and materials",
    "certification": "Handles professional certifications",
    "mentoring": "Manages mentoring and career coaching",
    "research": "Conducts innovation research and development",
    "incubator": "Manages innovation incubator programs",
    "partnerships": "Handles innovation partnerships",
    "labs": "Manages innovation labs and experimentation",
    "testing": "Handles quality testing and QA",
    "automation": "Manages test automation and frameworks",
    "compliance": "Ensures quality compliance and standards",
    "improvement": "Drives quality improvement initiatives",
    "assessment": "Conducts risk assessments",
    "mitigation": "Implements risk mitigation strategies",
    "monitoring": "Monitors risks and threats",
    "reporting": "Provides risk reporting and dashboards",
    "planning": "Handles project planning and scheduling",
    "tracking": "Tracks project progress and milestones",
    "resources": "Manages project resources and allocation",
    "reporting": "Provides project reports and updates",
    "onboarding": "Handles customer onboarding",
    "adoption": "Drives customer adoption and engagement",
    "renewals": "Manages customer renewals and retention",
    "advocacy": "Manages customer advocacy and references",
    "invoicing": "Handles billing and invoicing",
    "payments": "Manages payment processing",
    "disputes": "Handles billing disputes and adjustments",
    "adjustments": "Manages billing adjustments and corrections",
    "alliances": "Manages strategic alliances",
    "channel": "Handles channel partnerships",
    "programs": "Manages partner programs",
    "integration": "Handles partner integrations",
    "planning": "Handles event planning and coordination",
    "logistics": "Manages event logistics and operations",
    "marketing": "Handles event marketing and promotion",
    "coordination": "Coordinates event execution",
    "creation": "Creates content and copy",
    "editing": "Edits and reviews content",
    "strategy": "Develops content strategy",
    "distribution": "Manages content distribution and publishing",
    "market": "Conducts market research",
    "competitive": "Analyzes competitive landscape",
    "user": "Conducts user research studies",
    "data": "Analyzes research data and insights",
    "programs": "Manages ethics and compliance programs",
    "training": "Provides ethics training",
    "monitoring": "Monitors ethical compliance",
    "reporting": "Handles ethics reporting and concerns",
    "cash": "Manages cash and liquidity",
    "investments": "Handles treasury investments",
    "risk": "Manages financial risk",
    "operations": "Handles treasury operations",
    "planning": "Handles tax planning",
    "compliance": "Ensures tax compliance",
    "filing": "Manages tax filings",
    "advisory": "Provides tax advice",
    "financial": "Conducts financial audits",
    "operational": "Conducts operational audits",
    "it": "Conducts IT audits",
    "compliance": "Conducts compliance audits",
    "communications": "Handles investor communications",
    "events": "Manages investor events",
    "materials": "Creates investor presentation materials",
    "analysts": "Handles analyst relations",
    "ma": "Handles mergers and acquisitions",
    "strategy": "Develops corporate strategy",
    "planning": "Handles strategic planning",
    "analysis": "Conducts strategic analysis",
    "experience": "Manages employee experience",
    "culture": "Manages workplace culture",
    "dei": "Handles diversity, equity, and inclusion",
    "programs": "Manages workplace programs",
    "forecasting": "Handles revenue forecasting",
    "operations": "Manages revenue operations",
    "analytics": "Provides revenue analytics",
    "strategy": "Develops revenue strategy"
}
