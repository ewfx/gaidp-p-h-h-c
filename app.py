import streamlit as st

# Specify the path to your logo image
image_path = "WF_Logo.png"

# Display the logo in the top bar
st.logo(image_path, size = "large")

# Add some content to your app
st.title("Gen AI-Based Data Profiling", anchor="title")

def getRules():
    numRules = 50
    rulesList = [f"Rule {i}" for i in range(1, numRules)]
    return rulesList

# ------------------------------Upload Goes here--------------------------------
uploadContainer = st.container()

# uploadForm = uploadContainer.form(key="uploadForm")
instrucDoc = uploadContainer.file_uploader("Upload your Compliance instructions document", type=["pdf"])
reportingDataFile = uploadContainer.file_uploader("Upload the reporting data", type=["csv", "xlsx"])
uploadButton = uploadContainer.button("Upload")




# ------------------------------Generate Goes here--------------------------------
generateContainer = st.container()
generateContainer.header("Rules Section")
generateContainer.subheader("Generate Rules")
# col1, col2 = generateContainer.columns(2)
# col1.header("Rules Generated")
# col2.header("Refine Rules")
rulesWindow = generateContainer.container(height=300)


generateContainer.subheader("Refine Rules")
chatWindow = generateContainer.container()
rulesList = getRules()
for rule in rulesList:
    rulesWindow.checkbox(rule, key=rule)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with chatWindow.chat_message(message["role"]):
        chatWindow.markdown(message["content"])

# User input
if user_input := chatWindow.chat_input("Say something..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with chatWindow.chat_message("user"):
        chatWindow.markdown(user_input)

    # Simulate AI response
    response = f"You said: {user_input}"
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Display assistant message
    with chatWindow.chat_message("assistant"):
        chatWindow.markdown(response)



