import streamlit as st
from shared import setup_page, page_header, get_book_id, run_cached, summarize_book

setup_page("Summary", "📄")
page_header("Summary", "Extractive summary | NLP")

book_id = get_book_id()
if book_id and st.button("Generate summary"):
    result = run_cached("summarize", summarize_book, book_id)
    st.divider()
    st.write(result)