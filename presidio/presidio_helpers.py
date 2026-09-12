import json
import pandas as pd
from docx import Document
import PyPDF2
import xml.etree.ElementTree as ET
import io
import streamlit as st

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

from presidio_nlp_engine_config import (
    create_nlp_engine_with_spacy,
    create_nlp_engine_with_stanza,
)

# ================= FILE EXTRACTION =================
def extract_text_from_file(uploaded_file):
    file_type = uploaded_file.name.split(".")[-1].lower()

    try:
        if file_type == "txt":
            return str(uploaded_file.read(), "utf-8")

        elif file_type == "pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            return " ".join([p.extract_text() or "" for p in reader.pages])

        elif file_type == "docx":
            doc = Document(uploaded_file)
            return "\n".join([p.text for p in doc.paragraphs])

        elif file_type == "json":
            return json.dumps(json.load(uploaded_file), indent=2)

        elif file_type == "xml":
            tree = ET.parse(uploaded_file)
            return ET.tostring(tree.getroot(), encoding="unicode")

        else:
            return "Unsupported file"

    except Exception as e:
        return f"Error: {e}"


# ================= ENGINE =================
@st.cache_resource
def analyzer_engine(model_family, model_path):

    if "spacy" in model_family.lower():
        nlp, reg = create_nlp_engine_with_spacy(model_path)

    elif "stanza" in model_family.lower():
        nlp, reg = create_nlp_engine_with_stanza(model_path)

    else:
        raise ValueError("Unsupported model")

    return AnalyzerEngine(nlp_engine=nlp, registry=reg)


@st.cache_resource
def anonymizer_engine():
    return AnonymizerEngine()


# ================= ANALYZE =================
def analyze(text, model_family, model_path, entities, threshold=0.35):

    engine = analyzer_engine(model_family, model_path)

    return engine.analyze(
        text=text,
        entities=None if "All" in entities else entities,
        language="en",
        score_threshold=threshold,
        return_decision_process=True,
    )


# ================= ANONYMIZE =================
def anonymize(text, results, operator):

    if operator == "mask":
        config = {
            "type": "mask",
            "masking_char": "*",
            "chars_to_mask": 100,
            "from_end": False,
        }

    elif operator == "encrypt":
        config = {"key": "mysecretkey123"}

    elif operator == "hash":
        config = {"hash_type": "sha256"}

    else:
        config = {}

    return anonymizer_engine().anonymize(
        text=text,
        analyzer_results=results,
        operators={"DEFAULT": OperatorConfig(operator, config)},
    )


# ================= STRUCTURED DATA =================
def process_structured_data(df, model_family, model_path, operator, threshold):

    # 🔥 FIX 1: remove empty columns
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # 🔥 FIX 2: convert all to string
    df = df.astype(str)

    masked_df = df.copy()
    explanations = []

    for col in df.columns:
        for i, value in df[col].items():

            if not value or value.lower() == "nan":
                continue

            results = analyze(value, model_family, model_path, ["All"], threshold)

            masked_text = anonymize(value, results, operator).text

            masked_df.at[i, col] = masked_text

            for r in results:
                explanations.append({
                    "Column": col,
                    "Row": i,
                    "Entity": r.entity_type,
                    "Text": value[r.start:r.end],
                    "Score": r.score,
                    "Explanation": str(r.analysis_explanation)
                })

    return masked_df, explanations


# ================= DOWNLOAD =================
def generate_output_file(df):

    output = io.BytesIO()
    df.to_excel(output, index=False)
    return output.getvalue()