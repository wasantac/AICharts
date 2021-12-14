from bs4 import BeautifulSoup
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import re
import os
import errno


def create_dir(filename,data):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:

                    raise

    with open(filename, "a") as f:
        f.write(data)



def read_sgm():
    porter_stemmer = PorterStemmer()
    for i in range(0,22):
        numb = str(i)
        if i < 10:
            numb = '0' + str(i)
            
        print(numb) 
        filename = './reuters/reut2-0{number}.sgm'.format(number=numb)
        with open(filename ,'r') as file:
            data = file.read()
            soup = BeautifulSoup(data,'html.parser')
            contents = soup.findAll('reuters')
            for content in contents:
                docID = content.get('newid')
                topics = content.topics.contents
                if content.get('topics') == 'YES':
                    if content.body != '' or content.body != None:
                        body = str(content.body).replace('\n', ' ').replace('<body>','').replace('</body>','')
                        body = re.sub(' +', ' ', body)
                        body = re.sub("[^a-zA-Z\.]+"," ",body)
                        body = re.sub("[^a-zA-Z\s]+","",body)
                        nltk_tokens = nltk.word_tokenize(body)
                        if len(nltk_tokens) > 0:
                            nltk_tokens.pop()
                            for i in range(len(nltk_tokens)):
                                nltk_tokens[i] = porter_stemmer.stem(nltk_tokens[i])
                            body = ' '.join(nltk_tokens)
                            if len(topics) != 0:
                                for topic in topics:
                                    data_cat = "{category} {docID}\n".format(category=topic.contents[0],docID=docID)
                                    create_dir('./processed/reuters-cat-doc.qrels',data_cat)
                            
                            data_body = ".I {docID}\n.W\n{body}\n\n".format(docID=docID,body=body)
                            create_dir('./processed/reuters-training.dat',data_body)
                    
