# pyrefly: ignore [missing-import]
import streamlit as st
import tempfile
import os
from pathlib import Path

st.set_page_config(
    page_title="MarkItDown",
    page_icon="📝",
    layout="wide",
)

st.title("📝 MarkItDown")
st.caption("Convert files and URLs to Markdown — powered by [Microsoft MarkItDown](https://github.com/microsoft/markitdown)")

# Supported file types
SUPPORTED_EXTENSIONS = [
    "pdf", "pptx", "ppt", "docx", "doc",
    "xlsx", "xls", "csv", "json", "xml",
    "jpg", "jpeg", "png", "gif", "webp", "bmp", "tiff",
    "wav", "mp3",
    "html", "htm",
    "zip", "epub",
]

tab_file, tab_url = st.tabs(["📁 Upload File", "🔗 URL"])

markdown_result = None
source_name = None

with tab_file:
    uploaded = st.file_uploader(
        "Drop a file here",
        type=SUPPORTED_EXTENSIONS,
        label_visibility="collapsed",
    )
    if uploaded and st.button("Convert", key="btn_file", type="primary"):
        with st.spinner("Converting..."):
            try:
                from markitdown import MarkItDown
                suffix = Path(uploaded.name).suffix
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded.read())
                    tmp_path = tmp.name
                try:
                    md = MarkItDown()
                    result = md.convert(tmp_path)
                    markdown_result = result.text_content
                    source_name = uploaded.name
                finally:
                    os.unlink(tmp_path)
            except Exception as e:
                st.error(f"Conversion failed: {e}")

with tab_url:
    url_input = st.text_input("Paste a URL", placeholder="https://example.com/document.pdf")
    if url_input and st.button("Convert", key="btn_url", type="primary"):
        with st.spinner("Fetching and converting..."):
            try:
                from markitdown import MarkItDown
                md = MarkItDown()
                result = md.convert(url_input)
                markdown_result = result.text_content
                source_name = url_input
            except Exception as e:
                st.error(f"Conversion failed: {e}")

# Output section
if markdown_result is not None:
    st.divider()

    col_label, col_dl = st.columns([6, 1])
    with col_label:
        st.subheader("Result")
    with col_dl:
        out_name = Path(source_name).stem + ".md" if source_name else "output.md"
        st.download_button(
            "⬇️ Download .md",
            data=markdown_result,
            file_name=out_name,
            mime="text/markdown",
        )

    view_raw, view_preview = st.tabs(["Raw Markdown", "Preview"])

    with view_raw:
        st.code(markdown_result, language="markdown")

    with view_preview:
        st.markdown(markdown_result)
