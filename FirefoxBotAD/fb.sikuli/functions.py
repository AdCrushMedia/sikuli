from sikuli import *

import globalvariable 
reload(globalvariable) 
from globalvariable import *
import random 
from random import shuffle
import time
import csv



def developerModeEnable() :
	devImage = Pattern("images/developerMode.png").targetOffset(36,-1)
	if (exists(devImage)) :
		click(devImage);
		return
	return


def getcsvData(filename) :

	with open(filename, 'rU') as csvfile:
		csvreader = csv.reader(csvfile)
		my_list = list(csvreader)
		data = random.choice(my_list)
		return data

		
def openBrowser():
	browser = App("Firefox")
	isOpenChrome = 0

	if not browser.window(): 
		isOpenChrome = 1
	else:
		App.close("Mozilla Firefox.app")
		isOpenChrome = 1

	if (isOpenChrome == 1) :
		wait(5)
		App.open(broserLocation + " --start-maximized");wait(2)

		wait(55)
		#developerModeEnable()

		#browser.focus();wait(2)
		type('l', Key.CTRL);wait(3)
		type(fbUrl);wait(3)
		type(Key.ENTER)

	else :
		popup('Firefox not found')
		exit(1)

def getActions():

	random.shuffle(userAction)
	return userAction


def loginFacebook():

	
	textEmail = Pattern("images/Firefox/emailTextbox2.png").exact().targetOffset(-33,23)

	textPassword = Pattern("images/Firefox/passwordTextbox2.png").targetOffset(-5,22) #Pattern("images/passwordTextbox.png").similar(0.90).targetOffset(-63,7)

	loginButton = Pattern("images/Firefox/loginButton.png").targetOffset(-2,0)

	loginFBLogo = Pattern("images/Firefox/loginFbLogo.png").similar(0.90)

	rememberPopUp = Pattern("images/Firefox/rememberPopup.png")

	wait(8)

	if (exists(loginLogo)) :
		wait(3)

		return

	
	if (exists(loginFBLogo)) :
		wait(loginButton, FOREVER)
		click(textEmail);wait(2) #click email text box
		type('a', Key.CTRL);wait(1)
		type(Key.DELETE);wait(1)
		type(defaultEmail);wait(2) #start typing email

		click(textPassword);wait(2) #click the password text box
		type('a', Key.CTRL);wait(1)
		type(Key.DELETE);wait(1)
		type(defaultPassword);wait(2) #start typing password
		type(Key.ENTER);wait(3)
		#click(loginButton);wait(1) #click login button

		if (exists(rememberPopUp)) :
			click(rememberPopUp);wait(4)
			
		wait(loginLogo, FOREVER)
		wait(3)

			
		return
		
	
	#test
	#actionNotif();wait(2)

def popUpChrome() :

	addPhoneNumber = Pattern("images/addPhoneNumber.png").targetOffset(-214,2) 
	savePassword =  Pattern("images/savePass.png").similar(0.80).targetOffset(28,-3)
	notificationAlert = Pattern("images/notifAlert.png").similar(0.90).targetOffset(32,-5)
	notificationAlert2 = Pattern("images/notifAlert2.png").similar(0.80).targetOffset(43,1)
	blueAlert = Pattern("images/blueAlertClosedButton.png").similar(0.80)
	
	wait(3)

	if (exists(savePassword)) :
		click(savePassword);wait(3)

	if (exists(notificationAlert)) :
		click(notificationAlert);wait(3)

	if (exists(notificationAlert2)) :
		click(notificationAlert2);wait(3)

	if (exists(blueAlert)) :
		click(blueAlert);wait(3)

	if (exists(addPhoneNumber)) :
		click(addPhoneNumber);wait(2)
		type(Key.F5);wait(3)

	



def searchBarUrl(url) :

	reloadButton = Pattern("1465916645829.png").similar(0.80)

	type("l", KeyModifier.CTRL);wait(1)
	type('a', Key.CTRL);wait(0.5)
	type(Key.DELETE);wait(0.5)
	paste(url);wait(2)
	type(Key.ENTER);wait(3)

	if (exists(reloadButton)) :
		click(reloadButton);wait(1)

	wait(loginLogo, FOREVER)

