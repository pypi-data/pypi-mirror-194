import os
import json
import pymorphy2
import spacy
from natasha import (Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger,
                     NewsSyntaxParser, NewsNERTagger, Doc)
# for spacy
nlp = spacy.load("ru_core_news_sm")
nlp.max_length = 20000000
# for pymorphy2
morph = pymorphy2.MorphAnalyzer()
# for natasha
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

BASE_DIR = os.path.dirname(__file__)

class ExtractMosToponyms():
    def __init__(self, text):
        self.text = text

    def spacy_extract(self):
        spacy_dict = {}
        spacy_names = {}

        doc_spacy = nlp(self.text)

        for ent in doc_spacy.ents:
            if ent.label_ == 'LOC':
                twice_lem = morph.parse(ent.lemma_)[0]
                spacy_dict[ent.start_char] = twice_lem.normal_form
            elif ent.label_ == 'PER':
                spacy_names[ent.start_char] = ent.lemma_
        return spacy_dict, spacy_names

    def natasha_extract(self):  
        natasha_dict = {}
        natasha_names = {}
                        
        doc_natasha = Doc(self.text)
        doc_natasha.segment(segmenter)
        doc_natasha.tag_morph(morph_tagger)
        doc_natasha.parse_syntax(syntax_parser)
        doc_natasha.tag_ner(ner_tagger)

        for span in doc_natasha.spans:
            if span.type == 'LOC':
                span.normalize(morph_vocab)
                natasha_dict[span.start] = [span.text, span.normal, span.stop]  
            elif span.type == 'PER':
                span.normalize(morph_vocab)
                natasha_names[span.start] = (span.normal)
        return natasha_dict, natasha_names

    def merging_blacklists(self, spacy_names, natasha_names):
        extracted_names = []
        for i in spacy_names.keys():
            position = i
            if position in natasha_names.keys():
                if natasha_names[position] not in extracted_names:
                    extracted_names.append(natasha_names[position])
        with open(os.path.join(BASE_DIR, 'black_list.json')) as f:
            black_list = json.load(f)
        full_black_list = black_list + extracted_names
        return full_black_list

    def inner_merging_filtering(self, full_black_list, spacy_dict, natasha_dict):
        pre_final_spacy = {}
        pre_final_natasha = {}
        for i in spacy_dict.keys():
            position = i
            if position in natasha_dict.keys():
                loc_n = natasha_dict[position][1]
                loc_s = spacy_dict[position] # (the spelling can differ from loc_n after lemmatization)
                if loc_n not in full_black_list:
                    pre_final_natasha[position] = [natasha_dict[position][0], loc_n, natasha_dict[position][2]]  
                if loc_s not in full_black_list:
                    pre_final_spacy[position] = loc_s
        
        final_result = []
        for i in pre_final_spacy.keys():
            position = i
            if position in pre_final_natasha.keys():
                location_org = pre_final_natasha[position][0]
                location_lem = pre_final_natasha[position][1]
                start_value = position
                stop_value = pre_final_natasha[position][2]
                final_dict = {'toponym': location_org, 'lemmatized_toponym':location_lem, 'start_char':start_value, 'stop_char':stop_value}
                final_result.append(final_dict)
        return final_result 

      
class QuickExtract():
    def __init__(self, text):
        self.text = text
    
    def extract(self):
        extract_toponyms = ExtractMosToponyms(self.text)

        spacy_extracted = extract_toponyms.spacy_extract()
        spacy_dict = spacy_extracted[0]
        spacy_names = spacy_extracted[1]

        natasha_extractor = extract_toponyms.natasha_extract()
        natasha_dict = natasha_extractor[0]
        natasha_names = natasha_extractor[1]

        black_list = extract_toponyms.merging_blacklists(spacy_names, natasha_names)
        final_results = extract_toponyms.inner_merging_filtering(black_list, spacy_dict, natasha_dict)

        return final_results
