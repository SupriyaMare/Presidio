import streamlit as st
import pandas as pd
import io
import json

from presidio_helpers import (
    extract_text_from_file,
    analyze,
    anonymize,
    process_structured_data,
    generate_output_file
)

st.set_page_config(layout="wide")

st.title("🔐 PRESIDIO: PII Detection")

# ================= SIDEBAR =================
model = st.sidebar.selectbox(
    "Model",
    ["spaCy/en_core_web_lg", "stanza/en"]
)

model_family = model.split("/")[0]
model_name = model.split("/")[-1]

operator = st.sidebar.selectbox(
    "De-identification",
    ["replace", "redact", "mask", "hash"]
)

threshold = st.sidebar.slider("Threshold", 0.0, 1.0, 0.35)

# ================= INPUT TYPE =================
st.subheader("Select Input Type")

input_type = st.radio(
    "Choose how you want to provide data:",
    ["Upload File", "Enter Text"],
    index=None,
    key="input_type"
)

st.divider()

col1, col2 = st.columns(2)

uploaded_file = None
text = ""

# ================= FILE INPUT =================
if input_type == "Upload File":

    uploaded_file = st.file_uploader(
        "Upload file",
        type=["csv", "xlsx", "txt", "pdf", "docx", "json", "xml"],
        key="file_uploader"
    )

elif input_type == "Enter Text":

    st.subheader("✍️ Enter Text")
    text = st.text_area("Enter your text", key="user_input_text")

else:
    st.info("👆 Please select an input type to continue")

# ================= RUN BUTTON =================
run = st.button("🚀 Run")

# ================= EXECUTION =================
if run:

    # ================= FILE FLOW =================
    if input_type == "Upload File" and uploaded_file:

        file_type = uploaded_file.name.split(".")[-1].lower()

        # ========= STRUCTURED =========
        if file_type in ["csv", "xlsx"]:

            df = pd.read_excel(uploaded_file) if file_type == "xlsx" else pd.read_csv(uploaded_file)

            st.subheader("📊 Original Data")
            st.dataframe(df, use_container_width=True)

            masked_df, explanations = process_structured_data(
                df,
                model_family,
                model_name,
                operator,
                threshold
            )

            st.subheader("🔒 Masked Data")
            st.dataframe(masked_df, use_container_width=True)

            st.download_button(
                "⬇️ Download Masked Excel",
                data=generate_output_file(masked_df),
                file_name="masked_output.xlsx",
                key="download_excel"
            )

            if explanations:
                st.subheader("🧠 Detection Analysis")
                st.dataframe(pd.DataFrame(explanations), use_container_width=True)

        # ========= JSON =========
        elif file_type == "json":

            text = extract_text_from_file(uploaded_file)

            col1.subheader("Input JSON")
            col1.code(text, language="json")

            results = analyze(text, model_family, model_name, ["All"], threshold)
            output = anonymize(text, results, operator)

            col2.subheader("Masked JSON")
            col2.code(output.text, language="json")

            if results:
                st.subheader("🧠 Detection Analysis")
                st.dataframe(pd.DataFrame([
                    {
                        "Column": "",
                        "Row": "",
                        "Entity": r.entity_type,
                        "Text": text[r.start:r.end],
                        "Score": r.score,
                        "Explanation": str(r.analysis_explanation),
                    }
                    for r in results
                ]), use_container_width=True)

            try:
                json_data = json.loads(output.text)
                json_bytes = json.dumps(json_data, indent=2).encode()
            except:
                json_bytes = output.text.encode()

            st.download_button(
                "⬇️ Download Masked JSON",
                data=json_bytes,
                file_name="masked_output.json",
                mime="application/json",
                key="download_json"
            )

        # ========= OTHER =========
        else:
            text = extract_text_from_file(uploaded_file)

            col1.subheader("Input")
            col1.text_area("Input Text", text, height=300, key="file_input")

            results = analyze(text, model_family, model_name, ["All"], threshold)
            output = anonymize(text, results, operator)

            col2.subheader("Output")
            col2.text_area("Output Text", output.text, height=300, key="file_output")

            if results:
                st.subheader("🧠 Detection Analysis")
                st.dataframe(pd.DataFrame([
                    {
                        "Column": "",
                        "Row": "",
                        "Entity": r.entity_type,
                        "Text": text[r.start:r.end],
                        "Score": r.score,
                        "Explanation": str(r.analysis_explanation),
                    }
                    for r in results
                ]), use_container_width=True)

            st.download_button(
                "⬇️ Download Masked Text",
                data=output.text.encode(),
                file_name="masked_output.txt",
                key="download_text"
            )

    # ================= TEXT FLOW =================
    elif input_type == "Enter Text" and text:

        results = analyze(text, model_family, model_name, ["All"], threshold)
        output = anonymize(text, results, operator)

        col1.subheader("Input")
        col1.text_area("Original Text", text, height=300, key="manual_input")

        col2.subheader("Output")
        col2.text_area("Masked Output", output.text, height=300, key="manual_output")

        if results:
            st.subheader("🧠 Findings")
            st.dataframe(pd.DataFrame([
                {
                    "Column": "",
                    "Row": "",
                    "Entity": r.entity_type,
                    "Text": text[r.start:r.end],
                    "Score": r.score,
                    "Explanation": str(r.analysis_explanation),
                }
                for r in results
            ]), use_container_width=True)

    else:
        st.warning("⚠️ Please provide input before running.")