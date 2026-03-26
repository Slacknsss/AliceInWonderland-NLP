import streamlit as st
import pandas as pd
from pathlib import Path

from shared import setup_page, page_header, download_all_books
from features.components.get_offline_catalog import get_offline_catalogue


setup_page("Download", "📂")
page_header("Batch Download", "Download by author or category | Gutenberg")

st.write(
    "Download all books from a given author or subject category. "
    "Choose one of the two fields."
)

# Load catalogue
df = pd.read_csv(get_offline_catalogue())


# Extract authors and categories
authors = (df["Authors"].dropna().str.split(";").explode().str.strip())
authors = sorted(authors)
categories = (df["Bookshelves"].dropna().str.split(";").explode().str.replace("Category:", "", regex=False).str.strip().unique())

categories = sorted(categories)
# Select boxes with search
author = st.selectbox(
    "Author",
    options=[""] + authors,
    index=0,
    placeholder="Search an author..."
)

category = st.selectbox(
    "Category",
    options=[""] + categories,
    index=0,
    placeholder="Search a category..."
)

# Download button
if st.button("Download"):
    if not author and not category:
        st.error("Provide at least an author name or a category.")

    elif author and category:
        st.error("Choose either an author or a category, not both.")

    else:
        with st.spinner("Downloading…"):
            try:
                paths = download_all_books(
                    author if author else None,
                    category if category else None,
                )

                st.metric("Files downloaded", len(paths))

                for p in paths:
                    file_path = Path(p)

                    if file_path.exists():
                        with open(file_path, "rb") as f:
                            st.download_button(
                                label=f"Download {file_path.name}",
                                data=f,
                                file_name=file_path.name,
                                mime="text/plain"
                            )

            except (TypeError, ValueError) as e:
                st.error(str(e))