"""
UI helper functions for Streamlit app
"""
import streamlit as st
import pandas as pd


def display_query_results(df: pd.DataFrame, max_rows: int = 100):
    """Display query results in a professional format"""
    if df.empty:
        st.markdown("""
        <div class="info-box">
            <strong>ℹ️ No Results Found</strong><br>
            Your query executed successfully but returned no data.
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Results summary
    st.markdown(f"""
    <div class="success-box">
        <strong>✅ Query Successful</strong><br>
        Found <strong>{len(df):,}</strong> rows × <strong>{len(df.columns)}</strong> columns
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Display dataframe with better styling
    st.markdown("#### 📊 Results")
    st.dataframe(
        df.head(max_rows), 
        use_container_width=True,
        height=400
    )
    
    if len(df) > max_rows:
        st.info(f"📋 Showing first {max_rows:,} of {len(df):,} rows. Download CSV for complete data.")
    
    # Download button with better styling
    csv = df.to_csv(index=False)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="📥 Download Complete Results (CSV)",
            data=csv,
            file_name="enliten_query_results.csv",
            mime="text/csv",
            use_container_width=True
        )


def display_schema_info(schema_info: dict):
    """Display database schema information in a professional format"""
    
    # Summary metrics
    total_tables = len(schema_info)
    total_rows = sum(info['row_count'] for info in schema_info.values())
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #0066cc; margin: 0;">🗄️ {total_tables}</h3>
            <p style="margin: 0.5rem 0 0 0; color: #666;">Tables</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #0066cc; margin: 0;">📊 {total_rows:,}</h3>
            <p style="margin: 0.5rem 0 0 0; color: #666;">Total Records</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_columns = sum(len(info['dtypes']) for info in schema_info.values())
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #0066cc; margin: 0;">🔢 {total_columns}</h3>
            <p style="margin: 0.5rem 0 0 0; color: #666;">Total Columns</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Table details
    for table_name, info in schema_info.items():
        with st.expander(f"**📋 {table_name}** ({info['row_count']:,} rows)", expanded=False):
            st.markdown("##### Column Information")
            
            # Create columns info
            col_df = pd.DataFrame([
                {"Column Name": col, "Data Type": str(dtype)} 
                for col, dtype in info['dtypes'].items()
            ])
            st.dataframe(col_df, use_container_width=True, hide_index=True)
            
            st.markdown("##### Sample Data Preview")
            sample_df = pd.DataFrame(info['sample'])
            st.dataframe(sample_df, use_container_width=True, hide_index=True)


def format_sql_query(sql: str) -> str:
    """Format SQL query for display"""
    import sqlparse
    formatted = sqlparse.format(
        sql,
        reindent=True,
        keyword_case='upper'
    )
    return formatted