def actionNotif() :

	notifButton = Pattern("images/Firefox/notif.png");

	if (not exists(notifButton)) :
		return

	if(exists(notifButton)):
		wait(4)
		click(notifButton);wait(3)
		click(notifButton);wait(1)

		return

def loginLogoHover() :
	if (exists(loginLogo)) :
		hover(loginLogo);wait(2)
	
	return



def share() :
	
	count = 0
	maxCount = 3

	shareButton = Pattern("images/shareButton.png").similar(0.80).targetOffset(-4,-1)
	closedButton = Pattern("images/sharepost-closed.png").similar(0.90)
	sharePopUp = Pattern("images/Firefox/sharePopup.png").targetOffset(-62,-23)
	sharePostButton = Pattern("images/sharePostButton.png").targetOffset(84,-3)
	shareLinkButton = Pattern("images/Firefox/shareLinkButton.png").similar(0.80).targetOffset(87,-1)




	##searchBarUrl("https://www.facebook.com")

	if (not exists(shareButton)) :
		return 0

	if(exists(shareButton)):
		wait(3)
		click(shareButton);wait(3)
		

		if (exists(sharePopUp)) :
			wait(sharePopUp, FOREVER)
			click(sharePopUp);wait(1)
			wait(closedButton, FOREVER)
		#hover(closedButton)


		if (exists(sharePostButton)) :
			click(sharePostButton);wait(7)
			wheel(WHEEL_DOWN, 12);wait(1)

			
			return 1

		if (exists(shareLinkButton)) :
			click(shareLinkButton);wait(7)
			wheel(WHEEL_DOWN, 12);wait(1)

			
			return 1

		if (not exists(sharePostButton)) :
			wheel(WHEEL_DOWN, 4);

			if (exists(sharePostButton)) :
				click(sharePostButton);wait(7)
				wheel(WHEEL_DOWN, 12);wait(1)
				loginLogoHover()

				return 1

			if (exists(shareLinkButton)) :
				click(shareLinkButton);wait(7)
				wheel(WHEEL_DOWN, 12);wait(1)
				
				loginLogoHover()

				return 1


def like():
	
	count = 0
	maxCount = 3
	#wheel(WHEEL_DOWN, 4);wait(1)

	fbLikeButton = Pattern("images/Firefox/likeButton.png").similar(0.80)
	currentLikeButton = Pattern("images/currentLike.png").similar(0.96)


	#searchBarUrl("https://www.facebook.com")
	if (not exists(fbLikeButton)) :
		return 0

	if(exists(fbLikeButton)):
		wait(3)
		click(fbLikeButton);wait(2)
		loginLogoHover()

		return 1

def writeComment():

	try:

		C = db.cursor()
		C.execute ("SELECT * FROM comments ORDER BY RAND() LIMIT 1")
		row = C.fetchone()

	except Exception, e:
		print ("Failed to connect the database : Comment");

		return 1

	

	data =  row[1] #data = getcsvData(commentCsvPath)

	#writeImage = Pattern("images/write-comment.png").targetOffset(-20,0);


	writeImage = Pattern("images/Firefox/write-comment.png").targetOffset(-34,3);


	if (not exists(writeImage)) :
		return 0

	if(exists(writeImage)):
		wait(2)
		click(writeImage);wait(2)
		type(data); wait(2)
		type(Key.ENTER);wait(4)

		loginLogoHover()

		return 1


def commentLike():
	commentButton = "images/FireFox/comments.png"
	likeComment = Pattern("images/Firefox/likeComments.png").targetOffset(-25,-2)


	if (exists(commentButton)) :
		wait(3)
		click(commentButton);wait(4)
		if (exists(likeComment)) : 
			wait(3)
			click(random.choice(list(findAll(likeComment))));wait(1)

			return 1

		if (not exists(likeComment)) :
			return 0

	


