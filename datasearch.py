
import hashlib
import xlrd
import time
import os

from pyfingerprint.pyfingerprint import PyFingerprint

wb = xlrd.open_workbook('/home/lalit/Desktop/DE-2A/python-fingerprint/examples/hello.xlsx')
sheet = wb.sheet_by_index(0)


try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

## Gets some sensor information
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Tries to search the finger and calculate hash
try:
    print('Waiting for finger...')

    ## Wait that finger is read
    while ( f.readImage() == False ):
        pass
    f.convertImage(0x01)

    ## Searchs template
    result = f.searchTemplate()

    positionNumber = result[0]
    accuracyScore = result[1]

    if ( positionNumber == -1 ):
        print('No match found!')
        exit(0)
    else:
        print('Found template at position #' + str(positionNumber))
        print('The accuracy score is: ' + str(accuracyScore))

        print("Driving licence NO:    : "+sheet.cell_value(positionNumber+1,1))
        print("Name                   : "+sheet.cell_value(positionNumber+1,2))
        print("DOB                    : "+sheet.cell_value(positionNumber+1,3))
        print("Issue Date             : "+sheet.cell_value(positionNumber+1,4))
        print("Validity               : "+sheet.cell_value(positionNumber+1,5))
        print("Authorisation to Drive : "+sheet.cell_value(positionNumber+1,6))
        if time.strftime("%d-%m-%Y")<sheet.cell_value(positionNumber+1,5):
            print("------------------UptoDate------------------")
            os.system("python3 myface.py")
        else:
            print("------------------Expired------------------")
                                           
        


    ## Loads the found template to charbuffer 1
    f.loadTemplate(positionNumber, 0x01)

    ## Downloads the characteristics of template loaded in charbuffer 1
    characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

    ## Hashes characteristics of template
    print('SHA-2 hash of template: '+ hashlib.sha256(characterics).hexdigest())




except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    exit(1)


