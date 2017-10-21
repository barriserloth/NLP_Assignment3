import nltk
from nltk import CFG

def main():
   f = open('cfg_sentences.txt').readlines()
   sentences = ' '.join(f).replace('\n', '')
   text = nltk.word_tokenize(sentences)
   tagged_text = nltk.pos_tag(text)
   print tagged_text

   chart_parser = nltk.ChartParser(tagged_text)

   for tree in chart_parser.parse(text):
       print tree


if __name__ == '__main__':
    main()
