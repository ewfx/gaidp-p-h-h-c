import streamlit as st
import os
from configuration.config import CONFIG
from extractRulesSQL import extract_rules_sql, flagTransactions


# Specify the path to your logo image
image_path = "WF_Logo.png"

# Display the logo in the top bar
st.logo(image_path, size = "large")

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
    uploadContainer.header("Upload Compliance Instructions and Reporting Data")

    # Form to upload files
    instrucDoc = uploadContainer.file_uploader("Upload your Compliance instructions document", type=["pdf"])
    reportingDataFile = uploadContainer.file_uploader("Upload the reporting data", type=["csv"])
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
    generateContainer.subheader("Generated Rules form the Compliance Instructions")
    rulesWindow = generateContainer.container(height=500)
    # rawRules = model()
    # rulesList = rawRules.split("\n")
    # rulesList = ['1.  Loan Amount > $10,000,000 and Internal Risk Rating in bottom two risk grades.', '2.  Past Due > 90 days and Outstanding Balance Fair Value < 50% of Original Loan Amount.', '3.  Guarantor LEI missing and Loan Amount > $5,000,000.', '4.  Purpose of Loan = "Unclassified" and Loan Amount > $1,000,000.', '5.  Country of Incorporation = High-Risk Jurisdiction and Loan Amount > $2,500,000.', '6.  Significant increase in Outstanding Balance Fair Value in a short period.', '7.  NAICS Code in a high-risk industry and Loan Amount > $5,000,000.', "8.  Borrower's Total Assets < $10,000,000 and Loan Amount > $1,000,000.", "9.  Borrower's Total Liabilities / Total Assets > 0.8 and Loan Amount > $2,500,000.", "10. Borrower's Net Income < 0 for the last two reporting periods and Loan Amount > $1,000,000.", '11. Loan Original Maturity Date within the next 12 months and no refinancing plan.', '12.  Collateral Type = "Intangible Assets" and Loan Amount > $5,000,000.', '13.  Loan Syndicated Flag = "Yes" and Lead Lender LEI missing.', '14.  Number of Lenders > 10 and Loan Amount > $25,000,000.', '15.  Loan Purpose = "Leveraged Buyout" and Loan Amount > $10,000,000.', '16.  Loan Type = "Commercial Real Estate" and LTV Ratio > 0.9.', "17.  Borrower's Debt Service Coverage Ratio < 1.0 and Loan Amount > $2,500,000.", "18.  Significant change in Borrower's NAICS Code.", '19.  Missing or invalid Obligor LEI for Loan Amount > $1,000,000.', '20.  Line of Business = "Unclassified" and Loan Amount > $1,000,000.', '21.  PD Calculation Method = "Point in Time" and Maximum Probability of Default > 0.1.', '22.  Internal Risk Rating changed significantly in a short period.', '23.  Loan Secured Flag = "No" and Loan Amount > $5,000,000.', "24.  Guarantor's Total Assets < $5,000,000 and Loan Amount > $1,000,000.", '25.  Missing or invalid Guarantor LEI for Loan Amount > $1,000,000.', '26.  Significant change in Outstanding Balance Amount in a short period.', '27.  Outstanding Balance Amount = 0 and Loan Status = "Active".', '28.  Loan Original Maturity Date in the past.', '29.  Combination of high LTV ratio and low Debt Service Coverage Ratio.', '30.  Multiple loans to the same obligor with aggregate exposure exceeding a defined threshold.']

    rulesSQLList = extract_rules_sql()

    for item in rulesSQLList:
        rule_container = rulesWindow.container(border=True)
        rule_container.markdown(item["rule"])
        # rule_container.divider()
    evaluateButton = generateContainer.button("Generate formulas from rules", type = "secondary", use_container_width=True)
    if(evaluateButton):
        next_page("evaluate")
        generateContainer.button("Evaluate Data", type="primary", use_container_width=True)
        # st.rerun()
    cancelButton = generateContainer.button("Cancel", type = "tertiary", use_container_width=True)
    if(cancelButton):
        next_page("upload")
        st.rerun()
elif st.session_state.page == "evaluate":
    # Create a container for generating rules
    evaluateContainer = st.container()
    evaluateContainer.subheader("Evaluate Data")
    evaluateContainer.write("Flagged transactions due to rules are as following:")
    rulesSQLList = extract_rules_sql()
    flaggedTr, rules_linked = flagTransactions(rulesSQLList)
    print("Hello")
    for i, tr in enumerate(flaggedTr):
        with st.expander(f"Rule {i+1}: {rules_linked[i]}"):
            st.dataframe(tr)

    homeButton = st.button("Home", use_container_width=True)
    if(homeButton):
        next_page("upload")
        st.rerun()
