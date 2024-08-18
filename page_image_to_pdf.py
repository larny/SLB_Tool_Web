# page_image_to_pdf.py

import streamlit as st
from PIL import Image
import tempfile
import os

def image_to_pdf_page():
    st.title('图片转PDF工具')
    
    # 允许用户选择多个文件
    uploaded_files = st.file_uploader("选择图片", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
    
    if uploaded_files:
        with tempfile.TemporaryDirectory() as temp_dir:
            # 创建PDF文件名
            pdf_path = os.path.join(temp_dir, "combined.pdf")
            
            # 初始化一个空的PDF文件
            pdf_image_list = []
            
            # 遍历所选的每个文件
            for uploaded_file in uploaded_files:
                # 读取每个文件作为PIL图像
                image = Image.open(uploaded_file)
                
                # 如果图像不是RGB模式，则将其转换为RGB
                if image.mode in ("RGBA", "LA", "P"):
                    image = image.convert("RGB")
                
                pdf_image_list.append(image)
            
            # 将所有图片保存到一个PDF文件
            pdf_image_list[0].save(pdf_path, "PDF", resolution=100.0, save_all=True, append_images=pdf_image_list[1:])
            
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="下载PDF文件",
                    data=f,
                    file_name="combined_images.pdf",
                    mime="application/pdf"
                )