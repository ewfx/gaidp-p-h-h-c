# 🚀 Gen AI based data profiling rules generation and execution

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#Innovation Behind It)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
In a rapidly evolving financial landscape, ensuring data compliance shouldn't be a bottleneck. Our solution harnesses the power of Generative AI to transform regulatory compliance into an intelligent, automated process. By seamlessly generating data profiling rules, converting them into SQL queries, and flagging non-compliant transactions, we introduce a smarter, faster, and more reliable approach to compliance management.

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](link-to-image)

## 💡 Innovation Behind It
Traditional data profiling relies heavily on manual efforts and human judgment, making it error-prone and time-intensive. Our innovative AI-powered platform automates this by understanding complex regulatory instructions and dynamically generating actionable rules. By fusing advanced AI with financial expertise, we eliminate inefficiencies and enhance decision-making for financial institutions.

## ⚙️ What It Does
- **AI-Driven Rule Generation:** Our Gen AI interprets regulatory instructions to generate comprehensive and accurate data profiling rules.
- **Seamless SQL Conversion:** The generated rules are automatically translated into SQL queries, ready to be executed on reported data.
- **Transaction Intelligence:** Suspicious transactions are identified and flagged with transparent explanations on rule violations.
- **Field-Level Insights:** Generates multiple rules per field, ensuring granular data validation for holistic compliance.
- **Data Security Assurance:** Keeps reported data strictly local while only sending regulatory instructions to the AI model.
- **Rule Mapping for Transparency:** Provides clear, actionable reports linking violations to specific rules.

## 🛠️ How We Built It
Our Tech Innovation
- **LangChain:** AI orchrestration tool that powers intelligent rule generation with Generative AI.
- **AI-Powered SQL Generation:** Generative AI autonomously converts profiling rules into efficient SQL queries for seamless data validation
- **Streamlit:** Delivers a dynamic, responsive user experience with an interactive UI.
- **DuckDB:** Executes SQL queries at lightning speed, handling large datasets effortlessly.

## 🚧 Challenges We Faced
- **Complex Regulatory Interpretation:** Accurately interpreting diverse regulatory instructions and converting them into actionable rules was a key challenge. We implemented adaptive AI fine-tuning to ensure consistent results.
- **Balancing Accuracy and Performance:** Generating detailed rules while maintaining low response times required optimizing both AI inference and SQL execution.
- **Data Validation Complexity:** Ensuring correct flagging of non-compliant transactions required rigorous validation and iterative refinement.
- **Scalability:** Designed the solution to handle large-scale financial data with real-time query execution using DuckDB's high-performance capabilities.
- **User-Friendly Experience:** Simplified the UI using Streamlit, ensuring users can easily generate, interpret, and act on compliance insights without technical expertise.

## 🏃 How to Run
1. **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```
2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3. **Configure Environment:**
    Create a `.env` file with your Gemini API Key:
    ```env
    GEMINI_API_KEY=<Your_Google_API_Key>
    ```
4. **Launch the App:**
    ```bash
    streamlit run app.py
    ```
5. **Upload Files:**
    - Regulatory instructions (PDF or text)
    - Reported data (CSV or Excel)
6. **Generate Insights:**
    - Click "Generate Rules" to create AI-powered profiling rules.
    - Review SQL queries and execute them.
    - Visualize flagged transactions and rule violations.

## 🛒 Tech Stack
- **Generative AI:** Gemini API via LangChain
- **Frontend:** Streamlit
- **Database:** DuckDB
- **Backend:** Python
- **Deployment:** Streamlit for rapid cloud or local hosting

## 👥 Team
- **Prakhar Agrawal** - [GitHub](https://github.com/prakhar2408) | [LinkedIn](https://www.linkedin.com/in/prakhar-agrawal-7388a61b4/)
- **Teammate 2** - [GitHub](https://github.com/roshanbara) | [LinkedIn](https://www.linkedin.com/in/roshanbara/)

Embrace the future of compliance with AI-driven automation. Let’s build a smarter, safer financial ecosystem together!
