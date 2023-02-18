
'''
Date: 7/05/2021
'''
__author__: "Vladislav Pikulin"



#classes____________________ for question 1

class Node:
    def __init__(self,freq:int=0):
        '''
        The constructor for the Node class
        :Time Complexity: worst = best O(1)
        '''
        self.ref= None
        self.freq = freq  # should only be 0 if not connected to anything.
        self.links = [None]*5  # key = 0:$, 1:A, 2:B, 3:C, 4:D
        self.sequence = None  # leaf node saves the entire sequence
        self.next_ref = None
        self.char = None

class SequenceDatabase:
    def __init__(self):
        '''
        The constructor for the sequence database
        :Time Complexity: worst = best O(1)
        '''
        self.root = Node()
        self.root.char = "$"
        self.empty = True
        self.last_seq = None


    def addSequence(self, key:str):  # insert
        '''
        Method used to insert a specific drug resistant gene sequence into the database
        :key: the specific drug resistant gene sequence to be inserted into the database
        :Pre-condition: key cannot be empty
        :Time Complexity: worst = best O(N) where N is the length of the key string parameter
        '''
        pointer = 0
        self.last_seq = key  # changes the instance of the last sequence stored. So we dont pass it in the recursive function
        node = self.addSequence_aux(self.root, pointer)  # use the recursive function
        self.empty = False  # something has been added. No longer empty

    def addSequence_aux(self, node:Node, pointer:int):
        '''
        Auxiliary function used to add a sequence into the SequenceDatabase. Called by addSequence
        :param node: an instance of Node
        :param pointer: pointer used to indicate the character being inserted
        :Time Complexity: worst = best O(N) where N is the sequence being added from pointer index to the end of the sequence
        '''
        if pointer>=len(self.last_seq):  # base case


            if node.links[0] == None:  # if doesnt exist
                freq = 1
                leaf = Node(freq)  # new node node meaning no other frequencies here, so 1st
                leaf.char = "$"
                leaf.sequence = self.last_seq
                node.links[0] = leaf

                if node.ref:  # check current reference node against the new node
                    if node.ref.freq == leaf.freq:  #if the two nodes are equal in frequency (both 1)
                        node.ref = leaf
                        node.freq = leaf.freq
                        node.next_ref = leaf


                else:  # if current node doesnt have an existing reference, set it to the leaf
                    node.ref = leaf
                    node.freq = leaf.freq
                    node.next_ref = leaf

                

            else:  # sequence exists, check the word for it and the frequency
                node.links[0].freq+=1  # new entry so must increment the previous frequency
                leaf = node.links[0]
                freq = leaf.freq

                if leaf.freq >= node.ref.freq:  # recheck the frequencies of leaf nodes
                    #swap
                    node.ref = leaf
                    node.freq = leaf.freq
                    node.next_ref = leaf
  
            return node  #return current word's leaf node and freq
            

        else: # if this is not the last character in the key

            index = ord(self.last_seq[pointer]) - 64
            next_node = None

            if node.links[index] is not None:
                next_node = node.links[index]

            else:  # if none, create a node
                next_node = Node()
                next_node.char = self.last_seq[pointer]
                node.links[index] = next_node
            
            pointer +=1
            next_node = self.addSequence_aux(next_node, pointer)


            if node.ref is None:
                node.ref = next_node.ref
                node.freq = next_node.freq
                node.next_ref = next_node

            else:  # if it has a ref it should have a next_ref

                if node.freq < next_node.freq:
                    node.ref = next_node.ref
                    node.freq = next_node.freq
                    node.next_ref = next_node

    
                elif node.freq == next_node.freq and node.next_ref.char >= next_node.char:
                    node.ref = next_node.ref
                    node.freq = next_node.freq
                    node.next_ref = next_node

            return node



    def query(self, key:str):  # search
        '''
        Method used to find the specified drug resistant gene sequences in the database
        :param key: the drug resistant gene sequence to look for containing only characters A,B,C,D as a single string
        :Time Complexity: worst case O(len(key)) where key is the key parameter string
        '''
        current = self.root

        if key == "": # empty string 
            if self.empty == False:
                return current.ref.sequence  # there is some sequence that has the largest freq
            else:
                return None  # there is nothing in the db
        
        for i in range(len(key)):
            index = ord(key[i])-64


            try:
                
                if current.links[index] is not None:  # There is a way!
                    current = current.links[index] # set the current to the next
                    if i+1 == len(key):  # last character in the query

                        return current.ref.sequence
                
                else: 
                    return None  # if cannot find a key char, return None as the prefix doesnt exist



            except Exception:
                return None  # doesnt exist





