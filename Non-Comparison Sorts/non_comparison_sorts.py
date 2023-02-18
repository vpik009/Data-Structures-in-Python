'''
Date: 24/03/2021
'''

__author__: "Vladislav Pikulin"



def countSort(new_list:list, num_list:list)->list:
    '''
    :Description: Sorts the new_list which contains single digits and rearranges elements in num_list according 
    to the rearranges that have been made in new_list so as to sort num_list. This function is used by radix and radixString functions.

    :Input:
        :param1 new_list: a list of single digits taken from each element of num_list at a certain same index
        :param2 num_list: a list that is to be sorted based on the index changes made to the new_list elements and returned back to the radix function

    :Output: a sorted list of non-negative integers

    :Time Complexity: 
        Worst: O(N+M), where N is the number of elements in new_list and num_list (same length), and M is the largest element in new_list
        Best: O(N+M), the same as the worst since the is no way to end the loop early

    :Space Complexity: 
        Auxiliary space = O(M+M+N) = O(M+N) where M is the largest element in new_list and N is the length of the new_list / num_list
        Total Space = Auxiliary + Input = O(M+M+N) + O(N+N) = O(M+M+N+N+N) = O(M+N)
    '''

    
    if len(num_list) == 0:
        return num_list #return empty list if empty


    #find the max  O(N)
    maximum = new_list[0] 
    for item in new_list:
         if item > maximum:
             maximum = item

    #initialize countSort array
    countSort_arr = [0]*(maximum+1)
  

    #update countSort array freq
    for item in new_list:
        countSort_arr[item] = countSort_arr[item] + 1 #increment
   

    #initilize position array with index 0 as 1
    pos_arr = [0]*(maximum+1)
    pos_arr[0] = 1

    for i in range(len(pos_arr)-1):
        pos_arr[i+1] = countSort_arr[i] + pos_arr[i]

    #reinsert into the original array based on the position in pos_arr
    output = [0]*len(new_list)

    for i in range(len(new_list)):
        insert = pos_arr[new_list[i]]-1
        output[insert] = num_list[i]
        pos_arr[new_list[i]]+=1

    return output




