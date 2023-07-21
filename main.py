import corpus_toolkit as ct
import corpus_nlp as tg

brown = ct.load_corpus("brown_single") #read all corpus files
print(len(brown)) #double check that there are 500 files. If not, check your directory (see point 2 above) and check your directory name

brown_tokenized = ct.tokenize(brown) #tokenize corpus

brown_lemmatized = ct.lemmatize(brown_tokenized) #create lemmatized version of the text
brown_bigrams = ct.ngrammer(brown_tokenized,2) #create bigram version
brown_trigrams = ct.ngrammer(brown_tokenized,3) #create trigram version

lemma_freq = ct.corpus_frequency(brown_lemmatized) #raw frequency
ct.high_val(lemma_freq) #use high_val function to see top 20 hits

run_collocates_mi = ct.collocator(brown_lemmatized,"run") #run default collocate analysis
ct.high_val(run_collocates_mi,hits = 10) #print top 10 collocates

#our lemmatized corpus will be written to a directory/folder entitled "brown_single_lemmas" in our working directory
ct.write_corpus("brown_single","brown_single_lemmas",brown_lemmatized)

#tag the brown corpus using default settings (lemmas and upos tags)
brown_upos = tg.tag_corpus("brown_single") #this may take a while. Consider getting some coffee!
print(len(brown_upos)) #check to make sure that there are 500 files here! Otherwise, there is a problem with your directory name OR your working directory!

upos_freq = ct.corpus_frequency(brown_upos) #raw frequency
ct.high_val(upos_freq,hits = 10) #use high_val function to see top 10 hits

run_upos_collocates_mi = ct.collocator(brown_upos,"run_VERB") #note that we have to include the appropriate tag in our search
ct.high_val(run_upos_collocates_mi,hits = 10) #use high_val function to see top 10 hits

#write tagged corpus files to a folder/directory entitled "brown_single_tagged"
ct.write_corpus("brown_single","brown_single_tagged",brown_upos)
