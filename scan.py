import os,sys
import PyPDF2
from PIL import Image
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode, ZBarSymbol

refn = sys.argv[1]

os.chdir('NAPS2')
com_naps = 'naps2.console.exe'
inp_file = '../Files/blank.pdf'
out_file = '../Files/outpt.pdf'
os.system(com_naps+' -i '+inp_file+' -o '+ out_file+ ' -f')
os.chdir('..')
pdf_file = 'Files/'+refn+'_ZPOD_0001_00.pdf'
log_file = 'Files/'+refn+'_ZPOD_0001_00.txt'
readxPDF = PyPDF2.PdfReader('Files/outpt.pdf')
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
    png_name = 'Files/'+refn+'_ZPOD_0001_00_'+str(i)+'.png'
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

for image in images:
    os.remove(image)

