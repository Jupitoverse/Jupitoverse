"""
Bulk Re-execute - Streamlit UI
================================

Purpose:
--------
Streamlit-based web interface for bulk re-execution of activities in Orion system.
Allows users to input bearer token and multiple activity/plan ID pairs for processing.

Features:
---------
- Bearer token input field
- Multi-line input for activity_id and plan_id pairs (comma-separated)
- Real-time line counter
- Confirmation dialog before execution
- 5-second delay between each API call to avoid production load
- Progress tracking with status updates
- Success/failure reporting

Author: Abhishek Agrahari
Last Modified: November 2025
"""

import streamlit as st
import requests
import time
from datetime import datetime
import csv
from io import StringIO

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Bulk Re-execute",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================

st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 20px 0;
        border-bottom: 3px solid #1f77b4;
        margin-bottom: 30px;
    }
    
    /* Info boxes */
    .info-box {
        background-color: #e7f3ff;
        border-left: 5px solid #1f77b4;
        padding: 15px;
        margin: 20px 0;
        border-radius: 5px;
    }
    
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        margin: 20px 0;
        border-radius: 5px;
    }
    
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        margin: 20px 0;
        border-radius: 5px;
    }
    
    .error-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 15px;
        margin: 20px 0;
        border-radius: 5px;
    }
    
    /* Line counter styling */
    .line-counter {
        font-size: 1.2rem;
        font-weight: bold;
        color: #28a745;
        padding: 10px;
        background-color: #f8f9fa;
        border-radius: 5px;
        text-align: center;
        margin: 10px 0;
    }
    
    /* Progress styling */
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# MAIN HEADER
# ============================================================================

st.markdown('<div class="main-header">⚡ Bulk Re-execute</div>', unsafe_allow_html=True)

# ============================================================================
# INFORMATION SECTION
# ============================================================================

with st.expander("ℹ️ How to Use", expanded=False):
    st.markdown("""
    ### Instructions:
    
    1. **Enter Bearer Token**: Paste your authentication bearer token
    2. **Enter Activity & Plan IDs**: 
       - Format: `activity_id, plan_id` (one pair per line)
       - Example:
         ```
         99A1C7B722584BC5A1617007D03015E2, 0F30089DABAC4A79A50EF9C8C87F45611737061897
         A70327A634EC48238035F813E574EC21, F9FC0070A02C4387AAABF618FA1506311737065038
         ```
    3. **Review Line Count**: Check the number of activities to be processed
    4. **Click Submit**: Confirm the operation when prompted
    5. **Monitor Progress**: Watch real-time execution status
    
    ### Important Notes:
    - ⏱️ There is a **5-second delay** between each API call to avoid overloading production
    - ✅ Each successful execution will be logged
    - ❌ Failed executions will be reported with error details
    - 📊 A summary report will be generated at the end
    """)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'execution_started' not in st.session_state:
    st.session_state.execution_started = False
if 'execution_results' not in st.session_state:
    st.session_state.execution_results = []
if 'confirmed' not in st.session_state:
    st.session_state.confirmed = False

# ============================================================================
# API EXECUTION FUNCTION
# ============================================================================

def execute_api(plan_id, activity_id, bearer_token, base_url):
    """
    Execute the rework API call for a single activity
    
    Args:
        plan_id (str): Plan ID
        activity_id (str): Activity ID
        bearer_token (str): Bearer token for authentication
        base_url (str): Base API URL
        
    Returns:
        dict: Result dictionary with status, message, and details
    """
    url = f"{base_url}/{plan_id}/{activity_id}"
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return {
                'status': 'success',
                'plan_id': plan_id,
                'activity_id': activity_id,
                'status_code': response.status_code,
                'message': 'Successfully executed'
            }
        elif response.status_code == 403:
            return {
                'status': 'error',
                'plan_id': plan_id,
                'activity_id': activity_id,
                'status_code': response.status_code,
                'message': 'Forbidden: No permission to access this resource'
            }
        else:
            return {
                'status': 'error',
                'plan_id': plan_id,
                'activity_id': activity_id,
                'status_code': response.status_code,
                'message': f'Failed with status code: {response.status_code}'
            }
    except requests.exceptions.Timeout:
        return {
            'status': 'error',
            'plan_id': plan_id,
            'activity_id': activity_id,
            'status_code': 'N/A',
            'message': 'Request timeout (30 seconds)'
        }
    except Exception as e:
        return {
            'status': 'error',
            'plan_id': plan_id,
            'activity_id': activity_id,
            'status_code': 'N/A',
            'message': f'Exception: {str(e)}'
        }

