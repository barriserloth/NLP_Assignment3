from nltk.parse.stanford import StanfordParser
import nltk

def generate_english_to_spanish():
  english_spanish = dict()

  f = open('english_to_spanish.txt')
  for line in f:
    words = line.split(':')
    english_spanish[words[0]] = words[1].replace('\n', '')

  return english_spanish

def translate_sentence(sentence, d):
  sentence = sentence.lower()
  sentence = nltk.word_tokenize(sentence)
  translated = ''
  for word in sentence:
    if d.get(word):
      translated += d[word] + ' '
    elif word == '.':
        translated += ''
    else:
      translated += '<OOV> '
  return translated

def calculate_bleu_score(candidate_sentences):
  reference_sentences = []
  with open('references.txt') as f:
    for line in f.readlines():
      reference_sentences.append(line.strip().lower())

  bleu_score = 0.0
  for i in range(len(candidate_sentences)):
    candidate = candidate_sentences[i]
    reference = reference_sentences[i]

    candidate_tokens = nltk.word_tokenize(candidate)
    reference_tokens = nltk.word_tokenize(reference)

    bleu_n_scores = [0.0, 0.0, 0.0, 0.0]

    # Loop through BLEU-1, -2, -3, and -4 for each candidate sentence
    for n in range(1, 5):
      candidate_ngrams = list(nltk.ngrams(candidate_tokens, n))
      reference_ngrams = list(nltk.ngrams(reference_tokens, n))

      # Some short sentences have 0 4-grams, and hence a 0 BLEU-4 score
      if len(candidate_ngrams) == 0:
        continue

      # Count ngram occurrences in reference sentence
      reference_ngram_counts = {}
      for ngram in reference_ngrams:
        try:
          reference_ngram_counts[ngram] += 1
        except KeyError:
          reference_ngram_counts[ngram] = 1

      # Count ngram occurrences in candidate sentence
      candidate_ngram_counts = {}
      for ngram in candidate_ngrams:
        try:
          # Clip ngram counts based on frequency in reference
          if candidate_ngram_counts[ngram] < reference_ngram_counts[ngram]:
            candidate_ngram_counts[ngram] += 1
        except KeyError:
          # Exclude entirely if ngram does not occur in reference
          if ngram in reference_ngrams:
            candidate_ngram_counts[ngram] = 1

      # Sum counts of matching ngrams in candidate
      candidate_ngram_sum = 0
      for count in candidate_ngram_counts.values():
        candidate_ngram_sum += count

      # Calculate BLEU-n score and save
      bleu_n_scores[n-1] = float(candidate_ngram_sum) / len(candidate_ngrams)

    # Calculate overall BLEU score of the candidate sentence
    sentence_bleu_score = 0.0
    zeroes = 0
    for score in bleu_n_scores:
      if score > 0:
        sentence_bleu_score += score
      else:
        zeroes += 1
    if zeroes < 4:
      bleu_score += sentence_bleu_score / (4 - zeroes)

  # System BLEU score is averaged across sentences
  return bleu_score / len(candidate_sentences)


def main():
  f = open('cfg_sentences.txt').readlines()
  sentences = ' '.join(f).replace('\n', '')

  text = nltk.word_tokenize(sentences)
  tagged_text = nltk.pos_tag(text)

  # english_parser = StanfordParser('stanford-parser.jar', 'stanford-parser-3.8.0-models.jar')

  # parsed = english_parser.raw_parse('This is a test')
  # for line in parsed:
    # print line

  translation_dict = generate_english_to_spanish()
  translated_sentences = []
  for line in f:
    translated_sentences.append(translate_sentence(line, translation_dict))
  print translated_sentences

  bleu_score = calculate_bleu_score(translated_sentences)
  print "System BLEU Score:", bleu_score

if __name__ == '__main__':
    main()
