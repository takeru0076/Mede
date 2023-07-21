#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 06:22:09 2019

@author: kkyle2
"""
#version .02 2019-8-9
#includes a number of minor bug fixes

import glob
import spacy #import spacy
nlp = spacy.load("en_core_web_sm") #load the English model. This can be changed - just make sure that you download the appropriate model first

def tag(text,tp = "upos", lemma = True, lower = True, connect = "_",ignore = ["PUNCT","SPACE","SYM"]):
	
	#check to make sure a valid tag was chosen
	if tp not in ["penn","upos","dep"]:
		print("Please use a valid tag type: 'penn','upos', or 'dep'")
		return #exit the function
	
	else:
		doc = nlp(text) #use spacy to tokenize, lemmatize, pos tag, and parse the text
		text_list = [] #empty list for output
		for token in doc: #iterate through the tokens in the document
			if token.pos_ in ignore: #if the universal POS tag is in our ignore list, then move to next word
				continue
			
			if lemma == True: #if we chose lemma (this is the default)
				word = token.lemma_ #then the word form will be a lemma
			else:
				if lower == True: #if we we chose lemma = False but we want our words lowered (this is default)
					word = token.text.lower() #then lower the word
				else:
					word = token.text #if we chose lemma = False and lower = False, just give us the word
			
			if tp == None: #if tp = None, then just give the tokenized word (and nothing else)
				text_list.append(word)
			
			else:
				if tp == "penn":
					tagged = token.tag_ #modified penn tag
				elif tp == "upos":
					tagged = token.pos_ #universal pos tag
				elif tp == "dep":
					tagged = token.dep_ #dependency relationship
			
			tagged_token = word + connect + tagged #add word, connector ("_" by default), and tag
			text_list.append(tagged_token) #add to list
		
		return(text_list) #return text list
		
		

def tag_corpus(dirname, ending = ".txt", tp = "upos", lemma = True, lower = True, connect = "_",ignore = ["PUNCT","SPACE"]):
	filenames = glob.glob(dirname + "/*" + ending) #gather all text names
	master_corpus = [] #holder for total corpus
	
	file_count  = 1 #this is to give the user updates about the pogram's progress
	total = len(filenames) #this is the total number of files to process
	for filename in filenames: #iterate through corpus filenames
		#user message
		print("Tagging " + str(file_count) + " of " + str(total) + " files.")
		file_count += 1 #add one to the file_count
		
		raw_text = open(filename, errors = "ignore").read() #open each file
		master_corpus.append(tag(raw_text,tp,lemma,lower,connect,ignore)) #add the tagged text to the master list
	
	return(master_corpus) #return list
	

#tag_corpus("small_sample")
#sample = "This is a sample text.!?"
#tag(sample)
#tag(sample,tag="dep")
#tag(sample, tag = "penn")
#tag(sample,lemma = False)
#
#doc = nlp(sample)
#for x in doc:
#	print(x.text,x.lemma_x.tag_,x.pos_,x.dep_)
