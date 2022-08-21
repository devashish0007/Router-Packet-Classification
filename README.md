
# Packet Classification


The objective of this program is to implement the following packet classification algorithm for IPv4: Set
Pruning Trie approach for two-dimensional classification.

The algorithms can be implemented using Python



## Trie Creation

 Construct F1 trie as in hierarchical tries (HT) method.
 I Construct F2 tries for each prefix node, as in HT.
 For each prefix node p in F1, let Ap include p and all the ancestor
 nodes of p that are also prefix nodes
 Merge all F2 tries of nodes in Ap to construct final F2 trie for p
 
## Match Operation

 Lookup: Find LMP in F1 trie and traverse LMP’s corresponding F2
 trie to find all matching rules in set R
 Select best applicable rule from R, as per policy


## Running Code

To run code, install a python3 and then run the following command

```bash
  python3 ./spt.py -p RuleFile.txt -i InputAddrFile.txt -o OutputFile.txt

```
or

```bash
  python ./spt.py -p RuleFile.txt -i InputAddrFile.txt -o OutputFile.txt
```

### Input files :

1) RuleFile:
####
```bash
1 128.16 12 130.205 16
2 112.36 14 112.0    8
.    .    .   .      .
.    .    .   .      .
.    .    .   .      .
```

2) InputAddrFile: 
####
```bash
128.18 130.205
112.38 112.34
  .      .
  .      .
  .      .
```


### Output files :

1) outputFile:
####
```bash
Address 1   Address 2   No. of Matches    Rules matched   Search Time (µs)
  128.18      130.205       1               1                 45.6
  112.38      112.34        1               2                 25.4
  .             .           .               .                   .
  .             .           .               .                   .
  .             .           .               .                   .
    
```

 
  
