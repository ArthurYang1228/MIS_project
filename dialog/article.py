url = ["https://www.ntuh.gov.tw/telehealth/information/_layouts/15/start.aspx#/SitePages/%E5%81%A5%E5%BA%B7%E5%A5%BD%E6%96%87.aspx",
       "http://fluforecast.cdc.gov.tw/#/AllTaiwan",
       ]
import csv
def create_sym_file():
       symptom = []
       with open('example4.csv','r') as file:
              reader = csv.DictReader(file)

              print(reader)
              for row in reader:
                     for syms in row['症狀'].split('\''):
                            if '.' in syms:
                                   for sym in syms.split('.'):
                                          if sym not in symptom:
                                                symptom.append(sym)

                            elif '．' in syms:
                                   for sym in syms.split('．'):
                                          if sym not in symptom:
                                                 symptom.append(sym)
              file.close()
       print(symptom)

       with open('sym.csv', 'w') as file:
              fieldnames = ['症狀']
              writer = csv.DictWriter(file, fieldnames=fieldnames)
              writer.writeheader()
              for sym in symptom:
                     if len(sym)<11:
                            writer.writerow({'症狀': sym})
              file.close()
def write_sym_file():
       symptom = []
       with open('sym.csv', 'r') as file:

              reader = csv.DictReader(file)
              print(reader)
              for row in reader:
                     print(row)
                     symptom.append(row['症狀'])
              file.close()
       with open('sym.csv','a') as file:
              fieldnames = ['症狀']
              writer = csv.writer(file,)

              while True:
                     txt = input('sym:')
                     if txt == 'stop':
                            break
                     elif txt not in symptom:
                            print(txt in symptom)
                            writer.writerow([txt])
                     else:
                            print(txt in symptom)
              file.close()
symptom = []

def to_txt():
       with open('sym.csv','r') as file:
              reader = csv.DictReader(file)
              print(reader)
              for row in reader:
                     print(row)
                     symptom.append(row['症狀'])
       print(symptom)
       with open('sym.txt','w') as sym:
              for s in symptom:
                     sym.write(s +' 10'+' n\n')
to_txt()
'''
       while True:
              txt = input('sym:')
              if txt == 'stop':
                     break
              elif txt not in symptom:
                     print(txt in symptom)
                     writer.writerow({'症狀': txt})
              else:
                     print(txt in symptom)
              for i in row['症狀'][0].split('.'):
                     if i not in symptom:
                            symptom.append(i)
'''

