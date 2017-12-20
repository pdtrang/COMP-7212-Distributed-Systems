from mpi4py import MPI
import random
import time
import sys
from itertools import product

def reverse_complement(s):
	complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
	reverse_complement = "".join(complement.get(base, base) for base in reversed(s))
	return reverse_complement

def countKmer(seqlist,k):
	count = {}
	for s in seqlist:
		count_seq = {}
		for i in range(len(s)-k+1):
						
			# main strand
			kmer = s[i:i+k]
			if kmer not in count_seq:
				count_seq[kmer] = 1
			else:
				count_seq[kmer] = count_seq[kmer] + 1

			# reverse complement
			rc_kmer = reverse_complement(kmer)
			if rc_kmer not in count_seq:
				count_seq[rc_kmer] = 1
			else:
				count_seq[rc_kmer] = count_seq[rc_kmer] + 1

		count[s] = count_seq

	return count

def readFiles(filename):
	f = open(filename,'r')
	Seq = []
	lines = f.readlines()
	for i in lines:
		if '>' not in i:
			Seq.append(i)

	return Seq

if __name__ == "__main__":
	
	k = int(sys.argv[2])
	t1 = time.time()

	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()
	size = comm.Get_size()
	name = MPI.Get_processor_name()

	if rank == 0:
		seqlist = readFiles(sys.argv[1])
		print("Number of input sequences:", len(seqlist))
		
	else:
		seqlist = None
	
	myList = comm.bcast(seqlist,root=0)
	chunk_size = int(len(myList)/size)
	
	if rank+1 == size:
		start, end = rank*chunk_size, len(myList)
	else:
		start, end = rank*chunk_size, rank*chunk_size+chunk_size

	
	print("\nProcess rank ", rank, " of ", size, " on ", name, " received ", len(myList), " sequences.")
	partial_count = countKmer(myList[start:end],k)
	print("Process rank ", rank, " of ", size, " on ", name, " processed ", len(myList[start:end]), " sequences from ", start, " to ", end-1)
	partial_freq = comm.gather(partial_count, root=0)
	
	if rank == 0:
		freq = {}
		for i in range(len(partial_freq)):
			for key in partial_freq[i]:
				freq[key] = partial_freq[i][key]

	if rank == 0:
		t2 = time.time()
		print ("\nNumber of processed sequences: ", len(freq))
		print("Time = %.16f sec\n"%(t2 - t1))
