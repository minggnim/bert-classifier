import streamlit as st
from tempfile import NamedTemporaryFile
from nlp_models.llm.base import LlmConfig
from nlp_models.llm.vectordbs import build_vectordb, load_vectordb
from nlp_models.llm.llms import build_llm
from nlp_models.llm.prompts import QAPrompt
from nlp_models.llm.apps import QaLlmApp

st.set_page_config(page_title='🤖 Llama2 Q&A on CPU', layout='wide', page_icon='🤖')


if 'query' not in st.session_state:
    st.session_state['query'] = ''
if 'response' not in st.session_state:
    st.session_state['response'] = ''


def generate_response():
    config = LlmConfig()
    # Load document if file is uploaded
    if uploaded_file is not None:
        llm_qa_app = QaLlmApp(llm=build_llm(config), prompt=QAPrompt().qa_prompt, vectordb=load_vectordb(config))
    if st.session_state.query:
        st.session_state.response = llm_qa_app(st.session_state.query)
        st.session_state.query = ''


# Page title
st.title("🦙 Llama2 🤖 Q&A on CPU")
st.subheader(" Powered by 🦙 Llama2 + 🦜🔗 LangChain + Streamlit")

# File upload
uploaded_file = st.file_uploader('Upload an article', type='pdf')
# submit button
submit_file = st.button('Submit', disabled=not uploaded_file)

if submit_file:
    with st.spinner('Calculating...'):
        with NamedTemporaryFile(dir='.', suffix='.pdf') as f:
            f.write(uploaded_file.getbuffer())
            build_vectordb(LlmConfig(), f.name)

st.session_state.query = st.text_input(
    'Enter your question:',
    placeholder='Please provide a short summary.',
    disabled=not uploaded_file
)

submit_query = st.button("Get Answer", on_click=generate_response, type='primary', disabled=not st.session_state.query)

if submit_query and st.session_state.query:
    st.info(st.session_state.response['result'])
