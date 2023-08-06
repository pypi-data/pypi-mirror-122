from transformers import pipeline
import re
nlp = pipeline('question-answering')

date_regex = r'\d{1,2}[-\/]\d{1,2}[-\/]\d{2,4}'
mail_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
phone_regex = r'\d{10}'


def extract(text,request):
    extracted = {}
    classes = find_class(request)
    if 'date' in classes:
        extracted['dates'] = re.findall(date_regex, text)
    if 'number' in classes:
        extracted['phone'] = re.findall(phone_regex, text)
    if 'mail' in classes:
        extracted['mails'] = re.findall(mail_regex, text)
    return extracted

def find_class(text):
    all_classes = []
    ans = nlp(context=text, question='What needs to be extracted ?')['answer']
    if 'date' in ans:
        all_classes.append('date')
    if 'number' in ans:
        all_classes.append('number')
    if 'mail' in ans:
        all_classes.append('mail')
    return all_classes