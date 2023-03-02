# YTSA - A Youtube comment section analysis website
<i>Team 10's repository for our 2023 Software Engineering Capstone Project, Georgia State University</i>

# Table Of Contents
1. [Project Summary](#project-summary)   
2. [Timeline](#timeline)  
3. [Technologies Used](#technologies-used)  
4. [Setup](#setup)   
5. [Contributors](#contributors)    
6. [Special Thanks](#special-thanks)  
7. [Citations](#citations)  

# Project Summary  
How can we judge comments beyond likes and pedantic numbers? Is there a way to really see what users think without relying on forced inputs?

The YTSA is an experimental project that attempts to add a new metric to comment sections: sentiment score. The website Youtube has been chosen for its popularity, ease of API access and orginizational structure. The sites core concept is using a machine learning algorithm to automatically rank comments for their emotional content also konwn as 'sentiment'. This means the direct input from a user can be incorporated in an overal opinion score for a video, channel or content category. 



# Timeline
This project is being done over 5 two week sprints. The due dates for each are as follows:

-Sprint 1:
-Sprint 2:
-Sprint 3 (MVP):
-Sprint 4:
-Sprint 5 (final):

# Technologies Used  
### [Python](https://www.python.org/) <img src="https://user-images.githubusercontent.com/60898339/222571123-81f8e8e4-b183-4f92-a4bc-95d9d3e9f007.png" width=25 height=25>

Primary programming language used besides web technologies  
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
		tagging, parsing, and semantic reasoning,wrappers for industrial-strength NLP libraries, 
		and an active discussion forum." -NLTK.org

The sentiment analysis performed on comments is done using [VADER](https://www.nltk.org/api/nltk.sentiment.vader.html) (Hutto, C.J. & Gilbert, E.E. 2014) that is built into the NLTK library.

# Setup 
Index:  
a. [Installing Requirements](#installing-requirements)  
b. [Getting Your API Key](#getting-your-api-key)  
c. [Setting Up Your env File](#setting-up-your-env-file)  
d. [Local Hosting](#local-hosting)  
 
### [Installing Requirements](https://www.geeksforgeeks.org/how-to-install-python-packages-with-requirements-txt/)
<i>Steps may vary slightly depending on operating system, though the final pip command is the same</i>  
1. Open a command line (seraching for 'terminal' in your programs should pull one up on a given OS)  
2. Navigate to the root project folder (where requirements.txt is located)  
3. Type the following command: pip install -r requirements.txt  
	It should look like the following:    
	
<div align="center">
	<img src="https://user-images.githubusercontent.com/60898339/222560998-33a6e556-66b3-4354-a8e2-8a6fecac2c1b.png" width=50% height=50%>
</div>

4. Wait for process to complete. If any errors occur reference the given error code.  
### [Getting Your API Key](https://blog.hubspot.com/website/how-to-get-youtube-api-key)
<i>Even locally hosting a YTSA instance requires a Youtube API key. You will need to first [create/log into a Google accout to proceed](https://support.google.com/accounts/answer/27441?hl=en)</i>
### Setting Up Your env File  
1. Navigate to the root folder of the YTSA project (where main.py is located)  
2. Create a text file titled .env (there should be no file name, just the extension)  
	It should look something like this if done correctly:  
	
<div align="center">
	<img src="https://user-images.githubusercontent.com/60898339/222562706-52bb9830-d476-48ca-bc31-5627d09f347b.png" width=25% height=25%>
</div>  

3. Open the .env file and type 'APIKEY=' and then paste your API key you made before right after the = symbol
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
3. Hilight and copy the displayed IP address hpyerlink (See image below for example)
<div align="center">
	<img src="https://user-images.githubusercontent.com/60898339/222568081-26f66f9a-54f6-494b-92df-5eaa479a8df5.png">
</div>
4. Open a Web browser and paste the link address in the URL bar and hit enter  
5. Welcome to the YTSA!  

# Citations  
>Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

# Special Thanks  

# Contributors  
Sam Repasky [<img src="https://user-images.githubusercontent.com/60898339/222575865-617bc990-796a-4e29-834e-b30762f11526.png" width=40 height=40>](https://github.com/samrepasky)[<img src="https://user-images.githubusercontent.com/60898339/222576175-1d3213f8-a001-4e7e-bb75-046fe5951fe3.png" width=40 height=40>](https://www.linkedin.com/)  
Jazmine B [<img src="https://user-images.githubusercontent.com/60898339/222575865-617bc990-796a-4e29-834e-b30762f11526.png" width=40 height=40>](https://github.com/jazbar07)[<img src="https://user-images.githubusercontent.com/60898339/222576175-1d3213f8-a001-4e7e-bb75-046fe5951fe3.png" width=40 height=40>](https://www.linkedin.com/)    
Hafsa Hassan  [<img src="https://user-images.githubusercontent.com/60898339/222575865-617bc990-796a-4e29-834e-b30762f11526.png" width=40 height=40>](https://github.com/hafsa-hassan)[<img src="https://user-images.githubusercontent.com/60898339/222576175-1d3213f8-a001-4e7e-bb75-046fe5951fe3.png" width=40 height=40>](https://www.linkedin.com/)     
Robert Tognoni [<img src="https://user-images.githubusercontent.com/60898339/222575865-617bc990-796a-4e29-834e-b30762f11526.png" width=40 height=40>](https://github.com/rtogn)[<img src="https://user-images.githubusercontent.com/60898339/222576175-1d3213f8-a001-4e7e-bb75-046fe5951fe3.png" width=40 height=40>](https://www.linkedin.com/in/robert-tognoni-9a4795b0)    
