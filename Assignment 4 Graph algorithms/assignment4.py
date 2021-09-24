
'''
Date: 28/05/2021
'''
__author__: "Vladislav Pikulin"


class Graph:
    def __init__(self, vertices):
        '''
        :vertices: number of vertices in the graph
        '''
        self.adj_list = []
        for i in range(vertices):
            self.adj_list.append(Vertex(i)) # no edges yet

        self.num_vertices = vertices

    def add_directed_edge(self, source, dest, weight):  # might not be necessary
        '''
        Method used to add a directed edge to two vertices in a graph
        :source: vertex from which the edge begins
        :dest: vertex to which the edge points
        :weight: the associated weight of the edge between source and dest
        '''
        self.adj_list[source].add_edge(self.adj_list[dest], weight)

class Vertex:
    def __init__(self, id) -> None:
        '''
        :id: the id of the vertex
        '''
        self.id = id
        self.edges = []

    def add_edge(self, dest, weight):  # source is self
        '''
        method used to add a weighted edge to this vertex
        :dest:  vertex to which the edge points
        :weight: the associated weight of the edge between this vertex and dest
        '''
        self.edges.append(WeightedEdge(self, dest, weight))

class WeightedEdge:
    def __init__(self, source, dest, weight):
        '''
        :source: the source vertex
        :dest: the destination vertex
        :weight: the weight of the edge from source to dest
        '''
        self.source = source
        self.dest = dest
        self.weight = weight







# Question 1

def best_trades(prices, starting_liquid,max_trades, townspeople):
    '''
    Function used to find the maximum profit you can get given the number of trades you can make, available trades and the associated prices of each liquid thats being traded
    :param prices: a list of prices for each liquid. Each index holds an id of the liquid
    :param starting_liquid: the liquid id of the liquid starting with
    :param max_trades: the maximum number of trades can make
    :param townspeople: list of tuples representing the people who are willing to make a specifc trade. (give, receive, ratio)
    :return: integer indicating the maximum profit that can be made by trading with the townspeople given the parameters
    :Time complexity: Worst = Best as we only terminate when the max trades is reached
                    -  O(TM) where T is the total number of trades available, and M is the maximum trades you can make
    '''
    #initialize the graph and its vertices
    graph = Graph(len(prices))
    # initialize the graph's edges
    for person in townspeople: 
        for trade in person:
            graph.add_directed_edge(trade[0],trade[1],trade[2])



    # previous iterations list holds volumes for previous iterations
    previous_iteration = [float("-inf")]*len(graph.adj_list)  # to use for the next iteration.  Holds volume of every vertex
    previous_iteration[starting_liquid] = 1

    this_iteration = [float("-inf")]*len(graph.adj_list)  # used for updating. Holds volume of every vertex 



    max = prices[starting_liquid]  # starting price



    for j in range(max_trades): # j-hops optimality for every vertex, at jth iteration


        for vertex in graph.adj_list:  #for all vertices

            vertex_volume = previous_iteration[vertex.id]

            for edge in vertex.edges:  # for all edges in a vertex

                previous_val = previous_iteration[edge.dest.id]  # the vertex's volume in the last iteration

                if vertex_volume != float('-inf') and (edge.weight*vertex_volume) > previous_val and (edge.weight*vertex_volume) > this_iteration[edge.dest.id]:
                    this_iteration[edge.dest.id] = (edge.weight*vertex_volume)  # update this iteration's volume


                    if (edge.weight*vertex_volume)*prices[edge.dest.id] > max:
                        max = (edge.weight*vertex_volume)*prices[edge.dest.id]



        for i in range(len(this_iteration)):
            previous_iteration[i] = this_iteration[i]


    return max




#Question 2
import heapq

class GraphQ2:
    def __init__(self, vertices):
        '''
        :vertices: number of vertices in the graph
        '''
        self.adj_list = []
        for i in range(vertices):
            self.adj_list.append(VertexQ2(i)) # no edges yet

        self.num_vertices = vertices
        self.graph_type = None

    def add_undirected_edge(self, source, dest, weight):  # add the edge both ways with the same weight
        '''
        Method used to add an udirected edge to two vertices in a graph
        :source: vertex from which the edge begins
        :dest: vertex to which the edge points
        :weight: the weight of the edge from source to dest
        '''
        self.adj_list[source].add_edge(self.adj_list[dest], weight)
        self.adj_list[dest].add_edge(self.adj_list[source], weight)
    

