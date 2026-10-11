from typing import Dict, Any

def check_crm_history(email: str)-> Dict[str, Any]:
    """
    Simulates an external CRM API lookup (like Salesforce).
    Takes a lead email and returns past engagement history, status, and notes.
    """

    # A mock database of lead emails mapped to CRM interaction histories
    mock_crm_database = {
        "jane@acmecorp.com": {
            "status": "Active Opportunity",
            "last_contact": "2026-09-15",
            "notes": "Attended Q3 Cloud Security webinar, expressed interest in enterprise tier.",
            "owner": "Sarah Jenkins"
        },
        "bob@widgetco.net": {
            "status": "Cold Lead",
            "last_contact": "2026-06-10",
            "notes": "Downloaded whitepaper on manufacturing supply chain automation.",
            "owner": "Unassigned"
        },
        "sarah@globex.org": {
            "status": "SQL (Sales Qualified Lead)",
            "last_contact": "2026-10-01",
            "notes": "Requested a custom demo for security compliance modules.",
            "owner": "Alex Rivera"
        }
    }

    # Clean the email input to prevent whitespace or case mismatches
    clean_email = email.strip().lower()

    # Return CRM record if found, otherwise return a default 'New Lead' state

    if clean_email in mock_crm_database:
        return mock_crm_database[clean_email]
    else:
        return {
            "status" : "New Lead",
            "last_contact" : "Never",
            "notes" : "No prior interaction found in CRM history.",
            "owner": "Unassigned"
        }