# YTSA - YouTube Comment Sentiment Analysis Site

<i>Team 10's repository for our 2023 Software Engineering Capstone Project, Georgia State University. This project was part of GSU's two-semester pilot Software Engineering course organized and taught by Meta engineers.</i>

<div align="center">
	<img src="https://user-images.githubusercontent.com/60898339/233756899-d1fe7df6-ebe9-4d40-9c7d-0aebfc592297.gif" width=75% height=75%>  
</div>


# Table Of Contents
1. [Project Summary](#project-summary)   
2. [How To Use](#how-to-use)  
3. [Timeline](#timeline)  
4. [Technologies Used](#technologies-used)  
5. [Linting Exceptions](#linting-exceptions)
6. [Setup](#setup)   
7. [Citations](#citations)  
8. [Special Thanks](#special-thanks)    
9. [Contributors](#contributors)  

# Project Summary  
How can we judge comments beyond likes and pedantic numbers? Is there a way to really see what users think without relying on forced inputs?

The YTSA is an experimental site that attempts to add a new metric to comment sections: sentiment score. The website YouTube has been chosen for its popularity, ease of API access and organizational structure. The site’s core concept is using a machine learning algorithm to automatically rank comments for their emotional content also known as 'sentiment'. This means the direct input from a user can be incorporated in an overall opinion score for a video, channel, or content category. 


# How To Use  
1.Type any search term you want into the bar at the top.   


<div align="center">
	<img src="https://user-images.githubusercontent.com/60898339/233756998-40da9834-d68a-4523-a46f-8d72be7d4a39.gif" width=75% height=75%>  
</div>



2. Click on a video thumbnail on the search results page that will load. (If you do not see video thumbnails you likely set up your API key incorrectly, please revisit the instructions for setup later in this document).  


<div align="center">
	<img src="https://user-images.githubusercontent.com/60898339/233757075-588492ff-c27f-48a7-8a8f-2954da97b8b2.png" width=50% height=50%>  
</div>

3. You will see a page displaying an embedded video. The sentiment score will be under the video and next to each individual comment. This score is between -1 and 1 where 1 is 'maximally positive' and -1 is 'maximally negative'.  


<div align="center">
	<img src="https://user-images.githubusercontent.com/60898339/233757168-e63b2eff-cf12-4f43-b017-29e8c3935016.png" width=50% height=50%>  
</div>  

# Timeline
This project is being done over 5 two-week sprints. The due dates for each are as follows:

-Sprint 1: 02/03/2023  
-Sprint 2: 02/17/2023  
-Sprint 3 (MVP): 03/03/2023   
-Sprint 4: 03/24/2023   
-Sprint 5 (final): 05/7/2023  

# Technologies Used  
### [Python](https://www.python.org/) <img src="https://user-images.githubusercontent.com/60898339/222571123-81f8e8e4-b183-4f92-a4bc-95d9d3e9f007.png" width=25 height=25>

Primary programming language used besides web technologies.  
### [Flask](https://flask.palletsprojects.com/en/2.2.x/) <img src="https://user-images.githubusercontent.com/60898339/222574843-b9c32f58-7b44-4d1f-a44a-d1a53a1a4496.png" width=45 height=45>  
For running the application and server functions 

### [SQL-Lite](https://www.sqlite.org/index.html)  <img src="https://user-images.githubusercontent.com/60898339/222572307-a5bdbe50-a20d-4ac9-af3a-4309e3fa0bfb.png" width=50 height=40>  
  
Database model  
### [HTML/CSS] <img src="https://user-images.githubusercontent.com/60898339/222574007-28bee166-7f24-405b-a047-ccc2bd4dcebf.png" width=40 height=30>    
  
Markup and styling  
### [Java Script](https://www.javascript.com/)  <img src="https://user-images.githubusercontent.com/60898339/222573321-d3cf30f6-b451-4bf7-aa0e-b2952cd582bc.png" width=25 height=25>    
Website interactivity etc  
### [NTLK & Sentiment Analysis Model](https://www.nltk.org/)  
	
		"NLTK is a leading platform for building Python programs to work with human language data. 
		It provides easy-to-use interfaces to over 50 corpora and lexical resources such as WordNet, 
		along with a suite of text processing libraries for classification, tokenization, stemming, 
		tagging, parsing, and semantic reasoning, wrappers for industrial-strength NLP libraries, 
		and an active discussion forum." -NLTK.org

The sentiment analysis performed on comments is done using [VADER](https://www.nltk.org/api/nltk.sentiment.vader.html) (Hutto, C.J. & Gilbert, E.E. 2014) that is built into the NLTK library.

# Linting Exceptions  
The following linting exceptions are applied:
1. sql_models.py: too-few-public-methods.   
	This section includes SQL classes, not standard data classes so they do not need to follow all normal conventions of class structure
2. vader.py: protected-access  
	This section includes SSL calls for setup that are unnecessarily flagging under pylint

3. main.py->function video_view(): disable=too-many-statements
	This is a very long routing function that involves a lot of API information. The current plan is to attempt a refactor but it has been placed on disable for now for linting. 


# Setup 
Index:  
a. [Installing Requirements](#installing-requirements)  
b. [Setting Up Your API Key](#setting-up-your-api-key)  
c. [Setting Up Your env File](#setting-up-your-env-file)  
d. [Local Hosting](#local-hosting)  
 
### [Installing Requirements](https://www.geeksforgeeks.org/how-to-install-python-packages-with-requirements-txt/)
<i>Steps may vary slightly depending on operating system, though the final pip command is the same</i>  
1. Open a command line (searching for 'terminal' in your programs should pull one up on a given OS)  
2. Navigate to the root project folder (where requirements.txt is located)  
3. Type the following command: pip install -r requirements.txt  
	It should look like the following:    
	
<div align="center">
	<img src="https://user-images.githubusercontent.com/60898339/222609251-fcd33540-6c5a-4ad6-a89c-c803303b6acc.png" width=50% height=50%>
</div>

4. Wait for process to complete. If any errors occur reference the given error code.  


### [Setting Up Your API Key](https://developers.google.com/youtube/v3/getting-started)
<i>Even locally hosting a YTSA instance requires a YouTube API key. You will need to first [create/log into a Google account](https://support.google.com/accounts/answer/27441?hl=en) to proceed</i>
1. Navigate to (https://console.cloud.google.com/apis/dashboard)
2. Click on Credentials on the sidebar (see below)
3. Click on + CREATE CREDENTIALS on the top of the window
<div align="center">
	<img src="https://user-images.githubusercontent.com/60898339/222607858-0d541aac-352e-429a-9751-e48df3144a3c.png" width=50% height=50%>
</div>

4. Select API Key from the dropdown menu and wait for it to be created. The text listed in "Your API Key" made up of random letters is your new key. You will return to this page to copy the key later for your .env (environment) file.  
5. On the same page select 'Enabled APIs & services' on the side bara, then select '+ ENABLE APIS AND SERVICES' at the top of the page  
6. After being redirected, type 'YouTube' in the search bar and hit enter  
7. A few options will come up, select 'YouTube Data API v3'  

<div align="center">
	<img src="https://user-images.githubusercontent.com/60898339/222608508-ef2b6974-c49c-4419-8aca-a22cb2fd47a7.png" width=50% height=50%>
</div>
8. On the next page click the blue ENABLE button to activate the YouTube data API
<div align="center">
	<img src="https://user-images.githubusercontent.com/60898339/222608627-18347a2b-abce-431f-b0bc-1ec4a0c55084.png" width=50% height=50%>
</div>


### Setting Up Your env File  
1. Navigate to the root folder of the YTSA project (where main.py is located)  
2. Create a text file titled .env (there should be no file name, just the extension)  
	It should look something like this if done correctly:  
	
<div align="center">
	<img src="https://user-images.githubusercontent.com/60898339/222562706-52bb9830-d476-48ca-bc31-5627d09f347b.png" width=25% height=25%>
</div>  

3. Open the .env file and type 'APIKEY=' and then paste your API key ([get it here](https://console.cloud.google.com/apis/credentials)) you made before right after the = symbol
	It should be the only thing in the file and be placed on the first line with no spaces.  
	And it will look something like this (the key listed here is random keyboard mashing):  
	
<div align="center">
	<img src="https://user-images.githubusercontent.com/60898339/222563638-c778f76c-ecf7-493e-9ef5-ee78b98796fa.png" width=50% height=50%>
	</div>  
	
4. Save your .env document
5. You are now ready to locally host the YTSA site!


### Local Hosting  
<i>Hosting a local instance is easy! If all of the above requirements (python reqs, api key, .env file etc) you should only have to click main.py and you are running.</i>
1. Navigate the main YTSA folder
2. Run main.py (command: py main.py)
3. Highlight and copy the displayed IP address hyperlink (See image below for example)
<div align="center">
	<img src="https://user-images.githubusercontent.com/60898339/222568081-26f66f9a-54f6-494b-92df-5eaa479a8df5.png">
</div>
4. Open a Web browser and paste the link address in the URL bar and hit enter  
5. Welcome to the YTSA!  

# Citations  
>Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

# Special Thanks  
Team 10 would like to thank our Capstone guides: John Martin & Batya Zamansky from Meta!

# Contributors  
<div align="center">
	<img src="https://user-images.githubusercontent.com/60898339/222605336-a48fb95a-0920-4272-bb12-c356879eabf0.png">
</div>    

<div align="center">
	<tr>
		<td>
		Jazmine Barnett <a href="https://github.com/jazbar07"><img src="https://user-images.githubusercontent.com/60898339/222575865-617bc990-796a-4e29-834e-b30762f11526.png" width=40 height=40></a>
		<a href="https://www.linkedin.com/in/jazmine-barnett-21b744236"><img src="https://user-images.githubusercontent.com/60898339/222576175-1d3213f8-a001-4e7e-bb75-046fe5951fe3.png" width=40 height=40></a>
		</td>  
		<td>
		Hafsa Hassan <a href="https://github.com/hafsa-hassan"><img src="https://user-images.githubusercontent.com/60898339/222575865-617bc990-796a-4e29-834e-b30762f11526.png" width=40 height=40></a>
		<a href="https://www.linkedin.com/in/hafsa-hassan-609751227"><img src="https://user-images.githubusercontent.com/60898339/222576175-1d3213f8-a001-4e7e-bb75-046fe5951fe3.png" width=40 height=40></a>
		</td>  
		<td>
		Sam Repasky <a href="https://github.com/samrepasky"><img src="https://user-images.githubusercontent.com/60898339/222575865-617bc990-796a-4e29-834e-b30762f11526.png" width=40 height=40></a>
		<a href="https://www.linkedin.com/in/samantha-repasky-44188918b/"><img src="https://user-images.githubusercontent.com/60898339/222576175-1d3213f8-a001-4e7e-bb75-046fe5951fe3.png" width=40 height=40></a>
		</td>  
		<td>
		Robert Tognoni <a href="https://github.com/rtogn"><img src="https://user-images.githubusercontent.com/60898339/222575865-617bc990-796a-4e29-834e-b30762f11526.png" width=40 height=40></a>
		<a href="https://www.linkedin.com/in/robert-tognoni-9a4795b0"><img src="https://user-images.githubusercontent.com/60898339/222576175-1d3213f8-a001-4e7e-bb75-046fe5951fe3.png" width=40 height=40></a>
		</td>  
	</tr>
</div>


