from collections import Counter
from random import choice
from nltk.corpus import stopwords as stop
from textblob_aptagger import PerceptronTagger
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import sentence_tokenizer
import re
import sys

class Container:
    """Refers to the words being held as we pull them out"""
    def __init__(self):
        self.next_word = Counter() # refers to number of times a word appears

    def add_next_word(self, word):
        """Adds word to data structure and increments number of times seen"""
        self.next_word[word] += 1


class NGrammer(PorterStemmer, SnowballStemmer):
    
    def generate_from_string(self, order, text):
        """Generate words based from string"""
        text = re.sub("""[,\.?"-\'!:;]""",'', text)
        conts = {}
        conts = NGrammer.make_containers(order, text)
        first_token = choice(list(conts.keys())) 
        this_token = first_token
        generated_words = []
        generated_words += list(this_token)
        next_word = "" 

        for i in generated_words:
            if conts.has_key(this_token):
                next_word = NGrammer.most_common(2, conts[this_token])
            else:
                this_token = choice(list(conts.keys()))
                next_word = NGrammer.most_common(2, conts[this_token])

            temp = list(this_token)
            temp.pop(0) 
            temp.append(next_word) 
            next_token = tuple(temp)
            this_token = next_token
            generated_words += [next_word]

        return(generated_words)
        

    def generate(self, order, text):
        """Generate words from text file"""
            
        text = re.sub('[,\.?"-\'!:;]','', text)
        conts = {}
        conts = NGrammer.make_containers(order, text)

        first_token = choice(list(conts.keys())) 
        this_token = first_token
        generated_words = []
        generated_words += list(this_token)
        next_word = "" 

        for i in generated_words:
            next_word = NGrammer.most_common(1, conts[this_token])
            temp = list(this_token)
            temp.pop(0) # remove first word in token
            temp.append(next_word) # add new word to the token
            next_token = tuple(temp)
            this_token = next_token
            generated_words += [next_word]

        print(' '.join(generated_words))
        

    def make_containers(self, order, text):
        """Makes unique container with the different words, for the text"""
        conts = dict()
        words = re.findall(r"([\w]+)", text)
        token = []
        next_word = ''
        for i in range(len(words)-order):
            next_word = words[i+order]
            for j in range(order):
                token.append(words[i+j])
            if tuple(token) not in conts:
                conts[tuple(token)] = Container()
                conts[tuple(token)].add_next_word(next_word)
            else:
                conts[tuple(token)].add_next_word(next_word)
        return conts

    def most_common(self, n, conts):
        """Returns most frequent word"""
        return Counter.most_common(conts)
        
    def trim_threshold(self, conts, lowThresh, highThresh):
        for key, value in conts: 
            if value < lowThresh or value > highThresh:
                conts.pop(key)
        return conts 
    
    def print_containers(self, conts):
        for token in conts.keys():
            print("key %s : nextword %s" %(token, conts[token].next_word))
          
        
class Word(PerceptronTagger):
    """Works on the individual word"""
    
    # class member variables - static
    port = PorterStemmer()
    lemma = WordNetLemmatizer()
    snow = SnowballStemmer('english')
    
    def __init__(self):
        self.tokens = []
        self.word = None
        self.context = None
        self.start = None
        self.end = None
        
    def normalize(self, word):
        if word.isalpha():
            new = word.lower()
            return new
        else: 
            return word

    def snow_stemmer(self, tokens, snow):
        self.tokens = [snow.stem(x) for x in tokens]
        
    def porter_stemmer(self, tokens, port):
        self.tokens = [port.stem(x) for x in tokens]
        
    def lemmatizer(self, tokens, lemma):
        self.tokens = [lemma.lemmatize(x) for x in tokens]
                
    def stop_words(self, words):
        stopwords = set(stop.words('english')) 
        tokens = [t for t in words if t not in stopwords]
        self.tokens = tokens
        
    def tag(self, tokens):
        prev, prev2 = self.start
        tags = []
        context = self.start + [self.normalize(w) for w in tokens] + self.end
        for tokens, word in enumerate(tokens):
            tag = self.tagdict.get()
            if not tag:
                features = self.__init__(tokens, word, context, prev, prev2)
                tag = self.model.predict(features) 
            tags.append(tag)
            prev2 = prev
            prev = tag
        return tags
    
    def get_tokens(self):
        return self.tokens  


        
    

if __name__ == "__main__":
    """ Accepts command line Argument, should be of the format:
    
            python filename.py directoryName 
                *for default setting, which assumes lemmatizing, word
                    tagging, and no stop words, stemmers, or threshold
                
            otherwise, should be of format:
                
            python filename.py directoryName option1 parameter1 parameter2 ... option2 parameter1 ... option3 ...
                Options include:
                    word tagging: tag
                    lemmatizing: lemmatizer
                    trim threshold: thresh
                    stop words: stop
                    snow stemmer: snow
                    porter stemmer: port
                parameters include:
                    stop words: 1. filename of stopwords (.txt file)
                    trim threshold: 1. lowThreshold, 2. highThreshold
                    
                            """
    NGrammer = NGrammer()
    Word = Word()
    docs = sentence_tokenizer.dir_sents(sys.argv[1]) 
    #print(sents)
    order = 0
    
    if "stop" in sys.argv: 
        index = sys.argv.index("stop")
        filename = sys.argv[index+1]
        with open(filename) as f:
            lines = f.read().splitlines()
    if "thresh" in sys.argv:
        index = sys.argv.index("thresh")
        lowThresh = sys.argv[index+1]
        highThresh = sys.argv[index+2]
    for doc in docs:
        for sent in doc:            
            #sentence = NGrammer.generate(order, sent)
            words = NGrammer.generate_from_string(order, sent)
            print(words)
            break
            if len(sys.argv) == 1 or "lemmatizer" in sys.argv:
                dictionary = Word.lemmatizer(words, Word.lemma)
            if len(sys.argv) == 1 or "tag" in sys.argv: 
                key1 = Word.tag(sent)
            if "snow" in sys.argv: 
                words = Word.snow_stemmer(words, Word.lemma)
            if "port" in sys.argv: 
                words = Word.porter_stemmer(words, Word.lemma)
            if "stop" in sys.argv:
                Word.stop_words(lines)
            if "thresh" in sys.argv:
                NGrammer.trim_threshold(words, lowThresh, highThresh)
            order ++ 1
