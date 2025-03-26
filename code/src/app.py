import streamlit as st
import os
from configuration.config import CONFIG
from extractRulesSQL import extract_rules_sql, flagTransactions
from model import model
import pandas as pd


# Add some content to your app
st.title("Gen AI-Based Data Profiling", anchor="title")


# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "upload"

if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

files_upload_flag = False
generate_rules_flag = False
evaluate_data_flag = False

# Navigation function
def next_page(page_name):
    st.session_state.page = page_name
    st.session_state.form_submitted = False  # Reset form submission flag

def getRules():
    numRules = 50
    rulesList = [f"Rule {i}" for i in range(1, numRules)]
    return rulesList

if st.session_state.page == "upload":
    # Create a container
    uploadContainer = st.container(border=True)
    uploadContainer.header("Upload Regulatory Reporting Instructions and Reported Data")

    # Form to upload files
    instrucDoc = uploadContainer.file_uploader("Upload Regulatory Reporting instructions document", type=["pdf"])
    reportingDataFile = uploadContainer.file_uploader("Upload the reported data", type=["csv"])
    submit_button = uploadContainer.button("Upload", use_container_width=True)

    # Initialize dictionary to store file names
    file_names = {}

    # Only process when the form is submitted and both files are uploaded
    if submit_button:
        if instrucDoc is None or reportingDataFile is None:
            st.error("Please upload both files before submitting.")
        else:
            # Create the directory if it doesn't exist
            os.makedirs(CONFIG["DATA_DIR"], exist_ok=True)

            instruc_path = CONFIG["COMPLIANCE_DOC_FILE_PATH"]
            reporting_path = CONFIG["DATA_FILE_PATH"]

            with open(instruc_path, "wb") as f:
                f.write(instrucDoc.getbuffer())

            with open(reporting_path, "wb") as f:
                f.write(reportingDataFile.getbuffer())

            st.success("Files uploaded successfully!")
            st.session_state.form_submitted = True

            # Immediately move to the next page after successful form submission
            if st.session_state.form_submitted:
                next_page("generate")
            generateButton = uploadContainer.button("Generate Rules", type="primary", use_container_width=True)

elif st.session_state.page == "generate":
    # Create a container for generating rules
    generateContainer = st.container()    
    generateContainer.subheader("Generated Rules form the regulatory instructions")
    rulesWindow = generateContainer.container(height=500)


    if not os.path.isfile(CONFIG["GENERATED_SQL_PATH"]):
        model()

    rulesSQLList = extract_rules_sql()

    for i, item in enumerate(rulesSQLList):
        rule_container = rulesWindow.container(border=True)
        rule_container.markdown(f"{i+1}. " + item["rule"])
    evaluateButton = generateContainer.button("Generate formulas from rules", type = "secondary", use_container_width=True)
    if(evaluateButton):
        next_page("evaluate")
        generateContainer.button("Evaluate Data", type="primary", use_container_width=True)
    exportRulesButton = generateContainer.button("Export Rules", type="secondary", use_container_width=True)
    if(exportRulesButton):
        output_file = CONFIG["GENERATED_RULES_REPORT_PATH"]
        with open(output_file, 'w') as f:
            for i, item in enumerate(rulesSQLList):
                f.write(f"{i+1}. {item['rule']}\n{item['query']}\n\n")
        generateContainer.success("Rules saved successfully!")
    cancelButton = generateContainer.button("Cancel", type = "tertiary", use_container_width=True)
    if(cancelButton):
        next_page("upload")
        st.rerun()
elif st.session_state.page == "evaluate":
    # Create a container for generating rules
    evaluateContainer = st.container()
    evaluateContainer.subheader("Flagged Transactions")
    evaluateContainer.write("Flagged transactions due to voilated rules are as following:")
    rulesSQLList = extract_rules_sql()
    flaggedTr, rules_linked = flagTransactions(rulesSQLList)
    for i, tr in enumerate(flaggedTr):
        with st.expander(f"Rule {i+1}: {rules_linked[i]}"):
            st.dataframe(tr)

    downloadResultsButton = st.button("Download Results", type="primary", use_container_width=True)
    if(downloadResultsButton):
        output_path = CONFIG["EXPORT_RESULTS_PATH"]
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            for i, tr in enumerate(flaggedTr):
                df = pd.DataFrame(tr)
                df.to_excel(writer, sheet_name=f"Rule {i+1}", index=False)
        rulesMappingFileName = CONFIG["RESULT_RULES_MAPPING_PATH"]
        with open(rulesMappingFileName, 'w') as f:
            for i, r1 in enumerate(rules_linked):
                f.write(f"{i+1}. {r1}\n")

        # print(f"List saved to {output_file}")
        st.success("File saved successfully!")


    homeButton = st.button("Home", use_container_width=True)
    if(homeButton):
        next_page("upload")
        st.rerun()


# Specify the Excel file path

    # Use ExcelWriter to save multiple sheets

