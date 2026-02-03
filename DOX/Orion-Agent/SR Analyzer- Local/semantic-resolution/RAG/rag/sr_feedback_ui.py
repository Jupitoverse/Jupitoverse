"""
SR Feedback UI - Streamlit Application
Display SR analysis results with upvote/downvote functionality
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from feedback_storage import WorkaroundFeedbackStorage


def init_session_state():
    """Initialize session state variables"""
    if 'feedback_storage' not in st.session_state:
        st.session_state.feedback_storage = WorkaroundFeedbackStorage()
    if 'current_file' not in st.session_state:
        st.session_state.current_file = None
    if 'df' not in st.session_state:
        st.session_state.df = None


def load_excel_file(file_path: Path) -> pd.DataFrame:
    """Load Excel file with SR analysis results"""
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None


def display_workaround_with_votes(
    sr_id: str,
    workaround_label: str,
    workaround_text: str,
    workaround_type: str,
    feedback_storage: WorkaroundFeedbackStorage,
    key_prefix: str
):
    """Display a workaround box with upvote/downvote buttons"""
    
    # Skip if workaround is not available
    if not workaround_text or workaround_text in ['N/A', 'Not available', 'nan']:
        return
    
    # Get current votes
    votes = feedback_storage.get_votes(sr_id, workaround_type)
    
    # Display workaround in an expander
    with st.expander(f"{workaround_label} Workaround", expanded=True):
        # Display workaround text
        st.text_area(
            "Workaround Details",
            value=workaround_text,
            height=150,
            key=f"{key_prefix}_text",
            disabled=True,
            label_visibility="collapsed"
        )
        
        # Vote buttons and display
        col1, col2, col3, col4 = st.columns([1, 1, 2, 2])
        
        with col1:
            if st.button(f"👍 {votes['upvotes']}", key=f"{key_prefix}_up", help="Upvote this workaround"):
                feedback_storage.upvote(sr_id, workaround_type, workaround_text)
                st.rerun()
        
        with col2:
            if st.button(f"👎 {votes['downvotes']}", key=f"{key_prefix}_down", help="Downvote this workaround"):
                feedback_storage.downvote(sr_id, workaround_type, workaround_text)
                st.rerun()
        
        with col3:
            score = votes['score']
            # Determine emoji based on score
            if score > 5:
                score_emoji = "🔥"
                score_label = "Highly Validated"
            elif score > 0:
                score_emoji = "✅"
                score_label = "Validated"
            elif score == 0 and (votes['upvotes'] > 0 or votes['downvotes'] > 0):
                score_emoji = "⚖️"
                score_label = "Mixed"
            elif score < 0:
                score_emoji = "⚠️"
                score_label = "Problematic"
            else:
                score_emoji = "📊"
                score_label = "Not Rated"
            
            st.markdown(f"{score_emoji} **Score: {score:+d}** ({score_label})")


def display_sr_box(row: pd.Series, feedback_storage: WorkaroundFeedbackStorage, index: int):
    """Display a single SR analysis box with all workarounds"""
    
    sr_id = row.get('SR ID', f'SR-{index}')
    match_pct = row.get('Match Similarity', 'N/A')
    resolution_cat = row.get('Resolution Category', 'N/A')
    status_reason = row.get('Status Reason', 'N/A')
    
    # Create a nice bordered box
    with st.container():
        st.markdown(f"""
        <div style="border: 2px solid #4CAF50; border-radius: 10px; padding: 20px; margin: 20px 0;">
            <h3>📊 {sr_id} <span style="float: right; color: #4CAF50;">[{match_pct}]</span></h3>
            <hr style="border: 1px solid #ddd;">
            <p><strong>📋 Resolution Categorization:</strong> {resolution_cat}</p>
            <p><strong>🎯 SLA Resolution:</strong> {status_reason}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Display workarounds with voting
        
        # 1. Original/Semantic Workaround
        semantic_workaround = row.get('Semantic Workaround', '')
        if semantic_workaround and str(semantic_workaround) not in ['N/A', 'Not available', 'nan']:
            display_workaround_with_votes(
                sr_id=sr_id,
                workaround_label="💡 Original",
                workaround_text=str(semantic_workaround),
                workaround_type='original',
                feedback_storage=feedback_storage,
                key_prefix=f"{sr_id}_original_{index}"
            )
        
        # 2. AI Workaround
        ai_workaround = row.get('AI Workaround', '')
        if ai_workaround and str(ai_workaround) not in ['N/A', 'Not available', 'nan']:
            display_workaround_with_votes(
                sr_id=sr_id,
                workaround_label="🤖 AI",
                workaround_text=str(ai_workaround),
                workaround_type='ai',
                feedback_storage=feedback_storage,
                key_prefix=f"{sr_id}_ai_{index}"
            )
        
        # 3. User Corrected Workaround
        user_corrected = row.get('User Corrected Workaround', '')
        if user_corrected and str(user_corrected) not in ['N/A', 'Not available', 'nan', '']:
            display_workaround_with_votes(
                sr_id=sr_id,
                workaround_label="🌟 User Correction",
                workaround_text=str(user_corrected),
                workaround_type='user_corrected',
                feedback_storage=feedback_storage,
                key_prefix=f"{sr_id}_user_{index}"
            )
        
        st.markdown("---")