def actionLike():
	
	maxLike = 3
	maxLikeComment = 1
	radomizeLike = ['likes', 'skip', 'skip']

	fbLikeButton = Pattern("images/Firefox/likeButton.png").similar(0.90)


	currentLikeButton = Pattern("images/currentLike.png").similar(0.96)
	moreComments = Pattern("images/Firefox/viewMoreComments.png")
	likeCommentsButton = Pattern("images/Firefox/likeComments.png").targetOffset(-25,-2)

	homeButton = "images/home.png"

	if (not exists(homeButton)) :
		type(Key.HOME);wait(3)


	if (exists(homeButton)) :
		click(homeButton)
		wait(4)

		while(1) :

			actions = random.choice(radomizeLike)

			loginLogoHover()

			wheel(WHEEL_DOWN, 2);wait(5)

			if (maxLike <= 0 ) :

				break

			if (actions == "skip") :
				wheel(WHEEL_DOWN, 3);wait(5)
				continue
			else :

				if (not exists(fbLikeButton)) :
					continue

				if(exists(fbLikeButton) and not exists(currentLikeButton)):
					wait(3)
					click(fbLikeButton);wait(3)
					maxLike = maxLike - 1
					

					if (maxLikeComment > 0) :

						if (exists(moreComments)) :
							click(moreComments);wait(3)

						if (exists(likeCommentsButton)) :
							wait(3)
							click(likeCommentsButton);wait(3)
							maxLikeComment = maxLikeComment - 1

	if (not exists(homeButton)) :
		return

						

				

def Friends() :
	newsFeedButton  = Pattern("images/Home.png").targetOffset(-32,1)
	friendTab = Pattern("images/about.png").targetOffset(81,2)
	friendsButton = Pattern("images/friends.png").similar(0.80).targetOffset(-295,1)
	timelineText = "images/timeline.png"

	scrollLimit = 5

	if (exists(newsFeedButton)) :
		click(newsFeedButton); wait(3)
		wait(friendTab, FOREVER); 
		click(friendTab);wait(2)

		while(1) :

			if (scrollLimit <= 0) :

				print "end"
				break;
			wheel(WHEEL_DOWN, 3);wait(5)
			
			if (exists(friendsButton)) :
				click(random.choice(list(findAll(friendsButton))))
				wait(timelineText, FOREVER)
				loginLogoHover()
				startScrollLimit = scrollLimit - 1

			if (not exists(friendsButton)) :
				scrollLimit = scrollLimit - 1
			#click(random.choice(list(findAll(Pattern(addFriendButton).similar(0.80).targetOffset(-546,2)))))

	if (not exists(newsFeedButton)) :

		return





def buzzFeed() :


	try:

		C = db.cursor()
		C.execute ("SELECT * FROM fan_pages ORDER BY RAND() LIMIT 1")
		row = C.fetchone()

	except Exception, e:
		print ("Failed to connect the database : BuzzFeed");

		return 1


 
	data =  row[2] #data = getcsvData(commentCsvPath)

	homeButton = "images/home.png"
	seeMore = "images/seeMore.png"
	searchButton = Pattern("images/search.png").similar(0.80).targetOffset(-60,0)

	buzzFeedImage = 'images/loginLogo.png' #Pattern(data).exact()
	typeText = row[5]
	fanPageLikeButton = Pattern("images/Firefox/fanPageLikeButton.png").exact()


	radomizeAct = ['likes', 'skip',  'share', 'writeComment']#['likes', 'skip', 'skip', 'share', 'writeComment'] #'likes', 'skip', 'skip', 'share', 'writeComment'

	likeLimit = 1
	shareLimit = 1
	writeLimit =  1

	if (not exists(homeButton)) :
		type(Key.HOME);wait(3)

	if (exists(homeButton)) :
		click(homeButton)
		#wait(searchButton, FOREVER)
		wait(4)
		#click(searchButton);wait(3)
		#type(typeText); wait(2)

		type("l", KeyModifier.CTRL)
		paste(typeText);wait(5)
		type(Key.ENTER)

		wait(buzzFeedImage, FOREVER);wait(7)

		if (exists(buzzFeedImage)) :


			if (exists(fanPageLikeButton)) : 
				click(fanPageLikeButton);wait(3)

			while(1) :

				#if (exists(seeMore)) :
					#click(seeMore);wait(5)

				wheel(WHEEL_DOWN, 3);wait(5)

				if (shareLimit <= 0 and 'share' in radomizeAct) :
					radomizeAct.remove('share')
        
				if (likeLimit <= 0 and 'likes' in radomizeAct) :
					radomizeAct.remove('likes')

				if (writeLimit <= 0 and 'writeComment' in radomizeAct) :
					radomizeAct.remove('writeComment')

				actions = random.choice(radomizeAct)

				if (likeLimit <= 0 and shareLimit <= 0 and writeLimit <= 0) : 
					break

				if (actions == "skip") :
					wheel(WHEEL_DOWN, 3);wait(5)
					continue

				if (actions == "likes") :
					like()
					likeLimit = likeLimit - 1


				if (actions == 'share') :
					share()
					shareLimit  = shareLimit - 1

				if (actions == 'writeComment') : 
					writeComment()
					writeLimit = writeLimit - 1

		if (not exists(buzzFeedImage)) :
			
			return 1


