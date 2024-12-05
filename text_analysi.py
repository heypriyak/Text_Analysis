import os
import re
import nltk
import pandas as pd
import textstat
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

# Setup NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Paths for the stopwords and dictionary files
STOPWORDS_PATH = "../data/StopWords/"
MASTER_DICT_PATH = "../data/MasterDictionary/"
ARTICLES_PATH = "../data/output/extracted_articles/"
OUTPUT_PATH = "../Output Data Structure.xlsx"
INPUT_PATH = "../data/input.xlsx"

def load_stopwords():
    stopwords_files = ['StopWords_Auditor.txt', 'StopWords_Currencies.txt', 'StopWords_DatesandNumbers.txt', 'StopWords_Generic.txt', 'StopWords_Geographic.txt', 'StopWords_Names.txt']
    stopwords_set = set()

    for file in stopwords_files:
        with open(os.path.join(STOPWORDS_PATH, file), 'r') as f:
            for line in f:
                stopwords_set.add(line.strip())

    # Add NLTK stopwords too
    stopwords_set.update(stopwords.words('english'))
    
    return stopwords_set

def load_urls(url_id):
    input_df = pd.read_excel(INPUT_PATH)
    url = input_df.loc[input_df['URL_ID'] == url_id, 'URL'].values[0]
    return url

def load_master_dictionary():
    positive_words = set()
    negative_words = set()
    
    with open(os.path.join(MASTER_DICT_PATH, 'positive-words.txt'), 'r') as f:
        positive_words.update([line.strip() for line in f if line.strip() and not line.startswith(';')])

    with open(os.path.join(MASTER_DICT_PATH, 'negative-words.txt'), 'r') as f:
        negative_words.update([line.strip() for line in f if line.strip() and not line.startswith(';')])
    
    return positive_words, negative_words

def clean_and_tokenize(text, stopwords_set):
    words = word_tokenize(text.lower())
    cleaned_words = [word for word in words if word.isalpha() and word not in stopwords_set]
    sentences = sent_tokenize(text)
    return cleaned_words, sentences

def compute_sentiment_scores(cleaned_words, positive_words, negative_words):
    positive_score = sum(1 for word in cleaned_words if word in positive_words)
    negative_score = sum(1 for word in cleaned_words if word in negative_words)
    
    total_score = positive_score + negative_score
    if total_score == 0:
        polarity_score = 0.0
        subjectivity_score = 0.0
    else:
        polarity_score = (positive_score - negative_score) / total_score
        subjectivity_score = (positive_score + negative_score) / total_score
    
    return positive_score, negative_score, polarity_score, subjectivity_score

def compute_readability_metrics(text):
    avg_sentence_length = textstat.sentence_count(text)
    fog_index = textstat.gunning_fog(text)
    return avg_sentence_length, fog_index

def count_syllables(word):
    vowels = "aeiou"
    count = sum(1 for char in word if char in vowels)
    if word.endswith("es") or word.endswith("ed"):
        count -= 1
    return count

def count_complex_words(words):
    complex_words_count = sum(1 for word in words if count_syllables(word) > 2)
    return complex_words_count

def count_personal_pronouns(text):
    pronouns = re.findall(r'\b(I|we|my|ours|us)\b', text, re.I)
    return len(pronouns)

def avg_word_length(cleaned_words):
    total_characters = sum(len(word) for word in cleaned_words)
    return total_characters / len(cleaned_words) if cleaned_words else 0

def analyze_article(url_id, text, positive_words, negative_words, stopwords_set):
    cleaned_words, sentences = clean_and_tokenize(text, stopwords_set)
    url = load_urls(url_id)
    positive_score, negative_score, polarity_score, subjectivity_score = compute_sentiment_scores(cleaned_words, positive_words, negative_words)
    avg_sentence_length, fog_index = compute_readability_metrics(text)
    complex_word_count = count_complex_words(cleaned_words)
    word_count = len(cleaned_words)
    syllable_per_word = sum(count_syllables(word) for word in cleaned_words) / word_count if word_count > 0 else 0
    personal_pronoun_count = count_personal_pronouns(text)
    avg_word_len = avg_word_length(cleaned_words)
    
    return {
        "URL_ID": url_id,
        "URL": url,
        "POSITIVE_SCORE": round(positive_score, 2),
        "NEGATIVE_SCORE": round(negative_score, 2),
        "POLARITY_SCORE": round(polarity_score, 2),
        "SUBJECTIVITY_SCORE": round(subjectivity_score, 2),
        "AVERAGE_SENTENCE_LENGTH": round(avg_sentence_length, 2),
        "FOG_INDEX": round(fog_index, 2),
        "COMPLEX_WORD_COUNT": round(complex_word_count, 2),
        "WORD_COUNT": round(word_count, 2),
        "SYLLABLE_PER_WORD": round(syllable_per_word, 2),
        "PERSONAL_PRONOUN_COUNT": round(personal_pronoun_count, 2),
        "AVERAGE_WORD_LENGTH": round(avg_word_len, 2)
    }

def main():
    stopwords_set = load_stopwords()
    positive_words, negative_words = load_master_dictionary()
 
    output = []
    
    for txt_file in os.listdir(ARTICLES_PATH):
        url_id = txt_file.split(".")[0]
        with open(os.path.join(ARTICLES_PATH, txt_file), "r", encoding="utf-8") as file:
            text = file.read()
            analysis_results = analyze_article(url_id, text, positive_words, negative_words, stopwords_set)
            output.append(analysis_results)
    
    output_df = pd.DataFrame(output)
    output_df.to_excel(OUTPUT_PATH, index=False)
    
    print(f"Analysis complete! Results saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
