#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#version .02 2019-8-9
#includes a number of minor bug fixes
import glob
import math
import operator
import math
#for writing modified corpus files
import os
import sys
import shutil

'''
copied from https://github.com/kristopherkyle/Corpus-Methods-Intro/blob/master/Python_Tutorial_7.md
'''
def write_corpus(dirname,new_dirname,corpus,ending = "txt"):
	dirsep = os.path.sep
	name_list = []
	for x in glob.glob(dirname + "/*" + ending):
		simple_name = x.split(dirsep)[-1] #split the long directory name by the file separator and take the last item (the short filename)
		name_list.append(simple_name)
	if len(name_list) != len(corpus):
		print("Your directory name and your corpus don't match. Please correct this and try again")
		return
	try:	
		os.mkdir(new_dirname + "/") #make the new folder
	except FileExistsError: #if folder already exists, then print message
		print("Writing files to existing folder")
		
	for i, document in enumerate(corpus): #use enumerate to iterate through the corpus list
		new_filename = new_dirname + "/" + name_list[i] #create new filename
		outf = open(new_filename,"w") #create outfile with new filename
		corpus_string = " ".join(document) #turn corpus list into string
		outf.write(corpus_string) #write corpus list
		outf.flush()
		outf.close()
	
'''
copied from https://github.com/kristopherkyle/Corpus-Methods-Intro/blob/master/Python_Tutorial_4.md
'''
def load_lemma(lemma_file): #this is how we load a lemma_list
	lemma_dict = {} #empty dictionary for {token : lemma} key : value pairs
	lemma_list = open(lemma_file, errors = "ignore").read() #open lemma_list
	lemma_list = lemma_list.replace("\t->","") #replace marker, if it exists
	lemma_list = lemma_list.split("\n") #split on newline characters
	for line in lemma_list: #iterate through each line
		tokens = line.split("\t") #split each line into tokens
		if len(tokens) <= 2: #if there are only two items in the token list, skip the item (this fixed some problems with the antconc list)
			continue
		lemma = tokens[0] #the lemma is the first item on the list
		for token in tokens[1:]: #iterate through every token, starting with the second one
			if token in lemma_dict:#if the token has already been assigned a lemma - this solved some problems in the antconc list
				continue
			else: 
				lemma_dict[token] = lemma #make the key the word, and the lemma the value
	
	return(lemma_dict)
			
				
lemma_dict = load_lemma("antbnc_lemmas_ver_003.txt")
#family_dict = load_lemma("classic_familizer_dict_antconc.txt")

'''
copied from https://github.com/kristopherkyle/Corpus-Methods-Intro/blob/master/Python_Tutorial_4.md
'''
#this function will load the whole corpus into memory. This is fine for small to medium-sized corpora, but won't work with huge corpora
def load_corpus(dir_name, ending = '.txt', lower = True): #this function takes a directory/folder name as an argument, and returns a list of strings (each string is a document)
	master_corpus = [] #empty list for storing the corpus documents
	filenames = glob.glob(dir_name + "/*" + ending) #make a list of all ".txt" files in the directory
	for filename in filenames: #iterate through the list of filenames
		if lower == True:
			master_corpus.append(open(filename, errors = "ignore").read().lower()) #open each file, lower it and add strings to list
		else:
			master_corpus.append(open(filename, errors = "ignore").read())#open each file, (but don't lower it) and add strings to list
			
	return(master_corpus) #output list of strings (i.e., the corpus)

### Example ###
# make sure that your folder name is correct and that you have set your working directory!!! ###

#sample_corpus = load_corpus("small_sample") #create a list strings (each list item will be a corpus document)
#print(sample_corpus[0]) #print first item in corpus
#
##or, we can print all items in the corpus:
#for x in sample_corpus:
#	print(x)

#This function will clean up and tokenize our corpus.
#First, it will delete any items in the list we give it (optional)
#then, it will turn each string (document) into a list of strings

