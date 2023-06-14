import streamlit as st
import openai

# Initial system message
initial_message = "You are a helpful assistant that teaches a Year 10 student preparing for GCSE in a conversational manner. Always provide step-by-step explanations. Include example code snippet in your responses when it would help to illustrate the concept."

st.title('GCSE Computing Learning Assistant')

# Add a warning at the top of the application
st.warning('**Disclaimer:** This app helps you learn GCSE Computing and sometimes provides code examples. We encourage you to practice these examples in your own environment. However, do not run code that you do not understand, due to potential unforeseen results.')

def main():

    # Input for OpenAI API Key
    st.markdown("<div style='background-color: #ffa500; padding:10px; margin-bottom:10px;'>Input your OpenAI API Key:</div>", unsafe_allow_html=True)
    openai.api_key = st.text_input("", type="password")

    # Define topic contexts
    topic_contexts = {
        'Computational Thinking': "The student is learning about the fundamentals of decomposition, abstraction and algorithmic sequencing, which are the concepts that underpin computing.",
        'Computer Systems': "The student is learning about the hardware and software that work together to create a computer system, with a heavy focus on the CPU – the brain of a computer.",
        'Data Representation': "Students learn about the binary number system, and how it is used to represent all data. They learn how different files such as images or audio files are stored as binary numbers.",
        'Programming Basics': "Students apply the concepts of computing using block-based programming and pseudocode.",
        'Python Programming': "Students apply their earlier established knowledge of programming to the Python programming language.",
        'Development and Testing': "Students learn about the software development cycle, different error types, and the techniques that can be used to test for and fix them. Of particular importance is the use of Trace Tables as a way of identifying logic errors.",
        'Network': "How networks work, and the different ways in which networks can be connected, including the distinctions between wireless/wired, LAN/WAN/PAN and different topologies.",
        'Cyber Security': "The threats that affect computer systems, and the security methods used to counteract them.",
        'Advanced Programming': "Applying advanced programming techniques in the Python programming language, including the use of external data structures and GUIs.",
        'Advanced Number Systems': "Calculations involving binary, such as binary shifts and binary addition.",
        'Ethical, Legal and Environmental Impact': "Thinking about how developments in computing impact the wider world, balancing the huge positives with the negatives."
    }

    # Select topic
    topic = st.selectbox("Select a topic", list(topic_contexts.keys()))
    if 'current_topic' not in st.session_state or st.session_state['current_topic'] != topic:
        st.session_state['current_topic'] = topic
        st.session_state['context'] = topic_contexts[topic]

    if 'num_questions' not in st.session_state:
        st.session_state['num_questions'] = 0

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    user_input = st.text_input(f"Ask a {st.session_state['current_topic']} question")

    if st.button('Send'):
        st.session_state['num_questions'] += 1

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{initial_message}\n{st.session_state['context']}\nStudent asks a {st.session_state['current_topic']} question: {user_input}\nHow would you teach them?",
            max_tokens=500,
        )
        assistant_message = response.choices[0].text.strip()

        st.session_state['chat_history'].insert(0, f'Assistant: {assistant_message}')
        st.session_state['chat_history'].insert(0, f'**You: {user_input.replace("You: ", "")}**')

        for message in st.session_state['chat_history']:
            st.markdown(message, unsafe_allow_html=True)
        st.write(f'You have asked {st.session_state["num_questions"]} questions.')

if __name__ == "__main__":
    main()
