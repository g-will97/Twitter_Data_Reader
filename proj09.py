'''Skeleton file with all strings for Mimir testing'''
###################
#CSE 234 Project 9
#
#
#   Algorithm 
#      prompt for input file
#      input file name
#      anlaysis of data
#      prints top three hashtags combined
#      prints top three hashtags by the individual
#      prints all the users
#      loop for user names
#          test usernames are in list
#      prompt for two usernames seperated by comma
#      input usernames
#      displays similarity of usernames by month
#      prompts for plotting
#      input answer
#      if yes is entered 
#          displays plot of month to similarity
##################
import string, calendar, pylab
import operator

MONTH_NAMES = [calendar.month_name[month] for month in range(1,13)]

def open_file():
    '''Asks for input for file name
        if openable file returns filepointer
        error printed if file not found'''
    while True:
        try:
            fp=open(input("Input a filename: "),'r')
            return(fp) #returns file name if openable
        except FileNotFoundError:
            print("Error in input filename. Please try again.") #prints error if no file is found

def validate_hashtag(s):
    '''Takes in string as an arguement
        if string is number returns false
        if string has punctuation returns false
        returns true otherwise'''
    if s.strip('#').isdigit() == True:
        if len(s.strip('#'))==1: #if hashtag is single digit does not count
            return(False)
    for ch in s.strip('#'):
        if ch in string.punctuation:
            return(False) #if punctuation is found does not count it
    else:
        return(True) # returns true if no punctuation or single digit found

def get_hashtags(s):
    '''Takes in string as arguement
        splits string by spaces
        tests for hashtag for every word
        returns list of valid hashtags'''
    hashtags=[]
    s=s.split()
    for word in s: #every word in tweet tested for valid hashtag
        if word[0]=='#': #makes sure word starts with pound symbol (for valid hashtag)
            if validate_hashtag(word) == True:
                hashtags.append(word) #appends valid hashtags to list
            
    return(hashtags) # retruns list of valid hashtags
def read_data(fp):
    '''Takes in file as arguement
        reads every line in file
        stores every line value in list
        returns list of all lines with data'''
    big_list=[]
    for line in fp: #reads data file line by line
        line_list=[]
        line=line.split(',') #splits three data sets by comma
        line_list.append(line[0]) #appends names to list of the line
        line_list.append(int(line[1])) #appends month to list of the line
        line_list.append(get_hashtags(line[2])) #validates words in string and appends any valid hashtags
        big_list.append(line_list) #appends list of line into big list of all data
    return(big_list) #returns all data vis big list
        
        

def get_histogram_tag_count_for_users(data,usernames):
    '''takes in list of data and list of usernames
        sorts data for hashtags
        finds name with hashtag
        counts value hashtag was used by user
        returns dictionary of hashtag and hashtag count'''
    dictionary={}
    user_dict={}
    for line in data: #reads data by line
        hashtags=line[2] #finds hashtag in line
        for name in usernames:
            if name == line[0]: #if name is in usernames
                for hashtag in hashtags:
                    if hashtag in dictionary:
                        dictionary[hashtag]=dictionary[hashtag]+1 #adds one for everytime hashtag is seen again
                        
                    else:
                        dictionary[hashtag]=1 #if hashtg was never used before sets equal to zero
                        
                
    
    return(dictionary)

def get_tags_by_month_for_users(data,usernames):
    '''takes in list of data and list of usernames
        creates dictionary with each month number to empty set
        adds definitions of dictionary with key as month and value as set with hashtag to user
        converts dictionary into final list
        returns final list of tuples of month and count
        '''
    dictt={}
    for i in range(1,13): #creates dicitonary of month numbers to empty sets 
        dictt[i]=set()
    for line in data: #reads data list
        user_set=set() #initializes set
        month=line[1] #sets month number variable
        hashtags=line[2] #sets hashtag variable
        for name in usernames:
            if name==line[0]:
                if dictt[month]==set():
                    for hashtag in hashtags: #adds each hashtag to set
                        user_set.add(hashtag)
                    dictt[month]=user_set #new set for month added to dicitonary
                else:
                    user_set=dictt[month] #existing set called
                    for hashtag in hashtags:
                        user_set.add(hashtag) #adds hashtag to existing set
                    dictt[month]=user_set #new value of sets for that month
    final_list=[(k,v) for k, v in dictt.items()] #turns dictionary to list of tuples (month to set)
    return(final_list) #returns list of tuples

def get_user_names(L):
    '''given list of data
        creates empty set
        adds user to set
        returns sorted list of sets'''
    sett=set() #empty set
    for line in L: #reads every line in data list
        user=line[0] #user variable assigned username
        sett.add(user) #user added to set
    sett=list(sett) #changes set to list
    sett=sorted(sett)#sorts list of users 
    return(sett) #returns final set of all suers 



def three_most_common_hashtags_combined(L,usernames):
    '''takes in data and usernames
        turns dictionary into list of tuples
        sorts list by highest count
        returns top 3 occurances'''
    dictt=get_histogram_tag_count_for_users(L,usernames) #pulls dictionary of all hashtags
    listt=[(v,k) for k,v in dictt.items()] #changes dicitonary to list
    listt.sort(key=operator.itemgetter(0),reverse=True) #sorts by number of occurance
    listt=listt[0:3] #cuts out the top 3
    return(listt) #returns top 3 used hashtags
    

