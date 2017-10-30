#! /usr/bin/python
import sys
import subprocess
import os.path

scriptDir = os.path.dirname(os.path.realpath(__file__))
dsk = "%s/dsk/build/bin/dsk" % scriptDir
dsk2ascii = "%s/dsk/build/bin/dsk2ascii" % scriptDir

def fa2dict(filename):
        fa_dict = {}
        seq_name = ""
        for l in open(filename):
                line = l.rstrip()
                if line[0] == ">":
                        seq_name = line[1:].split()[0]
                        fa_dict[seq_name] = []
                else:
                        fa_dict[seq_name].append(line)
        result = {}
        for seq in fa_dict:
                result[seq] = "".join(fa_dict[seq])
        return result

def revcom(x):
	return "".join([{"A":"T","C":"G","G":"C","T":"A"}[x[i]] for i in range(len(x)-1,-1,-1)])



if len(sys.argv)!=5:
	print "find_kmer_matches.py <kmer.fa> <genome.fa> <outfile.txt> <threads>"; quit()
kmerfile = sys.argv[1]
genomefile = sys.argv[2]
outfile = sys.argv[3]
threads = sys.argv[4]
fdict = fa2dict(kmerfile)
FNULL = open("/dev/null","w")
for klen in sorted(set([len(x) for x in fdict.values()])):
	print "Counting kmers with length=%s" % (klen)
	subprocess.call("%s -nb-cores %s -file %s -kmer-size %s -out %s.k%s.h5 && %s -file %s.k%s.h5 -out %s.k%s.txt" % (dsk,threads,genomefile,klen,genomefile,klen,dsk2ascii,genomefile,klen,genomefile,klen),shell=True,stderr=FNULL,stdout=FNULL)

FNULL.close()

O = open(outfile,"w")	
for kname in fdict:
	kseq = fdict[kname]
	krc = revcom(kseq)
	klen = len(kseq)
	kfile = "%s.k%s.txt" % (genomefile,klen)
	num = 0
	for l in open(kfile):
		arr = l.rstrip().split()
		if arr[0]==kseq or arr[0]==krc:
			num+=int(arr[1])
	O.write("%s\t%s\t%s\n" % (kname,kseq,num))
O.close()

