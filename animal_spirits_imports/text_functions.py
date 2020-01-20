import re
import string
import spacy

# load in punctuation for removal
punctuations = string.punctuation

# load in stopwords for removal
nlp = spacy.load('en_core_web_sm')
stop_words = spacy.lang.en.stop_words.STOP_WORDS

spacy.lang.en.English()

# instantiate spaCy's english parser
parser = spacy.lang.en.English()


def clean_text(text): 
    """Clean our tweets using regex. Remove weird characters and links."""
    cleanedup = text.lower()
    return re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", cleanedup)

# create a function to tokenize and lemmatize tweets, and remove stopwords and punctuation
def spacy_tokenizer(sentence):
    # Creating our token object, which is used to create documents with linguistic annotations.
    mytokens = parser(sentence)

    # Lemmatizing each token and converting each token into lowercase
    mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]

    # Removing stop words
    mytokens = [ word for word in mytokens if word not in stop_words and word not in punctuations ]

    # return preprocessed list of tokens
    return mytokens
