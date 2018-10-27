import xml.etree.ElementTree as ET
import html
import csv

tree = ET.parse("XMLMergedFile.xml")
root = tree.getroot()

formspring_data_csv = open('formspring_data.csv', 'w')

csvwriter = csv.writer(formspring_data_csv)
head = ['text','label']
csvwriter.writerow(head)

for formspringid in root.findall('FORMSPRINGID'):
    for post in formspringid.findall('POST'):

        text = post.find('TEXT').text

        question = text.split('A:')[0].replace('Q:', '')
        answer = text.split('A:')[1]

        is_cyber_bullying_question = False
        is_cyber_bullying_answer = False
        for cyber_bullying_check in post.findall('LABELDATA'):
            cyber_bullying_check_answer = cyber_bullying_check.find('ANSWER').text
            cyber_bullying_word = cyber_bullying_check.find('CYBERBULLYWORD').text if cyber_bullying_check.find('CYBERBULLYWORD').text != None else ''

            if cyber_bullying_check_answer == 'Yes' and cyber_bullying_word in question:
                is_cyber_bullying_question = True
            if cyber_bullying_check_answer == 'Yes' and cyber_bullying_word in answer:
                is_cyber_bullying_answer = True

        if question != '' and question is not None:
            question_row = [html.unescape(question.encode('ascii', 'ignore').decode()).replace('<br>', ''), is_cyber_bullying_question]
            csvwriter.writerow(question_row)
        if answer != '' and answer is not None:
            answer_row = [html.unescape(answer.encode('ascii', 'ignore').decode()).replace('<br>', ''), is_cyber_bullying_answer]
            csvwriter.writerow(answer_row)

formspring_data_csv.close()
