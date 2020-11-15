# Dijkstra's shortest algorithm help taken from: https://www.youtube.com/watch?v=IG1QioWSXRI&feature=emb_title
# My code makes use of pandas

import pandas as pd

#Graph class initializer
class Graph:
	def __init__(self):
		self.router_paths = {}

	# My graph is unidirectional. So the start node gets added to the dictionary, and the end node and length of path is added to its value dictionary.
	# Then the end node gets added to the dictionary with an empty dictionary as it's value.
	def add_edge(self, start, end, cost) :
		# Check if start node is already in graph
		if start in self.router_paths:
			if end not in self.router_paths[start]:
				self.router_paths[start][end] = cost
			else:
				print("\nPath already in graph. Please delete previous path if you want to add new version.")
		else:
			self.router_paths[start] = {}
			self.router_paths[start][end] = cost

		# Check if end node is already in graph
		if end not in self.router_paths:
			self.router_paths[end] = {}

# Router class initializer
class Router:
	def __init__(self, start, graph):
		self.start = start
		self.graph = graph

	# Code for Dijkstra's shortest algorithm.
	# Help taken from: https://www.youtube.com/watch?v=IG1QioWSXRI&feature=emb_title
	def find_path(self, end):
		shortest_distance = {}
		Nodes = list(self.graph.keys())

		# Make every distance from current node to other nodes infinity and distance from itself to itself 0
		for node in Nodes:
			shortest_distance[node] = float("inf")
		shortest_distance[self.start] = 0

		# Go through nodes list and adds shortest paths to predecessor dictionary
		predecessor = {}
		while len(Nodes) > 0:
			minNode = None
			for node in Nodes:
				if minNode is None:
					minNode = node
				elif shortest_distance[node] < shortest_distance[minNode]:
					minNode = node
			for subNode, cost in self.graph[minNode].items():
				if cost + shortest_distance[minNode] < shortest_distance[subNode]:
					shortest_distance[subNode] = cost + shortest_distance[minNode]
					predecessor[subNode] = minNode
			Nodes.remove(minNode)
		
		# Go through predecessor dictionary and create path list from nodes
		path = []
		current = end
		path.append(self.start)
		while current != self.start:
			try:
				path.insert(-1, current)
				current = predecessor[current]
			except KeyError:
				break

		# If selected routers are connected return path and total path length
		if shortest_distance[end] != float("inf"):
			path_forward = [path[i] for i in range(len(path)-1,-1,-1)]
			return(self.start, end, "->".join(path_forward), str(shortest_distance[end]))
		else:
			return(self.start, end, "Unconnected", "Null")

	# Prints out results from specific start and end router
	def get_path(self, end):
		s, e, p, c = self.find_path(end)
		print("\nStart: " + s)
		print("End: " + e)
		print("Path: " + p)
		print("Cost: " + c)

	# Prints routing table for specific current router
	def print_routing_table(self):
		st = []
		ed = []
		ph = []
		ct = []
		end_list = sorted([node for node in self.graph if node != self.start])
		for end in end_list:
			s, e, p, c = self.find_path(end)
			st.append(s)
			ed.append(e)
			ph.append(p)
			ct.append(c)
		routing_table = {'From:': st, 'To:': ed, "Cost:": ct, "Path:": ph}
		print()
		print(pd.DataFrame.from_dict(routing_table))

	# Removes specific router from graph and prints resulting routing table for current router
	def remove_router(self, router_name):
		if router_name in graph.router_paths:
			graph.router_paths.pop(router_name)
		for node in graph.router_paths:
			if router_name in graph.router_paths[node]:
				graph.router_paths[node].pop(router_name)
		self.print_routing_table()

	# Removes specific path between 2 routers
	def remove_path(self, path_name):
		graph.router_paths[self.name].pop(path_name)
		print("\nDone.")

