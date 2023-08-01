'''

Lines 20 through 28 and 35 through 43 were copied from https://github.com/kristopherkyle/Corpus-Methods-Intro/blob/master/Python_Tutorial_8.md.

'''
import corpus_toolkit as ct
import corpus_nlp as tg
import os
import sys
import glob

print("Input the directory name containing corpus file. ") #feature3
name = input()

if(os.path.isdir(name) != True):
  print(name + " didn't find directory")
  sys.exit()

#
word = ct.load_corpus(name) #read all corpus files
#print(type(word))
print(len(word)) #double check that there are 500 files. If not, check your directory (see point 2 above) and check your directory name

word_tokenized = ct.tokenize(word) #tokenize corpus

word_lemmatized = ct.lemmatize(word_tokenized) #create lemmatized version of the text

lemma_freq = ct.corpus_frequency(word_lemmatized) #feature1, feature2
#print(lemma_freq)
#ct.high_val(lemma_freq) #use high_val function to see top 20 hits

ct.find_least(name) #feature7, featurre9, feature10

#our lemmatized corpus will be written to a directory/folder entitled "word_single_lemmas" in our working directory
ct.write_corpus(name, name + "_lemmas",word_lemmatized)

#tag the word corpus using default settings (lemmas and upos tags)
#feature13
word_upos = tg.tag_corpus(name) #feature13, this may take a while. Consider getting some coffee!
print(len(word_upos)) #check to make sure that there are 500 files here! Otherwise, there is a problem with your directory name OR your working directory!

#write tagged corpus files to a folder/directory entitled "word_single_tagged"
ct.write_corpus(name ,name + "_tagged",word_upos)

ct.display_string(word_lemmatized)#feature14,feature15

ct.search_pos(word_upos)#feature16

pos, count = tg.count_pos(word_lemmatized, name)#feature17

#print(pos)
#print(count)

ct.pos_least(pos, count, name)#feature20, feature21, feature22