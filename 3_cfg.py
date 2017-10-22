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
        translated += '. '
    else:
      translated += '<OOV> '
  return translated

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

if __name__ == '__main__':
    main()