def three_most_common_hashtags_individuals(data_lst,usernames):
    '''takes in data list and list of usernames
        goes by every user in usernames
        gets list of tag count for that user
        adds user to each list in the big list
        adds list to big list 
        sorts by most hashtags used
        turns list into tuple
        returns top three tuples
    '''
    final_dict={}
    listed=[]
    list2=[]
    for user in usernames:
        lis=[]
        lis.append(user)
        dictt=get_histogram_tag_count_for_users(data_lst,lis)
        listt=[[v,k] for k,v in dictt.items()] #list of tuples for hashtag and hashtag count
        for lst in listt:
            lst.append(user) #appends the user to each list 
        listed.extend(listt) #extends list of users to big list
    listed.sort(key=operator.itemgetter(0),reverse=True) #sorts by count of hashtag
    listed=listed[0:3] #top 3 used hashtags
    listed=[tuple(L) for L in listed] #converts list to tuple
    
    return(listed) #returns list
        
         
def similarity(data_lst,user1,user2):
    '''takes in data list and 2 users
        creates list of hashtags used by month
        tests simlarity between lists by month
        creates tuple of month to similar hashtags used
        returns list of month to similar hashtags'''
    user1s=[]
    listt=[]
    user1s.append(user1)
    user2s=[]
    user2s.append(user2)
    user1s=get_tags_by_month_for_users(data_lst,user1s)
    user2s=get_tags_by_month_for_users(data_lst,user2s)
    for i in range(1,13):
        month=i #month number
        set1=user1s[i-1][1] #user 1's set of hashtags
        set2=user2s[i-1][1] #user 2's set of hashtags
        tup=(month,set1 & set2) #intersect of both sets and its month
        listt.append(tup)
    
    return(listt) #returns list of all similar hashtags by month
        
def plot_similarity(x_list,y_list,name1,name2):
    '''Plot y vs. x with name1 and name2 in the title.'''
    
    pylab.plot(x_list,y_list)
    pylab.xticks(x_list,MONTH_NAMES,rotation=45,ha='right')
    pylab.ylabel('Hashtag Similarity')
    pylab.title('Twitter Similarity Between '+name1+' and '+name2)
    pylab.tight_layout()
    pylab.show()
    # the next line is simply to illustrate how to save the plot
    # leave it commented out in the version you submit
    #pylab.savefig("plot.png")


def main():
    fp=open_file() #calls open file function
    print()
    data=read_data(fp)# Read the data from the file in lsit
    usernames=get_user_names(data)# Create username list from data
    top3=three_most_common_hashtags_combined(data,usernames)# Calculated the top three hashtags combined for all users in list
    top3i=three_most_common_hashtags_individuals(data,usernames)  # Calculate the top three hashtags individually for all users in list
    print("Top Three Hashtags Combined")
    print("{:>6s} {:<20s}".format("Count","Hashtag"))
    for i in range(len(top3)): #for every item in top3 list prints
        count=top3[i][0]
        hashed=top3[i][1]
        print("{:>6.0f} {:<20s}".format(count,hashed)) #prints formatted count and hashtag
    print()
    print("Top Three Hashtags by Individual")
    print("{:>6s} {:<20s} {:<20s}".format("Count","Hashtag","User"))
    for i in range(len(top3i)):
        count=top3i[i][0]
        hashed=top3i[i][1]
        user=top3i[i][2]
        print("{:>6.0f} {:<20s} {:<20s}".format(count,hashed,user)) #prints count of hashtag, hashtag, and username with it
    print()
    string=''
    for i in range(len(usernames)): #list of usernames converted to one big string
        if i==len(usernames) or i == 0:
            string=string+usernames[i]
        else:
            string=string+', '+usernames[i]
    print("Usernames: ", string) #prints usernames in string
    user_valid=False
    while user_valid==False: #keeps running loop until user_valid is not False
        user_str = input("Input two user names from the list, comma separated: ") #asks for two user name inputs
        user_str=user_str.split(',') #splits input by commas
        user_str=[z.strip() for z in user_str] #strips spaces for every word in user string
        for user in user_str:
            if user not in usernames:#if username not in list of usernames loops again
                user_valid=False 
            if user in usernames:
                user_valid=True #exists loops if usernames in list of usernames
        if user_valid==False:
            print("Error in user names.  Please try again") #if username not in list prints error
    
        
    user1,user2=user_str
    similar=similarity(data,user1,user2) #calls similarity function
    print()
    print("Similarities for "+user1+' and '+user2)
    print("{:12s}{:6s}".format("Month","Count"))
    for i in range(len(similar)):
        month=similar[i][0] #month numerical
        month=calendar.month_name[month] #changes number of month to string of month name
        hashed=similar[i][1] #set of hashtags
        count=len(hashed) # count of number of hashtags
        print("{:12s}{:<6.0f}".format(month,count)) #prints amount of similar tweets in the month
    print()
    choice = input("Do you want to plot (yes/no)?: ") #asks if want to plot similarity data
    if choice.lower() == 'yes': #if choice equals yes plots data
        x_list=[] #initialized lists
        y_list=[]
        for i in range(1,13):
            x_list.append(i)#appends number of each month in list
        for i in x_list:
            i=calendar.month_name[i] #changes number of month to string of month name in list
        for i in range(len(similar)):
            count=len(similar[i][1]) #count of similarity for each month
            y_list.append(count)#adds each count for each month
        plot_similarity(x_list,y_list,user1,user2) #plots data
        
if __name__ == '__main__':
    main()