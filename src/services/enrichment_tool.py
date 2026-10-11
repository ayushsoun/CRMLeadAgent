from typing import Dict, Any

def lookup_domain_info(domain:str)-> Dict[str, Any]:
    """
    Simulates an external B2B company enrichment API (like Clearbit).
    Takes a company domain and returns firmographic data.
    """

    # A mock database of company domains mapped to firmographic profiles
    mock_database={
        "acmecorp.com": {
            "company_name": "Acme Corp",
            "industry": "SaaS / Cloud Software",
            "revenue": "$50M–$100M",
            "employee_count": 450,
            "location": "San Francisco, CA"
        },
        "widgetco.net": {
            "company_name": "Widget Co",
            "industry": "Manufacturing",
            "revenue": "$10M–$25M",
            "employee_count": 120,
            "location": "Chicago, IL"
        },
        "globex.org": {
            "company_name": "Globex Corporation",
            "industry": "Enterprise Security",
            "revenue": "$250M+",
            "employee_count": 2100,
            "location": "New York, NY"
        }
    }

    #clean domain setting to ensure standard lookup
    clean_domain = domain.strip().lower()

    # Return company data if found, otherwise return a default fallback response
    if clean_domain in mock_database:
        return mock_database[clean_domain]
    else:
        return{
            "error":"Company not found",
            "message": f"No enrichment data available for domain: {domain}"
        }