COMPUTE K-MER FREQUENCIES OF DNA SEQUENCES USING MPI FOR PYTHON

REQUIREMENT:
	- Python 3.
	- Python packages: mpi4py.
	- openmpi-bin


HOSTFILE:
In order to run the program on cluster. User should setup the cluster first (follow steps in readme_setupCluster.txt). It is not necessary to have hostfile since user can specify hostname in the command. Howerver, it could be more convenient to use hostfile. Hostfile contains all hostnames, each hostnames is in one line. For example, the cluster has two machines named client1 and client2. The hostfile should be 

client1:n
client2:m

where n,m are number of processes (optional).


HOW TO RUN:
Input file should be in fasta format.

1) Peer-to-Peer:

	Run on one machine:
		mpirun −np number_of_processes python mpi_kmer_p2p.py input_file k

	Run on cluster:
		mpirun −np number_of_processes -hosts server_hostname,client_hostname python mpi_kmer_p2p.py input_file k

		Ex: mpirun -np 4 -hosts master,slave python mpi_kmer_p2p.py test.fasta 12

	The following command is for using hostfile

		mpirun −np number_of_processes -f hostfile python mpi_kmer_p2p.py input_file k

2) Collective:

	Run on one machine:
		Using scatter: mpirun −np number_of_processes python mpi_kmer_collective.py input_file k
		Using bcast:   mpirun -np number_of_processes python mpi_kmer_bcast.py input_file k

	Run on cluster:
		Using scatter: mpirun −np number_of_processes -hosts server_hostname,client_hostname python mpi_kmer_collective.py input_file k
		Using bcast:   mpirun −np number_of_processes -hosts server_hostname,client_hostname python mpi_kmer_bcast.py input_file k

		Ex: mpirun -np 4 -hosts master,slave python mpi_kmer_collective.py test.fasta 12

	The following command is for using hostfile

		mpirun −np number_of_processes -f hostfile python mpi_kmer_collective.py input_file k


WALKTHROUGH:
The program reads in put file and stores all sequences in a list. Process with rank 0 is considered as coordinator, which divides the workload, distribute to other processes and collect results from other processes.

The number of sequences to each process is total number of input sequences divided by number of processes. If number of processes is 1 or not specified, the program runs as normal progam without any parallelism.

All results computed by other processes will be sent to process with rank 0, and this process will perform all other work after that.



