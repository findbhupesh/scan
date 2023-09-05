from pypdf import PdfReader, PdfWriter

reader = PdfReader("big_file.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.compress_content_streams()  # This is CPU intensive!
    writer.add_page(page)

with open("small.pdf", "wb") as f:
    writer.write(f)