class VertexQ2:
    def __init__(self, id) -> None:
        '''
        :id: the id of the vertex
        '''
        self.id = id
        self.edges = []
        self.discovered = False  # in the min heap
        self.profit = float("inf")  # we want lowest, so initialize to infinity
        self.predecessor = None
        self.visited = False  # if visited, means we dont have to push it to the min heap


    def add_edge(self, dest, weight):  # source is self
        '''
        method used to add a weighted edge to this vertex
        :dest:  vertex to which the edge points
        :weight: the associated weight of the edge between this vertex and dest
        '''
        self.edges.append(WeightedEdge(self, dest, weight))

    def __lt__(self, other):  # used for comparison of vertices in minheap
        '''
        Magic method used to help the min heap heapify when comparing vertex id's
        '''
        if self.profit < other.profit:
            return True
        else:
            return False

class WeightedEdgeQ2:
    def __init__(self, source, dest, weight):
        '''
        :source: the source vertex
        :dest: the destination vertex
        :weight: the weight of the edge from source to dest
        '''
        self.source = source
        self.dest = dest
        self.weight = weight









def opt_delivery(n, roads, start, end, delivery):
    '''
    Function used to find the path that gives you the most profit, or the least money spent, from start to end
    either with or without the delivery.
    :param1 n: n is the number of cities represented as an integer from 0 to n-1
    :param2 roads: list of tuples in the form (u,v,w), 
                        roads[0] = city to go from
                        roads[1] = city the road leads you to
                        roads[2] = the cost of travelling by that road
    :param3 start: an integer in the range 0 to n-1 representing the starting city
    :param4 end: an integer in the range 0 to n-1 representing the ending city
    :param5 delivey: a tuple containing 3 elements (u,v,w). 
                        delivery[0] = the pick up city 
                        delivery[1] = city where the delivery has to be dropped off
                        delivery[2] = the amount you can make from making the delivery 

    :Time complexity: Best = Worst  O(E Log V)
                        
    '''
    # create the graph
    graph_list = []
    for i in range(4):  # generate four graphs
        graph = GraphQ2(n)  # pass in the number of vertices (cities: vertices)
        graph.graph_type = 1  # change this a list of graphs and this be an index


        #connect the edges (roads to cities)
        for road in roads:
            graph.add_undirected_edge(road[0],road[1],road[2])

        graph_list.append(graph)


    start_list = [start, start, delivery[0],delivery[1]]
    end_list =  [end, delivery[0],delivery[1],end]

    non_delivery_path = []
    non_delivery_profit = 0

    delivery_path = []
    delivery_profit = 0-delivery[2]


    for i in range(len(graph_list)):  # a constant of 4 graphs
        min_heap = []   #initialize the min heap
        # min_heap = VertexQ2MinHeap()
        source = graph_list[i].adj_list[start_list[i]] 
        source.profit = 0
        heapq.heappush(min_heap,source)  # using heapq for minimum heap
        # min_heap.push(source)  # push the first city into the heap
        source.discovered = True
        source.visited = True


        while len(min_heap) > 0:  # first run to get the distance from start to end without priority on delivery
            
            heapq.heapify(min_heap)
            # pop the min element
            vertex = heapq.heappop(min_heap)  # distance is finilized


            if vertex.id == graph_list[i].adj_list[end_list[i]].id:

                if i == 0: # if its the first graph, add paths to non delivery
                    non_delivery_profit+=vertex.profit
                    while vertex is not None:
                        non_delivery_path.append(vertex.id)
                        vertex = vertex.predecessor
                    non_delivery_path = non_delivery_path[::-1]
                else:  # else have to consider routes for start-pickup-delivery-end
                    tmp = []
                    delivery_profit+=vertex.profit
                    if i < 3:
                        vertex = vertex.predecessor  # dont consider last city since its considered in the start of the other routes
                    while vertex is not None:
                        tmp.append(vertex.id)
                        vertex = vertex.predecessor
                    for i in range(len(tmp)-1,-1,-1):
                        delivery_path.append(tmp[i])

                break  # reached the end city

            for edge in vertex.edges:
                if not edge.dest.discovered:

                    edge.dest.discovered = True
                    edge.dest.visited = True
                    edge.dest.profit = vertex.profit + edge.weight
                    # set previous
                    edge.dest.predecessor = vertex
                    heapq.heappush(min_heap,edge.dest)


                elif edge.dest.visited:
                    if vertex.profit + edge.weight < edge.dest.profit:
                        edge.dest.profit = vertex.profit + edge.weight
                        # set previous
                        edge.dest.predecessor = vertex


    if delivery_profit < non_delivery_profit:
        return (delivery_profit,delivery_path)
    else:
        return (non_delivery_profit,non_delivery_path)






