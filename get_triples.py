import re
import spacy
import neuralcoref
from pycorenlp import *
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
nlp = spacy.load('en_core_web_sm')
neuralcoref.add_to_pipe(nlp)

standford_nlp = StanfordCoreNLP("http://localhost:9000/")
caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    if text.strip().endswith("<stop>"):
        sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

def neuralcorefIt(text):
    sentences = split_into_sentences(text)
#     sentences[0] = sentences[0].capitalize()
    for s in sentences:
        if s[-1] == '?':
            sentences.remove(s)
    result = ""
    for sentence in sentences:
        doc = nlp(sentence)
        result += " " + doc._.coref_resolved
    return result.strip()

def getPresentTense(triples):
    lmtzr = WordNetLemmatizer()
    for t in range(0, len(triples)):
        for i in range(0,len(triples[t])):
            for word in triples[t][i].split(" "):
                triples[t][i] = triples[t][i].replace(word, lmtzr.lemmatize(word,'v'))
    return triples

def produceTriples(text):
    processedText = neuralcorefIt(text)
    output = standford_nlp.annotate(processedText,
                          properties={"annotators":"tokenize,ssplit,pos,lemma,depparse,natlog,openie,dcoref",
                                      "outputFormat": "json","triple.strict":"true"})
    triples = []
    result2 = []
    # result = [output["sentences"][0]["openie"] for item in output]
    for i in range(0,len(output["sentences"])):
        result2.append(output['sentences'][i]['openie'])
        for i in range(0, len(result2)):
            for rel in result2[i]:
                subj = rel['subject']
                obj = rel['object']
                for ref in output['corefs']:
                    if len(output['corefs'][ref]) > 1 and output['corefs'][ref][1]['position'][0] == i + 1:
                        if output['corefs'][ref][1]['text'] == subj:
                            subj = output['corefs'][ref][0]['text']
                relationSent=[subj.lower(), obj.lower(), rel['relation'].lower()]
                triples.append(relationSent)
    return getPresentTense(triples)

from tqdm import tqdm

def write_to_file(triples, out_put_file):
    file_out = open(out_put_file, 'w')
    for triple in tqdm(triples):
        line = "\t".join(triple)
        file_out.write(line + "\n")
    file_out.close()

# def addTriples(sentence):
#     triples = produceTriples(sentence)
#     return triples