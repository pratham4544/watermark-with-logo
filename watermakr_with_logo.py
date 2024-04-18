import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def add_watermark(pdf_path, img_path):
    # Open the PDF file and read its contents
    pdf = PdfReader(pdf_path)
    output_pdf = PdfWriter()

    # Create a temporary PDF file for the watermark image
    c = canvas.Canvas("temp.pdf", pagesize=letter)
    c.drawImage(img_path, 450, 0, width=90, height=30)  # Adjust the width and height as needed
    c.save()

    # Iterate over each page in the PDF file
    for page in pdf.pages:
        # Merge the original page with the watermark image
        overlay = PdfReader("temp.pdf").pages[0]
        page.merge_page(overlay)

        # Add the modified page to the output PDF
        output_pdf.add_page(page)

    return output_pdf

def main():
    st.title("PDF Watermark App")
    
    # File uploader for uploading PDF files
    uploaded_files = st.file_uploader("Upload PDF files", accept_multiple_files=True, type="pdf")
    
    # File uploader for uploading watermark image
    watermark_image = st.file_uploader("Upload Watermark Image", type=["jpg", "jpeg", "png"])

    if uploaded_files and watermark_image:
        # Process uploaded PDF files
        for pdf_file in uploaded_files:
            with open(pdf_file.name, "wb") as f:
                f.write(pdf_file.getbuffer())
            
            output_pdf = add_watermark(pdf_file.name, watermark_image.name)
            output_filename = f"watermarked_{pdf_file.name}"
            
            with open(output_filename, "wb") as f:
                output_pdf.write(f)
            
            st.success(f"Watermark added successfully to {pdf_file.name}.")
            st.download_button(label="Download Watermarked PDF", data=open(output_filename, "rb").read(), file_name=output_filename)

# Run the app
if __name__ == "__main__":
    main()
