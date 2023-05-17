import cv2,os,sys
import PyPDF2
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode, ZBarSymbol

refn = sys.argv[1]

os.chdir('NAPS2')
com_naps = 'naps2.console.exe'
inp_file = '../Files/blank.pdf'
out_file = '../Files/outpt.pdf'
pdf_file = '../Files/POD_'+refn+'.pdf'
log_file = '../Files/POD_'+refn+'.txt'
os.system(com_naps+' -i '+inp_file+' -o '+ out_file+ ' -f')

readxPDF = PyPDF2.PdfReader(out_file)
writePDF = PyPDF2.PdfWriter()
pagesPDF = len(readxPDF.pages)
outptPDF = open(pdf_file,"wb")
for i in range(pagesPDF):
    pagexPDF = readxPDF.pages[i]
    textxPDF  = pagexPDF.extract_text()
    if pagesPDF == 1:
        writePDF.add_page(pagexPDF)
    else:
        if (len(textxPDF) > 0):
            writePDF.addPage(pagexPDF)

writePDF.write(outptPDF)

outptPDF.close()

pages = convert_from_path(pdf_file,500,poppler_path=r"../poppler/bin")

images = []
for i in range(len(pages)):
    name = '../Files/POD_'+refn+'_'+str(i)+'.png'
    images.append(name)
    pages[i].save(name,'PNG')

barlist =[]
for name in images:
    image = cv2.imread(name) 
    barcodes = decode(image)
    for barcode in barcodes:
        data = barcode.data
        stri = data.decode('utf8', 'strict')
        if barcode.type == 'CODE128':
            barlist.append(stri)
#    cv2.namedWindow("POD", cv2.WINDOW_NORMAL)
#    cv2.imshow("POD", image)
#    cv2.waitKey(0)

f = open(log_file, "w")
if len(barlist) > 0:
    f.write(barlist[0])
else:
    f.write("0000000000")
f.close()

for image in images:
    os.remove(image)

