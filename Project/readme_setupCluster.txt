SETUP MPI CLUSTER:

REQUIREMENT:
	- openssh-server
	- sshfs

The following steps should be done on ALL machines in cluster.

PASSWORDLESS LOGIN
After installing ssh, user should be able to login to other node by 

	ssh username@hostname

User will be asked to provide password of username. In order to enable easier login, user needs to generate keys and copy them to other nodes's list of authorized_keys.

User can follow these steps to generate keys and copy keys to other nodes. From terminal, enter these commands:

+ Generate RSA keys:

	ssh-keygen -t rsa

+ Add generated keys to other node:

	ssh-copy-id client

	the "client" here can be IP address or username@hostname. If all nodes have common usernames, "client" will be IP address or hostname. If nodes have different user account, user should specify username@hostname. The keys should be done between all pairs of nodes in the cluster. 

+ ssh to all machines once so that they can be added to list of known_hosts. This step is essential to make sure that there will be no failure on passwordless ssh later.


+ After setting up ssh, user should be able to login to other nodes without any password prompt.

	ssh client


MOUNTING OVER THE NETWORK
After this step, user can make a new directory to start mounting remotely file systems over SSH. For example, I named the directory on server as server_cloud and the directory on client as client_cloud.

This part is unstruction for mounting directory on Linux. Instruction for Windows will be explained at the end of this section. From terminal on client side, user can use this command line to mount the directories on client to server:

sudo sshfs -o allow_other username@servername:/home/server_username/server_cloud /home/client_username/client_cloud


The option allow_other is to allow multiple user to make a change to the directory. If there are only two nodes (server and client), it may not necessary to have this option. However, it is recommended that user should put this option so that there are no errors in the future when user add more nodes to the cluster.

User can check for mounting by command:

df -h


In order to export the server_cloud directory, user should create an entry in /etc/exports on server side. 

/home/server_name/server_cloud client_hostname(rw,sync,no_root_squash,no_subtree_check)

where:

- client_hostname: the IP address or hostname of client where user wants to share server_cloud directory to.
- rw: enable both read and write option. User can user "ro" for read-only.
- sync: change to the shared directory only after changes are committed.
- no_subtree_check: prevent the subtree checking. When a shared directory is the subdirectory of a larger filesystem, the sshfs performs scans of every directory above it, in order to verify its permission and details. Disabling the subtree check may inscrease the reliability of sshfs, but reduce security.
- no_root_squash: allow root account to connect to the folder.


After making entry in /etc/exports, user should always run:

sudo exportfs -a

SETUP HOST
User needs to specify IP address of nodes for each MPI run. However, user can create a host file and store all IP addresses with their names.

Setting up host file at /etc/hosts with the following content:

server_IP_address server_hostname
client_IP_address client_hostname

The host file on server should contain information from all clients, whereas host file on client only needs information for server and that client.

ACCESS PERMISSION
It is required to change the access permission of server_cloud directory to allow clients to read, write or execute files in that directory.

User can change access permission using this command:

	sudo chmod ugo+rwx /home/server_username/server_cloud


where:

ugo: u - user, g - group, o-others
+rwx: + is to allow ugo to have permission to do "r" (read), "w" (write) or "x" (execute).

FIREWALL
Firewall on both server and all clients should be turned off in order to make sure that there will not have any problem with connection.

Firewall can be turned off with following command:
	
	sudo ufw disable
	
User can turn on again firewall by using this command:
	
	sudo ufw enable
	

MISC
In /etc/hosts file, user should comment out the line 127.0.1.1 to avoid connection error on both server and clients.

For example, the content in host file:
127.0.0.1 localhost
127.0.1.1 hostname

# MPI cluster setup
server_IP_address server_hostname
client_IP_address client_hostname


User should comment out the line "127.0.1.1 hostname" as following:

127.0.0.1 localhost
#127.0.1.1 hostname

# MPI cluster setup
server_IP_address server_hostname
client_IP_address client_hostname















