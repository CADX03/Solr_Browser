import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

stop_words = stopwords.words('english') # English stop words

output_file = "solr/stopwords.txt"

with open(output_file, "w") as file:
    for word in stop_words:
        file.write(word + "\n")