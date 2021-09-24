'''
FIT2004 Assignmnent 2
This module holds all of the relevant fuctions to perform task 1 and task 2 of the second assignment for FIT2004
Date: 14/04/2021
'''

__author__: "Vladislav Pikulin"




#QUESTION 1___________________________________________________________________

def best_schedule(weekly_income, competitions):
    '''
    :Description: 
        Function calculates the largest possible profit one can make given a schedule consisting of weekly incomes and competitions with their pay
        
    :Input:
        :param1 weekly_income: a list of positive integers indicating the amount of pay the person makes if he were to coach that week.
        :param2 competitions: a list of tuples with 3 indexes 
            0: starting week of the competition
            1: ending week of the competition
            2: pay of the competition


    :Output: a non negative integer that indicates the maximum amount of profit that is possible to make given the arguments.

    :Time Complexity: 
        Worst: O(NlogN), where N is the combined length of competitions and weekly_income
        Best: O(NlogN), the same as the worst since the is no way to end the loop early. We have to sort the combined list regardless which is worst O(NlogN) complexity

    :Space Complexity: 
        Auxiliary space = O(N) where N is the combined length of weekly_income and competitions. Space required to store combined list. sort sorts in-place according to python doc. 
        Total Space = Auxiliary + Input = O(N+N) = O(N)
    
    '''
    #contraint = number of weeks
    merged = [None]*(len(weekly_income)+len(competitions))
    memo = [-1]*(len(weekly_income)+1) #+1 for base case
    memo[0] = 0 # the amount of profit made where there is no weeks to consider 

    #put weekly_income into tuples
    for i in range(len(weekly_income)):
        merged[i] = (i,i,weekly_income[i])
    
    #put both arguments together
    j = 0
    for i in range(len(weekly_income),len(merged)):
        merged[i] = competitions[j]
        j+=1

    
    merged.sort(key=lambda a: a[1]) #sort by the second elements O(N Log N)

    #BUILD THE MEOIZATION and store 
    #for each value in the memoization you are going through all combinations (coins in the coin exchange example)

    i = 1 #memo pointer, start from 1 to avoid base case
    j=0 #pointer for the current item in the combined list

    while j < len(merged):

        if i>=len(memo): #no more weeks to check
            break

        if merged[j][1] <= i: # if the ending week is smaller or equal to the current position in the memo

            week = merged[j][0]-1 #calculate the last week available for payment if taking the current option for the week

            if week>=0:
                if (merged[j][2]+memo[week+1])>memo[i]: #check if the current calculation is larger than the one already in the memo (+1 to week due to base case in memo)
                    memo[i] = merged[j][2] + memo[week+1] #+1 in memo since including base case
            else:
                if merged[j][2]>memo[i]:  #check if the current calculation is larger than the one already in the memo (cannot add pay from previous weeks)
                    memo[i] = merged[j][2] 


            if j+1 < len(merged) and merged[j+1][1] == merged[j][1]: #if the next item has the same ending week, increment j
                j+=1

            else: #otherwise, we are checking pay for the upcoming week (i++)
                i+=1
                j+=1

        else: #if not, increment position in memo
            i+=1

    #return the final optimal profit
    return memo[len(memo)-1] 


#QUESTION 2_______________________________________________________________

