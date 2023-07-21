import re

import operator
import math

from numpy import shape

ignore_list = [""," ", "  ", "   ", "    "] #list of items we want to ignore in our frequency calculations

def corpus_frequency(corpus_list, ignore = ignore_list, calc = 'freq', normed = False): #options for calc are 'freq' or 'range'
	freq_dict = {} #empty dictionary

	for tokenized in corpus_list: #iterate through the tokenized texts
		if calc == 'range': #if range was selected:
			tokenized = list(set(tokenized)) #this creates a list of types (unique words)
			print(tokenized)

		for token in tokenized: #iterate through each word in the texts
			print(token)
			if token in ignore_list: #if token is in ignore list
				continue #move on to next word
			if token not in freq_dict: #if the token isn't already in the dictionary:
				freq_dict[token] = 1 #set the token as the key and the value as 1
			else: #if it is in the dictionary
				freq_dict[token] += 1 #add one to the count

	print(freq_dict)

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
			print("OK")
			keyness_dict[item] = log_ratio(freq_dict1[item],size1,freq_dict2[item],size2)

		elif effect == "%diff":
			keyness_dict[item] = perc_diff(freq_dict1[item],size1,freq_dict2[item],size2)

		elif effect == "odds-ratio":
			keyness_dict[item] = odds_ratio(freq_dict1[item],size1,freq_dict2[item],size2)

	return(keyness_dict)


#print("enter number of files")
#n = input()
#for i in range(n) :
#	filename.append(input())
path = '/Users/kabukikota/Library/Mobile Documents/com~apple~CloudDocs/share/Datasets/Q dataset.txt'
with open(path) as f:
	tokenized_corpus = re.split('[.,\n ]',f.read())
#print(tokenized_corpus)
print(len(tokenized_corpus))

corp_freq = corpus_frequency(tokenized_corpus)
#print(corp_freq["this"])

corp_freq_normalized = corpus_frequency(tokenized_corpus,normed = True)
#print(corp_freq_normalized["this"])

corp_range = corpus_frequency(tokenized_corpus,calc = 'range')
#print(corp_range["this"])

corp_range_normalized = corpus_frequency(tokenized_corpus,calc = 'range',normed = True)
#print(corp_range["this"])

high_val(corp_freq)

high_list = high_val(corp_freq, output = True)

high_val(corp_freq,filename = "freq_results.txt")