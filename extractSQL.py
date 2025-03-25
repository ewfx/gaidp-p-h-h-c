import re
import duckdb
from configuration.config import CONFIG

def extractSQL(content):
    # Regex pattern to extract SQL queries
    sql_pattern = r"(SELECT\b.*?;)"
    queries = re.findall(sql_pattern, content, re.DOTALL | re.IGNORECASE)

    # Display the extracted SQL queries
    # print("\n--- Extracted SQL Queries ---\n")
    # for i, query in enumerate(queries, 1):
    #     print(f"Query {i}:\n{query}\n")
    return queries


def flagTransactions(queries = []):

    queries = ['SELECT * FROM H1 WHERE LoanAmount > 10000000;', 'SELECT * FROM H1 WHERE PastDue > 90;', "SELECT * FROM H1 WHERE LoanPurpose = 'Unclassified' OR LoanPurpose = 'Other';", 'SELECT * FROM H1 WHERE ObligorInternalRiskRating IN (SELECT ObligorInternalRiskRating FROM H1 ORDER BY ObligorInternalRiskRating ASC LIMIT 2);', "SELECT * FROM H1 WHERE LoanOriginationDate >= DATE('now', '-3 months');", 'SELECT * FROM H1 WHERE ABS(OriginalLoanAmount - LoanAmount) / OriginalLoanAmount > 0.2;', 'SELECT h1.* FROM H1 h1 JOIN H1_Prior hp ON h1.LoanNumber = hp.LoanNumber WHERE h1.CommittedExposureGlobal / hp.CommittedExposureGlobal > 1.2;', "SELECT * FROM H1 WHERE LoanMaturityDate <= DATE('now', '+12 months');", "SELECT * FROM H1 WHERE GuarantorCreditRating IS NULL OR GuarantorCreditRating < 'Investment Grade';", 'SELECT * FROM H1 WHERE CollateralValue < LoanAmount;', 'SELECT * FROM H1 WHERE (LoanAmount / CollateralValue) > 1;', 'SELECT * FROM H1 WHERE DSCR < 1;', 'SELECT * FROM H1 h1 JOIN H1_Prior hp ON h1.LoanNumber = hp.LoanNumber WHERE ABS(h1.ObligorRevenue - hp.ObligorRevenue)/hp.ObligorRevenue > 0.2;', 'SELECT * FROM H1 WHERE ObligorLEI IS NULL OR LENGTH(ObligorLEI) != 20;', "SELECT h1.* FROM H1 h1 JOIN H1_Prior hp ON h1.LoanNumber = hp.LoanNumber WHERE h1.LoanStatus IN ('Non-Accrual', 'Default') AND hp.LoanStatus NOT IN ('Non-Accrual', 'Default');", 'SELECT * FROM H1 WHERE NumberOfModifications > 3;', 'SELECT * FROM H1 WHERE ABS(FairValue - OutstandingBalance) / OutstandingBalance > 0.1;', 'SELECT ObligorName, COUNT(*) AS LoanCount FROM H1 GROUP BY ObligorName HAVING LoanCount > (SELECT AVG(LoanCount) FROM (SELECT ObligorName, COUNT(*) as LoanCount FROM H1 GROUP BY ObligorName));', 'SELECT h1.* FROM H1 h1 JOIN H1_Prior hp ON h1.LoanNumber = hp.LoanNumber WHERE h1.ObligorInternalRiskRating < hp.ObligorInternalRiskRating;', 'SELECT * FROM H1 WHERE ProbabilityOfDefault > 0.05;', "SELECT * FROM H1 WHERE AmortizationType IN ('None', 'Interest Only') AND LoanTerm > 365;", 'SELECT * FROM H1 WHERE LoanAmount IS NULL OR LoanOriginationDate IS NULL;', 'SELECT * FROM H1 WHERE LoanAmount > 10000000;', 'SELECT * FROM H1 WHERE PastDue > 90;', "SELECT * FROM H1 WHERE LoanPurpose IN ('Unclassified', 'Other');", 'SELECT * FROM H1 WHERE ObligorInternalRiskRating IN (SELECT ObligorInternalRiskRating FROM H1 ORDER BY ObligorInternalRiskRating ASC LIMIT 2);', "SELECT * FROM H1 WHERE LoanOriginationDate >= DATE('now', '-3 months');", 'SELECT * FROM H1 WHERE ABS(OriginalLoanAmount - LoanAmount) / OriginalLoanAmount > 0.2;', 'SELECT h1.* FROM H1 h1 JOIN H1_Prior hp ON h1.LoanNumber = hp.LoanNumber WHERE (h1.CommittedBalance - hp.CommittedBalance) / hp.CommittedBalance > 0.2;', "SELECT * FROM H1 WHERE LoanMaturityDate <= DATE('now', '+12 months');", 'SELECT * FROM H1 WHERE GuarantorCreditRating IS NULL OR GuarantorCreditRating < 5;', 'SELECT * FROM H1 WHERE Value < LoanAmount;', 'SELECT * FROM H1 WHERE (LoanAmount / Value) > 1;', 'SELECT * FROM H1 WHERE DSCR < 1;', 'SELECT h1.* FROM H1 h1 JOIN H1_Prior hp ON h1.InternalObligorID = hp.InternalObligorID WHERE ABS(h1.NetSalesCurrent - hp.NetSalesCurrent) / hp.NetSalesCurrent > 0.2;', 'SELECT h1.* FROM H1 h1 JOIN HighRiskIndustries hri ON h1.Industry = hri.Industry;', 'SELECT h1.* FROM H1 h1 JOIN HighRiskLocations hrl ON h1.ObligorLocation = hrl.Location;', "SELECT * FROM H1 WHERE CollateralType IN ('Intangible', 'Volatile Asset');", "SELECT * FROM H1 WHERE RepaymentSource = 'Speculative';", "SELECT * FROM H1 WHERE DocumentationCompleteness = 'Incomplete';", 'SELECT * FROM H1 WHERE ObligorLEI IS NULL OR LENGTH(ObligorLEI) != 20;', "SELECT h1.* FROM H1 h1 JOIN H1_Prior hp ON h1.LoanNumber = hp.LoanNumber WHERE h1.NonAccrualDate <> '9999-12-31' AND hp.NonAccrualDate = '9999-12-31';", 'SELECT * FROM H1 WHERE NumberOfModifications > 3;', 'SELECT * FROM H1 WHERE ABS(OutstandingBalanceFairValue - OutstandingBalance) / OutstandingBalance > 0.1;', 'SELECT ObligorName, COUNT(*) AS LoanCount FROM H1 GROUP BY ObligorName HAVING LoanCount > 5;', 'SELECT * FROM H1 WHERE ProbabilityOfDefault > 0.05;', "SELECT * FROM H1 WHERE AmortizationType IN ('None', 'Interest Only') AND MaturityDate > DATE('now', '+3 years');", 'SELECT * FROM H1 WHERE LoanAmount IS NULL OR LoanOriginationDate IS NULL;']
    # Path to your CSV file
    csv_file = CONFIG["DATA_FILE_PATH"]

    # SQL query to find rows where 'ObligorName' contains 'Jones'
    # query = f"""
    #     SELECT *
    #     FROM '{csv_file}'
    #     WHERE ObligorName ILIKE '%Jones%'
    # """
    modified_queries = [query.replace("H1", f"'{csv_file}'") for query in queries]
    # queries = [f"""SELECT * FROM '{csv_file}' WHERE ObligorName ILIKE '%Jones%'""", f"""SELECT * FROM '{csv_file}' WHERE ObligorName ILIKE '%Jones%'"""]
    # print(query)
    # Run the query and convert the result to a DataFrame
    # result = duckdb.query(query).to_df()
    results = []
    for query in modified_queries:
        try:
            results.append(duckdb.query(query).to_df())
        except Exception as e:
            print(f"Error in query {query}: Error: {e}")

    # Display the result
    return results

print(flagTransactions())