def actionLikeFanPage():

	homeButton = "images/home.png"
	likePages = "images/likepages.png"
	postButton = "images/postButton.png"

	yourPage = Pattern("images/yourPage.png").similar(0.85)
	approvedPage = Pattern("images/approvedPage.png").similar(0.90).targetOffset(-16,1) #Pattern("images/approvedPage.png").similar(0.90).targetOffset(-55,-128)
	likeButton = "images/pagesLikeButton.png"
	fanPageLikeButton = Pattern("images/FireFox/fanPageLikeButton.png").similar(0.90)

	likeLimit = 2
	scrollLimit = 10
	limit = 10
	approvedPageLimit = 20;
	startScroll = 0;
	approvedScroll = 0


	if (not exists(homeButton)) :
		type(Key.HOME);wait(3)


	if (exists(homeButton)) : 
		click(homeButton)
		wait(postButton, FOREVER)

		while(not exists(likePages)) :
			wheel(WHEEL_DOWN, 3);wait(3)
			
			limit = limit - 1

			if (limit <= 0) :

				break
				return

		else :

			if (exists(likePages)) :
				doubleClick(likePages);
				approvedScroll = 1
			else :
				return 


	if (approvedScroll == 1) :
		wait(loginLogo, FOREVER)
		while (not exists(approvedPage)) :
			wheel(WHEEL_DOWN, 3);wait(3)
			approvedPageLimit = approvedPageLimit - 1

			if (approvedPageLimit <= 0) :

				break
				return
		else :

			if (exists(approvedPage)) :
				click(approvedPage);wait(loginLogo, 20)
				startScroll = 1
			else :
				return 


	if (startScroll == 1) :

			
		
			while (not exists(fanPageLikeButton)) :
				wheel(WHEEL_DOWN, 3);wait(3)
				scrollLimit = scrollLimit - 1

				if (scrollLimit <= 0) :

					break
					return

			else :
				if (exists(fanPageLikeButton)) : 
					wait(5)
					click(fanPageLikeButton)
					return
				else :
					return


def actionPageFeed() :

	pageFeedButton = "images/pagesFeed.png"
	homeButton = "images/home.png"
	postButton = "images/postButton.png"

	radomizeLike = ['likes', 'skip', 'commentLike', 'skip', 'share'] #'likes', 'skip', 'commentLike' 'skip', 'share'

	shareLimit = 1
	likeLimit = 2
	commentLikeLimit = 2
	startScroll = False

	limit = 20

	if (not exists(homeButton)) :
		type(Key.HOME);wait(3)

	if (exists(homeButton)) :
		click(homeButton)
		wait(postButton, FOREVER)
		wait(3)

	if (not exists(homeButton)) :
		return

	while (not exists(pageFeedButton)) :
		wheel(WHEEL_DOWN, 3);wait(5)

		limit = limit - 1

		if (limit <= 0) :
			return

	else :
		click(pageFeedButton);wait(7)
		startScroll = True

	if (startScroll == True) :

		while(1) :
			actions = random.choice(radomizeLike)
			wheel(WHEEL_DOWN, 3);wait(5)
			
			loginLogoHover()

			if (likeLimit <= 0 and shareLimit <= 0 and commentLikeLimit <= 0) :

				break

			if (actions == "skip") : 
				wheel(WHEEL_DOWN, 4)

			if (actions == 'likes' and likeLimit > 0) :
				like();wait(3)
				likeLimit = likeLimit - 1
				wheel(WHEEL_DOWN, 3);wait(5)
				if (likeLimit <= 0) :
					radomizeLike.remove('likes')

			if (actions == 'share' and shareLimit > 0) :
				share();wait(3)
				shareLimit = shareLimit - 1
				wheel(WHEEL_DOWN, 3)
				if (shareLimit <= 0) :
					radomizeLike.remove('share')
				

			if (actions == "commentLike" and commentLikeLimit > 0) :
				commentLike()
				commentLikeLimit = commentLikeLimit - 1
				wheel(WHEEL_DOWN, 5)
				if (commentLikeLimit <= 0) :
					radomizeLike.remove('commentLike')

