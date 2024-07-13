import os
import pandas as pd
from textblob import TextBlob
import re

# Load the input data
input_file = os.path.join('..', 'data', 'Input.xlsx')
input_df = pd.read_excel(input_file)

# Create a directory for output if it doesn't exist
output_dir = os.path.join('..', 'output')
os.makedirs(output_dir, exist_ok=True)

# Function to count syllables in a word
def count_syllables(word):
    word = word.lower()
    vowels = "aeiouy"
    count = 0
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if word.endswith("le") and len(word) > 2 and word[-3] not in vowels:
        count += 1
    if count == 0:
        count += 1
    return count

# Load positive and negative words
positive_words_file = os.path.join('..', 'data', 'positive-words.txt')
negative_words_file = os.path.join('..', 'data', 'negative-words.txt')

with open(positive_words_file, 'r', encoding='ISO-8859-1') as file:
    positive_words = set(file.read().splitlines())

with open(negative_words_file, 'r', encoding='ISO-8859-1') as file:
    negative_words = set(file.read().splitlines())

# Function to perform text analysis
def analyze_text(text):
    # Calculate positive and negative scores
    words = re.findall(r'\w+', text.lower())
    positive_score = sum(1 for word in words if word in positive_words)
    negative_score = sum(1 for word in words if word in negative_words)
    
    # Calculate polarity and subjectivity scores
    blob = TextBlob(text)
    polarity_score = blob.sentiment.polarity
    subjectivity_score = blob.sentiment.subjectivity
    
    # Calculate average sentence length
    sentences = blob.sentences
    avg_sentence_length = sum(len(sentence.words) for sentence in sentences) / len(sentences) if sentences else 0
    
    # Calculate percentage of complex words
    complex_words = [word for word in words if count_syllables(word) > 2]
    percentage_complex_words = len(complex_words) / len(words) if words else 0
    
    # Calculate fog index
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words * 100)
    
    # Calculate other metrics
    word_count = len(words)
    syllables_per_word = sum(count_syllables(word) for word in words) / len(words) if words else 0
    personal_pronouns = len(re.findall(r'\b(I|we|my|ours|us)\b', text, re.I))
    avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
    
    return {
        'POSITIVE SCORE': positive_score,
        'NEGATIVE SCORE': negative_score,
        'POLARITY SCORE': polarity_score,
        'SUBJECTIVITY SCORE': subjectivity_score,
        'AVG SENTENCE LENGTH': avg_sentence_length,
        'PERCENTAGE OF COMPLEX WORDS': percentage_complex_words * 100,
        'FOG INDEX': fog_index,
        'AVG NUMBER OF WORDS PER SENTENCE': avg_sentence_length, 
        'COMPLEX WORD COUNT': len(complex_words),
        'WORD COUNT': word_count,
        'SYLLABLE PER WORD': syllables_per_word,
        'PERSONAL PRONOUNS': personal_pronouns,
        'AVG WORD LENGTH': avg_word_length
    }

# Initialize the output dataframe
output_columns = [
    'URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE',
    'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE',
    'COMPLEX WORD COUNT', 'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'
]
output_df = pd.DataFrame(columns=output_columns)

# Directory containing extracted articles
extracted_articles_dir = os.path.join('..', 'data', 'extracted_articles')

# Iterate through each URL_ID and analyze the corresponding article text
for index, row in input_df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    
    try:
        file_path = os.path.join(extracted_articles_dir, f'{url_id}.txt')
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        analysis_results = analyze_text(text)
        new_row = {
            'URL_ID': url_id,
            'URL': url,
            **analysis_results
        }
        output_df = pd.concat([output_df, pd.DataFrame([new_row])], ignore_index=True)
        print(f'Successfully processed article {url_id}')
    except Exception as e:
        print(f'Failed to process article {url_id}: {e}')

# Save the output to an Excel file
output_file = os.path.join(output_dir, 'Output Data Structure.xlsx')
output_df.to_excel(output_file, index=False)
print('Output saved to Output Data Structure.xlsx')
