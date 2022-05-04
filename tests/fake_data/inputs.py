def app():
    print("go in village")
    data = {
        "request_data": {
            "trigger_name": "careerhub_entity_search_results",
            "current_user_email": "payal.sonawane@redcrackle.com",
            "limit": 10,
            "start": 0,
            # "cursor": '',
            "term": "Microsoft Office",
            "fq": {
                "position_skills": [
                    {"name": "Business Strategy"},
                    {"name": "Management"},
                    {"name": "Software Development"},
                    {"name": "Project Management"},
                    {"name": "Frameworks"},
                    {"name": "Design Analysis"},
                    {"name": "Interactive Media"},
                    {"name": "Soft Skills"},
                    {"name": "Brand Identity"},
                    {"name": "Business Requirements"},
                    {"name": "Project Manager"},
                    {"name": "AWS"},
                    {"name": "Proofing"},
                ],
                "profile_skills": [{"name": "Management"}],
                "required_skills": [
                    {"name": "Research"},
                    {"name": "Public Speaking"},
                    {"name": "Strategic Planning"},
                    {"name": "Software Engineering"},
                    {"name": "Leadership"},
                    {"name": "Microsoft Office"},
                    {"name": "Sales"},
                    {"name": "Linux"},
                    {"name": "CSS"},
                    {"name": "Navy"},
                    {"name": "Dod"},
                    {"name": "Entrepreneurship"},
                    {"name": "Information Assurance"},
                    {"name": "Integration"},
                    {"name": "Accounting"},
                    {"name": "Event Planning"},
                    {"name": "Negotiation"},
                    {"name": "New Business Development"},
                    {"name": "Small Business"},
                    {"name": "Team Building"},
                    {"name": "Financial Accountability"},
                    {"name": "Daily Accounting"},
                    {"name": "Other Accounting"},
                    {"name": "Accounting Information Systems"},
                    {"name": "Revenue Accounting"},
                    {"name": "Accounts Payable"},
                    {"name": "Account Payables"},
                    {"name": "Collating"},
                    {"name": "Managerial Accounting"},
                    {"name": "Auditing"},
                    {"name": "Full Cycle Accounting"},
                    {"name": "GAAP"},
                    {"name": "Field Account"},
                    {"name": "Account Payable"},
                    {"name": "Cost Accounting"},
                    {"name": "Payroll Accounting"},
                    {"name": "Management Accounting"},
                    {"name": "Investment Accounting"},
                    {"name": "Accounting Operations"},
                    {"name": "Major Account"},
                    {"name": "Account Reconciliation"},
                    {"name": "Fasb"},
                    {"name": "Account Reconciliations"},
                    {"name": "Accounting Systems"},
                    {"name": "Manage Accounts"},
                    {"name": "Peachtree Accounting"},
                    {"name": "Business Accounting"},
                    {"name": "Accounts Receivable"},
                    {"name": "Accounting Analysis"},
                    {"name": "Professional Accounting"},
                    {"name": "General Accounting"},
                    {"name": "Corporate Accounting"},
                    {"name": "Account Receivable"},
                    {"name": "Marketing"},
                    {"name": "Reporting"},
                    {"name": "Inventory Accounting"},
                    {"name": "IT Auditing"},
                    {"name": "Office Accounting"},
                    {"name": "Technical Accounting"},
                    {"name": "Portfolio Accounting"},
                    {"name": "Large Accounts"},
                    {"name": "Individual Accounts"},
                    {"name": "Accounts Receivables"},
                    {"name": "P&l Accounts"},
                    {"name": "Project Accounting"},
                    {"name": "Public Accounting"},
                    {"name": "Intermediate Accounting"},
                    {"name": "Financial Accounting"},
                    {"name": "Accounting and Finance"},
                    {"name": "Forensic Accounting"},
                    {"name": "Account Analysis"},
                    {"name": "Maintained Accounts"},
                    {"name": "Budgeting"},
                    {"name": "Account Receivables"},
                    {"name": "Account Rep"},
                    {"name": "Tax Accounting"},
                    {"name": "Sales Accounting"},
                    {"name": "Accounting Management"},
                    {"name": "GAAP Accounting"},
                    {"name": "Account Planning"},
                    {"name": "Fund Accounting"},
                    {"name": "NetMeeting"},
                    {"name": "Accounts Payables"},
                    {"name": "Cascading Style Sheets (Css)"},
                    {"name": "Less"},
                    {"name": "PostScript"},
                    {"name": "Cascading Style Sheets ( CSS )"},
                    {"name": "ECMAScript 6"},
                    {"name": "JSSE"},
                    {"name": "Html Scripting"},
                    {"name": "Html + CSS"},
                    {"name": "LotusScript"},
                    {"name": "Java Script"},
                    {"name": "CoffeeScript"},
                    {"name": "Google Apps Script"},
                    {"name": "CSS3"},
                    {"name": "TypeScript"},
                    {"name": "JavaScript"},
                    {"name": "SCSS"},
                    {"name": "Sass"},
                    {"name": "Cascading Style Sheets %28css%29"},
                    {"name": "Comics"},
                    {"name": "Cascading"},
                    {"name": "Cascade"},
                    {"name": "Advanced CSS"},
                    {"name": "ECMAScript"},
                    {"name": "Html/CSS"},
                    {"name": "Entrepreneur"},
                    {"name": "Social Entrepreneurship"},
                    {"name": "Internet Entrepreneur"},
                    {"name": "Meeting Planning"},
                    {"name": "Event Management"},
                    {"name": "Wedding Planning"},
                    {"name": "Travel Planning"},
                    {"name": "Schedule Planning"},
                    {"name": "Event Producing"},
                    {"name": "Event Marketing"},
                    {"name": "Marketing Event Planning"},
                    {"name": "Live Events"},
                    {"name": "Event Marketing Strategy"},
                    {"name": "Information Security"},
                    {"name": "Operations"},
                    {"name": "Server Migration"},
                    {"name": "Application Integration"},
                    {"name": "Integrator"},
                    {"name": "Migration Strategy"},
                    {"name": "CMMI"},
                    {"name": "Data Integration"},
                    {"name": "ODI"},
                    {"name": "Technology Integration"},
                    {"name": "Migration"},
                    {"name": "Microsoft SQL Server Integration Services"},
                    {"name": "Systems Integration"},
                    {"name": "System Integration Testing"},
                    {"name": "Pmi"},
                    {"name": "Monetization"},
                    {"name": "Integration Testing"},
                    {"name": "Data Migration"},
                    {"name": "Mitigation"},
                    {"name": "Data Integrity"},
                    {"name": "Migrations"},
                    {"name": "IMS"},
                    {"name": "Data Integrator"},
                    {"name": "System Integration"},
                    {"name": "Network Operations"},
                    {"name": "Enterprise Integration"},
                    {"name": "SQL Server Integration Services"},
                    {"name": "CRM Integration"},
                    {"name": "EAI"},
                    {"name": "Merger & Acquisition Integration"},
                    {"name": "Rational Software"},
                    {"name": "Software Integration"},
                    {"name": "Hardware Integration"},
                    {"name": "Infrastructure Migration"},
                    {"name": "Oracle Data Integrator"},
                    {"name": "Automation"},
                    {"name": "Replication"},
                    {"name": "Test Integration"},
                    {"name": "Integration Design"},
                    {"name": "M&a Integration"},
                    {"name": "Identity Federation"},
                    {"name": "Process Integration"},
                    {"name": "Estimation"},
                    {"name": "Continuous Integration"},
                    {"name": "Operational Support"},
                    {"name": "Documentation"},
                    {"name": "Acquisition Integration"},
                    {"name": "Optimization"},
                    {"name": "Enterprise Application Integration"},
                    {"name": "Integration Architecture"},
                    {"name": "CTi"},
                    {"name": "System Operation"},
                    {"name": "Team Leadership"},
                    {"name": "Student Leadership"},
                    {"name": "Leadership Development"},
                    {"name": "Technical Project Leadership"},
                    {"name": "Sales & Marketing Leadership"},
                    {"name": "Cross Functional Team Leadership"},
                    {"name": "Global Cross-Functional Team Leadership"},
                    {"name": "Project Leadership"},
                    {"name": "Strategic Leadership"},
                    {"name": "Collaborative Leadership"},
                    {"name": "Strategic Human Resources Leadership"},
                    {"name": "Change Leadership"},
                    {"name": "Situational Leadership"},
                    {"name": "Non-Profit Leadership"},
                    {"name": "Educational Leadership"},
                    {"name": "Technical Leadership"},
                    {"name": "Cross-Functional Team Leadership"},
                    {"name": "Team Lead"},
                    {"name": "Leadership Effectiveness"},
                    {"name": "Engineering Leadership"},
                    {"name": "Senior Executive Leadership"},
                    {"name": "Thought Leadership"},
                    {"name": "Technology Leadership"},
                    {"name": "Executive Leadership"},
                    {"name": "Organizational Leadership"},
                    {"name": "Leadership Skills"},
                ],
                "project_skills": [
                    {"name": "Business Strategy"},
                    {"name": "Management"},
                ],
                "skill_goals": [{"name": "Business Strategy"}, {"name": "Management"}],
            },
        },
        "app_settings": {
            "degreed_client_id": "7b5a18386173507b",
            "degreed_client_secret": "259ad32f98f366ea5b29b9cb8c3cd4c8",
            "degreed_base_url": "betatest.degreed.com",
            "language": "en",
            "recommended_course_limit": 30,
            "degreed_test_email": "payal.sonawane@redcrackle.com",
            "use_test_email": "True",
        },
    }
    return data