def postStatus() :

	try:

		C = db.cursor()
		C.execute ("SELECT * FROM posts ORDER BY RAND() LIMIT 1")
		row = C.fetchone()

	except Exception, e:

		print "Failed to connect to the database. Please check your internet connection : Post Status"
		return 1


	data =  row[1] #data = getcsvData(postCsvPath)
	postMessage = data

	homeButton = "images/home.png"
	postButton = Pattern("images/postButton").targetOffset(52,-4)
	writeStatus = "images/writestatus"

	if (not exists(homeButton)) :
		type(Key.HOME);wait(3)


	if (exists(homeButton)) :
		click(homeButton)
		wait(postButton, FOREVER)
		wait(3)

	if (not exists(homeButton)) :
		return

	wait(postButton, FOREVER)

	while(not exists(postButton)) :
		wheel(WHEEL_DOWN, 3);wait(5)
	else :
		wait(3)
		click(writeStatus);wait(3)
		type(postMessage);wait(2)
		click(postButton);wait(5)

				

def aboutPage() :

	newsFeedButton =  Pattern("images/home.png").similar(0.80).targetOffset(-56,1)
	aboutButton = "images/about.png"
	sports = "images/sports.png"   
	sportsNextButton = Pattern("images/sports.png").targetOffset(765,184)
	close = "images/aboutClose.png"

	if (exists(newsFeedButton)) :
		click(newsFeedButton)
		wait(aboutButton, FOREVER)

		if (exists(aboutButton)) :
			click(aboutButton);wait(2)

			while(1) :
				wheel(WHEEL_DOWN, 3);wait(3)

				if (exists(sports)) :
					wheel(WHEEL_DOWN, 1);wait(3)
					click(Pattern(sports).targetOffset(48,191));wait(1)
					click(Pattern(sports).targetOffset(359,193));wait(1)
					click(close);wait(1)

					#if (exists(sports)) :
						#click(Pattern(sports).targetOffset(48,191));wait(1)
						#click(sportsNextButton);wait(1)
						#click(Pattern(sports).targetOffset(359,193));wait(1)
						#click(close);wait(1)

def actionTrending() :

	endResult = "images/endResult.png"
    
	homeButton = "images/home.png"
	LoginLogo = 'images/loginLogo.png' #Pattern(data).exact()
	trendingImage = Pattern("images/trending.png").similar(0.90).targetOffset(-4,1)
	trendingArrow = Pattern("images/trendingArrow.png").similar(0.90).targetOffset(20,0)

	radomizeAct = ['likes', 'skip',  'share']

	trendingCount = 0;
	flag = 0;

	likeLimit = 1
	shareLimit = 1
	writeLimit =  1

	if (not exists(homeButton)) :
		type(Key.HOME);wait(3)

	if (exists(homeButton)) :
		wait(3)
		click(homeButton)

		wait(4)

		if (exists(LoginLogo)) : 

			while(not exists(trendingArrow)) :

				if (trendingArrow == 10) :
					break

					return

				trendingCount = trendingCount + 1;

			else :
				wait(3)

				if (exists(trendingArrow)) :
					click(random.choice(list(findAll(trendingArrow))));wait(5)
					flag = 1
				else :
					return

		if (flag == 1)	:

			while(1) :

				if (exists(endResult)) :
					break
					return

				wheel(WHEEL_DOWN, 3);wait(5)

				if (shareLimit <= 0 and 'share' in radomizeAct) :
					radomizeAct.remove('share')
        
				if (likeLimit <= 0 and 'likes' in radomizeAct) :
					radomizeAct.remove('likes')

				

				actions = random.choice(radomizeAct)

				if (likeLimit <= 0 and shareLimit <= 0) : 

					return
					break

				if (actions == "skip") :
					wheel(WHEEL_DOWN, 3);wait(5)
					continue

				if (actions == "likes") :

					like()
					likeLimit = likeLimit - 1


				if (actions == 'share') :
					share()
					shareLimit  = shareLimit - 1


		if (not exists(LoginLogo)) :
			
			return 1