# ============================================================================
# PARSE INPUT FUNCTION
# ============================================================================

def parse_input(input_text):
    """
    Parse the multi-line input text into activity_id and plan_id pairs
    
    Args:
        input_text (str): Multi-line input with comma-separated values
        
    Returns:
        list: List of tuples (activity_id, plan_id)
    """
    pairs = []
    lines = input_text.strip().split('\n')
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:  # Skip empty lines
            continue
            
        parts = [part.strip() for part in line.split(',')]
        
        if len(parts) == 2:
            activity_id, plan_id = parts
            pairs.append((activity_id, plan_id))
        else:
            st.warning(f"⚠️ Line {line_num} has invalid format (expected 2 values, got {len(parts)}): {line}")
    
    return pairs

# ============================================================================
# INPUT SECTION
# ============================================================================

st.markdown("### 🔑 Authentication")
bearer_token = st.text_input(
    "Bearer Token",
    type="password",
    placeholder="Paste your bearer token here",
    help="Enter the authentication bearer token for API access"
)

st.markdown("---")

st.markdown("### 📝 Activity & Plan IDs")
st.markdown("""
<div class="info-box">
    <strong>Format:</strong> <code>activity_id, plan_id</code> (one pair per line)<br>
    <strong>Example:</strong><br>
    <code>99A1C7B722584BC5A1617007D03015E2, 0F30089DABAC4A79A50EF9C8C87F45611737061897</code><br>
    <code>A70327A634EC48238035F813E574EC21, F9FC0070A02C4387AAABF618FA1506311737065038</code>
</div>
""", unsafe_allow_html=True)

input_text = st.text_area(
    "Enter Activity ID and Plan ID pairs (comma-separated, one per line)",
    height=300,
    placeholder="activity_id, plan_id\nactivity_id, plan_id\n...",
    help="Enter one activity_id and plan_id pair per line, separated by comma"
)

# ============================================================================
# LINE COUNTER
# ============================================================================

if input_text:
    parsed_pairs = parse_input(input_text)
    line_count = len(parsed_pairs)
    
    st.markdown(f"""
    <div class="line-counter">
        📊 Total Lines: <strong>{line_count}</strong> activities to be processed
    </div>
    """, unsafe_allow_html=True)
