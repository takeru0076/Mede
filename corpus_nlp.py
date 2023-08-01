#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#version .02 2019-8-9
#includes a number of minor bug fixes
import os
import glob
import spacy #import spacy
nlp = spacy.load("en_core_web_sm") #load the English model. This can be changed - just make sure that you download the appropriate model first

'''
copied from https://github.com/kristopherkyle/Corpus-Methods-Intro/blob/master/Python_Tutorial_7.md
'''
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

'''
copied from https://github.com/kristopherkyle/Corpus-Methods-Intro/blob/master/Python_Tutorial_7.md
'''
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

def count_pos(corpus, dir) :
	pos = [0 for i in range(len(corpus))]	#Create a List for each file(POS pattern).
	count = [0 for i in range(len(corpus))]	#Create a List for each file(number of POS pattern).
	dict = {}	#POS pattern
	file_list = os.listdir(dir)

	for num in range(len(corpus)) :
		cnt = 0
		for sentence in corpus[num]:
			doc = nlp(sentence)
			'''
			"pos_pattern = tuple(token.pos_ for token in doc)" this code was copied from chatGPT
			https://chat.openai.com/c/ed981557-3e41-4d83-b7a8-21f96c36c783
			'''
			pos_pattern = tuple(token.pos_ for token in doc)

			if pos_pattern in dict:
				dict[pos_pattern] += 1	#If the POS pattern is already in the dictionary, add +1
			else:
				dict[pos_pattern] = 1	#If the POS pattern is not in the dictionary, add a new one.
		
		#Make a List
		#the number of POS patterns for each file.
		pos[num] = [0 for j in range(len(dict))]
		count[num] = [0 for j in range(len(dict))]
		print(file_list[num] + ' :')
		for key, value in dict.items() :
			pos[num][cnt] = key
			count[num][cnt] = value
			cnt = cnt + 1
			print(key, value)
		print()
		dict.clear()

	return pos, count