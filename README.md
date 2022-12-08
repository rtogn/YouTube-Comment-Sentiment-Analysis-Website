You should use Markdown for your document. You can embed images using the tips here.
1.	Introduction 1.1 Purpose
The purpose of this document is to describe the implementation details and objectives of our Youtube Comment Sentiment Analysis application
1.2 Intended Audience*
This document is indented primarily for our developers and the instructor if the course. 
1.3 Intended Use
1.4 Scope
1.5 Definitions and Acronyms
This document will use the following naming conventions:
o	YCSA - Youtube Comment Sentiment Analysis. The application being discussed in this document
o	NLTK - Natural Language Toolkit (https://www.nltk.org/), Library being used for the base textual sentiment analysis.
The following words are defined as such:
o	‘User’ refers to a person that accesses the YCSA application or the general Youtube website.
o	‘Comment’ refers to a text post attached to a Youtube video made by Users.
2.	Overall Description-
2.1 User Needs
YCSA is an attempt to address two things at once:
1)	Users of the Youtube site often encounter comments that are overly negative or even offensive and there is no built-in way to screen for these comments. 
2)	Metrics such as view count and subscriptions are not necessarily indicative of the overall opinion of a video. Additionally, the removal of the ‘dislike’ count by google leaves Users with only likes to gauge how a video is received. This does not allow for negative views on a video to be considered in their selection. 
The YCSA has the potential to give Users the ability to screen out negative comments and additionally the same functionality can be used to scan comment feeds and give an opinion-based score to a video. This will improve the user experience of Youtube without interfering with the already existing interface. 
2.2 Assumptions and Dependencies
	The following assumptions are made:
1)	A sustainable number of Users both read video comments and are interested in filtering based on comment sentiment.
2)	Comment sentiment analysis is an effective metric to qualify the quality of a video in the first place. 
3)	Youtube will continue to allow comment scraping and video embedding for their videos in the future
Major dependencies:
1)	This app relies on third party libraries and APIs such as Google’s Youtube API 
2)	NLTK is used for textual analysis.
Currently these APIs are offered free of charge for use but availability and development activity could change at any time. 
3.	System Features and Requirements
3.1 Functional Requirements
3.2 External Interface Requirements
Use your design mocks for this section. 
3.3 System Requirements*
For a user, any computer with specifications sufficient for web browsing will be adequate. 
A server hosting the application backend must have enough power to process NLTK sentiment analysis. Research on the exact requirements is ongoing. 
3.4 Nonfunctional Requirements

Test:
| Task        | Owner       | Priority | Level of Effort Estimate (Days) | Additional Notes                    |
| ----------- | ----------- | -------- | ------------------------------- | ----------------------------------- |
| Implement Google Books search API call | John Martin| P1 | 3 | Some uncertainty here because google API is changing versions | 
| Style the search results page  | Mark Zuckerberg| P2 | 3  | Time-boxed task -- I'll do as much as I can in the 3 days |
| Add animations to "add" and "delete" buttons  | Elon Musk | P3 | 10 | Do you think we can charge people $8 for this too? | 
| Set up basic Flask server with favorite books | John Martin| P1 | 2 | | 
| Add and wire up search bar on main page | Bill Gates | P1 | 5 | Depends on John's API call work |
| Set up database and data models | Steve Jobs | P1 | 3 | |
| Add ability to add/delete books from favorites | John Martin | P1 |  | Depends on Steve's database work |
| Add ability to recommend further books based on existing favorites | Grace Hopper | P3 | 15 | Requires additional API research |
