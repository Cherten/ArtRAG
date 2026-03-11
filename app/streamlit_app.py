import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.rag_pipeline import RAGPipeline

st.set_page_config(page_title="Art RAG Assistant", page_icon="🎨")
st.title("🎨 Art RAG Assistant")
st.markdown("Задайте вопрос об искусстве, художниках и направлениях. Ответы основаны на статьях Википедии (CC BY-SA).")

@st.cache_resource
def load_pipeline():
    return RAGPipeline()

pipeline = load_pipeline()

query = st.text_input("Ваш вопрос:", placeholder="Кто написал «Мону Лизу»?")
if query:
    with st.spinner("Ищу ответ..."):
        result = pipeline.answer(query)
    st.subheader("Ответ:")
    st.write(result["answer"])
    st.subheader("Источники (CC BY-SA):")
    for url in result["sources"]:
        st.markdown(f"- [{url}]({url})")