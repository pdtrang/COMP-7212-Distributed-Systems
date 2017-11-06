REQUIREMENT:
	- Python 3.
	- Python packages: networkx, matplotlib.

HOW TO RUN:

	python hw2.py

FEATURES:
	- The program will ask for a node ID to initialize Chord.

	- User can interact with Chord to INSERT new node or DELETE node. 
		+ Negative ID will not be accepted by the program. 
		+ Input for insertion and deletion can be random point.
		+ If node ID already exists, no deletion or insertion will be done.

	- User can choose option to DRAW Chord from the Menu.
		+ YELLOW nodes are the actual nodes.
		+ Every time a node is inserted or deleted, Chord will be drawn in ASCII mode.

	- User can LOOKUP for an ID.

WALKTHROUGH:
	1) Insert node into Chord:
		- User needs to give a specific ID for a node to insert. This ID is random.
		- Chord will lookup for successor and predecessor of the given ID.
		- Notify both successor and predecessor that a new node will be inserted between them.
		- Insert new node, update pointers to successor and predecessor, transfer data from successor.
		- Update pointers of predecessor and successor.
		- If ID conflicts, return.

	2) Delete node in Chord:
		- User needs to give a specific ID for a node to be deleted. This ID is ID of any actual node.
		- Chord will lookup for successor and predecessor of the given ID.
		- Notify both successor and predecessor that a node between them will be deleted.
		- Transfer data from the node to successor.
		- Update pointers of predecessor and successor.
		- Delete node with the given ID.

	3) Lookup/Visual Lookup:
		- User need to give a specific ID to lookup.
		- Chord will start looking up from the first node.
		- Return ID of successor if found, return None if the ID is not exists.

	3) Draw ASCII/Visualization.
		- User can select option to visualize the Chord from the Menu.