def radix(num_list:list)->list:
    '''
    :Description: The function takes in a list of none negative integers and returns a sorted list of those none negative integers.

    :Input:
        :param1 num_list: a list of numbers to be sorted

    :Output: A sorted list of non-negative integers

    :Complexity: 
        Worst: O(N*M) where N is the length of num_list and M is the largest number of digits of any element of N
        Best: O(N*M) same as worst case since no way to end the loop early 

    :Space Complexity: 
        Auxiliary Space = O(N) from new_list and O(N) from countSort, where N is the length of num_list input list. Therefore O(2N) = O(N)
        Total Space = Auxiliary + Input = O(N)+O(N) = O(N)
    '''
    #FIRST if the STRiNGS dont have same number of digits ! add spaces!
    base = 26

    #find largest digits in integer (power) O(N*M)
    current_power = 0
    powermax = 0
    for item in num_list:
        current_power = 0
        while item > 0: 
            item = item // 10 # divide the item by 10 until its 0
            if item > 0:
                current_power += 1
        if current_power > powermax:
            powermax = current_power
        
    power = 0
    #list to store the single digits of each integer of num_list
    new_list = [0]*len(num_list)
 
    #do this *powermax for the integer with max digits
    for i in range(powermax+1): #+1 for inclusive  O(M) M is the largest digit

        for j in range(len(num_list)): #O(N) N is the length of num_list

            new_list[j] = (num_list[j]//(base**power))%base 
            
        num_list = countSort(new_list,num_list)
        power+=1 #increment power for the next digit

    #test return
    return num_list

def radixString(string_list:list)->list:
    '''
    :Description: The function takes in a list of string and returns a sorted list of strings.

    :Input:
        :param1 string_list: a list of string to be sorted

    :Output: A sorted list of strings

    :Time Complexity: 
        Worst: O(N*M) where N is the length of num_list and M is the largest string length in the string_list
        Best: O(N*M) same as worst case since no way to end the loop early 

    :Space Complexity: 
        Auxiliay Space: O(N) from the tmp_list and O(N) from the auxiliary space from countSort, where N is the length of string_list. Therefore = O(N)
        Total Space: Auxiliary + Input = O(N) + O(N) = O(N) 
    '''
    #FIRST if the STRiNGS dont have same number of digits ! add spaces!

    #pad words based on maximum length
    #find maxlength
    maxlength = 0


    #list1 O(2*N1) 
    for i in range(len(string_list)):
        if len(string_list[i][0])>maxlength:
            maxlength = len(string_list[i][0])

    for i in range(len(string_list)):
        if len(string_list[i][0])<maxlength:
            string_list[i][0] =string_list[i][0] + "_"*(maxlength-len(string_list[i][0]))


    #get last character from right 
    tmp_list = [0]*len(string_list) #to hold each character of a string
    for i in range(maxlength-1,-1,-1): 
        for j in range(len(string_list)):
            tmp_list[j] = ord(string_list[j][0][i])-95 #95 since '_' is 95 in ascii, hence a = 2

        string_list = countSort(tmp_list,string_list)

    #unpad 
    for i in range(len(string_list)):
        length = 0
        for j in range(len(string_list[i][0])):#length of word
            if string_list[i][0][j] != "_":
                length+=1
            else:
                string_list[i][0] = string_list[i][0][0:length]
                break #move on to the next word




    return string_list



#____QUESTION 1_________

def best_interval(transactions:list,t:int)->tuple:
    '''
    :Description: This function takes finds the interval with the largest number of transactions within the given time and returns the starting time of the transaction interval and the number of transactions 
    occured within the time in a tuple respectively

    :Input:
        :param1 transactions: a list of non-negative integers, each representing the time the transaction occured
        :param2 t: a none negative integer, representing time in seconds

    :Output: a tuple containing the best_t: the starting time of the interval with the largest transactions and count: the number of transaction that occured within the given time respectively

    :Time Complexity: 
        Worst: O(N*M) where N is the length of transactions and M is the length of the largest integer in transactions
        Best:  O(N*M) restricted by the fact that the time complexity of radix sort is best = worst. 

    :Space Complexity:
        Auxiliary Space: O(N) from radix, where N is the length of transactions list
        Total Space: Auxiliary + Input = O(N) + O(N) + O(1) = O(N)
    '''

    if len(transactions)==0:
        return (0,0)

    #sort transactions
    transactions = radix(transactions)

    best_t = 0

    count = 0

    maximum = transactions[0]+t #initialize maximum to first value + t
    #get the number of elements for the first interval
    while count<len(transactions) and transactions[count]<=maximum:
        count+=1

    endpoint = count-1 #index of the endpoint


    i = 1   #pointer for the min edge value (starts at 1 since the count has already been done for value at index 0)
    #count is to be used in the loop to count the number of elements in other intervals
    maxCount = count #set maxCount to count as a initial comparison point

    current_enpoint = endpoint
    while i<len(transactions):
        count -= 1 #decrement by 1 since the start of the interval incremented
        minedge = transactions[i]
        maxedge = minedge+t

        k = current_enpoint+1
    
        while k<len(transactions) and transactions[k]<=maxedge: #find the next nextpoint and set k to that endpoint
            count+=1  #for 2 its 6 but its 5 

            k+=1
            current_enpoint+=1


        if count>maxCount: #has to be larger than two since min is increase by one and max is increased by one, which in this algorithm contributes to 1 count. Therefore to be larger than the previous max is needs to be more by 2 elements
            maxCount=count #set maxCount to count-1 -1 since the the addition from the last maximum may not contribute to the last element count since min is also increased by 1
            endpoint = current_enpoint #the new best endpoint is the current endpoint


        i+=1 #increment start of the interval


        if k>=len(transactions): #the maxedge is out of bound of the list. Hence, no other interval will have a larger number of elements.
            break

    best_t = transactions[endpoint]-t

    if best_t<0: #time cannot be negative. If negative, set to 0
        best_t = 0

    return (best_t,maxCount)


#______________________


#_____QUESTION 2________
def words_with_anagrams(list1:list,list2:list)->list:
    '''
    :Description: This function takes in two lists of strings, find anagrams in the two lists, and outputs a list of string from list1 which have one or more anagrams in list2

    :Input:
        :param1 list1: a list of strings with characters from a-z (lowercase)
        :param2 list2: a list of strings with characters from a-z (lowercase)

    :Output: A list of strings from list1 which have at least one anagram in list2

    :Time Complexity: 
        Worst: O(N1*M1 + N2*M2) where N1 is the length of list1, M1 is the length of the largest string in list1, and N2 is the length of list2, and M2 is the length of the largest string in list2
        Best:  O(N1*M1 + N2*M2) restricted by the fact that the time complexity of radix sort is best = worst. 

    :Space Complexity:
        Auxiliary Space:  O(N1+N2) from merged + O(N1+N2) from alphabetical sort tmp_list + O(N1+N2) from radixString aux space. Therefore = O(3N1+3N2) = O(N1+N2)
        Total Space: Auxiliary + Input = O(N1+N2)+O(N1)+O(N2) = O(N1+N2)
    '''




    #merge two lists O(2*(N1+N2))
    mergedlist = [0]*(len(list1)+len(list2))


    for i in range(len(list1)):
        mergedlist[i] = [list1[i],i,1] #index @1 = index @2 represents the list number

    for i in range(len(list1),len(list1)+len(list2)):
        mergedlist[i] = [list2[i-len(list1)],i,2] #index @1 = index @2 represents the list number
 

    #sort in alphabetical order 

    #SORTING BY CHARACTER O(N1*3M)
    for i in range(len(mergedlist)): #every words O(N)
        tmp_list = [0]*len(mergedlist[i][0]) #keeps integers for each character hence length of word O(M1+M2)
        for j in range(len(mergedlist[i][0])-1,-1,-1): #every character from right O(M)

            tmp_list[j] = ord(mergedlist[i][0][j])-97


        tmp_list = countSort(tmp_list,tmp_list) #sort tmp_list and reference index change to no other list but tmp_list
        mergedlist[i][0] = ""

        for j in range(len(tmp_list)): #every character merge O(M)
            mergedlist[i][0] += chr(tmp_list[j]+97)


    #sort by words

    mergedlist = radixString(mergedlist) 


    #compare

    i = 0 #merged list pointer 1
    j = 0 #merged list pointer 2 start at 0 incase there is no index 1
    output = [] #used to store anagrams found in list1

    while j < len(mergedlist)-1 and i<len(mergedlist): #O(N) since the loop is limited by either j or i counter

        if mergedlist[j+1][0] == mergedlist[i][0]: #same word
            if mergedlist[j+1][2] == mergedlist[i][2]: #same list

                j+=1

            else: #not the same list

                output.append(list1[mergedlist[i][1]])
                i+=1
                while mergedlist[i][2]!=1: #find the next element from list1

                    i+=1
                    if i >= len(mergedlist): #there are no more elements from list1, hence none more to return. break
                        break
                j=i #list 2 elements appear after list1 elements. Hence, compare from i onwards


        else: #the words arent the same 
                i+=1
                while mergedlist[i][2]!=1: #find the next element from list1
              
                    i+=1
                    if i >= len(mergedlist): #there are no more elements from list1, hence none more to return. break
                        break
                j=i #list 2 elements appear after list1 elements. Hence, compare from i onwards 

       
        
            
    return output 