def best_itinerary(profit, quarantine_time,home):
    '''
    :Description: 
        Function calculates the best possible profit one can make with the given profit per city per day, each city's respective quarantine times, and the starting city.
        
    :Input:
        :param1 profit: a list of lists, elements of which include lists that contain the profit to be made in each city for that day, for every day. Each inner list is of identical length.
        :param2 quarantine_time: a list that includes the quarantine time (in days) for each city
        :param3 home: a non negative integer that is used to specify which city to start at.

    :Output: a non negative integer that indicates the maximum amount of profit that is possible to make given the arguments.

    :Time Complexity: 
        Worst: O(D*N), where D is the number of days and N is the number of cities
        Best: O(D*N), the same as the worst since the is no way to end the loop early. We have to fill every spot in the memoization in order to terminate.

    :Space Complexity: 
        Auxiliary space = O(N*D) where N is the number of cities and D is the number of days. This is the space required for the memoization, which is a list (length of days) of lists (length of cities)
        Total Space = Auxiliary + Input = O(N*D + N*D) = O(N*D)
    
    '''
    #probably not possible since home will incorrect here regardless
    if len(profit) == 0 or len(profit[0]) == 0 or home is None:
        return 0
 

    city_num = len(profit[0]) #the number of cities
    day_num = len(profit) # the number of days
    travel_time = 1 # time taken in days to travel 1 city. travel time is constant

    memo = []

    #fill up the memo with -1 since we are looking for the largest pay
    #Boolean used to specify "Did not work in this city on this day"
    for i in range(day_num): 
        sublist = [[-1,-1]]*city_num # index 0 for the maximum pay and index 1 for maximum pay if we were in quarantine on that day
        memo.append(sublist)

    #base case
    for i in range(city_num):
        memo[day_num-1][i] = [profit[day_num-1][i],0] #if its the last day, the best option is to stay and get paid (base case), and we cant make any money if we are in quarantine on the last day



    for i in range(day_num-2,-1,-1): #start at second last city to avoid base case
            for j in range(city_num): #loop through all cities in the day

                #if already quarantined and can work on the current day
                #move right
                if j+1<city_num and i+travel_time+quarantine_time[j+1]<day_num and memo[i+travel_time+quarantine_time[j+1]][j+1][0]>memo[i][j][0]:
                    memo[i][j] = [memo[i+travel_time+quarantine_time[j+1]][j+1][0],memo[i][j][1]]

                    if  memo[i+travel_time+quarantine_time[j+1]][j+1][0]>memo[i][j][1]: # since traveling now means it requires you to quarantine in new city, we check max for 'if not quarantined' for current city
                        memo[i][j] = [memo[i][j][0],memo[i+travel_time+quarantine_time[j+1]][j+1][0]]

                #move left
                if j-1>=0 and i+travel_time+quarantine_time[j-1]<day_num and memo[i+travel_time+quarantine_time[j-1]][j-1][0]>memo[i][j][0]:
                    memo[i][j] = [memo[i+travel_time+quarantine_time[j-1]][j-1][0],memo[i][j][1]]

                    if  memo[i+travel_time+quarantine_time[j-1]][j-1][0]>memo[i][j][1]: # since traveling now means it requires you to quarantine in new city, we check max for 'if not quarantined' for current city
                        memo[i][j] = [memo[i][j][0],memo[i+travel_time+quarantine_time[j-1]][j-1][0]]

                #if you work at the current city. Check the current pay + next day.
                if memo[i+1][j][0]+profit[i][j] > memo[i][j][0]: 
                    memo[i][j] = [memo[i+1][j][0]+profit[i][j],memo[i][j][1]]

                #if not quarantined yet at the current city    
                #since you have to quarantine at the current city, might as well quarantine at the right or left city if its more profitable that way

                if i+quarantine_time[j]<day_num and memo[i+quarantine_time[j]][j][0]+profit[i+quarantine_time[j]][j] > memo[i][j][1]:
                    memo[i][j] = [memo[i][j][0],memo[i+quarantine_time[j]][j][0]] #no profit from current day since in quarantine

                #right If we can get more from right while in quarantine, set that to the optimal for when in quarantine
                if j+1<city_num and i+1<day_num and memo[i][j][1] < memo[i+1][j+1][1]:
                    memo[i][j] = [memo[i][j][0],memo[i+1][j+1][1]]
            
                #left. If we can get more from left while in quarantine, set that to the optimal for when in quarantine
                if j-1>=0 and i+1<day_num and memo[i][j][1]<memo[i+1][j-1][1]:
                    memo[i][j] = [memo[i][j][0],memo[i+1][j-1][1]]

                    
                #check optimal. If the profit is larger for when we are in the city in quarantine, set that to the optimal since we can get this pay by traveling to other cities on this day
                if memo[i][j][1] > memo[i][j][0]:
                        memo[i][j][0] = memo[i][j][1]



    return memo[0][home][0]



