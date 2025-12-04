"""
LLM utilities for text-to-SQL conversion and query explanation
Uses OpenAI GPT-4
"""
import os
from typing import Tuple, Optional
from openai import OpenAI


class LLMManager:
    """Manages LLM interactions for text-to-SQL using OpenAI"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize LLM Manager with OpenAI
        
        Args:
            api_key: OpenAI API key. If None, tries to get from environment variable
        """
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4-turbo-preview"
        print(f"✅ Using OpenAI ({self.model})")
    
    def text_to_sql(self, natural_language_query: str, schema_description: str) -> Tuple[str, str]:
        """
        Convert natural language query to SQL
        Returns: (sql_query, explanation)
        """
        system_prompt = f"""You are a medical data SQL expert helping physicians query patient databases.

Database Schema:
{schema_description}

Important Context:
- This is medical/patient data for physicians
- Tables contain: assessments (QoL, Anxiety, Depression, Behavioral scores), medications (Med A-E dosages), seizures (daily_total, daily_severe counts)
- Always use proper SQL syntax for SQLite
- Only generate SELECT queries
- Be precise with column names
- Use appropriate aggregations and filters
- When asked about trends, use date ordering
- When asked about averages or statistics, use aggregate functions

Return ONLY valid SQL query, no explanations in the SQL itself."""

        user_prompt = f"""Convert this natural language query to SQL:
"{natural_language_query}"

Generate a clean SQL query that answers this question."""

        try:
            # Generate SQL using OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )
            sql_query = response.choices[0].message.content.strip()
            
            # Clean up SQL query (remove markdown code blocks if present)
            sql_query = self._clean_sql(sql_query)
            
            # Generate explanation
            explanation = self._generate_explanation(natural_language_query, sql_query)
            
            return sql_query, explanation
            
        except Exception as e:
            raise Exception(f"LLM error: {str(e)}")
    
    def _clean_sql(self, sql_query: str) -> str:
        """Clean SQL query by removing markdown formatting"""
        if sql_query.startswith("```sql"):
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        elif sql_query.startswith("```"):
            sql_query = sql_query.replace("```", "").strip()
        return sql_query
    
    def _generate_explanation(self, question: str, sql_query: str) -> str:
        """Generate human-readable explanation of the SQL query"""
        system_prompt = """You are a helpful medical data assistant. 
Explain SQL queries in simple terms that physicians can understand."""

        user_prompt = f"""The user asked: "{question}"
The generated SQL query is:
{sql_query}

Provide a brief, clear explanation (2-3 sentences) of what this query does."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return "Query explanation unavailable."
    
    def generate_answer(self, question: str, query_result: str) -> str:
        """Generate natural language answer from query results"""
        system_prompt = """You are a medical data assistant helping physicians understand patient data.
Provide clear, concise answers based on the query results.
Use medical terminology appropriately.
Keep responses professional and focused on the data."""

        user_prompt = f"""Question: {question}

Query Results:
{query_result}

Provide a clear, professional answer to the physician's question based on these results."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5,
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return "Unable to generate answer summary."