default_punct_list = [",",".","?","'",'"',"!",":",";","(",")","[","]","''","``","--"] #we can add more items to this if needed
default_space_list = ["\n","\t","    ","   ","  "]

'''
copied from https://github.com/kristopherkyle/Corpus-Methods-Intro/blob/master/Python_Tutorial_4.md
'''
def tokenize(corpus_list, remove_list = default_punct_list, space_list = default_space_list, split_token = " "):
	master_corpus = [] #holder list for entire corpus
	
	for text in corpus_list: #iterate through each string in the corpus_list
		for item in remove_list:
			text = text.replace(item,"") #replace each item in list with "" (i.e., nothing)
		for item in space_list:
			text = text.replace(item," ")
			
		#then we will tokenize the document and add it to the corpus
		tokenized = text.split(split_token) #split string into list using the split token (by default this is a space " ")
	
		master_corpus.append(tokenized) #add tokenized text to the master_corpus list
	
	return(master_corpus)

### Examples ###

#tokenized_sample = tokenize([sample_corpus[0]]) #we can process a single text by placing it in a list
#print(tokenized_sample)
#
#tokenized_corpus = tokenize(sample_corpus)
#print(tokenized_corpus)

'''
copied from https://github.com/kristopherkyle/Corpus-Methods-Intro/blob/master/Python_Tutorial_4.md
'''
def lemmatize(tokenized_corpus,lemma = lemma_dict): #takes a list of lists (a tokenized corpus) and a lemma dictionary as arguments
	master_corpus = [] #holder for lemma corpus
	for text in tokenized_corpus: #iterate through corpus documents
		lemma_text = [] #holder for lemma text
		
		for word in text: #iterate through words in text
			if word in lemma: #if word is in lemma dictionary
				lemma_text.append(lemma[word]) #add the lemma for to lemma_text
			else:
				lemma_text.append(word) #otherwise, add the raw word to the lemma_text
		
		master_corpus.append(lemma_text) #add lemma version of the text to the master corpus
	
	return(master_corpus) #return lemmatized corpus
		
#lemmatized_corpus = lemmatize(tokenized_corpus, lemma = lemma_dict)

#print(lemmatized_corpus)

#n-grams
#Takes a tokenized list and converts it into a list of n-grams
'''
copied from https://github.com/kristopherkyle/Corpus-Methods-Intro/blob/master/Python_Tutorial_4.md
'''
def ngrammer(tokenized_corpus,number):
	master_ngram_list = [] #list for entire corpus
	
	for tokenized in tokenized_corpus:
		ngram_list = [] #empty list for ngrams
		last_index = len(tokenized) - 1 #this will let us know what the last index number is
		for i , token in enumerate(tokenized): #enumerate allows us to get the index number for each iteration (this is i) and the item
			if i + number > last_index: #if the next index doesn't exist (because it is larger than the last index)
				continue
			else:
				ngram = tokenized[i:i+number] #the ngram will start at the current word, and continue until the nth word
				ngram_string = "_".join(ngram) #turn list of words into an n-gram string
				ngram_list.append(ngram_string) #add string to ngram_list
		
		master_ngram_list.append(ngram_list) #add ngram_list to master list
		
	return(master_ngram_list)
		 
### Examples

#sample_bigram = ngrammer(tokenized_sample,2)
#sample_trigram = ngrammer(tokenized_sample,3)
#
#corpus_bigram = ngrammer(tokenized_corpus,2)
#corpus_trigram = ngrammer(tokenized_corpus,3)

###
'''
copied from https://github.com/kristopherkyle/Corpus-Methods-Intro/blob/master/Python_Tutorial_5.md
'''
ignore_list = [""," ", "  ", "   ", "    "] #list of items we want to ignore in our frequency calculations

