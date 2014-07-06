import re
from pprint import pprint
import argparse
try:
   import cPickle as pickle
except:
   import pickle

def get_filtered_lines(filename):
    lines = [['<begin>'] + re.sub(r'[^a-z ]+', '', line.lower())[:-1].split() + ['<end>'] for line in open(filename, 'r').readlines()]
    #print lines
    return lines
    

def trigrammatize(sent_as_list):
    return [sent_as_list[i:i + 3] for i in range(len(sent_as_list) - 2)]

def setup_lm_dict(filename, verbose=None):
    if verbose:
        print "Forming trigrams..,"
    
    trigrams = []
    for line in  get_filtered_lines(filename): trigrams.extend(trigrammatize(line))
    
    if verbose:
        print "Done."
    
    if verbose:
        print "Building Language Model..."
    lm_dict = {}
    count = 0
    for line in trigrams:
        count += 1
        if lm_dict.has_key(line[0]):
            if lm_dict[ line[0] ].has_key(line[1]):
                if lm_dict[ line[0] ][ line[1] ].has_key(line[2]):
                    lm_dict[ line[0] ][ line[1] ][ line[2] ] += 1.0
                else:
                    lm_dict[ line[0] ][ line[1] ][ line[2] ] = 1.0
            else:
                lm_dict[ line[0] ][ line[1] ] = { line[2] : 1.0 }
        else:
            lm_dict[ line[0] ] = { line[1] : { line[2] : 1.0 }} 
    if verbose:
        print "Done..."
        print "Trigram Count: {}".format(count) 
    return lm_dict

    

def count_prob_estimator(lm_dict):
    for word1, l1dict in lm_dict.items():
        for word2, l2dict in l1dict.items():
            total = sum(l2dict.values())
            for word3 in l2dict.keys():
                l2dict[word3] /= total
#TODO: Implement other estimators.

def dump_lm(lm_dict, outfile):
    pickle.dump(lm_dict, open(outfile, 'wb'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Efficient probabalistic language model (unsmoothed).\n Eg. $ python languagemodel.py -o model samp')

    parser.add_argument("-v", "--verbose", help="turns on verbose mode.", action="store_true")
    parser.add_argument("inputfile", help="text input file with one sentence per line (see file samp for example)", action="store")
    parser.add_argument("-o", "--output", help="output model file. prints to stdout if unspecified.", action="store")
    #TODO: Add options for different estimator implementations.
    args = parser.parse_args()
    
    lm_dict = setup_lm_dict(args.inputfile, args.verbose)
    
    if args.verbose:
        print "Estimating trigram probabilities (count)..."
    count_prob_estimator(lm_dict)
    if args.verbose:
        print "Done."
    
    
    if args.output:
        if args.verbose:
            print "Dumping Langiage Model..."
        dump_lm(lm_dict, args.output)
        if args.verbose:
            print "Done."
    else:
        pprint(lm_dict)
    
    
        
