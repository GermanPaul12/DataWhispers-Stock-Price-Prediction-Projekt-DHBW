import re

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary NLTK data
#nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text)

    # Removing stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    # Normalization (converting to lower case and removing punctuation)
    normalized_tokens = [re.sub(r'[^\w\s]', '', word.lower()) for word in filtered_tokens]
    normalized_tokens = [word for word in normalized_tokens if word]  # Remove empty strings
    normalized_tokens = [word for word in normalized_tokens if not word.isdigit()] # Remove numbers
    normalized_tokens = [word for word in normalized_tokens if not len(word) == 1] # Remove single characters

    return normalized_tokens


