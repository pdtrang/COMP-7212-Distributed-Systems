# Author: Diem-Trang Pham

import networkx as nx
import matplotlib.pyplot as plt

class Node(object):
	def __init__(self, iden=None, data=None):
		self.id = iden
		self.data = data
		self.next = None
		self.prev = None


class Chord(object):
	def __init__(self):
		self.head = None
		self.id = None

	# find predecessor of a node
	def find_predecessor(self, new_iden):
		temp = self.head
		prev = Node()
		while temp:
			if temp.id < new_iden:
				prev = temp
				if temp.next:
					temp = temp.next
				else:
					return prev
			else:
				return prev

	# find successor of a node
	def find_successor(self, new_iden):
		temp = self.head
		while temp:
			if temp.id < new_iden:
				temp = temp.next
			else:
				return temp

	# lookup (k)
	def lookup(self, k):
		p = self.find_successor(k)
		if p:
			return p.id
		else:
			return -1

	# check if node is already in Chord
	def findNode(self,k):
		temp = self.head
		while temp:
			if temp.id == k:
				return temp
			temp = temp.next

		return None

	# insert new node at arbitrary position using id
	def insert(self, new_iden):
		if new_iden < 0:
			print("ID can not be negative number.")
			return

		if self.findNode(new_iden):
			print("\nID conflicts!!! Node ID %s is already in Chord." %(new_iden))
			return

		# look for predecessor
		pred = self.find_predecessor(new_iden)
		# look for successor
		succ = self.find_successor(new_iden)
					
		print("\n Inserting Node ", new_iden)
		if pred == None and succ == None: # insert in empty chord
			new_node = Node(new_iden)

			# generate Data Key
			new_node.data = generateDataKey(0, new_iden)

			# update pointers
			new_node.next = None
			new_node.prev = None

			self.head = new_node

			return
		elif pred.id == None and succ != None: # insert node at the beginning
			new_node = Node(new_iden)

			# generate Data Key
			new_node.data = generateDataKey(0, new_iden)
			succ.data = generateDataKey(new_iden+1, succ.id)
			
			# update pointers
			new_node.next = self.head
			new_node.prev = None
			
			self.head = new_node
			return
		elif pred.id != None and succ == None: # insert at the end
			new_node = Node(new_iden)

			# generate Data Key
			new_node.data = generateDataKey(pred.id+1, new_iden)

			# update pointers
			new_node.next = pred.next
			pred.next = new_node
			new_node.prev = pred

			pred.data = generateDataKey(min(pred.data),pred.id)
			return

		elif pred.id != None and succ != None: # insert node between pred and succ
			new_node = Node(new_iden)

			# generate Data Key
			new_node.data = generateDataKey(pred.id+1, new_node.id)
			succ.data = generateDataKey(new_iden+1, succ.id)

			# update pointers
			new_node.next = pred.next
			new_node.prev = pred

			pred.next = new_node
			succ.prev = new_node
			return

	# delete new node at arbitrary position using id
	def delete(self, iden):
		if iden < 0:
			print("ID can not be negative number.")
			return

		temp = self.findNode(iden)
		if  temp == None:
			print("\nNode is not in chord!!! Cannot delete node with ID ", iden)
			return

		# look for predecessor
		pred = self.find_predecessor(temp.id)
		# look for successor
		succ = self.find_successor(temp.id+1)
		
		print("\n Deleting Node ", iden)
		if pred.id == None and succ != None: # delete node at the beginning
			succ.prev = None
			self.head = succ

			# regenerate Data Key
			succ.data = generateDataKey(0,succ.id)
			
			return 

		elif pred.id != None and succ != None: # delete a node between two nodes
			pred.next = succ
			succ.prev = pred
			
			succ.data = generateDataKey(pred.id+1, succ.id)
			
		elif pred.id !=None and succ == None: # delete node at the end
			pred.next = None
			return
		elif pred.id == None and succ == None: # delete the only node 
			self.head = None
			return 

	# return size of chord (number of nodes)
	def size(self):
		temp = self.head
		count = 0
		while temp:
			count += 1
			temp = temp.next
		return count

	# draw Chord in ASCII
	def printChord(self):
		if self.size() == 0:
			print ("\nEmpty chord! There is no node to delete.")
			return

		print("\nChord")
		temp = self.head
		s = ""
		while temp:
			# print (temp.id)
			s = s + "---" +str(temp.id)
			temp = temp.next

		s = s + "---\n"
		s = s + generateLink(s)
		print ("\t"+s)

	# get id of all nodes in Chord
	def getNodes(self):
		temp = self.head
		ids = []
		while temp:
			ids.append(temp.id)
			temp = temp.next

		return ids

	def draw_current_lookup(self, iden):
		ids = self.getNodes()

		G = nx.Graph()

		for i in range(0,max(ids)+1):
			G.add_node(i)
			if i+1 < max(ids)+1:
				G.add_edge(i, i+1)
			else:
				G.add_edge(i, 0)


		pos = nx.circular_layout(G)
		nx.draw(G, pos, node_color='w', node_size=500,with_labels = True)
		nx.draw_networkx_nodes(G,pos, nodelist=ids, node_color='y',node_size=500)
		nx.draw_networkx_nodes(G,pos, nodelist=[iden], node_color='r',node_size=500)

		print ("Close figure to continue.")
		plt.show()	


	# function for visual lookup
	def visual_lookup(self, iden):
		temp = self.head
		while temp:
			print("\n Looking up at node ", temp.id)
			if iden in temp.data:
				print (" --> ID ", iden, "is at node ", temp.id)
				ch.draw_current_lookup(temp.id)
				return

			print (" --> ID ", iden, " is not at node ", temp.id)
			ch.draw_current_lookup(temp.id)
			temp = temp.next
			if temp:
				print (" Moving to next node...")
			else:
				print (" Can not find ", iden, " at any node.")
				return

	# draw Chord
	def drawGraph(self):
		ids = self.getNodes()

		G = nx.Graph()

		for i in range(0,max(ids)+1):
			G.add_node(i)
			if i+1 < max(ids)+1:
				G.add_edge(i, i+1)
				
			else:
				G.add_edge(i, 0)
				

		pos = nx.circular_layout(G)
		nx.draw(G, pos, node_color='w', node_size=500,with_labels = True)
		nx.draw_networkx_nodes(G,pos, nodelist=ids, node_color='y',node_size=500)

		print ("Close figure to return to menu.")
		plt.show()	