#____________________________
#  classes for question 2__________TODO
class NodeOrf:
    def __init__(self):
        '''
        Contructor for the NodeOrf class
        :Time Complexity: O(1)
        '''
        self.links = [None]*5  # key = 0:$, 1:A, 2:B, 3:C, 4:D
        self.indexes = []  # indices of the individual character




class OrfFinder:
    def __init__(self, genome:str):
        '''
        The constructor of the OrfFinder. Used to instantiate
        :param genome: A string from which a suffic trie is to be created
        :Time complexity: worst = best O(1)+O(N^2) = O(N^2) from create_trie method.
        '''
        self.root = NodeOrf()  # root node
        self.genome = genome
        self.create_trie()


    def create_trie(self):
        '''
        This function is used to create a suffix trie of the self.genome string instance variable of the OrfFinder instance.
        :Time Complexity: O(N)*O(N)= O(N^2) worst = best, where N is the number of characters in self.genome
        '''

        for i in range(len(self.genome)): # for all suffix starting characters
            current = self.root # begin new suffix from root
            self.create_trie_aux(current, i)  # use an auxiliary function for recursive call

                    
    def create_trie_aux(self, current:Node , start:int):
        '''
        Auxiliary function used as an auxiliary function to create a suffix trie recursively
        :param current: An instance of NodeOrf
        :param start: The starting point of the genome suffix as an integer
        :Time Complexity: worst = best since suffix nodes have to be traversed and created regardless. O(N) where N is the length of the genome string from start to the length of self.genome
        '''

        index = ord(self.genome[start])-64  # get the index of the current character
                
        if current.links[index] is not None: 
            current = current.links[index]
            current.indexes.append(start) # append the current index of the char to the node


        else:  # if node doesnt exist
            current.links[index] = NodeOrf()  # create a new node
            current = current.links[index]
            current.indexes.append(start)  # append the current index of the char to the node

        if start<len(self.genome)-1:
            self.create_trie_aux(current,start+1)
            

    def find_aux(self, current:Node, string:str, position:int = 0):
        '''
        An auxiliary function used to find the indices of the string in the suffix trie of this instance
        :param current: an NodeOrf instance
        :param string: the string that is being searched for
        :param position: an optional parameter used as a pointer on the string param to specify which we are currently at
        :Time Complexity: worst case O(len(string)) 

        '''

        if current == None:  # if the first position doesnt exist
            return None

        if position+1 >= len(string):
            indices =  current.indexes  # get the indexes of the last character


        elif current.links[ord(string[position+1])-64] is not None:
            indices = self.find_aux(current.links[ord(string[position+1])-64], string, position+1)

        else:
            return None  # the sequence trying to find does not exist

        return indices


            

    def find(self, start:str, end:str):
        '''
        Function used to find all the characters between start and end substrings
        :param start: the substring used to identify starting points for the list of substrings 
        :param end: the substring used to identify ending points for the list of substrings
        :Time Complexity: worst case O(len(start)) + O(len(end) + O(U) = O(len(start)+len(end)+U) Where U is the number of substrings that are between different instances of start and end substrings

        '''
        current = self.root
        indexes_start = None
        indexes_end = None
        return_list = []  # initialize the return list

        #get the starting and ending indexes
        indexes_start = self.find_aux(current.links[ord(start[0])-64], start)
        indexes_end = self.find_aux(current.links[ord(end[0])-64], end)
        
        if not indexes_end or not indexes_start:
            return return_list
 

        for i in range(len(indexes_start)):  # loop through the starting indices
            for j in range(len(indexes_end)): # loop through the ending indices
                if (indexes_end[j]-len(end)+1) > (indexes_start[i]):  # ending index has to be larger than starting and not '==' to prevent overlapping
                    return_list.append(self.genome[(indexes_start[i]-len(start)+1):indexes_end[j]+1])

        return return_list





