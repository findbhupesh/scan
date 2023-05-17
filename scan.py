import cv2,os,sys
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode, ZBarSymbol

refn = sys.argv[1]

naps = 'naps2.console.exe'
inpf = ' -i C:\SAP\Scan\Files\Initial.pdf'
outf = ' -o C:\SAP\Scan\Files\POD_'+refn+'.pdf -f'
os.chdir('NAPS2')
os.system(naps+inpf+outf)
os.chdir('..')
pdf_name = 'Files/POD_'+refn+'.pdf'
pages = convert_from_path(pdf_name,500,poppler_path=r"poppler/bin")

images = []
for i in range(len(pages)):
    name = 'files/POD_'+refn+'_'+str(i)+'.png'
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
            if stri[0:3] == '919':
                barlist.append(stri)
#        print(stri)
#        print(barcode.type)
#    cv2.namedWindow("POD", cv2.WINDOW_NORMAL)
#    cv2.imshow("POD", image)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()

print(barlist[0])
inv_numb = ""
for c in pdf_name:
    if c.isdigit():
        inv_numb = inv_numb + c
print(inv_numb)
log_file = 'Files/POD_'+refn+'.txt'
f = open(log_file, "w")
f.write(barlist[0])
f.close()

for image in images:
    os.remove(image)