def generateLink(s):
	l = "\t|" + (len(s)-3)*" " + "|\n"
	l = l + "\t"+(len(s)-1)*"-"
	return l

def generateDataKey(p,s):
	data = []
	for i in range(p, s+1):
		data.append(i)
	return data

def menu():
	print("\n\n############################")
	print("1. INSERT node into Chord.")
	print("2. DELETE node in Chord.")
	print("3. Lookup.")
	print("4. Visual Lookup.")
	print("5. Draw Chord.")
	print("6. Exit")
	print("############################\n\n")

if __name__ == "__main__":
	print("Initializing Chord...")
	ch = Chord()

	print("Chord needs a node to start...")
	i = input("\nEnter a number for node ID you want to start with: ")
	ch.insert(int(i))

	ch.printChord()

	while True:
		menu()
		choice = input("Please select : ")
		if choice == '1':
			i = input("Enter node ID you want to INSERT: ")
			ch.insert(int(i))
			ch.printChord()
		elif choice == '2':
			d = input("Enter node ID you want to DELETE: ")
			ch.delete(int(d))
			ch.printChord()
		elif choice == '3':
			k = input("Enter ID you want to look up: ")
			l = ch.lookup(int(k))
			if l >= 0:
				print("\n Data ID %s is stored at Node %s" %(k, l))
			else:
				print(k, " is out of range.")
		elif choice =='4':
			k = input("Enter ID you want to look up: ")
			print ("\n")
			l = ch.visual_lookup(int(k))
		elif choice =='5':
			print ("YELLOW nodes are actual nodes.")
			ch.drawGraph()
		elif choice == '6':
			print("Exit!")
			exit()
		else:
			print("Wrong option.")



	
	

	

