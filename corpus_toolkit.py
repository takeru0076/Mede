#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 08:00:19 2019

@author: kkyle2
"""
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


def keyness(freq_dict1,freq_dict2,effect = "log-ratio"): #this assumes that raw frequencies were used. effect options = "log-ratio", "%diff", "odds-ratio"
	keyness_dict = {}
	ref_dict = {}
	
	size1 = sum(freq_dict1.values())
	size2 = sum(freq_dict2.values())
	
	def log_ratio(freq1,size1,freq2,size2): #presumes that the frequencies are normed
		freq1_norm = freq1/size1 * 1000000
		freq2_norm = freq2/size2 * 1000000
		index = math.log2(freq1/freq2)
		return(index)
	
	def perc_diff(freq1,size1,freq2,size2):
		freq1_norm = freq1/size1 * 1000000
		freq2_norm = freq2/size2 * 1000000
		index = ((freq1_norm-freq2_norm)  * 100)/freq2_norm
		return(index)
	
	def odds_ratio(freq1,size1,freq2,size2):
		if size1 - freq1 == 0: #this will be a very rare case, but would kill program
			size1 += 1
		if size2 - freq2 == 0: #this will be a very rare case, but would kill program
			size2 += 1
		index = (freq1/(size1-freq1))/(freq2/(size2-freq2))
		return(index)
			
	
	#create combined word list (we will actually use a dictionary for speed)
	for x in freq_dict1:
		if x not in ref_dict:
			ref_dict[x] = 0 #the zero isn't used for anything
	for x in freq_dict2:
		if x not in ref_dict:
			ref_dict[x] = 0 #the zero isn't used for anything
	
	#if our item doesn't occur in one of our reference corpora, we need to make an adjustment
	#here, we change the frequency to a very small number (.00000001) instead of zero
	#this is because zeros will cause problems in our calculation of keyness
	for item in ref_dict:
		if item not in freq_dict1 or freq_dict1[item] == 0:
			freq_dict1[item] = .00000001 #tiny number
		if item not in freq_dict2 or freq_dict2[item] == 0:
			freq_dict2[item] = .00000001 #tiny number
		
		if effect == 'log-ratio':
			keyness_dict[item] = log_ratio(freq_dict1[item],size1,freq_dict2[item],size2)
		
		elif effect == "%diff":
			keyness_dict[item] = perc_diff(freq_dict1[item],size1,freq_dict2[item],size2)
		
		elif effect == "odds-ratio":
			keyness_dict[item] = odds_ratio(freq_dict1[item],size1,freq_dict2[item],size2)

	return(keyness_dict)

#key_dict = keyness({"word" : 6893, "poop" : 0},{"word" : 3784,"poop" : 4312})
#key_dict2 = keyness({"word" : 6893, "poop" : 0},{"word" : 3784,"poop" : 4312}, effect = "%diff")
#key_dict3 = keyness({"word" : 6893, "poop" : 0},{"word" : 3784,"poop" : 4312}, effect = "odds-ratio")

##############################
### Write Output to a file ###
##############################

def list_writer(outf_name,dict_list,header_list = ["word","frequency"],cutoff = 5, sep = ","):
	outf = open(outf_name, "w") #create output file
	
	outf.write(",".join(header_list) + "\n") #turn header_list into a string, then write the header
	
	#use the first dictionary in the dict_list for the basis of sorting
	#this will output a list of (word,frequency) tuples
	sorted_list = sorted(dict_list[0].items(),key=operator.itemgetter(1),reverse = True)
	
	for x in sorted_list: #iterate through (word, frequency) list items
		word = x[0]
		freq = x[1]
		if freq < cutoff: #if the frequency doesn't meet the frequency cutoff
			continue #skip that item
		out_list = [word] #create list for output that includes the word
		for entry in dict_list: #iterate through all dictionaries in the dict_list (there may only be one)
			if word in entry: #make sure entry is in dictionary
				out_list.append(str(entry[word])) #add the value to the list. Note, we convert the value to a string using str()
			else:
				out_list.append("0") #if it isn't in the dictioanary, set it to "0"
		
		outf.write(sep.join(out_list) + "\n") #write the line to the file
	
	outf.flush() #flush the buffer
	outf.close()#close the file
	print("Finished writing file")
	
### Examples ###
#list_writer("sample_results.csv",dict_list = [corp_freq,corp_range], header_list = ["word","frequency","range"],cutoff = 2)
#
#list_writer("lemma_sample.csv", [corpus_frequency(lemmatized_corpus),corpus_frequency(lemmatized_corpus,calc = "range")],["word","frequency","range"],2)

def collocator(corpus_list,target, left = 4,right = 4, stat = "MI", cutoff = 5): #returns a dictionary of collocation values
	corp_freq = corpus_frequency(corpus_list) #use the corpus_frequency function to create frequency list
	nwords = sum(corp_freq.values()) #get corpus size for statistical calculations
	collocate_freq = {} #empty dictionary for storing collocation frequencies
	r_freq = {} #for hits to the right
	l_freq = {}  #for hits to the left
	stat_dict = {} #for storing the values for whichever stat was used
	
	def freq(l,d): #this takes a list (l) and a dictionary (d) as arguments
		for x in l: #for x in list
			if x not in d: #if x not in dictionary
				d[x] = 1 #create new entry
			else: #else: add one to entry
				d[x] += 1
	
	#begin collocation frequency analysis
	for text in corpus_list:
		if target not in text: #if target not in the text, don't search it for other words
			continue
		else:
			last_index = len(text) -1 #get last index number
			for i , word in enumerate(text):
				if word == target:
					start = i-left #beginning of left span
					end = i + right + 1 #end of right span. Note, we have to add 1 because of the way that slices work in python
					if start < 0: #if the left span goes beyond the text
						start = 0 #start at the first word
					#words to the right
					lspan_list = text[start:i] #for counting words on right
					freq(lspan_list,l_freq) #update l_freq dictionary
					freq(lspan_list,collocate_freq) #update collocate_freq dictionary
					
					rspan_list = text[i+1:end] #for counting words on left. Note, have to add +1 to ignore node word
					freq(rspan_list,r_freq) #update r_freq dictionary
					freq(rspan_list,collocate_freq) #update collocate_freq dictionary
	
	#begin collocation stat calculation

	for x in collocate_freq:
		observed = collocate_freq[x]
		if observed < cutoff: #if the collocate frequency doesn't meet the cutoff, ignore it
			continue
		else:
			expected = (corp_freq[target] * corp_freq[x])/nwords #expected = (frequency of target word (in entire corpus) * frequency of collocate (in entire corpus)) / number of words in corpus
			if stat == "MI": #pointwise mutual information
				mi_score = math.log2(observed/expected) #log base 2 of observed co-occurence/expected co-occurence
				stat_dict[x] = mi_score
			elif stat == "T": #t-score
				t_score = math.log2((observed - expected)/math.sqrt(expected))
				stat_dict[x] = t_score
			elif stat == "freq":
				stat_dict[x] = collocate_freq[x]
			elif stat == "right": #right frequency
				stat_dict[x] = r_freq[x] 
			elif stat == "left":
				stat_dict[x] = l_freq[x]
				
	return(stat_dict) #return stat dict


	
#print(sorted(corp_freq.items(),key=operator.itemgetter(1),reverse = True)[:20])
#
#collocator(tokenized_corpus,"in",stat = "MI")
#collocator(tokenized_corpus,"in",stat = "T")	
#collocator(tokenized_corpus,"in",stat = "freq")	
#collocator(tokenized_corpus,"in",stat = "right")	
#collocator(tokenized_corpus,"in",stat = "left")	

def high_val(stat_dict,hits = 20,hsort = True,output = False,filename = None, sep = "\t"):
	#first, create sorted list. Presumes that operator has been imported
	sorted_list = sorted(stat_dict.items(),key=operator.itemgetter(1),reverse = hsort)[:hits]
	
	if output == False and filename == None: #if we aren't writing a file or returning a list
		for x in sorted_list: #iterate through the output
			print(x[0] + "\t" + str(x[1])) #print the sorted list in a nice format
	
	elif filename is not None: #if a filename was provided
		outf = open(filename,"w") #create a blank file in the working directory using the filename
		for x in sorted_list: #iterate through list
			outf.write(x[0] + sep + str(x[1])+"\n") #write each line to a file using the separator
		outf.flush() #flush the file buffer
		outf.close() #close the file

	if output == True: #if output is true
		return(sorted_list) #return the sorted list

#high_val(corp_freq)
#high_list = high_val(corp_freq,output = True)
#high_val(corp_freq,filename = "top_freq.txt")
				
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

	print("Do you want to rule out " + file + "?")
	print("y / n : ", end = ' ')
	rep = input()
	if(rep == "y"):
		source_file = dir_name + "/" + file
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
		print("Input the question corpus file name including extension(Exit = -1)")
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