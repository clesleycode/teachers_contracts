from nltk import sent_tokenize
import os
from unidecode import unidecode

def doc_sents_string(doc):
    """Returns the sentences in a document
    Input:
        doc: the document in string form
    Output:
        sents: a list of the sentences in the document
    """
    #use sent_tokenize and return
    sents = sent_tokenize(doc)
    return(sents)
    

def doc_sents(docFile,encode = "utf8"):
    """Returns the sentences in a text file
    Input:
        docFile: filepath for a text file
        encode: the encoding of the text file, defaults to utf8
    Output:
        sents: a list of sentences in the text file
    """
    #read the text file and return the sentences
    with open(docFile,'r',encoding = encode) as f:
        doc = unidecode(f.read())
        sents = doc_sents_string(doc)
        return(sents)
        
def corpus_sents(corpus,encoding = "utf8"):
    """Returns the sentences in each text file in a corpus
    Input:
        corpus: a list of filepaths to the text files
        encoding: the encoding of the text files, defaults to utf8
    Output:
        sents: a dictionary of lists of sentences in each text file.
                sents[fileName] = list of sentences
    """
    docs = []
    #iterate through the documents in the corpus
    for doc in corpus:
        #get the file name w/o extension
        path, fileName = os.path.split(doc)
        fName = os.path.splitext(fileName)[0]
        docs.append(doc_sents(doc,encode = encoding))

    return(docs)
    
def dir_sents(directory,encoding = "utf8"):
    """Returns the sentences in each text file in a directory
    Input:
        directory: filepath to the directory
        encoding: the encoding of the text files, defaults to utf8
    Output:
        sents: a dictionary of lists of sentences in each text file.
                sents[fileName] = list of sentences
    """
    #get a list of the files in a directory
    corpus = os.listdir(directory)
    #join the file path to the directory to the file names
    for i in range(len(corpus)):
        corpus[i] = os.path.join(directory,corpus[i])
    #get the sentences and return
    docs = corpus_sents(corpus)
    return(docs)