def logout() :
	
	#logOutMenu =  Pattern("images/logoutmenu.png").similar(0.80).targetOffset(12,-1)
	#logoutBtn = Pattern("images/logout.png").similar(0.80).targetOffset(-8,0)
	#loginBtn = "images/loginButton.png"
	wait(3)

	type('w', Key.CTRL)
	exit(1)
	#App.close("Google Chrome.app")

	#if (not exists(logOutMenu)) :
		#App.close("Google Chrome.app")
	#else :

		#click(logOutMenu);wait(5)
		#if (exists(logoutBtn)) :
			#click(logoutBtn);wait(3)
			#wait(loginBtn, FOREVER);wait(2)
			#App.close("Google Chrome.app")
		#else :
			#App.close("Google Chrome.app")



'''
	count = 0
	maxCount = 3
	#wheel(WHEEL_DOWN, 4);wait(1)

	fbLikeButton = Pattern("images/likeButton.png").similar(0.90).targetOffset(-98,-2)
	currentLikeButton = Pattern("images/currentLike.png").similar(0.96)

	#searchBarUrl("https://www.facebook.com")
	if (not exists(fbLikeButton)) :
		return 0

	if(exists(fbLikeButton)):
		click(fbLikeButton);wait(1)

		return 1
	

def actionLikeFanPage():
	count = 0
	maxCount = 3
	
	yourPage = Pattern("images/yourPage.png").similar(0.85)
	topSuggestion = "images/top-suggestions.png"
	pagesLikeButton = Pattern("images/pagesLikeButton.png").similar(0.79)
	securityCheck =  Pattern("images/securitycheck.png").similar(0.81) 
	
	searchBarUrl("https://www.facebook.com/pages/?category=top")
	wait(yourPage, FOREVER);
	

	if (exists(topSuggestion)) :
		click(topSuggestion);wait(1);
		wait(yourPage, FOREVER)

		while(1):

			wheel(WHEEL_DOWN, 4);wait(1)
			if (exists(pagesLikeButton)) :
				click(pagesLikeButton)
				wheel(WHEEL_DOWN, 4);wait(1)

			if (exists(securityCheck)) :
				break

			count = count + 1

			if (count == maxCount):
				return


def actionSharePost() :

	count = 0
	maxCount = 3

	shareButton = Pattern("images/shareButton.png").similar(0.80).targetOffset(-4,-1)
	sharePopUp = Pattern("images/sharePopup.png").targetOffset(-46,0)
	sharePostButton = Pattern("images/sharePostButton.png").targetOffset(84,-3)

	##searchBarUrl("https://www.facebook.com")

	if (not exists(shareButton)) :
		return 0

	if(exists(shareButton)):
		click(shareButton)
		wait(sharePopUp, FOREVER)
		click(sharePopUp)
		wait(sharePostButton, FOREVER)
		click(sharePostButton);wait(7)
		wheel(WHEEL_DOWN, 12);wait(1)

		return 1
def actionHidePost() :

	postArrow = Pattern("images/postArrow.png").similar(0.99)
	hidePost = Pattern("images/hidePost.png").targetOffset(-56,-3)

	if (not exists(postArrow)) :
		return 0

	if(exists(postArrow)):
		click(postArrow);wait(1)

		if(exists(hidePost)):
			click(hidePost);wait(2)
			return 1

		if (not exists(hidePost)) :
			return 0

def actionNotif() :

	notifButton = Pattern("images/notif.png").exact().targetOffset(-55,2)

	if (not exists(notifButton)) :
		return 0

	if(exists(notifButton)):
		wait(4)
		click(notifButton);wait(3)
		click(notifButton);wait(1)

		return 1

'''

