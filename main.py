#chatGPT
#https://chat.openai.com/c/ed981557-3e41-4d83-b7a8-21f96c36c783
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

word = ct.load_corpus(name) #read all corpus files
#print(type(word))
print(len(word)) #double check that there are 500 files. If not, check your directory (see point 2 above) and check your directory name

word_tokenized = ct.tokenize(word) #tokenize corpus

word_lemmatized = ct.lemmatize(word_tokenized) #create lemmatized version of the text
word_bigrams = ct.ngrammer(word_tokenized,2) #create bigram version
word_trigrams = ct.ngrammer(word_tokenized,3) #create trigram version

lemma_freq = ct.corpus_frequency(word_lemmatized) #feature1, feature2
#print(lemma_freq)
#ct.high_val(lemma_freq) #use high_val function to see top 20 hits

ct.find_least(name) #feature7, featurre9, feature10

run_collocates_mi = ct.collocator(word_lemmatized,"run") #run default collocate analysis
ct.high_val(run_collocates_mi,hits = 10) #print top 10 collocates

#our lemmatized corpus will be written to a directory/folder entitled "word_single_lemmas" in our working directory
ct.write_corpus(name, name + "_lemmas",word_lemmatized)

#tag the word corpus using default settings (lemmas and upos tags)
#feature13
word_upos = tg.tag_corpus(name) #feature13, this may take a while. Consider getting some coffee!
print(len(word_upos)) #check to make sure that there are 500 files here! Otherwise, there is a problem with your directory name OR your working directory!

upos_freq = ct.corpus_frequency(word_upos) #raw frequency
#ct.high_val(upos_freq,hits = 10) #use high_val function to see top 10 hits

run_upos_collocates_mi = ct.collocator(word_upos,"run_VERB") #note that we have to include the appropriate tag in our search
#ct.high_val(run_upos_collocates_mi,hits = 10) #use high_val function to see top 10 hits

#write tagged corpus files to a folder/directory entitled "word_single_tagged"
ct.write_corpus(name ,name + "_tagged",word_upos)

ct.display_string(word_lemmatized)#feature14,feature15

ct.search_pos(word_upos)#feature16

pos, count = tg.count_pos(word_lemmatized, name)#feature17

#print(pos)
#print(count)

ct.pos_least(pos, count, name)#feature20, feature21, feature22