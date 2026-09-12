# 🔐 PRESIDIO PII Detection & De-identification System

> A professional Streamlit application for detecting, analyzing, and
> de-identifying Personally Identifiable Information (PII) using
> Microsoft Presidio.
> Here is the Live Preview : https://supriya-presidio.streamlit.app/

## Overview

**PRESIDIO: PII Detection** provides a simple interface for
privacy-aware data processing. Users can upload files or enter text,
detect sensitive information, review confidence scores and analysis
explanations, apply a de-identification technique, and download the
protected output.

### Core workflow

**Input → PII Detection → Confidence Threshold → Findings & Analysis →
De-identification → Protected Output → Download**

## Key Features

-   PII detection using Microsoft Presidio Analyzer
-   spaCy and Stanza NLP model selection
-   Configurable acceptance threshold
-   Replace, redact, mask, and hash de-identification
-   Structured data processing for CSV and Excel
-   Unstructured processing for TXT, PDF, DOCX, JSON, and XML
-   Detection findings with entity, detected text, position, and
    confidence score
-   Analysis explanations from Presidio recognizers
-   Preview of original and protected data
-   Downloadable protected output

## Supported Input Types

  Input   Processing                     Typical Output
  ------- ------------------------------ -------------------------------
  TXT     Text extraction and analysis   Protected text
  PDF     Text extraction and analysis   Protected text
  DOCX    Text extraction and analysis   Protected text
  CSV     Cell-by-cell analysis          Protected CSV/structured data
  XLSX    Cell-by-cell analysis          Protected Excel
  JSON    JSON text analysis             Protected JSON
  XML     XML text analysis              Protected XML/text

## NLP Models

### spaCy

Configured model:

``` text
spaCy/en_core_web_lg
```

### Stanza

Configured model:

``` text
stanza/en
```

The selected NLP engine can affect entity detection and confidence
scores.

## De-identification

### Replace

Replaces detected entities with their Presidio entity label.

Example:

``` text
Rahul Sharma
```

becomes:

``` text
<PERSON>
```

### Redact

Removes or redacts the detected sensitive value.

### Mask

Replaces sensitive characters with masking characters such as `*`.

### Hash

Transforms the detected value into a hash representation.

> The actual output depends on the Presidio anonymizer operator
> configuration used by the application.

## Acceptance Threshold

The threshold controls the minimum confidence score accepted by the
analyzer.

Typical starting point:

``` text
0.35
```

A lower threshold can increase sensitivity but may also increase false
positives. A higher threshold is more conservative and may miss weaker
detections. Thresholds should be validated using representative test
data.

## Detection Analysis

For each accepted detection, the application can display:

-   Entity type
-   Detected text
-   Start position
-   End position
-   Confidence score
-   Recognizer analysis explanation

For CSV and Excel files, the analysis additionally identifies the
relevant column and row.

## Project Structure

``` text
presidio/
│
├── presidio_streamlit.py
├── presidio_helpers.py
├── presidio_nlp_engine_config.py
├── requirements.txt
├── README.md
│
└── sample_data/
    ├── sample.txt
    ├── sample.json
    ├── sample.xml
    ├── sample.csv
    └── sample.xlsx
```

### Main files

**`presidio_streamlit.py`**\
Contains the Streamlit UI, model selection, input selection, file
upload, processing flow, result display, findings, and download
controls.

**`presidio_helpers.py`**\
Contains file extraction, Presidio analyzer initialization, PII
analysis, anonymization, structured-data processing, and output
generation.

**`presidio_nlp_engine_config.py`**\
Contains spaCy and Stanza NLP engine configuration and Presidio
recognizer registration.

## Installation

### 1. Open the project

Windows:

``` cmd
cd C:\Users\SUPRIYA\Downloads\presidio
```

### 2. Create a virtual environment

``` cmd
python -m venv venv
```

### 3. Activate it

CMD:

``` cmd
venv\Scripts\activate
```

PowerShell:

``` powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

``` cmd
pip install -r requirements.txt
```

Typical dependencies include:

``` text
streamlit
pandas
openpyxl
python-docx
PyPDF2
spacy
stanza
presidio-analyzer
presidio-anonymizer
```

### 5. Install the spaCy model

``` cmd
python -m spacy download en_core_web_lg
```

### 6. Download Stanza English resources

``` cmd
python -c "import stanza; stanza.download('en')"
```

## Run the Application

From the project directory:

``` cmd
streamlit run presidio_streamlit.py
```

If Streamlit is not recognized:

``` cmd
python -m streamlit run presidio_streamlit.py
```

Open the local URL shown in the terminal, normally:

``` text
http://localhost:8501
```

To stop the application:

``` text
Ctrl + C
```

## Example Test Data

``` text
Customer Name: Rahul Sharma
Email: rahul.sharma@example.com
Phone: +91-9000012345
Address: 12 Main Street, Bangalore
IP Address: 192.168.1.25
Credit Card: 4111-1111-1111-1111
```

The exact entities detected depend on the configured recognizers, NLP
model, context, and threshold.

## Architecture

``` text
                    User Input
                        │
             ┌──────────┴──────────┐
             │                     │
        Upload File            Enter Text
             │                     │
             └──────────┬──────────┘
                        │
                 Data Extraction
                        │
                        ▼
               Presidio Analyzer
                        │
                 NLP Engine
              ┌─────────┴─────────┐
              │                   │
            spaCy               Stanza
              │                   │
              └─────────┬─────────┘
                        ▼
                  PII Findings
                        │
                        ▼
              Confidence Threshold
                        │
                        ▼
              Presidio Anonymizer
                        │
          ┌─────────────┼─────────────┐
          │             │             │
       Replace        Redact        Mask/Hash
          │             │             │
          └─────────────┴─────────────┘
                        │
                        ▼
               Protected Output
                        │
             ┌──────────┴──────────┐
             │                     │
          Preview              Download
```

## Security Considerations

This project should be treated as a PII-processing application.

For production use:

-   Do not hard-code encryption or secret keys.
-   Use secure secret management.
-   Avoid logging raw PII.
-   Restrict access to uploaded and generated files.
-   Define retention and deletion policies.
-   Use HTTPS for remote deployment.
-   Validate false positives and false negatives.
-   Test detection using representative datasets.
-   Do not assume that undetected data is automatically non-sensitive.

## Limitations

PII detection is probabilistic and context-dependent. No automated
detector should be considered a guarantee that every sensitive value has
been found.

Detection quality can vary according to:

-   NLP model
-   Entity type
-   Language
-   Text context
-   Formatting
-   Confidence threshold
-   Recognizer configuration

For production privacy workflows, automated detection should be combined
with validation and appropriate security controls.

## Troubleshooting

### Streamlit command not found

``` cmd
python -m streamlit run presidio_streamlit.py
```

### spaCy model missing

``` cmd
python -m spacy download en_core_web_lg
```

### Stanza resources missing

``` cmd
python -c "import stanza; stanza.download('en')"
```

### Port 8501 already in use

``` cmd
streamlit run presidio_streamlit.py --server.port 8502
```

### ModuleNotFoundError

Activate the environment first:

``` cmd
venv\Scripts\activate
```

Then install the required package:

``` cmd
pip install <package-name>
```

## Technology Stack

  Technology                      Purpose
  ------------------------------- ----------------------------
  Python                          Application development
  Streamlit                       Web interface
  Microsoft Presidio Analyzer     PII detection
  Microsoft Presidio Anonymizer   De-identification
  spaCy                           NLP processing
  Stanza                          NLP processing
  Pandas                          Structured data processing
  OpenPyXL                        Excel processing
  PyPDF2                          PDF text extraction
  python-docx                     DOCX extraction

## Project Objective

The project demonstrates a practical privacy engineering workflow:

**Detect sensitive information → evaluate confidence → explain findings
→ de-identify data → generate protected output.**

It can be used as a foundation for privacy-aware data processing, PII
testing, demonstrations, and future integration with enterprise data
pipelines.

## Future Enhancements

Potential extensions include:

-   Custom Presidio recognizers
-   Additional languages
-   Custom PII entity types
-   Batch processing
-   Database scanning
-   REST API integration
-   Authentication and authorization
-   Audit reports
-   PII risk scoring
-   Dashboard analytics
-   Custom masking policies
-   Enterprise data pipeline integration

## Project Status

-   ✅ Streamlit UI
-   ✅ spaCy integration
-   ✅ Stanza integration
-   ✅ Structured data processing
-   ✅ Unstructured data processing
-   ✅ Multiple de-identification techniques
-   ✅ Confidence threshold
-   ✅ Detection findings
-   ✅ Analysis explanations
-   ✅ Downloadable protected output

------------------------------------------------------------------------

### 🔐 Detect. Analyze. Protect.

**PRESIDIO: PII Detection & De-identification System**

Built with Python, Streamlit, and Microsoft Presidio.
