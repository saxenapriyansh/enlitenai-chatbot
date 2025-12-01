"""
Database utilities for loading CSV files into SQLite
"""
import sqlite3
import pandas as pd
import os
from pathlib import Path
from typing import Dict, List


class DatabaseManager:
    """Manages SQLite database operations for CSV data"""
    
    def __init__(self, data_folder: str = "data"):
        self.data_folder = data_folder
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.tables = {}
        self.schema_info = {}
        
    def load_csvs_to_db(self) -> Dict[str, pd.DataFrame]:
        """Load all CSV files from data folder into SQLite tables"""
        csv_files = Path(self.data_folder).glob("*.csv")
        
        for csv_file in csv_files:
            table_name = csv_file.stem  # filename without extension
            df = pd.read_csv(csv_file)
            
            # Store DataFrame
            self.tables[table_name] = df
            
            # Load into SQLite
            df.to_sql(table_name, self.conn, if_exists="replace", index=False)
            
            # Store schema info
            self.schema_info[table_name] = {
                "columns": list(df.columns),
                "dtypes": df.dtypes.to_dict(),
                "row_count": len(df),
                "sample": df.head(3).to_dict(orient='records')
            }
            
        return self.tables
    
    def get_table_names(self) -> List[str]:
        """Get list of all table names"""
        return list(self.tables.keys())
    
    def get_schema_info(self) -> Dict:
        """Get schema information for all tables"""
        return self.schema_info
    
    def execute_query(self, sql_query: str) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame"""
        try:
            result = pd.read_sql_query(sql_query, self.conn)
            return result
        except Exception as e:
            raise Exception(f"Query execution error: {str(e)}")
    
    def validate_sql(self, sql_query: str) -> tuple[bool, str]:
        """
        Validate SQL query for safety
        Returns: (is_valid, error_message)
        """
        sql_lower = sql_query.lower().strip()
        
        # Dangerous commands
        dangerous_keywords = [
            'drop', 'delete', 'insert', 'update', 
            'alter', 'create', 'truncate', 'exec',
            'execute', 'grant', 'revoke'
        ]
        
        for keyword in dangerous_keywords:
            if keyword in sql_lower:
                return False, f"Dangerous SQL keyword detected: {keyword}"
        
        # Must start with SELECT
        if not sql_lower.startswith('select'):
            return False, "Only SELECT queries are allowed"
        
        return True, ""
    
    def get_schema_description(self) -> str:
        """Get human-readable schema description for LLM context"""
        description = "Available tables and their schemas:\n\n"
        
        for table_name, info in self.schema_info.items():
            description += f"Table: {table_name}\n"
            description += f"Columns: {', '.join(info['columns'])}\n"
            description += f"Row count: {info['row_count']}\n"
            
            # Add data types
            description += "Data types:\n"
            for col, dtype in info['dtypes'].items():
                description += f"  - {col}: {dtype}\n"
            
            # Add sample data
            description += f"Sample data (first 3 rows):\n"
            for i, row in enumerate(info['sample'], 1):
                description += f"  Row {i}: {row}\n"
            
            description += "\n"
        
        return description
    
    def close(self):
        """Close database connection"""
        self.conn.close()

