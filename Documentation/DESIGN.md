CS50 Design Documentation.


Overview:
The application is mainly a series of calls to the database when certain buttons are clicked.
The webpage is static, and to make it user friendly we decided to design it simply.

Backend Design:
Using CS50’s finance a s template, we implemented a number of functions to be run for specific routes.
Here we will describe what each route does:
/check
checks if the username the user picked is available because username is something we require to be unique for our web app to run well.
It will let the user know if the username is available or not in the form of a pop-up notification. We borrowed this functionality from
cs50’s finance and kept it because it is a good way to avoid duplicate values in our database.
“/”
This is the route for our index page which displays all the links to events in their respective categories with accompanying linkified
images for user friendliness. This works by getting information from a list of strings called categories that is hard-coded and linkifies each string.
This page does not require login since it is for public use.

“/search”
This function collects information from the search form and makes a database call collecting from our events table  any pieces of data that is
like the information the user has searched for. If there is none, the user is informed that no items match the search.
“/login” and “/register”
Inspired by cs50 finance, these routes allow our pre-assigned administrators to login and register. The /register route makes sure
no one puts in information that could potentially be a SQL injection attack.
“/newevent”
Allows preassigned administrator to post new events by filling out a form. From this form we extract information about the event, and
after checking that none of the information provided is empty, we insert into the events table of our database to store this information.
The admin then gets redirected to the index page after posting.

"/study_abroad", "/research", "/internship", "/volunteer", "/boston", "/clubs", "/campus", "/other"
These routes all have the same structure. They  each take in the respective category name as a parameter to query the database. The results
of the query then get stored   in a list of dictionaries called ordered_events. The list is then parsed as the events.html pages is rendered.


/events
This route allows the displaying of all the events available. Using a hardcoded list of event categories, a for loop is made querying
the database for events in each category in the list and appending an empty list called "orderedevents" each time. Ordered_events
in this case is a list of lists of dictionaries. The list ordered_events is then parsed when allevents.html is rendered. We chose to
structure it this way rather than hard-coding the data in an html table so as to  make it such that the displayed events will be accurate each time.

/history
Only available to logged in admins. This route allows admins to view a history of all the events they have posted since registering. This works
by collecting all events the logged in admin has posted from the database using the logged in user’s unique id. This information is stored in a list
of dictionaries, which is then parsed when the history.html page is rendered.
/reviews
This allows users to leave reviews of events they have attended. Data is collected from the form and when blanks have been checked for, the information
is inserted into a stored into a reviews table. Users are also not permitted to review events that never occured.
/feedback
This allows users to view feedback left by other users. It makes a query to the database to fetch all data in the reviews table and stores it
in a list of dictionaries. This list is then parsed when the feedback.html page is rendered.

Front End
This is mainly rendering of html pages.
Index.html
It displays all the links to the different categories in the form of a table against a clear background.
Events.html
This page is dynamic, containing a for loop that loops through a list of dictionaries called ordered_events that presents. For each dictionary called
row in the list ordered events, the event_name, event_category, event_location, event_date, and event_time all displayed in the form of descending
header sizes. All /category routes parse information to this page.
Allevents.html
This is also a dynamic page similar to events.html. The only difference is that it has ordered events being a list of lists of dictionaries and
so has two for loops to ensure eventual indexing into the dictionary called row. The information comes from the /events route.
Feedback.html, Review.html
Review.html displays a form for the user to put in their review information for an event. This information gets posted and ends up being
stored in the database.
Feedback.html allows users to view all the reviews left by other users using the similar layout to events.html
Newevent.html
This is only available to logged in admins and it displays a form for the admin to input information and post new events.
Style.css
This takes care of some of the aesthetics of our page that we prefered to not use bootstrap for.
Share button
This allows user to share an event they like with a friend using mailto functionality which opens the default mailing app on the user's computer.
There is a default message in the body of the mail that they can edit and send.