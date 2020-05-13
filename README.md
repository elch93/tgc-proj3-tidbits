# TIDBITS - Notes Sharing Website for the GCE 'O' Levels 
The website can be viewed [here](https://lch-notes-app.herokuapp.com/).

## Data-Centric Development Milestone Project
Build a full-stack website that allows user to manage a common dataset, which includes allowing users to share their own data with the community and having access to data by others. Main technologies used should include HTML, CSS, JavaScript, Python, Flask & Mongodb.

## Strategy
### Problem
Many students may not have access to tuition financially or may find it difficult to approach others. An online platform that provides them a degree of anonymity will allow them to have access to academic help or to offer help. 

### Proposed Solution
Create a web application to provide a self-help platform where anyone(preferably students themselves) can volunteer to teach share notes and tips. For a start, let's limit the scope to the GCE 'O' Levels. Additionally, as the saying goes, the best way to learn something is to teach.  This online platform gives users an opportunity to teach and consolidate their ideas.

### External Users' Goals
Users who want to share notes: 
1. To volunteer teach, help others out in solving school work and get better academic results.
2. Improve their own teaching skills or to build confidence in certain concepts themselves.

Students/Learners: 
1. To gain further insights, fill their knowledge gaps or learn advanced concepts from others.

### Site Owner's Goals
1. To encourage self-learning and resourcefulness.
2. Providing a platform for needy students to access notes of anyone who wants to help.

## Scope
### Required Functionalities
- CREATE/UPDATE/DELETE: Allows users to create a profile and post their notes. (flask, mongodb, summernote)
- READ: Users can access and search for the subjects they want to learn about. (js, mongodb, flask)
- Allow users to save notes to their accounts. (mongodb)
- Allow users to give a like to the note. (js, mongodb)
- Profile pages should allow users to view their own notes, saved notes from elsewhere.
- Backend codes will handle(CRUD) the database(MongoDB). Frontend codes will handle the UI/UX.
- Present notes and ideas in an elegant and neat manner.

### Frontend
HTML
CSS
JS, JQUERY
Bootstrap

### Backend
Mongodb
Python

### API
Summernote

### Syallabus
#### Geography
1. Our Dynamic Planet
2. Our Changing World

#### Chemistry
1. Experimental Chemistry
2. Atomic Structure & Stoichiometry
3. Chemistry of Reactions
4. Periodicity
5. Atmosphere
6. Organic Chemistry

#### Physics
1. Measurement
2. Newtonian Mechanics
3. Thermal Physics
4. Waves
5. Electricity & Magnetism

#### Math
1. Number & Algebra
2. Geometry & Measurement
3. Statistics & Probablity

## Structure
![Structure](readme/structure.jpg)

The website is designed such that the user will experience the following sequence:
1. Home Page:
- Gives a brief introduction about the website for users to understand the website's purpose.
- Displays the brand name and hero image for visitors to know and remember.
- Provides a login/register link for users to move to the next step.

2. Profile Page:
- Provides a brief information about the user or other users.
- The 4 panels will equip the user with knowledge about where to navigate to next and make the best use of the website.

3. CRUD Tools
- Create/Update Page should allow the user to simply create a note without much hassle.
- Search/My Notes/Liked Notes Page should allow the user to find notes according to a keyword search or by topics and subjects.
- Multiple results can be handled by pagination.

## Skeleton
The images below do not represent the actual state of the website as it is constantly improved upon. They are prototype skeletal plans for the initial making of the website. Enter the website to fully enjoy the illustrations and content.

![Skeleton-Home](readme/skeleton-home.png)

#### Home Page
Essentially, the home page is split into two halves. The top half will provide space for the hero image and brand name, while the second half will display a Hero message and a short introductory paragraph that will not take up too much attention span of students using the website. A 'get started' button is the call to action button that will allow users to login/register.


![Skeleton-Profile](readme/skeleton-profile.png)

#### Profile Page
The profile page will give the user a first look inside the website. The toolbar on the left acts as a navigation panel to the CRUD tools available for the website's objectives. The main feature of this page is the 4 panels with mascots that guide the user on their next course of action.

![Skeleton-Create](readme/skeleton-create.png)

#### Create/Update Page
The create and update page will simply provide the user with an interface of a text editor Summernote API to create/edit their notes.

![Skeleton-Read](readme/skeleton-search.png)

#### Search/Liked Notes/My Notes Page
These pages will feature a search bar on top, allowing users to search by subjects, topics and even by keywords. The desired results will then be displayed in the section below.


## UX/Surface
### Concept
Tidbits is a notes sharing website for students. The name depicts how the bite-sized information on notes can be digested by learners to fill in their knowledge gaps, just like how people eat tidbits to satisfy their appetite for food.

The mascots' design are based on the look of a notebook. Since a notes sharing website will be expected to mainly filled with text, I have decided to implement more images to strike a balance. Additionally, the mascots lighten the mood of studying since it is often viewed as unnerving and daunting to students. The multiple mascots signify the community that comes together and interacting with each other.

The tool bar on the left allows easy access for the user to choose their next course of action. It is for users to easily create or search for notes with a few clicks.

### Color Scheme
The colors of the website are mainly restricted to black, white and orange. Blue and red were intially considered as according to psychology, these two colors can help boost the efficiency of learning. However, I believe that blue will only work, for instance, on the walls of a classroom and red is used for highlighting keywords on the notes itself. Hence these two colors might be not as effective in their effects on a website.

Orange is chosen because I find that not only it meshes well with black and white, but this color also represents feelings of optimism, excitement, enthusiasm and warmth. I hope that this color will fill these emotions with inquisitive and dilligent students as they use the website.

### User Stories
1. As a teacher/student, I will click on the 'Get Started' button to sign in or sign up for an account, so that I can use the functions of this website.
2. As a content creator, I will click on the create button/panel, so that I can start creating a note and post it online.
3. As a teacher/student, I will use the options on the search bar, so that I can look for a specific note, or notes under a subject and topic.
4. As a teacher/student, I will navigate to the search page, so that I can look for a specific note, or notes under a subject and topic.
5. As a content creator, I will navigate to the my notes page, so that I can view the notes that I have created.
6. As a student, I will navigate to the liked notes page, so that I can see the notes that I have liked and saved for future references.
7. As a user, I will click on the logout button on the left panel, so that I can sign out of the website.
8. As a user, I will click on my followers/following, to view the followers/following users that I might be interested in.
9. As a user, I will click on the follow/unfollow button in a particular user's profile, so that I can follow that user and easily access his/her notes in the future. 
10. As a user, I will click on the heart-shaped icon on a note that I like, so that I can save it and view it again in the future.

## Features
### Existing Features
#### Flask Login Module
Flask Login is implemented on this website. Users have to sign up or login with an account to fully enjoy the features of the website. Flask Login provides basic security and privacy features. To sign up, the display name and email must be unique than those registered users in my Mongo database. It is possible to sign up with a dummy/fake email account (e.g. alpha@codeinstitute.com ) since there is no email verification. A bootstrap alert will appear if the display name or email the user is trying to create already exists in the database and the user has to attempt again. pbkdf2_sha256 from the passlib python module is used to encrypt users' passwords in the database.

#### Profile Info
- Own profile page
- Navigating to someone else's profile page

#### Create with Summernote API
Create a note and share your knowledge with others! The Summernote API provides features such as:
- subscript superscript (useful for math & sciences)
- highlight
- bold, italics, underline, font styles & family, font sizes
- table
- list
- fullscreen view 

#### Search Bar & Results
Search results are returned in a card form from Mongo database. Search can be done by subject, topic and keywords (or even a partial word). Each card will contain details besides the shared content such as the date posted, note owner, number of likes, subject and topic. Basic pagination allows users to view results in a more organized manner.

#### My Notes
View your own creations. Update or edit your note by clicking the edit icon on the top right. Delete a note by clicking the trash icon on the top right.

#### Like System
View your liked/saved notes in the Liked Notes page. Javascript, together with Jinja conditional-wrapped HTML, work together with my Mongo database to update the number of likes real-time (in the profile page & the respective search/my notes/liked notes pages) and will also identify liked notes such that these notes will load with hearts that are already red in color. Likes for the particular notes will appear at the bottom right of each note. Total likes received and number of liked notes by the user can be view on the user's profile page.

#### Followers System
The profile page will display the number of followers and followed users for the logged in user. Similarly to that of the Like System, Javascript, Jinja and pymongo work together to update the number of followers real-time in the profile page. However, this system is a last-minute addition and an auxiliary feature in the scope of this project. It is more of a potential feature and the pages will look unpolished, although he basic logic and coding of this feature work.


### Features Left to Implement
<!-- - News widget: Provides news articles for users to read and keep up to date with the current situation
- WHO tips & advice: Provides tips and guides on personal hygiene by WHO.
- Comparison feature: Compares statistics between two countries of interest. -->

## Technologies Used
- HTML
- CSS
- Javascript
- Jquery
- Bootstrap
- Python
- Flask, Pymongo
- Mongodb
- Google Fonts ()
- Font Awesome
- Visual Studio Code
- Git
- Github
- Heroku
- Google Chrome, Firefox
- Adobe Illustrator

## Testing
### Website Functions
<!-- - On page load, a Bootstrap modal will appear and it can be closed by clicking on either the 'Close' button or cross icon on the top right.

- Clicking on the grey search button on the top left makes the search options available. Clicking on the yellow search will make the overlap shrink and loads the desired data across the website. If not, clicking on the cross icon on the top left exits the overlay.

- Clicking on the globe button displays the global statistics. Clicking on the legends of the World Trend Chart JS filters the graph accordingly. Again, the cross icon will allow the user to exit the overlay.

- Clicking on the list button displays the countries in a list format. Clicking on the ranking button will sort the list according to their total cases. Clicking on the 'A-Z' button will sort the list according to alphabetical order. Clicking on the back to top button will bring the user to the top of the list. The cross icon will allow the user to exit the overlay as well.

- On click, the markers on the Leaflet map will load the flag image and case results for that particular country on a popup. The zoom controls allow the user to zoom in and out of the map. Clicking the x on the top right of the popup will close the popup.

- The left and right buttons on the carousel will allow the previous and next panels to be shown respectively. Clicking on the indicators below will also display the selected panel. Indicators are lighted up according to the current panel displayed. Indicators and the (prev/next) buttons change color upon hover as well. 

- Both Chart JS and DC JS graphs will allow the user to see details upon hover along the plotted points in the line. -->

### Known Bugs
<!-- - For the line chart in the Global Statistics section, the latest plot on the line does not display its details on hover.

- The console will have error messages regarding the initialisation of the Leaflet map but this does not affect the functions of the website or obstruct its goal.

- Since the API by Pomber is updated daily according to his Timezone, I have to deduct 1-2 days from the current date in order to retrieve the 'latest' data due to our Timezone differences. That being said, the numbers shown on the website will definitely be slightly behind that of those reported by the news or governments.

- Certain country names between the 2 APIs are named differently and I had to either manually rename each of them or exclude them from the data. Stats from cruise ships such as Diamond Princess were also excluded.

- I am aware that my codes, especially Javascript codes, can be further optimized. -->

### Main Challenges
<!-- - Previously, the statistics on the page usually did not display on the first time the website is loaded. This could be due to the clash in load timings of the map and APIs. To combat this issue, I deployed some setTimeout functions to allow the map to load properly first before appending statistics across the page and this seemed to have worked.

- Working on the DC JS, its syntax can be very challenging for beginner coders like me. On the other hand, Chart JS is more beginner friendly. Both have their own perks and cons. I chose to use both in this website in order to practice my coding. Arguably, I should be consistent and stick to one type next time. -->

## Deployment
### My Process
<!-- 1. The project is based on Code Institute's template and was cloned upon initialisation to my local drive through git clone in the command prompt.

2. Visual Studio Code was employed to code the website. Chrome browser was my go to browser to preview my website. 

3. The master branch of the website was deployed through Github. -->

### Running My Code
<!-- 1. You can either use the fork function on github or clone/download button to duplicate the files in my master branch. For cloning, type git clone https://github.com/elch93/tgc-proj2-covid19world.git in your system's command prompt.

2. Use a code editor/IDE such as Visual Studio Code or Gitpod to open the folder and preview the website by running the code. -->


## Credits

### Content
<!-- - COVID-19 Time Series API by [Pomber](https://github.com/pomber/covid19).
- Countries information (e.g. flag pictures, country coordinates) API by [Apilayer](https://github.com/apilayer/restcountries).
- W3Schools for various tutorials: bootstrap modal, custom carousel.
- Stackoverflow for helpful answers in helping me create my dc d3 js charts and modifying the Leaflet map, as well as teaching me the code for thousands separator.
- Leaflet Map tutorial by my [lecturer](https://github.com/kunxin-chor/tgc5-leaflet).  -->


### Media
<!-- - Country flags are credited to restcountries API as stated above. -->

### Acknowledgements
- This project is inspired by an app called Deepstash and websites like StackOverflow.
- The original character design is inspired by artist [Brent Kobayashi](http://www.meowza.org/).
- This is for educational use.
