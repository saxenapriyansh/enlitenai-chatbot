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
- 🤖 **OpenAI GPT-4** - Intelligent SQL generation with state-of-the-art language model
- 🔒 **Safe Queries** - Validates SQL to prevent dangerous operations
- 📊 **Rich Visualizations** - View results in tables with download options
- 📝 **Query History** - Track all your queries and results
- 🎯 **Medical Context** - Optimized for patient data queries

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- **OpenAI API Key** - [Get it here](https://platform.openai.com/)
- Microphone (for voice input)

### Installation

```bash
# 1. Navigate to project directory
cd /path/to/enliten-text-sql

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API key (choose one method):

# Method A: Streamlit Secrets (Recommended)
mkdir -p .streamlit
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
# Edit .streamlit/secrets.toml and add your OpenAI API key

# Method B: Environment Variable
echo 'OPENAI_API_KEY=your-api-key-here' > .env

# 5. Run the application
./run.sh
# Or directly: streamlit run app.py
```

### Configuration Options

**For Local Development:**
- Create `.streamlit/secrets.toml` from the template
- Or use `.env` file with `OPENAI_API_KEY`

**For Streamlit Cloud:**
1. Go to your app dashboard
2. Click on "⚙️ Settings" → "Secrets"
3. Add:
```toml
OPENAI_API_KEY = "your-api-key-here"
```
4. Click "Save"

**OpenAI (GPT-4 + Voice Features)**
- Uses GPT-4 Turbo for intelligent text-to-SQL conversion
- Whisper for speech-to-text transcription
- OpenAI TTS for natural voice output
- ✅ Text-to-SQL ✅ Voice Input ✅ Voice Output
- 💰 Pay-per-use (~$0.01-0.03 per query)

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
- **OpenAI GPT-4 Turbo** - Text-to-SQL conversion
- **OpenAI Whisper** - Speech recognition
- **OpenAI TTS** - Text-to-speech

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
    ├── llm.py                  # LLM integration (OpenAI GPT-4)
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

## 💰 Cost Estimate

| Usage | Text Query | Voice Query | Monthly Cost |
|-------|------------|-------------|--------------|
| 50 queries/mo | $0.01-0.03 | $0.02-0.04 | $1-2 |
| 500 queries/mo | $0.01-0.03 | $0.02-0.04 | $10-20 |

**Note**: Actual costs depend on:
- Query complexity (affects token usage)
- Voice recording length
- GPT-4 API pricing (check [OpenAI pricing](https://openai.com/pricing))

---

## 🔧 Troubleshooting

### "API key not found"
- Make sure you configured OPENAI_API_KEY in `.streamlit/secrets.toml` or `.env` file
- Check that the API key is valid and has available credits
- For Streamlit Cloud: Verify the secret is saved in App Settings → Secrets

### "Voice features not working"
- Voice requires OpenAI API key with sufficient credits
- Check your OpenAI account has API access enabled
- Ensure microphone permissions are granted in your browser

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

**Getting Your OpenAI API Key:**
1. Visit https://platform.openai.com/
2. Sign up or log in
3. Navigate to https://platform.openai.com/api-keys
4. Create new secret key
5. Add $5-10 credit to your account for API access

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

The application automatically loads your API key from Streamlit secrets or environment variables:

**Local Development:**
- Create `.streamlit/secrets.toml` with your API key, OR
- Create `.env` file with `OPENAI_API_KEY=your-key`

**Streamlit Cloud:**
- Go to App Settings → Secrets
- Add: `OPENAI_API_KEY = "your-key"`

**Note:** API keys are never stored in the codebase or git repository.

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
