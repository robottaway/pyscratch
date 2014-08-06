from trie import SuffixTree

substrs = ['ith', 'orn', 'iev', 'ass', 'net']

def main():
    st = SuffixTree()
    with open('/Users/rob/Documents/wordlist.csv', 'r') as fd:
        for word in fd:
                st.index_string(word.split(',')[0].strip().lower()) 

    for substr in substrs:
        print "looking for words with '%s' in them" % substr
        found, metadata = st.trie.contains_path(substr)
        if found:
            for item in metadata:
                print ">>> %s" % item

if __name__ == "__main__":
    main()
