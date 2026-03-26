#!/usr/bin/env python3
"""
ACL Automated Workflow - Streamlit Frontend
=============================================

A web interface for the ACL automation workflow with three steps:
1. Generate ACL
2. Test on Digital Twin
3. Push & Test in Production
"""

import streamlit as st
import sys
import os

# Load environment variables before any other imports
from dotenv import load_dotenv
load_dotenv()

# Add the current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jinja2 import Environment, FileSystemLoader
import yaml
import utilities
import gen_prod_acl

# Page configuration
st.set_page_config(
    page_title="ACL Automated Workflow",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .step-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ff7f0e;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .status-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .status-error {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .status-info {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    .status-pending {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
    </style>
""", unsafe_allow_html=True)


def load_current_acl():
    """Load the current ACL from file if it exists."""
    output_file = './output/production_acl.txt'
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            return f.read()
    return None


def init_session_state():
    """Initialize session state variables for workflow tracking."""
    if 'step1_complete' not in st.session_state:
        st.session_state.step1_complete = False
    if 'step2_complete' not in st.session_state:
        st.session_state.step2_complete = False
    if 'step3_complete' not in st.session_state:
        st.session_state.step3_complete = False
    if 'generated_acl' not in st.session_state:
        st.session_state.generated_acl = None
    if 'dns_ips' not in st.session_state:
        st.session_state.dns_ips = None
    if 'current_acl' not in st.session_state:
        st.session_state.current_acl = load_current_acl()


def step_2_test_digital_twin() -> bool:
    """
    Step 2: Test ACL on Digital Twin.
    
    This is a framework placeholder for the Digital Twin testing step.
    
    Returns:
        True if successful, False otherwise
    """
    st.info("🧪 Digital Twin Testing Framework")
    st.write("This step will test the generated ACL on a digital twin environment.")
    
    # Placeholder for actual implementation
    with st.spinner("Connecting to Digital Twin environment..."):
        # Simulate some processing time
        import time
        time.sleep(1)
    
    st.success("✅ Digital Twin connection established (placeholder)")
    
    with st.expander("View Test Details"):
        st.write("- ACL syntax validation")
        st.write("- Configuration merge simulation")
        st.write("- Traffic flow validation")
        st.write("- Policy compliance checks")
    
    return True


def step_3_push_production() -> bool:
    """
    Step 3: Push ACL to Production and Test.
    
    This is a framework placeholder for the Production deployment step.
    
    Returns:
        True if successful, False otherwise
    """
    st.info("🚀 Production Deployment Framework")
    st.write("This step will deploy the tested ACL to production devices.")
    
    # Placeholder for actual implementation
    with st.spinner("Preparing production deployment..."):
        # Simulate some processing time
        import time
        time.sleep(1)
    
    st.success("✅ Production deployment ready (placeholder)")
    
    with st.expander("View Deployment Steps"):
        st.write("1. Pre-deployment snapshot")
        st.write("2. Configuration backup")
        st.write("3. ACL push to devices")
        st.write("4. Post-deployment validation")
        st.write("5. Connectivity tests")
        st.write("6. Rollback procedure ready")
    
    return True


def render_sidebar():
    """Render the sidebar with workflow status."""
    st.sidebar.markdown("## Workflow Status")
    
    # Step 1 status
    if st.session_state.step1_complete:
        st.sidebar.success("✅ Step 1: Generate ACL")
    else:
        st.sidebar.warning("⏳ Step 1: Generate ACL")
    
    # Step 2 status
    if st.session_state.step2_complete:
        st.sidebar.success("✅ Step 2: Test on Digital Twin")
    else:
        st.sidebar.warning("⏳ Step 2: Test on Digital Twin")
    
    # Step 3 status
    if st.session_state.step3_complete:
        st.sidebar.success("✅ Step 3: Push & Test in Production")
    else:
        st.sidebar.warning("⏳ Step 3: Push & Test in Production")
    
    st.sidebar.markdown("---")
    st.sidebar.info("Use the main panel to execute each step of the workflow.")


def main():
    """Main Streamlit application."""
    # Initialize session state
    init_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Main header
    st.markdown('<p class="main-header">🔒 ACL Automated Workflow</p>', unsafe_allow_html=True)
    st.write("Generate, test, and deploy ACL configurations through a guided workflow.")
    
    st.markdown("---")
    
    # Configuration section
    st.subheader("⚙️ Configuration")
    
    # InfraHub checkbox (maps to -i option)
    use_infrahub = st.checkbox(
        "Use InfraHub Source of Truth",
        value=False,
        help="When enabled, fetch DHCP IPs from InfraHub API. When disabled, use prod_dhcp_ips.yml file."
    )
    
    if use_infrahub:
        st.info("📡 Will fetch IPs from InfraHub API")
    else:
        st.info("📄 Will load IPs from prod_dhcp_ips.yml")
    
    st.markdown("---")
    
    # Step 1: Generate ACL
    st.markdown('<p class="step-header">Step 1: Generate ACL</p>', unsafe_allow_html=True)
    
    # Expanding section describing what will be done
    with st.expander("ℹ️ What happens in this step?"):
        st.markdown("""
        **ACL Generation creates the access control list configuration:**
        
        1. **Source Selection**: Choose between InfraHub API or local YAML file for IP addresses
        2. **IP Retrieval**: Fetch IPs from selected source (with automatic fallback to local file if InfraHub fails)
        3. **Template Rendering**: Generate ACL using Jinja2 template with the retrieved IPs
        4. **Configuration Output**: Display and save the generated ACL to `./output/production_acl.txt`
        
        *The generated ACL will be used in subsequent steps for testing and deployment.*
        """)
    
    if st.button("📝 Generate ACL", type="primary", use_container_width=True):
        # Acknowledge the checkbox state
        if use_infrahub:
            st.info("📡 Using InfraHub Source of Truth - Fetching IPs from InfraHub API...")
        else:
            st.info("📄 Using Local File Source - Loading IPs from prod_dhcp_ips.yml...")
        
        # Use the shared generate_acl function (with fallback enabled for Streamlit)
        dns_ips, rendered_acl, source, error_msg = gen_prod_acl.generate_acl(
            use_infrahub=use_infrahub, 
            fallback_on_error=True
        )
        
        if error_msg:
            # Check if it was an InfraHub fallback
            if use_infrahub and "fallback" in str(source):
                st.warning(f"⚠️ InfraHub failed: {error_msg}")
                st.info("📄 Fell back to local file (prod_dhcp_ips.yml)")
            else:
                st.error(f"❌ {error_msg}")
        elif use_infrahub and "fallback" in str(source):
            # InfraHub returned empty list, fell back to local file
            st.warning("⚠️ InfraHub returned 0 IP addresses")
            st.info("📄 Fell back to local file (prod_dhcp_ips.yml)")
        
        if dns_ips and rendered_acl:
            # Store in session state
            st.session_state.dns_ips = dns_ips
            st.session_state.generated_acl = rendered_acl
            st.session_state.current_acl = rendered_acl
            st.session_state.step1_complete = True
            
            # Display results
            st.success(f"✅ Retrieved {len(dns_ips)} IP(s) from {source}")
            with st.expander(f"📋 View IPs from {source}", expanded=True):
                st.write(dns_ips)
            
            st.success("✅ ACL generated successfully!")
            with st.expander("📄 View Generated ACL", expanded=True):
                st.code(rendered_acl, language="text")
            st.info("💾 ACL saved to: `./output/production_acl.txt`")
        else:
            st.error("❌ Failed to obtain IPs or generate ACL.")
    
    st.markdown("---")
    
    # Step 2: Test on Digital Twin
    st.markdown('<p class="step-header">Step 2: Test on Digital Twin</p>', unsafe_allow_html=True)
    
    # Expanding section describing what will be done
    with st.expander("ℹ️ What happens in this step?"):
        st.markdown("""
        **Digital Twin Testing validates the generated ACL in a simulated environment:**
        
        - **ACL Syntax Validation**: Verify the configuration has no syntax errors
        - **Configuration Merge Simulation**: Test how the ACL merges with existing device config
        - **Traffic Flow Validation**: Simulate network traffic to ensure expected behavior
        - **Policy Compliance Checks**: Verify the ACL meets security policy requirements
        - **Rollback Testing**: Validate that the ACL can be safely removed if needed
        
        *This step ensures the ACL is safe to deploy before touching production devices.*
        """)
    
    if not st.session_state.step1_complete:
        st.warning("⚠️ Complete Step 1 (Generate ACL) before proceeding to testing.")
    
    if st.button("🧪 Test on Digital Twin", 
                 type="primary", 
                 use_container_width=True,
                 disabled=bool(not st.session_state.get('step1_complete', False))):
        with st.spinner("Running Digital Twin tests..."):
            success = step_2_test_digital_twin()
        
        if success:
            st.session_state.step2_complete = True
            st.success("✅ Digital Twin testing complete!")
            st.balloons()
            st.rerun()
    
    st.markdown("---")
    
    # Step 3: Push & Test in Production
    st.markdown('<p class="step-header">Step 3: Push & Test in Production</p>', unsafe_allow_html=True)
    
    # Expanding section describing what will be done
    with st.expander("ℹ️ What happens in this step?"):
        st.markdown("""
        **Production Deployment applies the tested ACL to live network devices:**
        
        1. **Pre-deployment Snapshot**: Capture current device state for rollback
        2. **Configuration Backup**: Backup existing device configurations
        3. **Maintenance Window Check**: Verify deployment is within scheduled window
        4. **ACL Push to Devices**: Deploy the ACL to production devices
        5. **Post-deployment Validation**: Verify ACL is applied correctly
        6. **Connectivity Tests**: Ensure network connectivity is maintained
        7. **Monitoring Period**: Watch for alerts during stabilization period
        8. **Rollback Procedure**: Keep rollback ready for quick recovery
        
        ⚠️ *This step affects production devices. Only proceed after successful Digital Twin testing.*
        """)
    
    if not st.session_state.get('step2_complete', False):
        st.warning("⚠️ Complete Step 2 (Test on Digital Twin) before deploying to production.")
    
    if st.button("🚀 Push & Test in Production", 
                 type="primary", 
                 use_container_width=True,
                 disabled=bool(not st.session_state.get('step2_complete', False))):
        
        # Add confirmation for production push
        confirm = st.checkbox("I confirm I want to deploy to production", key="confirm_prod")
        
        if confirm:
            with st.spinner("Deploying to production..."):
                success = step_3_push_production()
            
            if success:
                st.session_state.step3_complete = True
                st.success("✅ Production deployment complete!")
                st.balloons()
                st.rerun()
        else:
            st.warning("⚠️ Please confirm the production deployment by checking the box above.")
    
    st.markdown("---")
    
    # Workflow complete message
    if st.session_state.step3_complete:
        st.markdown("## 🎉 Workflow Complete!")
        st.write("All three steps have been completed successfully.")
        
        if st.button("🔄 Start New Workflow", type="secondary"):
            # Reset session state
            st.session_state.step1_complete = False
            st.session_state.step2_complete = False
            st.session_state.step3_complete = False
            st.session_state.generated_acl = None
            st.session_state.dns_ips = None
            st.rerun()


if __name__ == "__main__":
    main()
