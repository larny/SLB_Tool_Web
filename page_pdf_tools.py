import streamlit as st
import os
import sys
from pathlib import Path
from PIL import Image
import zipfile
import tempfile
import subprocess
import shutil

def pdf_tools_page():
    def get_gs_command():
        """根据操作系统返回适当的Ghostscript命令"""
        if sys.platform.startswith('win'):
            return "gswin64c.exe"
        else:
            return "gs"
    def compress_pdf(input_pdf, quality=0):
        gs_command = get_gs_command()
        output_pdf = input_pdf.replace(".pdf", "_compress.pdf")
        if quality == 0:
            quality_setting = '/default'
        elif quality == 1:
            quality_setting = '/screen'
        elif quality == 2:
            quality_setting = '/ebook'
        elif quality == 3:
            quality_setting = '/printer'
        elif quality == 4:
            quality_setting = '/prepress'
        else:
            raise ValueError("Unsupported quality setting.")
        
        command = [
            gs_command,
            "-sDEVICE=pdfwrite",
            f"-dPDFSETTINGS={quality_setting}",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={output_pdf}",
            input_pdf
        ]
        
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError:
            # 在这里处理错误，但不打印整个命令
            # st.error(f"无法压缩文件 {input_pdf}。请检查文件是否有效或太小以至于无法压缩。")
            pass

    # 在compress_folder_to_zip中对compress_pdf调用进行异常捕获的修改无需变动，
    # 因为异常处理已经在compress_pdf函数内部完成。

    def compress_folder_to_zip(folder_path, quality, output_zip_path):
        with zipfile.ZipFile(output_zip_path, 'w') as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    # 跳过.__开头的隐藏文件
                    if not file.startswith('.__'):
                        if file.lower().endswith('.pdf'):
                            input_pdf_path = str(Path(root) / file)
                            # 试图压缩PDF文件，捕获并记录可能的错误
                            try:
                                compress_pdf(input_pdf_path, quality)
                                compressed_pdf_name = file.replace(".pdf", "_compress.pdf")
                                compressed_pdf_path = str(Path(root) / compressed_pdf_name)
                                zipf.write(compressed_pdf_path, compressed_pdf_name)
                                os.remove(compressed_pdf_path)
                            except subprocess.CalledProcessError as e:
                                st.error(f"无法压缩文件 {input_pdf_path}: {e}")


    st.title('PDF Compression Tool')

    uploaded_file = st.file_uploader("Upload a PDF file or a ZIP file containing PDFs", ['pdf', 'zip'])
    quality = st.select_slider("选择压缩质量，默认是0，值越大质量最好", options=[0, 1, 2, 3, 4], value=0)

    if uploaded_file is not None and st.button("Compress"):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = Path(temp_dir) / uploaded_file.name
            temp_file_path.write_bytes(uploaded_file.getvalue())
            operation_completed = False
            
            if uploaded_file.type == "application/pdf":
                input_pdf_path = str(temp_file_path)
                compress_pdf(input_pdf_path, quality)
                output_pdf = temp_file_path.stem + "_compress.pdf"
                with open(Path(temp_dir) / output_pdf, "rb") as f:
                    st.download_button("Download Compressed PDF", f, file_name=output_pdf, mime="application/pdf")
                    operation_completed = True
                    
            elif uploaded_file.type == "application/zip":
                shutil.unpack_archive(str(temp_file_path), extract_dir=temp_dir)
                compressed_zip_path = Path(temp_dir) / "compressed_files.zip"
                compress_folder_to_zip(temp_dir, quality, compressed_zip_path)

                with open(compressed_zip_path, "rb") as f:
                    st.download_button("Download Compressed ZIP", f, file_name="compressed_files.zip", mime="application/zip")
                    operation_completed = True
            
            if operation_completed:
                st.success("Download ready.")