else:
    line_count = 0
    st.markdown("""
    <div class="line-counter" style="color: #6c757d;">
        📊 Total Lines: <strong>0</strong> (waiting for input)
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# SUBMIT BUTTON & CONFIRMATION
# ============================================================================

st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    submit_button = st.button(
        "🚀 Submit",
        type="primary",
        use_container_width=True,
        disabled=(not bearer_token or line_count == 0)
    )

# ============================================================================
# CONFIRMATION DIALOG
# ============================================================================

if submit_button and not st.session_state.confirmed:
    st.markdown(f"""
    <div class="warning-box">
        <h3>⚠️ Confirmation Required</h3>
        <p style="font-size: 1.2rem;">
            Are you sure you want to rework <strong>{line_count}</strong> activities?
        </p>
        <p>
            This will execute {line_count} API calls with a 5-second delay between each call.<br>
            <strong>Estimated time:</strong> {line_count * 5 // 60} minutes {line_count * 5 % 60} seconds
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("✅ Yes, Proceed", type="primary", use_container_width=True):
            st.session_state.confirmed = True
            st.session_state.execution_started = True
            st.rerun()
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.confirmed = False
            st.info("Operation cancelled.")

# ============================================================================
# EXECUTION SECTION
# ============================================================================

if st.session_state.execution_started and st.session_state.confirmed:
    st.markdown("---")
    st.markdown("### 🔄 Execution in Progress")
    
    # Parse input
    parsed_pairs = parse_input(input_text)
    
    # Base URL
    base_url = "https://oso.orion.comcast.com/frontend-services-ws-war/servicepoint/reworkActivity"
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Results containers
    results_container = st.container()
    
    # Execute API calls
    results = []
    total = len(parsed_pairs)
    
    for idx, (activity_id, plan_id) in enumerate(parsed_pairs, 1):
        # Update progress
        progress = idx / total
        progress_bar.progress(progress)
        status_text.markdown(f"""
        <div class="info-box">
            <strong>Processing:</strong> {idx} of {total}<br>
            <strong>Activity ID:</strong> {activity_id}<br>
            <strong>Plan ID:</strong> {plan_id}
        </div>
        """, unsafe_allow_html=True)
        
        # Execute API call
        result = execute_api(plan_id, activity_id, bearer_token, base_url)
        results.append(result)
        
        # Display result
        with results_container:
            if result['status'] == 'success':
                st.success(f"✅ [{idx}/{total}] Success - Activity: {activity_id[:20]}... | Plan: {plan_id[:20]}...")
            else:
                st.error(f"❌ [{idx}/{total}] Failed - Activity: {activity_id[:20]}... | {result['message']}")
        
        # Wait 5 seconds before next call (except for last one)
        if idx < total:
            for remaining in range(5, 0, -1):
                status_text.markdown(f"""
                <div class="warning-box">
                    ⏱️ Waiting {remaining} seconds before next call to avoid production load...
                </div>
                """, unsafe_allow_html=True)
                time.sleep(1)
    
    # Completion
    progress_bar.progress(1.0)
    status_text.markdown("""
    <div class="success-box">
        <h3>✅ Execution Completed!</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================================================
    # SUMMARY REPORT
    # ============================================================================
    
    st.markdown("---")
    st.markdown("### 📊 Execution Summary")
    
    # Calculate statistics
    success_count = sum(1 for r in results if r['status'] == 'success')
    error_count = sum(1 for r in results if r['status'] == 'error')
    
    # Display summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Processed", total)
    with col2:
        st.metric("Successful", success_count, delta=f"{success_count/total*100:.1f}%")
    with col3:
        st.metric("Failed", error_count, delta=f"-{error_count/total*100:.1f}%" if error_count > 0 else "0%")
    
    # Detailed results table
    st.markdown("#### Detailed Results")
    
    # Create HTML table with color coding
    table_html = """
    <style>
    .results-table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 0.9em;
    }
    .results-table th {
        background-color: #1f77b4;
        color: white;
        padding: 12px;
        text-align: left;
        font-weight: bold;
    }
    .results-table td {
        padding: 10px;
        border-bottom: 1px solid #ddd;
    }
    .results-table tr:hover {
        background-color: #f5f5f5;
    }
    .status-success {
        background-color: #d4edda;
        color: #155724;
        font-weight: bold;
        padding: 5px 10px;
        border-radius: 3px;
    }
    .status-error {
        background-color: #f8d7da;
        color: #721c24;
        font-weight: bold;
        padding: 5px 10px;
        border-radius: 3px;
    }
    </style>
    <div style="max-height: 400px; overflow-y: auto;">
    <table class="results-table">
        <thead>
            <tr>
                <th>Status</th>
                <th>Activity ID</th>
                <th>Plan ID</th>
                <th>Status Code</th>
                <th>Message</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for result in results:
        status_class = "status-success" if result['status'] == 'success' else "status-error"
        table_html += f"""
            <tr>
                <td><span class="{status_class}">{result['status']}</span></td>
                <td>{result['activity_id'][:30]}...</td>
                <td>{result['plan_id'][:30]}...</td>
                <td>{result['status_code']}</td>
                <td>{result['message']}</td>
            </tr>
        """
    
    table_html += """
        </tbody>
    </table>
    </div>
    """
    
    st.markdown(table_html, unsafe_allow_html=True)
    
    # Download results as CSV
    csv_buffer = StringIO()
    csv_writer = csv.DictWriter(csv_buffer, fieldnames=['status', 'activity_id', 'plan_id', 'status_code', 'message'])
    csv_writer.writeheader()
    csv_writer.writerows(results)
    csv_data = csv_buffer.getvalue()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv_data,
        file_name=f"bulk_rework_results_{timestamp}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    # Reset button
    st.markdown("---")
    if st.button("🔄 Start New Execution", type="primary", use_container_width=True):
        st.session_state.execution_started = False
        st.session_state.confirmed = False
        st.session_state.execution_results = []
        st.rerun()

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 20px;">
    <p><strong>Bulk Re-execute Tool</strong> | Orion System</p>
    <p>For support, contact: <a href="mailto:abhisha3@amdocs.com">abhisha3@amdocs.com</a></p>
</div>
""", unsafe_allow_html=True)

