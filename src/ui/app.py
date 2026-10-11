import sys
from pathlib import Path

# Automatically add project root to sys.path so we can import from src/
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import streamlit as st
from src.services.agent_orchestrator import LeadAgentOrchestrator

# Page configuration
st.set_page_config(
    page_title="CRM Lead Qualification Agent",
    page_icon="💼",
    layout="wide"
)

# Initialize session state for the lead email input if not present
if "lead_email" not in st.session_state:
    st.session_state.lead_email = ""

st.title("💼 Autonomous CRM Lead Qualification Agent")
st.markdown("Equip your SDR team with instant, AI-synthesized lead intelligence powered by OpenRouter.")

# Sidebar for Testing Presets
st.sidebar.header("🧪 Test Lead Presets")
st.sidebar.markdown("Click any preset email to test the agent instantly:")

preset_emails = [
    "jane@acmecorp.com",
    "bob@widgetco.net",
    "sarah@globex.org",
    "unknown@randomstartup.io"  # Tests fallback behavior
]

for email in preset_emails:
    if st.sidebar.button(email, use_container_width=True):
        st.session_state.lead_email = email
        st.rerun()  # Immediately rerun script to update text input

# Main Input Section
st.subheader("📥 Inbound Lead Submission")

# Bind text input directly to session state
lead_email_input = st.text_input(
    "Enter prospect email address:",
    key="lead_email",
    placeholder="e.g., jane@acmecorp.com"
)

if st.button("Qualify Lead", type="primary"):
    if lead_email_input.strip():
        with st.spinner(f"Agent is analyzing domain, querying CRM, and synthesizing insights for {lead_email_input}..."):
            # Run the agent orchestrator
            result = LeadAgentOrchestrator.qualify_lead(lead_email_input)

        # Defensive check for errors or missing result structure
        if not isinstance(result, dict):
            st.error("Invalid response received from agent orchestrator.")
        elif "error" in result:
            st.error(result["error"])
        else:
            st.success("Lead qualification completed successfully!")

            # Display Key Metrics Row using .get() for safety
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Extracted Domain", value=result.get("domain", "Unknown"))
            with col2:
                crm_history = result.get("crm_history", {})
                st.metric(label="CRM Status", value=crm_history.get("status", "Unknown"))
            with col3:
                score = result.get("lead_score", "Low")
                # Color code lead score based on priority
                if score == "High":
                    st.metric(label="Computed Lead Score", value=score, delta="🔥 Priority")
                elif score == "Medium":
                    st.metric(label="Computed Lead Score", value=score, delta="⚡ Standard")
                else:
                    st.metric(label="Computed Lead Score", value=score, delta="💤 Low", delta_color="inverse")

            # Expanders for Raw Tool Data
            st.markdown("---")
            col_left, col_right = st.columns(2)
            
            with col_left:
                with st.expander("📊 View Company Enrichment Data (Clearbit Mock)"):
                    st.json(result.get("domain_info", {}))

            with col_right:
                with st.expander("🗂️ View CRM Interaction History (Salesforce Mock)"):
                    st.json(result.get("crm_history", {}))

            # AI Sales-Ready Summary
            st.markdown("### 🤖 AI Sales-Ready Summary & Talking Points")
            st.info(result.get("sales_summary", "No summary generated."))
    else:
        st.warning("Please enter a valid lead email address.")