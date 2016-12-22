import functions 
reload(functions) 
from functions import *


import globalvariable 
reload(globalvariable) 
from globalvariable import *
import random


openBrowser() #open browser

loginFacebook()

#close popup from chrome
#popUpChrome()
#wait(3)


actionNotif()
wait(2)


actions = random.choice(actionPattern)

#popup(''.join(actions))

wait(2)

for action in actions :
    if action == "likes":
        actionLike()

    if action == "view_friends" :
        Friends()
        
    if action == "buzzfeed" :
        buzzFeed()
        
    if (action == "like_fan_page") :
        actionLikeFanPage()

    if (action == "page_feed") :
        actionPageFeed()

    if (action == "post_status") :
         postStatus()
    if (action == "trending") :
        actionTrending()

    if (action == 'logout') :
        logout()
        
        

       

        
        

        

        

        

        


       

       
        

        

        

    
        


        


       
   
           

 
       

     


     
    