def main():
    """Main Streamlit application"""
    
    st.set_page_config(
        page_title="SR Feedback System",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    init_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("📊 SR Feedback System")
        st.markdown("---")
        
        # File uploader
        st.subheader("📁 Load SR Analysis Results")
        uploaded_file = st.file_uploader(
            "Upload Excel file",
            type=['xlsx', 'xls'],
            help="Upload the SR analysis output Excel file"
        )
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            temp_path = Path("temp_upload.xlsx")
            with open(temp_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            # Load data
            df = load_excel_file(temp_path)
            if df is not None:
                st.session_state.df = df
                st.session_state.current_file = uploaded_file.name
                st.success(f"✅ Loaded {len(df)} SRs")
            
            # Clean up temp file
            if temp_path.exists():
                temp_path.unlink()
        
        # Or load from output directory
        st.markdown("---")
        st.subheader("📂 Or Select from Output Folder")
        
        output_dir = Path(__file__).parent.parent / "llm output"
        if output_dir.exists():
            excel_files = sorted(
                list(output_dir.glob("*.xlsx")),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            
            if excel_files:
                file_options = {f.name: f for f in excel_files}
                selected_file = st.selectbox(
                    "Select file",
                    options=list(file_options.keys()),
                    help="Most recent files appear first"
                )
                
                if st.button("Load Selected File"):
                    df = load_excel_file(file_options[selected_file])
                    if df is not None:
                        st.session_state.df = df
                        st.session_state.current_file = selected_file
                        st.success(f"✅ Loaded {len(df)} SRs")
                        st.rerun()
        
        # Statistics
        if st.session_state.df is not None:
            st.markdown("---")
            st.subheader("📈 Statistics")
            
            stats = st.session_state.feedback_storage.get_statistics()
            
            st.metric("Total Workarounds Rated", stats['total_workarounds_with_feedback'])
            st.metric("Total Upvotes", stats['total_upvotes'])
            st.metric("Total Downvotes", stats['total_downvotes'])
            st.metric("Average Score", f"{stats['average_score']:.2f}")
            
            if stats['best_workaround']['sr_id']:
                st.markdown(f"**🏆 Best:** {stats['best_workaround']['sr_id']} (Score: {stats['best_workaround']['score']})")
            
            if stats['worst_workaround']['sr_id']:
                st.markdown(f"**⚠️ Worst:** {stats['worst_workaround']['sr_id']} (Score: {stats['worst_workaround']['score']})")
        
        # Top workarounds
        if st.session_state.df is not None:
            st.markdown("---")
            if st.button("🏆 View Top Workarounds"):
                st.session_state.show_top = True
            if st.button("⚠️ View Bottom Workarounds"):
                st.session_state.show_bottom = True
    
    # Main content area
    if st.session_state.df is None:
        st.title("📊 SR Feedback System")
        st.info("👈 Please upload an Excel file or select one from the output folder in the sidebar.")
        
        # Display instructions
        st.markdown("""
        ## How to Use
        
        1. **Load Data**: Upload an SR analysis Excel file or select from recent outputs
        2. **Review Workarounds**: Scroll through the SR boxes below
        3. **Provide Feedback**: Click 👍 to upvote helpful workarounds or 👎 to downvote unhelpful ones
        4. **View Statistics**: Check the sidebar for overall feedback statistics
        
        ## Benefits
        
        - **Improve AI Responses**: Your feedback helps the system learn which workarounds are most effective
        - **Priority Ranking**: High-voted workarounds will be prioritized in future SR analysis
        - **Quality Assurance**: Identify problematic solutions that need improvement
        """)
        
        return
    
    # Display loaded data
    df = st.session_state.df
    
    st.title(f"📊 SR Analysis Results - {st.session_state.current_file}")
    st.markdown(f"**Total SRs:** {len(df)}")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Filter by Resolution Category
        categories = ['All'] + sorted(df['Resolution Category'].unique().tolist())
        selected_category = st.selectbox("Filter by Category", categories)
    
    with col2:
        # Filter by Java Error
        java_filter = st.selectbox("Filter by Java Error", ['All', 'Yes', 'No'])
    
    with col3:
        # Search by SR ID
        search_sr = st.text_input("Search SR ID", placeholder="Enter SR ID...")
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['Resolution Category'] == selected_category]
    
    if java_filter != 'All':
        filtered_df = filtered_df[filtered_df['Java Failure Detected'] == java_filter]
    
    if search_sr:
        filtered_df = filtered_df[filtered_df['SR ID'].astype(str).str.contains(search_sr, case=False)]
    
    st.markdown(f"**Showing:** {len(filtered_df)} SRs")
    st.markdown("---")
    
    # Display SR boxes
    if len(filtered_df) > 0:
        for idx, row in filtered_df.iterrows():
            display_sr_box(row, st.session_state.feedback_storage, idx)
    else:
        st.warning("No SRs match the selected filters.")
    
    # Show top/bottom workarounds if requested
    if hasattr(st.session_state, 'show_top') and st.session_state.show_top:
        st.markdown("---")
        st.subheader("🏆 Top Rated Workarounds")
        top_workarounds = st.session_state.feedback_storage.get_top_workarounds(limit=10)
        
        if top_workarounds:
            for idx, w in enumerate(top_workarounds, 1):
                st.markdown(f"""
                **#{idx}. {w['sr_id']}** - {w['workaround_type'].replace('_', ' ').title()}  
                👍 {w['upvotes']} | 👎 {w['downvotes']} | Score: **{w['score']:+d}**  
                {w['workaround_text'][:200]}...
                """)
                st.markdown("---")
        else:
            st.info("No workarounds have been rated yet.")
        
        st.session_state.show_top = False
    
    if hasattr(st.session_state, 'show_bottom') and st.session_state.show_bottom:
        st.markdown("---")
        st.subheader("⚠️ Lowest Rated Workarounds")
        bottom_workarounds = st.session_state.feedback_storage.get_bottom_workarounds(limit=10)
        
        if bottom_workarounds:
            for idx, w in enumerate(bottom_workarounds, 1):
                st.markdown(f"""
                **#{idx}. {w['sr_id']}** - {w['workaround_type'].replace('_', ' ').title()}  
                👍 {w['upvotes']} | 👎 {w['downvotes']} | Score: **{w['score']:+d}**  
                {w['workaround_text'][:200]}...
                """)
                st.markdown("---")
        else:
            st.info("No workarounds have been rated yet.")
        
        st.session_state.show_bottom = False


if __name__ == "__main__":
    main()

