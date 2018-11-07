import xml.etree.ElementTree as ET
import html
import csv

tree = ET.parse("XMLMergedFile.xml")
root = tree.getroot()

# SET THIS THRESHOLD
severity_threshold = 2.5

formspring_data_csv = open('formspring_data_severity_gt{0}.csv'.format(str(severity_threshold).replace('.', '_')), 'w')

csvwriter = csv.writer(formspring_data_csv)
head = ['text', 'label']
csvwriter.writerow(head)

for formspringid in root.findall('FORMSPRINGID'):
    for post in formspringid.findall('POST'):

        text = post.find('TEXT').text

        bullying_severity = 0
        for label in post.findall('LABELDATA'):
            bullying_severity += int(label.find('SEVERITY').text if label.find('SEVERITY').text is not None and label.find('SEVERITY').text != 'n/a0' and label.find('SEVERITY').text != 'n/a' and label.find('SEVERITY').text != 'o' and label.find('SEVERITY').text != '0`' and label.find('SEVERITY').text != '`0' and label.find('SEVERITY').text != 'N/a' else 0)

        if text != '' and text is not None:
            row = [html.unescape(text.encode('ascii', 'ignore').decode()).replace('<br>', ''), (bullying_severity/3 > severity_threshold)]
            csvwriter.writerow(row)

formspring_data_csv.close()
