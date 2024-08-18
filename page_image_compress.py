# page_image_compress.py

import streamlit as st
from PIL import Image
import os
import tempfile

def replace_last_dot(input_image_path):
    """
    将文件路径中最后一个点替换为'_compress.'
    """
    dirname, filename = os.path.split(input_image_path)
    name, ext = os.path.splitext(filename)
    
    new_filename = f"{name}_compress{ext}"
    
    new_image_path = os.path.join(dirname, new_filename)
    
    return new_image_path

def compress_image(input_image_path, quality):
    """
    使用Pillow库压缩图像文件。
    
    :param input_image_path: 输入图像文件的路径。
    :param output_image_path: 压缩后的输出图像文件路径。
    :param quality: 压缩质量，范围1到100。
    """
    output_image_path = replace_last_dot(input_image_path)
    # 打开原始图像
    image = Image.open(input_image_path)
    
    # 设置压缩质量
    quality_settings = [50, 10, 30, 60, 90]
    quality_setting = quality_settings[max(0, min(quality, len(quality_settings) - 1))]
    
    # 保存图像并指定压缩质量
    image.save(output_image_path, 'JPEG', quality=quality_setting)
    return output_image_path  # 返回压缩文件的路径以供下载

def image_compress_page():
    st.title('图片压缩工具')

    uploaded_file = st.file_uploader("选择图片进行压缩", type=['jpg', 'jpeg', 'png'])
    quality = st.select_slider("选择压缩质量，默认是0，值越大质量最好", options=[0, 1, 2, 3, 4], value=0)
    
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmpfile:
            tmpfile.write(uploaded_file.getvalue())
            output_image_path = compress_image(tmpfile.name, quality)
        
        with open(output_image_path, "rb") as file:
            st.download_button(
                label="下载压缩图片",
                data=file,
                file_name=os.path.basename(output_image_path),
                mime="image/jpeg"
            )