# Basic user interface
def ui():
	global graph
	n = input("\nEnter command to start or enter help for list of acceptable commands: ")
	
	if n == "help":

		print("\n These are the commands that can be entered:\n"
		"\n    1 : If you want to link to routers together. You must then enter the start router and the end router and the path length between them."
		"\n    2 : If you want to reset the router graph and delete all existing routers and their paths in it."
		"\n    3 : If you want to remove a router from the graph and disply the resulting routing table. You must then enter the name of the router you are stating from and the router you are deleting."
		"\n    4 : If you want to remove a specific linked path from a router. You must enter the start router and the end router."
		"\n    5 : If you want information relating to a specific start router and a specific end router."
		"\n    6 : If you want to display the routing table for specified router."
		"\n    7 : If you want to display multiple routing tables at the same time."
		"\n exit : If you want to exit the program.\n")
		ui()

	if n == "1":

		print("\nLink routers.")
		print("\nPlease enter back to leave or valid command to proceed.(Start Router - End Router - Path Length).")
		start_node = input("\nPlease enter the start router: ")
		
		if start_node != "back":
			end_node = input("Please enter the end router: ")
			
			if end_node != "back":
				distance = input("Please enter the length of the path between start and end: ")
				
				while distance.isnumeric() != True:
					if distance == "back":
						ui()
					else:
						print("\nLength entered is not valid. Please enter valid length.")
						distance = input("\nPlease enter the length of the path between start and end: ")

				graph.add_edge(start_node, end_node, int(distance))
		ui()

	elif n == "2":

		print("\nReset graph.")
		check = input("\nAre you sure you want to delete the existing graph (y) or (n): ")
		
		if check == "y":
			graph = Graph()
		else:
			ui()

	elif n == "3":

		print("\nDelete router.")
		print("\nPlease enter back to leave or valid command to proceed.(Starting Router - Deleting Router).")
		
		start_node = input("\nPlease enter the starting router: ")
		while start_node not in graph.router_paths:
			if start_node == "back":
				ui()
			else:
				print("\nStarting router not in router graph.")
				start_node = input("\nPlease enter the starting router: ")

		delete_node = input("\nPlease enter the router you wish to delete: ")
		if delete_node != "back":
			if delete_node not in graph.router_paths:
				print("\nRouter entered to delete is not in router graph.")
			else:
				router = Router(start_node, graph.router_paths)
				router.remove_router(delete_node)
		ui()

	elif n == "4":

		print("\nDelete path.")
		print("\nPlease enter back to leave or valid command to proceed.(Starting Router - Deleting Path).")
		
		start_node = input("\nPlease enter the router you wish to delete the path from: ")
		while start_node not in graph.router_paths:
			if start_node == "back":
				ui()
			else:
				print("\nStarting router not in router graph.")
				start_node = input("\nPlease enter the router you wish to delete the path from: ")

		delete_node = input("\nPlease enter the path you wish to delete: ")
		if delete_node != "back":
			if delete_node not in graph.router_paths:
				print("\nRouter entered to delete is not in router graph.")
			else:
				graph.router_paths[start_node].pop(delete_node)
				print("\nSuccesfully deleted path.")
		ui()

	elif n == "5":

		print("\nGet path.")
		print("\nPlease enter back to leave or valid command to proceed.(Starting Router - End Router).")
		
		start_node = input("\nPlease enter the router you wish to start at: ")
		while start_node not in graph.router_paths:
			if start_node == "back":
				ui()
			else:
				print("\nStarting router not in router graph.")
				start_node = input("\nPlease enter the router you wish to start at: ")

		end_node = input("\nPlease enter the router you wish to end at: ")
		while end_node not in graph.router_paths:
			if end_node == "back":
				ui()
			else:
				print("\nEnd router is not in router graph.")
				end_node = input("\nPlease enter the router you wish to end at: ")

		router = Router(start_node, graph.router_paths)
		router.get_path(end_node)
		ui()

	elif n == "6":

		print("\nRouting table.")
		print("\nPlease enter back to leave or valid command to proceed.(Starting Router).")
		
		start_node = input("\nPlease enter the router you wish to start at: ")
		while start_node not in graph.router_paths:
			if start_node == "back":
				ui()
			else:
				print("\nStarting router not in router graph.")
				start_node = input("\nPlease enter the router you wish to start at: ")

		router = Router(start_node, graph.router_paths)
		router.print_routing_table()
		ui()

	elif n == "7":

		print("\nMultiple routing tables.")
		print("\nPlease enter back to leave or valid command to proceed.\nType finish to stop adding routing tables and display all ones currently selected\n(Starting Router - finish).")
		router_list = []

		start_node = input("\nPlease enter the router you wish to start at: ")
		while start_node != "finish":

			if start_node == "back":
				ui()

			elif start_node not in graph.router_paths:
				print("\nStarting router not in router graph.")
				start_node = input("\nPlease enter another router you wish to start at or finish to display currently selected routing tables: ")
			
			else:
				router_list.append(start_node)
				start_node = input("\nPlease enter another router you wish to start at or finish to display currently selected routing tables: ")

		for node in router_list:
			router = Router(node, graph.router_paths)
			router.print_routing_table()
		ui()

	elif n == "exit":
		exit()

	else:
		print("\nError: Invalid command")
		ui()

# Sample inputs for brief display of what this program does
def do_it_for_me():
	global graph
	graph.add_edge("a", "b", 7)
	graph.add_edge("a", "c", 9)
	graph.add_edge("a", "f", 14)
	graph.add_edge("b", "c", 10)
	graph.add_edge("b", "d", 15)
	graph.add_edge("c", "d", 11)
	graph.add_edge("c", "f", 2)
	graph.add_edge("d", "e", 6)
	graph.add_edge("e", "f", 9)
	router = Router("a", graph.router_paths)
	print("\nDisplaying path from router (a) to router (f):")
	router.get_path("f")

	n = input("\nPress enter to continue.")

	print("\nDisplaying routing table for router (a):")
	router.print_routing_table()

	n = input("\nPress enter to continue.")

	print("\nDisplaying resulting routing table for router (b) after removing router (c) from graph:")
	router_two = Router("b", graph.router_paths)
	router_two.remove_router("c")

	n = input("\nPress enter to continue.")

	print("\nDisplaying that the routing table for router (a) is now also changed due to router (c) being removed from graph:")
	router.print_routing_table()

graph = Graph()
inpt = input("\nEnter 1 for UI or 2 for demonstration on what the program outputs: ")
if inpt == "1":
	ui()
elif inpt == "2":
	do_it_for_me()