def corpus_frequency(corpus_list, ignore = ignore_list, calc = 'freq', normed = False): #options for calc are 'freq' or 'range'
	freq_dict = {} #empty dictionary
	
	for tokenized in corpus_list: #iterate through the tokenized texts
		if calc == 'range': #if range was selected:
			tokenized = list(set(tokenized)) #this creates a list of types (unique words)
		
		for token in tokenized: #iterate through each word in the texts
			if token in ignore_list: #if token is in ignore list
				continue #move on to next word
			if token not in freq_dict: #if the token isn't already in the dictionary:
				freq_dict[token] = 1 #set the token as the key and the value as 1
			else: #if it is in the dictionary
				freq_dict[token] += 1 #add one to the count
	
	### Normalization:
	if normed == True and calc == 'freq':
		corp_size = sum(freq_dict.values()) #this sums all of the values in the dictionary
		for x in freq_dict:
			freq_dict[x] = freq_dict[x]/corp_size * 1000000 #norm per million words
	elif normed == True and calc == "range":
		corp_size = len(corpus_list) #number of documents in corpus
		for x in freq_dict:
			freq_dict[x] = freq_dict[x]/corp_size * 100 #create percentage (norm by 100)
	
	return(freq_dict)

### Examples ###
#output frequency dictionary
#corp_freq = corpus_frequency(tokenized_corpus)
#print(corp_freq["this"])
#
#corp_freq_normalized = corpus_frequency(tokenized_corpus,normed = True)
#print(corp_freq_normalized["this"])
#
##output range dictionary
#corp_range = corpus_frequency(tokenized_corpus,calc = 'range')
#print(corp_range["this"])

def find_least(dir_name, ending = '.txt', lower = True):
	print("Input the question corpus file name without .txt")
	q_name = input()
	q_file = (open(dir_name + "/" + q_name + ending, errors = "ignore").read().lower())
	q_file_list = q_file.split()

	master_corpus = [] #empty list for storing the corpus documents
	filenames = glob.glob(dir_name + "/*" + ending) #make a list of all ".txt" files in the directory

	#print(type(q_file))

	least = 0
	key_corpus = {}

	q_file_tokenized= tokenize(q_file_list)
	#print(q_file_tokenized)
	q_file_lemmatized = lemmatize(q_file_tokenized)
	#print(q_file_lemmatized)
	q_freq = corpus_frequency(q_file_lemmatized)
	#print(q_freq)
	sorted_q_freq = dict(sorted(q_freq.items(), key=lambda item: item[1], reverse=True))
	#print(sorted_q_freq)

	for filename in filenames: #iterate through the list of filenames
		#print(type(filename))
		if q_name+ending == filename : 
			#print(filename)
			continue
		if lower == True:
			master_corpus = (open(filename, errors = "ignore").read().lower()) #open each file, lower it and add strings to list
		else:
			master_corpus = (open(filename, errors = "ignore").read())#open each file, (but don't lower it) and add strings to list

		#print(master_corpus) -> ok
		master_corpus_list = master_corpus.split()
		#print(type(master_corpus_list))
		master_tokenized = tokenize(master_corpus_list)
		master_lemmatized = lemmatize(master_tokenized)
		master_freq = corpus_frequency(master_lemmatized)
		#print(master_freq)

		sorted_freq = dict(sorted(master_freq.items(), key=lambda item: item[1], reverse=True))
		#print(sorted_freq) -> x

		print("top 20 words of " + filename)
		print()
		flag = 1
		for i,v in sorted_freq.items():
			print(i + ":" + str(v))
			flag = flag + 1
			if(flag == 20):
				break

		count_i = 0
		sum  = 0

		for i in sorted_q_freq:
			for j,v in sorted_freq.items() :
				if (i == j):
					sum = sum + v
					break
			count_i = count_i + 1
			if(count_i == 19):
				break

		if(sum < least or least == 0):
			file = filename
			least = sum

		
	print("Least similar data set is " + file)
	
	file_list = file.split("/")
	file = file_list[1]

	print("Do you want to rule out " + file + "?")
	print("y / n : ", end = ' ')
	rep = input()
	if(rep == "y"):
		source_file =  dir_name + "/" + file
		destination_file = "removed/" + file
		shutil.move(source_file, destination_file)

		if os.path.exists(destination_file):
			print("success to remove file in the removed")
		else:
			print("fail to remove file")
	return

