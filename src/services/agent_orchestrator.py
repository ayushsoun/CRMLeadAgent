import re
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from src.core.config import settings
from src.services.enrichment_tool import lookup_domain_info
from src.services.crm_tool import check_crm_history

class LeadAgentOrchestrator:
    """Orchestrates lead qualification by extracting domains, calling tools, and synthesizing summaries."""

    @staticmethod
    def extract_domain(email: str) -> str:
        """Extracts the company domain from an email address using regex."""
        match = re.search(r"@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", email)
        if match:
            return match.group(1).lower()
        return ""

    @staticmethod
    def calculate_score(domain_info: Dict[str, Any], crm_history: Dict[str, Any]) -> str:
        """Applies business rules to compute a lead score based on revenue and CRM status."""
        status = crm_history.get("status", "New Lead")
        revenue = domain_info.get("revenue", "$0")

        if status in ["Active Opportunity", "SQL (Sales Qualified Lead)"]:
            return "High"
        elif any(rev in revenue for rev in ["$50M", "$250M"]):
            return "High"
        elif status == "Cold Lead":
            return "Medium"
        return "Low"

    @staticmethod
    def qualify_lead(lead_email: str) -> Dict[str, Any]:
        """Executes the end-to-end lead qualification workflow safely."""
        try:
            if not lead_email or "@" not in lead_email:
                return {"error": "Invalid email format provided."}

            # Step 1: Extract domain
            domain = LeadAgentOrchestrator.extract_domain(lead_email)
            if not domain:
                return {"error": f"Could not extract valid domain from {lead_email}"}

            # Step 2: Execute tool lookups
            domain_data = lookup_domain_info(domain)
            crm_data = check_crm_history(lead_email)

            # Step 3: Compute deterministic score
            lead_score = LeadAgentOrchestrator.calculate_score(domain_data, crm_data)

            # Step 4: Initialize OpenRouter LLM client
            llm = ChatOpenAI(
                model=settings.MODEL_NAME,
                temperature=settings.TEMPERATURE,
                api_key=settings.OPENROUTER_API_KEY,
                base_url=settings.OPENROUTER_BASE_URL,
                default_headers={
                    "HTTP-Referer": "https://github.com/ayushsoun/CSVReaderAgent",
                    "X-Title": "CRM Lead Qualification Agent"
                }
            )

            # Step 5: Construct system prompt and prompt LLM
            system_prompt = (
                "You are an expert Sales Development Representative (SDR) assistant AI. "
                "Your job is to synthesize company enrichment data and CRM history into a concise, "
                "professional, sales-ready qualification summary for a discovery call."
            )

            user_prompt = (
                f"Lead Email: {lead_email}\n"
                f"Extracted Domain: {domain}\n"
                f"Enrichment Data: {domain_data}\n"
                f"CRM History: {crm_data}\n"
                f"Computed Lead Score: {lead_score}\n\n"
                "Provide a sales-ready summary including company overview, past engagement notes, "
                "and suggested talking points for the SDR."
            )

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]

            response = llm.invoke(messages)
            summary_text = response.content

            # Return complete structured results packet
            return {
                "lead_email": lead_email,
                "domain": domain,
                "domain_info": domain_data,
                "crm_history": crm_data,
                "lead_score": lead_score,
                "sales_summary": summary_text
            }

        except Exception as e:
            # Catch any unexpected error and return it cleanly so Streamlit can display it
            return {"error": f"Orchestrator execution error: {str(e)}"}