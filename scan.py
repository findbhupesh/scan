import os,sys
import PyPDF2
from PIL import Image
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode, ZBarSymbol

file_name = 'out/'+sys.argv[1]+'_ZPOD_00'
pdf_file  = file_name + '.pdf'
log_file  = file_name + '.txt'

if not os.path.exists(pdf_file):
    os.chdir('NAPS2')
    os.system('naps2.console -i blank.pdf  -o ../out/outpt.pdf -f')
    os.chdir('..')

    readxPDF = PyPDF2.PdfReader('out/outpt.pdf')
    writePDF = PyPDF2.PdfWriter()
    pagesPDF = len(readxPDF.pages)
    outptPDF = open(pdf_file,"wb")

    for i in range(pagesPDF):
        pagexPDF = readxPDF.pages[i]
        if pagesPDF == 1:
            writePDF.add_page(pagexPDF)
        else:
            if i > 0:
                writePDF.add_page(pagexPDF)

    writePDF.write(outptPDF)

    outptPDF.close()

imgPages = convert_from_path(pdf_file,500,poppler_path=r"poppler\\bin")

images = []
for i in range(len(imgPages)):
    png_name = file_name+str(i)+'.png'
    images.append(png_name)
    imgPages[i].save(png_name,'PNG')

barlist =[]
for name in images:
    image = Image.open(name)
    barcodes = decode(image)
    for barcode in barcodes:
        data = barcode.data
        stri = data.decode('utf8', 'strict')
        print(barcode.type)
        print(stri)
        if barcode.type == 'CODE128':
            if len(stri) == 10:
                barlist.append(stri)
    image.show()    

f = open(log_file, "w")
if len(barlist) > 0:
    f.write(barlist[0])
else:
    f.write("0000000000")
f.close()
if os.path.exists("out/outpt.pdf"):
    os.remove("out/outpt.pdf")
for image in images:
    os.remove(image)


