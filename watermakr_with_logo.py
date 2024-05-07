import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import shutil
import zipfile

def add_watermark(pdf_path, img_path, top, bottom, width, height):
    # Open the PDF file and read its contents
    pdf = PdfReader(pdf_path)
    output_pdf = PdfWriter()

    # Create a temporary PDF file for the watermark image
    c = canvas.Canvas("temp.pdf", pagesize=A4)
    c.drawImage(img_path, top, bottom, width=width, height=height)  # Adjust the width and height as needed
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
    
    if watermark_image is None:
        default_logo_path = "logo.jpg"
        if not os.path.exists(default_logo_path):
            st.error("Default logo not found. Please upload a watermark image.")
            return

    if uploaded_files:
        top = st.slider("Top Margin", min_value=0, max_value=800, value=470)
        bottom = st.slider("Bottom Margin", min_value=0, max_value=800, value=0)
        width = st.slider("Width", min_value=20, max_value=400, value=120)
        height = st.slider("Height", min_value=20, max_value=400, value=40)

        # Process uploaded PDF files
        output_filenames = []
        for pdf_file in uploaded_files:
            with open(pdf_file.name, "wb") as f:
                f.write(pdf_file.getbuffer())
            
            if watermark_image:
                watermark_image_path = watermark_image.name
            else:
                watermark_image_path = default_logo_path
            
            output_pdf = add_watermark(pdf_file.name, watermark_image_path, top, bottom, width, height)
            output_filename = f"watermarked_{pdf_file.name}"
            
            with open(output_filename, "wb") as f:
                output_pdf.write(f)
            
            output_filenames.append(output_filename)
            st.success(f"Watermark added successfully to {pdf_file.name}.")

        # Create the static directory if it doesn't exist
        if not os.path.exists("static"):
            os.makedirs("static")

        # Create a zip file containing all the watermarked PDFs
        zip_filename = "watermarked_pdfs.zip"
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            for filename in output_filenames:
                zipf.write(filename)
        
        # Move the zip file to the static folder for download
        shutil.move(zip_filename, os.path.join("static", zip_filename))
        
        # Display download link for the zip file
        st.markdown(f"Download zip file containing all watermarked PDFs: [watermarked_pdfs.zip](./static/{zip_filename})")

        # Add a download button for the zip file
        st.download_button(label="Download Watermarked PDFs", data=open(os.path.join("static", zip_filename), "rb").read(), file_name=zip_filename)

# Run the app
if __name__ == "__main__":
    main()
