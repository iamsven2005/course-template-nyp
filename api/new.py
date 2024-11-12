import re
import pandas
import docx2txt

INPUT_FILE = 'jantest2.docx'
OUTPUT_FILE = 'jantest2.xlsx'

text = docx2txt.process(INPUT_FILE)
results = re.findall(r'(\d+-\d+)\n\n(.*)\n\n(.*)\n\n(.*)', text)
data = {'Case Number': [x[0] for x in results],
        'Report Date': [x[1] for x in results],
        'Address': [x[2] for x in results],
        'Statute Descripiton': [x[3] for x in results]}

data_frame = pandas.DataFrame(data=data)
writer = pandas.ExcelWriter(OUTPUT_FILE)
data_frame.to_excel(writer, 'Sheet1', index=False)
writer.save()
