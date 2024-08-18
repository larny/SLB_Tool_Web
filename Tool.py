# main.py

import streamlit as st
from page_image_to_pdf import image_to_pdf_page
from page_pdf_tools import pdf_tools_page
from page_image_compress import image_compress_page
from page_image_convert import image_convert_page

st.set_page_config(page_title="Demo App", page_icon="✨")

def main():
    st.sidebar.title("功能选择")
    # 将页面名称映射到对应的函数
    page_names_to_funcs = {
        "PDF处理": pdf_tools_page,
        "图片转PDF": image_to_pdf_page,
        "图片压缩": image_compress_page,
        "图片转换": image_convert_page,

    }

    demo_name = st.sidebar.selectbox("选择一个演示", list(page_names_to_funcs.keys()))

    # 根据选定的演示执行相应的函数
    page_function = page_names_to_funcs[demo_name]
    page_function()

if __name__ == "__main__":
    main()