def display_string(corpus) :
	while (True) :
		flag = True	#word->True, string->False
		print('')
		print('Input the word or string you wish to search for (Exit : -1)')
		search = (input())
		if (search == '-1') :
			break
		if ' ' in search :	#If a string is entered
			search = search.split(' ')
		if (isinstance(search, list) == True) :
			flag = False
		for i in range(len(corpus)) :
			for v in range(len(corpus[i])) :
				if flag :
					if search.lower() == corpus[i][v] :
						for j in range(13) :
							if (v-6+j < 0 or v-6+j == len(corpus[i])) :
								break
							else :
								print(corpus[i][v-6+j], end=' ')	#show 6 words before the target and 6 after the target word
						print('')
				else :
					for k in range(len(search)) :
						if (search[k].lower() == corpus[i][v+k]) :
							if (k == len(search)-1) : 	#If all words are equal
								for j in range(13+len(search)-1) :
									if (v-6+j < 0 or v-6+j == len(corpus[i])) :
										break
									else :
										print(corpus[i][v-6+j], end=' ')
								print('')
						else :
							break
	return

def search_pos(corpus) :
	dict1 = {}	#all POS patterns following the target word
	dict2 = {}	#A dictionary that contains the POS pattern following the target word only once.
	print()
	print('search for POS patterns following the target word.')
	print('e.g.')
	print('absolutely')
	print('JJ')
	while (True) :
		print('')
		print('Input the word you wish to search for (Exit : -1)')
		search = (input())
		if (search == '-1') :	##If -1 is entered, exit
			break
		for i in range(len(corpus)) :
			for v in range(len(corpus[i])) :
				if ((search+'_') in corpus[i][v]) : 
					if (v+1 == len(corpus[i])) :	#Break if the word is at the end of a sentence
						break
					dict1[corpus[i][v+1]] = 1	#Add POS following the word
		keys_view = dict1.keys()	#Create a List with keys from the dictionary
		for i in keys_view :
			index = i.find('_')
			pos = i[index+1:]
			dict2[pos] = 1
		keys_view = dict2.keys()
		for i in keys_view :
			print(i)
		dict1.clear()	#Clear so as not to affect the next data.
		dict2.clear()
	return

def pos_least(pos, count, dir) :
	sum = [0 for i in range(len(pos))]	#Sum of POS patterns for each dataset
	flag = False	#Whether the filename of the input data exists

	while True :
		print("Input the question corpus file name included extension(Exit = -1)")
		q_name = input()
		if q_name == '-1' :	#If -1 is entered, exit
			return
		
		file_list = os.listdir(dir)
		for num in range(len(file_list)) :
			if q_name == file_list[num] :
				index = num	#The qestion data is in file_list[index].
				flag = True
		if flag == False :
			print('does not exist')
		else :
			break

	for i in range(len(pos)) :
		if index == i :	#If the data is in qestion, move on to the next data.
			continue
		for j in range(len(pos[index])) :
			for k in range(len(pos[i])) :
				if pos[index][j] == pos[i][k] :
					sum[i] = sum[i] + count[i][k]	#Add up the same POS patterns that are in the Qestion's data

	min = sum[0]
	file = 0
	if index == 0 :
		min = sum[1]
		file = 1
	for i in range(1, len(sum)) :
		if index == i :
			continue
		if (min > sum[i]) :
			file = i
			min = sum[i]
	print('Least similar data set is ' + file_list[file])

	print("Do you want to rule out " + file_list[file] + "?")	#The following is an operation to exclude data sets with low similarity from the directory
	print("y / n : ", end=' ')
	rep = input()
	if(rep == "y"):
		source_file = dir + "/" + file_list[file]
		destination_file = "removed/" + file_list[file]
		shutil.move(source_file, destination_file)

		if os.path.exists(destination_file):
			print("success to remove file in the removed")
		else: 
			print("fail to remove file")
	return