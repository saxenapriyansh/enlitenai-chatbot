"""
Voice-Enabled Medical Data Query System
A Streamlit app for physicians to query patient data using natural language and voice
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import os
import tempfile

# Import utilities
from utils.db import DatabaseManager
from utils.llm import LLMManager
from utils.voice import VoiceManager
from utils.ui import (
    display_query_results, 
    display_schema_info, 
    format_sql_query
)

# Page configuration
st.set_page_config(
    page_title="EnlitenAI - Medical Data Query System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - EnlitenAI Branding
st.markdown("""
<style>
    /* EnlitenAI Color Palette */
    :root {
        --primary-color: #0066cc;
        --secondary-color: #00a3e0;
        --accent-color: #4CAF50;
        --text-dark: #1a1a1a;
        --text-light: #666666;
        --bg-light: #f8f9fa;
    }
    
    /* Main Header */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: var(--primary-color);
        text-align: center;
        margin-bottom: 0.5rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .subtitle {
        text-align: center;
        color: var(--text-light);
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background-color: var(--primary-color);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: var(--secondary-color);
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
        transform: translateY(-2px);
    }
    
    /* Success Box */
    .success-box {
        padding: 1.5rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 5px solid var(--accent-color);
        color: #155724;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Error Box */
    .error-box {
        padding: 1.5rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 5px solid #dc3545;
        color: #721c24;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Info Box */
    .info-box {
        padding: 1.5rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border-left: 5px solid var(--secondary-color);
        color: #0c5460;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        border-left: 4px solid var(--primary-color);
        margin-bottom: 1rem;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: var(--bg-light);
    }
    
    /* Text Input */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.1);
    }
    
    /* Tables */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* SQL Code Block */
    .sql-block {
        background-color: #2d2d2d;
        color: #f8f8f2;
        padding: 1.5rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        overflow-x: auto;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: var(--text-light);
        font-size: 0.9rem;
        border-top: 1px solid #e0e0e0;
        margin-top: 3rem;
    }
    
    /* EnlitenAI Logo Text */
    .enliten-logo {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = None
    if 'llm_manager' not in st.session_state:
        st.session_state.llm_manager = None
    if 'voice_manager' not in st.session_state:
        st.session_state.voice_manager = None
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []
    if 'query_input' not in st.session_state:
        st.session_state.query_input = ""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Query Interface"


def initialize_managers():
    """Initialize all managers"""
    try:
        # Get API key from Streamlit secrets or environment variable
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
        except (KeyError, FileNotFoundError):
            api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            st.error("⚠️ OpenAI API key not found. Please configure OPENAI_API_KEY in Streamlit secrets or .env file")
            st.info("💡 For Streamlit Cloud: Go to App Settings → Secrets and add:\n```\nOPENAI_API_KEY = \"your-api-key-here\"\n```")
            st.stop()
        
        # Initialize database
        if st.session_state.db_manager is None:
            with st.spinner("Loading database..."):
                st.session_state.db_manager = DatabaseManager("data")
                st.session_state.db_manager.load_csvs_to_db()
        
        # Initialize LLM (OpenAI only)
        if st.session_state.llm_manager is None:
            try:
                st.session_state.llm_manager = LLMManager(api_key)
            except Exception as e:
                st.error(f"⚠️ LLM initialization error: {str(e)}")
                st.stop()
        
        # Initialize Voice (OpenAI)
        if st.session_state.voice_manager is None:
            try:
                st.session_state.voice_manager = VoiceManager(api_key)
            except Exception as e:
                st.warning(f"⚠️ Voice features unavailable: {str(e)}")
                st.session_state.voice_manager = None
            
        return True
    except Exception as e:
        st.error(f"❌ Initialization error: {str(e)}")
        return False


def process_text_query(query: str):
    """Process a text query"""
    try:
        db = st.session_state.db_manager
        llm = st.session_state.llm_manager
        
        # Get schema description
        schema_desc = db.get_schema_description()
        
        # Generate SQL
        with st.spinner("🤖 Generating SQL query..."):
            sql_query, explanation = llm.text_to_sql(query, schema_desc)
        
        # Validate SQL
        is_valid, error_msg = db.validate_sql(sql_query)
        if not is_valid:
            st.error(f"❌ SQL validation failed: {error_msg}")
            return
        
        # Display generated SQL
        st.subheader("🔍 Generated SQL Query")
        st.code(format_sql_query(sql_query), language="sql")
        st.info(f"**Explanation:** {explanation}")
        
        # Execute query
        with st.spinner("⚙️ Executing query..."):
            results = db.execute_query(sql_query)
        
        # Display results
        st.subheader("📊 Query Results")
        display_query_results(results)
        
        # Generate natural language answer
        with st.spinner("💬 Generating answer..."):
            result_text = results.to_string() if not results.empty else "No results found"
            answer = llm.generate_answer(query, result_text)
        
        st.subheader("💡 Answer Summary")
        st.success(answer)
        
        # Add to history
        st.session_state.query_history.append({
            "query": query,
            "sql": sql_query,
            "results": len(results),
            "answer": answer
        })
        
        return answer
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None


def main():
    """Main application"""
    init_session_state()
    
    # Initialize managers first (before building UI)
    if not initialize_managers():
        return
    
    # EnlitenAI Header
    st.markdown('<div class="enliten-logo">EnlitenAI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Decision Support Software for Neurological Care</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; color: #666; margin-bottom: 2rem;">Transforming passive monitoring into proactive, personalized intervention</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        # Logo in sidebar
        logo_path = "assets/logo.png"
        if os.path.exists(logo_path):
            st.image(logo_path, use_column_width=True)
            st.markdown("---")
        else:
            st.markdown("### 🧠 EnlitenAI")
            st.markdown("**Medical Data Query System**")
            st.markdown("---")
        
        
        st.title("📋 Navigation")
        
        page = st.radio(
            "Select Page",
            ["Query Interface", "Database Schema", "Query History"],
            index=["Query Interface", "Database Schema", "Query History"].index(st.session_state.current_page),
            label_visibility="collapsed"
        )
        
        # Update session state if page changed
        if page != st.session_state.current_page:
            st.session_state.current_page = page
        
        st.divider()
        
        # Show LLM provider info
        st.markdown("""
        <div class="info-box" style="padding: 0.75rem; margin-bottom: 1rem;">
            <strong>🤖 AI Model:</strong> OPENAI (GPT-4)
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Mode selection
        st.subheader("Query Mode")
        
        # Check if voice is available
        available_modes = ["Text Input", "Direct SQL"]
        if st.session_state.voice_manager is not None:
            available_modes.insert(1, "Voice Input")
        
        query_mode = st.radio(
            "Choose input method:",
            available_modes,
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Settings
        st.subheader("⚙️ Settings")
        tts_enabled = st.checkbox("Enable Text-to-Speech", value=True)
        tts_voice = st.selectbox(
            "TTS Voice",
            ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
            index=0
        )
        
        st.divider()
        st.caption("💡 Tip: Use natural language to query patient data!")
    
    # Main content
    if page == "Query Interface":
        show_query_interface(query_mode, tts_enabled, tts_voice)
    elif page == "Database Schema":
        show_schema_page()
    elif page == "Query History":
        show_history_page()


def show_query_interface(query_mode: str, tts_enabled: bool, tts_voice: str):
    """Display the main query interface with improved layout"""
    
    # Quick help banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                padding: 1rem; border-radius: 10px; margin-bottom: 1.5rem; 
                border-left: 4px solid #0066cc;">
        <strong>💬 Ask questions in plain English</strong> — No SQL knowledge required!<br>
        <span style="font-size: 0.9rem; color: #555;">
        Examples: "What is the average QoL score?" • "Show seizure trends" • "Compare medication dosages"
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Main layout with two columns
    main_col, example_col = st.columns([2, 1])
    
    with main_col:
        # Query input section
        st.markdown("### 🔍 Your Question")
        st.markdown('<p style="color: #666; font-size: 0.9rem; margin-bottom: 0.5rem;">Ask about patients, medications, seizures, or assessments</p>', unsafe_allow_html=True)
        
        if query_mode == "Text Input":
            query = st.text_area(
                "Type your question in natural language:",
                value=st.session_state.query_input,
                height=120,
                placeholder="e.g., What is the average QoL score for patient P001?",
                label_visibility="collapsed"
            )
            
            # Action buttons
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                submit_button = st.button("🔍 Search", type="primary", use_container_width=True)
            with col2:
                clear_button = st.button("🗑️ Clear", use_container_width=True)
            with col3:
                if st.button("📊 Schema", use_container_width=True):
                    st.session_state.current_page = "Database Schema"
                    st.rerun()
            
            if clear_button:
                st.session_state.query_input = ""
                st.rerun()
            
            if submit_button and query:
                answer = process_text_query(query)
                
                # Text-to-speech (if available)
                if tts_enabled and answer and st.session_state.voice_manager:
                    try:
                        with st.spinner("🔊 Generating audio..."):
                            voice_mgr = st.session_state.voice_manager
                            audio_bytes = voice_mgr.text_to_speech(answer, voice=tts_voice)
                        
                        st.audio(audio_bytes, format="audio/mp3")
                    except Exception as e:
                        st.warning(f"TTS unavailable: {str(e)}")
    
        elif query_mode == "Voice Input":
            if st.session_state.voice_manager is None:
                st.error("⚠️ Voice features require OpenAI API key. Please set OPENAI_API_KEY in .env file.")
                st.info("💡 You can still use Text Input or Direct SQL modes with Gemini.")
                return
            
            st.info("🎤 Voice input requires microphone access")
            
            # Import audio recorder
            try:
                from audio_recorder_streamlit import audio_recorder
                
                st.write("Click the button below and speak your question:")
                audio_bytes = audio_recorder()
                
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/wav")
                    
                    if st.button("🔍 Process Voice Query", type="primary"):
                        try:
                            with st.spinner("🎧 Transcribing audio..."):
                                voice_mgr = st.session_state.voice_manager
                                transcribed_text = voice_mgr.transcribe_audio(audio_bytes, "wav")
                            
                            st.success(f"**Transcribed:** {transcribed_text}")
                            
                            # Process the transcribed query
                            answer = process_text_query(transcribed_text)
                            
                            # Text-to-speech response
                            if tts_enabled and answer:
                                with st.spinner("🔊 Generating audio response..."):
                                    audio_response = voice_mgr.text_to_speech(answer, voice=tts_voice)
                                st.audio(audio_response, format="audio/mp3")
                                
                        except Exception as e:
                            st.error(f"❌ Voice processing error: {str(e)}")
            except ImportError:
                st.warning("⚠️ Voice recording component not available. Install with: pip install audio-recorder-streamlit")
                st.info("You can still use Text Input mode or install the component.")
        
        elif query_mode == "Direct SQL":
            st.warning("⚠️ Advanced mode: Enter SQL queries directly")
            
            sql_query = st.text_area(
                "Enter SQL query:",
                height=150,
                placeholder="SELECT * FROM assessments_dummy WHERE patient_id = 'P001' LIMIT 10;",
                label_visibility="collapsed"
            )
            
            if st.button("▶️ Execute SQL", type="primary", use_container_width=True):
                if sql_query:
                    try:
                        db = st.session_state.db_manager
                        
                        # Validate
                        is_valid, error_msg = db.validate_sql(sql_query)
                        if not is_valid:
                            st.error(f"❌ {error_msg}")
                            return
                        
                        # Execute
                        with st.spinner("⚙️ Executing..."):
                            results = db.execute_query(sql_query)
                        
                        st.subheader("📊 Results")
                        display_query_results(results)
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # Example queries in the right column
    with example_col:
        show_example_queries_compact()


def show_schema_page():
    """Display database schema information"""
    st.markdown('<div class="main-header" style="font-size: 2rem;">📊 Database Schema</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; margin-bottom: 2rem;">View data structure and available tables</p>', unsafe_allow_html=True)
    
    if st.session_state.db_manager:
        schema_info = st.session_state.db_manager.get_schema_info()
        display_schema_info(schema_info)
        
        # Show table statistics
        st.subheader("📈 Database Statistics")
        stats = []
        for table_name, info in schema_info.items():
            stats.append({
                "Table": table_name,
                "Rows": info['row_count'],
                "Columns": len(info['columns'])
            })
        
        st.dataframe(pd.DataFrame(stats), use_container_width=True, hide_index=True)
    else:
        st.error("Database not initialized")


def show_history_page():
    """Display query history"""
    st.markdown('<div class="main-header" style="font-size: 2rem;">📝 Query History</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; margin-bottom: 2rem;">Review your previous queries and results</p>', unsafe_allow_html=True)
    
    if not st.session_state.query_history:
        st.info("No queries executed yet.")
        return
    
    # Display history in reverse order (most recent first)
    for i, item in enumerate(reversed(st.session_state.query_history)):
        with st.expander(f"Query {len(st.session_state.query_history) - i}: {item['query'][:50]}..."):
            st.write("**Question:**", item['query'])
            st.code(item['sql'], language="sql")
            st.write("**Results:**", f"{item['results']} rows")
            st.write("**Answer:**", item['answer'])
    
    # Clear history button
    if st.button("🗑️ Clear History"):
        st.session_state.query_history = []
        st.rerun()


def show_example_queries_compact():
    """Display example queries in sidebar/column"""
    st.markdown("### 💡 Example Queries")
    st.markdown('<p style="font-size: 0.85rem; color: #666; margin-bottom: 1rem;">Click any question to try it:</p>', unsafe_allow_html=True)
    
    # Categorized examples with full questions
    examples = {
        "👤 Patient-Specific": [
            "What is the average QoL score for patient P001?",
            "Show me all seizure events for patient P002 in the last month",
            "List all assessments for patient P003",
        ],
        "📊 Comparative Analysis": [
            "Which patients had the highest anxiety scores?",
            "Compare medication dosages between patients P001 and P003",
            "Show me patients with QoL scores below 50",
        ],
        "📈 Trend Analysis": [
            "Show me the trend of behavioral scores for patient P004",
            "What's the correlation between medication Med A dosage and seizure frequency?",
        ],
        "🔢 Statistical Queries": [
            "What is the average number of seizures per patient?",
            "How many severe seizures did patient P005 have in total?",
        ]
    }
    
    for category, queries in examples.items():
        with st.expander(category, expanded=True):
            for query in queries:
                if st.button(query, key=f"example_{query[:30]}", use_container_width=True):
                    st.session_state.query_input = query
                    st.rerun()
    
    # Quick stats
    st.markdown("---")
    st.markdown("##### 📊 Data Overview")
    if st.session_state.db_manager:
        schema = st.session_state.db_manager.get_schema_info()
        total_records = sum(info['row_count'] for info in schema.values())
        st.markdown(f"""
        <div style="font-size: 0.85rem; color: #666;">
        • <strong>3</strong> tables<br>
        • <strong>{total_records:,}</strong> records<br>
        • <strong>5</strong> patients
        </div>
        """, unsafe_allow_html=True)


def show_footer():
    """Display EnlitenAI footer"""
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p><strong>EnlitenAI</strong> - Decision Support Software Platform for Neurological Care</p>
        <p style="font-size: 0.85rem; margin-top: 0.5rem;">
            📧 <a href="mailto:info@enlitenai.com">info@enlitenai.com</a> | 
            📞 (408) 483-1742 | 
            🌐 <a href="https://enlitenai.com" target="_blank">enlitenai.com</a>
        </p>
        <p style="font-size: 0.8rem; color: #999; margin-top: 1rem;">
            © 2025 EnlitenAI | All Rights Reserved
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
    show_footer()

