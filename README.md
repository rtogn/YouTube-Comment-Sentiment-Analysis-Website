# YTSA - A Youtube comment section analysis website
<i>Team 10's repository for our 2023 Software Engineering Capstone Project, Georgia State University</i>

# Table Of Contents:
1. [Project Summary](#project-summary)   
2. [Timeline](#timeline)  
3. [Technologies Used](#technologies-used)  
4. [Setup](#setup)   
5. [Contributors](#contributors)    
6. [Special Thanks](#special-thanks)  
7. [Citations](#citations)  

# Project Summary  

# Timeline

# Technologies Used  
### [Python](https://www.python.org/)  
Primary programming language used besides web technologies  
### [Flask](https://flask.palletsprojects.com/en/2.2.x/)  
For running the application and server functions  
### [SQL-Lite](https://www.sqlite.org/index.html)  
Database model  
### [HTML/CSS]  
Markup and styling  
### [Java Script](https://www.javascript.com/)
Website interactivity etc  
### [NTLK & Sentiment Analysis Model](https://www.nltk.org/)  
	From NLTK.org:  
		><i>"NLTK is a leading platform for building Python programs to work with human language data. 
		It provides easy-to-use interfaces to over 50 corpora and lexical resources such as WordNet, 
		along with a suite of text processing libraries for classification, tokenization, stemming, 
		tagging, parsing, and semantic reasoning,wrappers for industrial-strength NLP libraries, 
		and an active discussion forum."</i>

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
[Sam Repasky](https://github.com/samrepasky)    
[Jazmine B](https://github.com/hafsa-hassan)    
[Hafsa Hassan](https://github.com/jazbar07)    
[Robert Tognoni](https://github.com/rtogn)  
