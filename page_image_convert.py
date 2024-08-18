# page_image_convert.py

import streamlit as st
from PIL import Image
import os
import tempfile

def convert_image_format(image_file, target_format):
    """
    将上传的图像文件转换为目标格式，并返回转换后文件的路径。
    """
    # 从上传的文件创建一个Pillow图像对象
    image = Image.open(image_file)
    
    # 创建临时文件，用于保存转换后的图像
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{target_format.lower()}") as tmpfile:
        # 构建临时输出文件路径
        output_image_path = tmpfile.name
        # 转换并保存图像到指定格式
        image.save(output_image_path, target_format.upper())
    
    return output_image_path

def image_convert_page():
    st.title('图片格式转换工具')
    
    uploaded_file = st.file_uploader("选择图片文件", type=['jpg', 'jpeg', 'png'])
    target_format = st.selectbox("选择目标格式", ['JPEG', 'PNG', 'TIFF'])
    
    if uploaded_file is not None and target_format:
        output_image_path = convert_image_format(uploaded_file, target_format)
        
        with open(output_image_path, "rb") as file:
            btn = st.download_button(
                    label="下载转换后的图片",
                    data=file,
                    file_name=os.path.basename(output_image_path)
                )