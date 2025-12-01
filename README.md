# EnlitenAI - Medical Data Query System

<div align="center">

**Decision Support Software Platform for Neurological Care**

*Transforming passive monitoring into proactive, personalized intervention*

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.31.0-FF4B4B.svg)](https://streamlit.io)

[Website](https://enlitenai.com/) • [Documentation](#documentation) • [Quick Start](#quick-start)

</div>

---

## 🎯 Overview

An AI-powered voice-enabled platform that allows physicians to query patient data using natural language. Built for seizure management and neurological care, the system converts natural language questions to SQL, executes queries on medical data, and provides both visual results and audio responses.

### Key Features

- 🗣️ **Voice Input** - Speak your queries using microphone
- 💬 **Natural Language Processing** - Ask questions in plain English
- 🔊 **Text-to-Speech** - Hear the answers spoken back
- 🤖 **Multi-LLM Support** - OpenAI GPT-4 or Google Gemini for intelligent SQL generation
- 🔒 **Safe Queries** - Validates SQL to prevent dangerous operations
- 📊 **Rich Visualizations** - View results in tables with download options
- 📝 **Query History** - Track all your queries and results
- 🎯 **Medical Context** - Optimized for patient data queries

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- **API Key** (choose one or both):
  - [OpenAI API key](https://platform.openai.com/) (for GPT-4 + voice features)
  - [Google Gemini API key](https://makersuite.google.com/app/apikey) (for Gemini text-to-SQL only)
- Microphone (for voice input, requires OpenAI)

### Installation

```bash
# 1. Navigate to project directory
cd /path/to/enliten-text-sql

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
./run.sh
# Or directly: streamlit run app.py

# 5. Configure API keys in the UI
# Open the app and enter your API keys in the sidebar
```

### Configuration Options

Configure your API keys directly in the application sidebar when you launch it.

**Option A: OpenAI (Full Features)**
- Select "openai" as provider
- Enter your OpenAI API key
- ✅ Text-to-SQL ✅ Voice Input ✅ Voice Output

**Option B: Gemini (Cost-Effective)**
- Select "gemini" as provider
- Enter your Gemini API key
- ✅ Text-to-SQL ❌ Voice Features  
- 💰 FREE tier: 1,500 requests/day

**Option C: Hybrid (Recommended)**
- Select "gemini" as provider
- Enter your Gemini API key (for Text-to-SQL)
- Optionally: Add OpenAI API key in the expandable section (for voice features)
- ✅ Text-to-SQL (via Gemini - cheap) ✅ Voice features (via OpenAI)

---

## 📊 Data Schema

### Tables

**assessments_dummy**
- Patient assessments: QoL, Anxiety, Depression, Behavioral scores
- 227 rows per patient, daily measurements

**medications_dummy**
- Daily medication dosages: Med A, B, C, D, E
- 365 rows per patient, one year of data

**seizures_dummy**
- Seizure tracking: daily_total, daily_severe counts
- 365 rows per patient, daily records

---

## 💡 Example Queries

### Patient-Specific
```
What is the average QoL score for patient P001?
Show me all seizure events for patient P002 in the last month
List all assessments for patient P003
```

### Comparative Analysis
```
Which patients had the highest anxiety scores?
Compare medication dosages between patients P001 and P003
Show me patients with QoL scores below 50
```

### Trend Analysis
```
Show me the trend of behavioral scores for patient P004
What's the correlation between medication Med A dosage and seizure frequency?
```

### Statistical Queries
```
What is the average number of seizures per patient?
How many severe seizures did patient P005 have in total?
```

---

## 🛠️ Technology Stack

### Core
- **Streamlit** - Web framework
- **Pandas** - Data processing
- **SQLite3** - In-memory database

### AI/ML
- **OpenAI GPT-4** - Text-to-SQL conversion
- **Google Gemini 2.0 Flash** - Alternative LLM provider
- **OpenAI Whisper** - Speech recognition (optional)
- **OpenAI TTS** - Text-to-speech (optional)

### Additional
- **python-dotenv** - Environment management
- **sqlparse** - SQL formatting
- **pydub** - Audio processing

---

## 📁 Project Structure

```
enliten-text-sql/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── run.sh                      # Automated startup script
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
├── assets/                     # Static assets
│   └── logo.png                # EnlitenAI logo
├── data/                       # CSV data files
│   ├── assessments_dummy.csv   # Patient assessments
│   ├── medications_dummy.csv   # Medication dosages
│   └── seizures_dummy.csv      # Seizure tracking
└── utils/                      # Utility modules
    ├── db.py                   # Database management
    ├── llm.py                  # LLM integration (OpenAI/Gemini)
    ├── voice.py                # Voice I/O
    └── ui.py                   # UI helpers
```

---

## 🎨 Features

### Three Query Modes

1. **Text Input** - Type natural language questions
2. **Voice Input** - Speak your questions (requires OpenAI)
3. **Direct SQL** - Write SQL queries directly

### User Interface

- Clean, professional design
- Responsive layout
- Real-time query results
- Query history tracking
- Schema browser
- Export results to CSV

### Security

- SQL sanitization (SELECT only)
- Input validation
- API keys entered securely in the UI (password-protected input fields)
- Read-only database access
- API keys stored only in session state (not persisted)

---

## 💰 Cost Comparison

| Provider | Text Query | Voice Query | 50 queries/mo | 500 queries/mo |
|----------|------------|-------------|---------------|----------------|
| OpenAI Only | $0.01-0.03 | $0.02-0.04 | $1-2 | $10-20 |
| Gemini + OpenAI | $0.001 | $0.005-0.01 | $0.25-0.50 | $2.50-5 |
| Gemini Only | $0.00 (free) | N/A | $0 | $0.50-1 |

---

## 🔧 Troubleshooting

### "API key not found" or "Please enter your API key"
- Make sure you entered your API key in the sidebar
- Verify you selected the correct provider (OpenAI or Gemini)
- Check that the API key is valid and has available credits
- The key is stored in session state and needs to be re-entered each time you start the app

### "Voice features not working"
- Voice requires OpenAI API key
- If using Gemini, expand the "Voice Features (Optional)" section in the sidebar
- Enter your OpenAI API key to enable voice input/output
- Or use text-only mode with Gemini

### Database loading errors
```bash
# Verify CSV files exist
ls -la data/*.csv

# Check file permissions
chmod 644 data/*.csv
```

---

## 📖 Documentation

### Getting API Keys

**OpenAI:**
1. Visit https://platform.openai.com/
2. Sign up or log in
3. Navigate to https://platform.openai.com/api-keys
4. Create new secret key
5. Add $5-10 credit to your account

**Google Gemini:**
1. Visit https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key (free tier: 1,500 requests/day)

### Running the Application

```bash
# Automated startup (recommended)
./run.sh

# Direct startup
streamlit run app.py

# With specific port
streamlit run app.py --server.port 8501
```

### API Configuration

API keys are now configured directly in the application UI:

1. Launch the application
2. Look for the **🔑 API Configuration** section in the sidebar
3. Select your preferred provider (OpenAI or Gemini)
4. Enter your API key in the password-protected field
5. For Gemini users: Optionally add OpenAI key for voice features

**Note:** API keys are stored only in the session and need to be entered each time you start the app. They are never saved to disk or transmitted anywhere except to the respective AI providers.

---

## 👥 About EnlitenAI

EnlitenAI is a decision support software platform for the treatment of neurological and neurobehavioral disorders. Founded by Dr. Himanshu Misra as a tribute to his son lost to drug-resistant epilepsy, EnlitenAI combines 20+ years of lived experience with expertise in computational sciences and digital technologies.

### Our Vision

Deliver precision neurological and neurobehavioral care by transforming passive monitoring into proactive, personalized intervention – powered by a device-agnostic, context-aware AI platform.

### Platform Capabilities

- Seizure management for epilepsy
- Autism spectrum disorder support
- PTSD, anxiety, and depression tracking
- Parkinson's disease monitoring
- Device-agnostic data integration
- FDA-cleared wearables and implantables support

[Learn more at enlitenai.com](https://enlitenai.com/)

---

## 📞 Contact

- **General Enquiries:** info@enlitenai.com
- **Careers:** career@enlitenai.com
- **Investment/Partnership:** himanshu@enlitenai.com
- **Phone:** (408) 483-1742

---

## 📄 License

© 2025 EnlitenAI | All Rights Reserved

---

<div align="center">

**Built with ❤️ for better neurological care**

[EnlitenAI Website](https://enlitenai.com/) • [Documentation](#documentation) • [Support](mailto:info@enlitenai.com)

</div>
