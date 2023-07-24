import corpus_toolkit as ct
import corpus_nlp as tg

word = ct.load_corpus("Datasets") #read all corpus files
print(len(word)) #double check that there are 500 files. If not, check your directory (see point 2 above) and check your directory name

word_tokenized = ct.tokenize(word) #tokenize corpus

word_lemmatized = ct.lemmatize(word_tokenized) #create lemmatized version of the text
word_bigrams = ct.ngrammer(word_tokenized,2) #create bigram version
word_trigrams = ct.ngrammer(word_tokenized,3) #create trigram version

lemma_freq = ct.corpus_frequency(word_lemmatized) #raw frequency
ct.high_val(lemma_freq) #use high_val function to see top 20 hits

run_collocates_mi = ct.collocator(word_lemmatized,"run") #run default collocate analysis
ct.high_val(run_collocates_mi,hits = 10) #print top 10 collocates

#our lemmatized corpus will be written to a directory/folder entitled "word_single_lemmas" in our working directory
ct.write_corpus("Datasets","Datasets_lemmas",word_lemmatized)

#tag the word corpus using default settings (lemmas and upos tags)
word_upos = tg.tag_corpus("Datasets") #this may take a while. Consider getting some coffee!
print(len(word_upos)) #check to make sure that there are 500 files here! Otherwise, there is a problem with your directory name OR your working directory!

upos_freq = ct.corpus_frequency(word_upos) #raw frequency
ct.high_val(upos_freq,hits = 10) #use high_val function to see top 10 hits

run_upos_collocates_mi = ct.collocator(word_upos,"run_VERB") #note that we have to include the appropriate tag in our search
ct.high_val(run_upos_collocates_mi,hits = 10) #use high_val function to see top 10 hits

#write tagged corpus files to a folder/directory entitled "word_single_tagged"
ct.write_corpus("Datasets","Datasets_tagged",word_upos)
