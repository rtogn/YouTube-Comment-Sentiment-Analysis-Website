You should use Markdown for your document. You can embed images using the tips here.
##1.	Introduction 
###1.1 Purpose
The purpose of this document is to describe the implementation details and objectives of our Youtube Comment Sentiment Analysis application
###1.2 Intended Audience*
This document is intended primarily for our developers and the instructor of the Software Engineering 4351 course. 

###1.3 Intended Use -- Sam


###1.4 Scope  -- Sam


###1.5 Definitions and Acronyms

This document will use the following naming conventions:
o	YCSA - Youtube Comment Sentiment Analysis. The application being discussed in this document
o	NLTK - Natural Language Toolkit (https://www.nltk.org/), Library being used for the base textual sentiment analysis.

The following words are defined as such:
o	‘User’ refers to a person that accesses the YCSA application or the general Youtube website.
o	‘Comment’ refers to a text post attached to a Youtube video made by Users.

##2.	Overall Description-

###2.1 User Needs

YCSA is an attempt to address two things at once:
1)	Users of the Youtube site often encounter comments that are overly negative or even offensive and there is no built-in way to screen for these comments. 
2)	Metrics such as view count and subscriptions are not necessarily indicative of the overall opinion of a video. Additionally, the removal of the ‘dislike’ count by google leaves Users with only likes to gauge how a video is received. This does not allow for negative views on a video to be considered in their selection. 
The YCSA has the potential to give Users the ability to screen out negative comments and additionally the same functionality can be used to scan comment feeds and give an opinion-based score to a video. This will improve the user experience of Youtube without interfering with the already existing interface. 

###2.2 Assumptions and Dependencies
	The following assumptions are made:
1)	A sustainable number of Users both read video comments and are interested in filtering based on comment sentiment.
2)	Comment sentiment analysis is an effective metric to qualify the quality of a video in the first place. 
3)	Youtube will continue to allow comment scraping and video embedding for their videos in the future

Major dependencies:
1)	This app relies on third party libraries and APIs such as Google’s Youtube API 
2)	NLTK is used for textual analysis.
Currently these APIs are offered free of charge for use but availability and development activity could change at any time. 
3. 	System Features and Requirements

###5.1 Functional Requirements – hafsa (+ Jaz will help bc she’s not sure what else to do)



###3.2 External Interface Requirements



###3.3 System Requirements*
For a user, any computer with specifications sufficient for web browsing will be adequate. 
A server hosting the application backend must have enough power to process NLTK sentiment analysis. Research on the exact requirements is ongoing. 

###3.4 Nonfunctional Requirements – Jaz

