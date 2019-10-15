import xlsxwriter 
  

workbook = xlsxwriter.Workbook('hello.xlsx') 
  

worksheet = workbook.add_worksheet("my sheet")

worksheet.write('A1', 'SR no') 
worksheet.write('B1', 'Licence No')
worksheet.write('C1', 'Name')
worksheet.write('D1','DOB')
worksheet.write('E1','Issue Date')
worksheet.write('F1','Validity')
worksheet.write('G1','Authorisation to Drive')

scores = ( 
    ['0','DL-0420110149646','Lalit Radadiya', '27-09-1999' ,'30-12-2019','30-12-2037','INVCRG'], 
    ['1','DL-0416151649646','Nirvik Patel', '05-10-1999' ,'16-02-2018','01-01-2018','LVM-NT'], 
    ['2','DL-1565166516656','Dhrupesh pokiya', '02-02-2000' ,'05-12-2019','03-01-2030','HMV'], 
    ['3','DL-5715616116656','Smit Patel', '10-05-1999' ,'08-10-2019','04-10-2023','MC EX50CC'], 
)
row=1
column=0

for Sr,Ln,Nm,Dob,Id,Vd,Ad in (scores):
   worksheet.write(row,column,Sr)
   worksheet.write(row,column+1,Ln)
   worksheet.write(row,column+2,Nm)
   worksheet.write(row,column+3,Dob)
   worksheet.write(row,column+4,Id)
   worksheet.write(row,column+5,Vd)
   worksheet.write(row,column+6,Ad)
   row+=1



workbook.close() 
