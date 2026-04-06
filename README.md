# 💊 MedQuery AI — Drug Information Chatbot
> An AI-powered drug information assistant built on the FDA's OpenFDA API and Anthropic's Claude
 
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Claude](https://img.shields.io/badge/AI-Claude%20Haiku-purple)
![FDA](https://img.shields.io/badge/Data-OpenFDA%20API-red)
 
---
 
## 📌 Overview
 
MedQuery AI is a conversational drug information assistant that allows users to ask natural language questions about medications and receive accurate, plain-English answers sourced directly from the FDA's drug label database. The system intelligently classifies user questions to fetch only the relevant data fields, minimizing API costs while maximizing response quality.
 
**Example queries the system can handle:**
- *"What is metformin used for?"*
- *"What are the risks of taking ibuprofen?"*
- *"Is amoxicillin safe during pregnancy?"*
- *"What are the side effects of lisinopril?"*
 
---
 
## 🏗️ Architecture
 
```
User Question
      ↓
 Claude (Classify)          ← Is this general or specific?
      ↓
 OpenFDA API Call           ← Fetch only the relevant fields
      ↓
 Claude (Summarize)         ← Synthesize into plain English
      ↓
 Answer returned to user
```
 
### Two-Query Modes
 
| Mode | Trigger | Fields Fetched | Cost |
|------|---------|----------------|------|
| **General Inquiry** | "Tell me about X" | All 4 MVP fields | Moderate |
| **Specific Query** | "What are the risks of X?" | Targeted fields only | Low |
 
---
 
## ✅ What's Been Built (Notebook Prototype)
 
### 1. OpenFDA API Integration
- Successfully connected to the [OpenFDA Drug Label endpoint](https://api.fda.gov/drug/label.json)
- Queried drugs by generic name using the `openfda.generic_name` field
- Parsed JSON responses into a Pandas DataFrame (38 columns returned per drug)
- Identified and selected the most relevant MVP columns
 
### 2. Data Extraction & Cleaning
- Identified all 38 available columns from the FDA drug label dataset
- Selected 4 MVP columns for the initial prototype:
  ```python
  MVP_COLUMNS = [
      'indications_and_usage',    # What the drug treats
      'warnings_and_cautions',    # Important safety warnings
      'adverse_reactions',        # Side effects
      'pregnancy'                 # Pregnancy safety
  ]
  ```
- Converted DataFrame rows into clean, structured strings for LLM consumption
- Reduced raw data from ~75,000 characters to ~6,000 characters through targeted field selection
 
### 3. Question Classification System
- Built a Claude-powered classifier using a structured system prompt
- Classifier determines whether a user question is:
  - A **general inquiry** → fetch all MVP fields
  - A **specific question** → return a JSON array of relevant fields only
- Output is structured JSON for reliable programmatic parsing
- Uses **Claude Haiku** for cost-efficient classification
 
### 4. Drug Summarization
- Built a `summarize()` function that sends FDA data + user question to Claude
- Claude returns a plain-English answer based strictly on FDA data
- Includes a medical disclaimer in every response
 
### Core Functions Built
```
classify_question(question)     → Identifies relevant FDA fields
fda_api_call(drug_name, fields) → Fetches targeted FDA data
summarize(question, drug_data)  → Generates plain-English answer
```
 
---
 
## 🛠️ Tech Stack
 
| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| AI Model | Anthropic Claude (Haiku for classification, Haiku for summarization) |
| Drug Data | OpenFDA Drug Label API (free, no auth required) |
| Data Processing | Pandas |
| HTTP Requests | Requests |
| Notebook | Jupyter |
