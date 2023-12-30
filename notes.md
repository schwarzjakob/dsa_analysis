# Notes for tracking progress and learning while coding

## Usefull resources to keep in mind

- [How to Update NPM Dependencies](https://www.freecodecamp.org/news/how-to-update-npm-dependencies/)
- [Create Modularized and Scalable Flask Application Using Blueprint](https://obikastanya.medium.com/create-modularized-and-scalable-flask-application-using-blueprint-15a71e2bd8a2)
- [How to Use Flask-SQLAlchemy to Interact with Databases in a Flask Application](https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application)
- [Why React developers should modularize their applications?](https://alexmngn.medium.com/why-react-developers-should-modularize-their-applications-d26d381854c1)
- [What is Redux? Store, Actions, and Reducers Explained for Beginners](https://www.freecodecamp.org/news/what-is-redux-store-actions-reducers-explained/)
- [Managing State](https://react.dev/learn/managing-state)

### While working on the project

- run project in virtual environment and install packages via requirements.txt inside the virtual environment
   - start the venv with ```source venv/bin/activate```
- Change last commit with: ```GIT_EDITOR=nano git commit --amend``` Make sure to add the files before with ```git add path/to/file```
- Showing the git tree: ```git ls-tree -r HEAD --name-only | tree --fromfile```
- Reloading Modules while testing in Pyhton shell:
 ```bash
 import dsa_analysis_app.character_analysis.character_analysis as ca
 from importlib import reload
 name = "Hanzo Shimada"
 get_character_best_and_worst_talents(name)
 reload(ca) # After changes in the script
 get_character_best_and_worst_talents(name)
 ```

## Ideas / Features planned

### General

1. [x] A good user interface landing page
2. [x] Current trait values (e.g.: MU: 14, GE: 16, ...)
    1. [x] create an empty csv file for each character and initialize it with 0
    2. [x] for each roll update this .csv with the (3) trait values
    3. [x] communicate with front end and visualize it in the analytics hub
3. [x] Relative Categories Distribution
4. [x] Modularization of Backend
5. [x] Login Landing page with Google Authentication
6. [ ] Modularization of Frontend
   1. [x] Charts into modules (Pie, Line, Data)
   2. [x] Better sorting (reusable function, cleaner code)
7. [ ] Remove webvitals
8. [ ] Check how logger can be used more usefull
   1. [ ] Debugging all accessed scripts
   2. [ ] in multiple scripts logging is imported the same way. Not sure if that makes sense, might change that
9.  [ ] Succes chance and expected value for next try of talents in the Talent, and Attack List table
    1.  [ ] First, include the same metrics into the attack table
    2.  [ ] then success chance and expected value algorithm
   1.  [ ] Need to determine current skill level of talent. (Current Traits already written down)
10. [ ] Talent list -> Talent vertical bar chart
11. [ ] Character insights
   1. [ ] Top and Worst performing talents
      1. [ ] Success Rate
      2. [ ] Avg. TaP
   2. [ ] Correlation (Scatter Plot) between total attempts and
      1. [ ] Success Rate
      2. [ ] Avg. TaP
   3. [ ] Professional skills (e.g. plus 7 for last 10 attempts = pro, plus 14 for last 10 attempts = master, or 7 for 9/10 and 14 for 9/10 attempts)
   4. [ ] Character types derived from the most used talents/categories
   5. [ ] Wasted talents ("You seem to be good in Schleichen, but you barely use it")
12. [ ] Start screen content
   1. [x] Background image
   2. [ ] guides
   3. [ ] background information
   4. [ ] video/gif/slides explaining the project
   5. [ ] faq
13. [ ] Predicter of future talent outcomes like (Hanzo Shimada: Schleichen -> 14)
14. [ ] Talent upgrade suggestions (you used "Fährtensuchen" a lot recently but your average performance was low (2). What about an upgrade)
   1. [ ] Upgrade suggestions based on XP input (this will be super complicated)
15. [ ] Talent values (recent TaW/ZfW)
16. [ ] Include list of spells for Wizards
   1. [ ] Setup Wizard attribute to Character
17. [ ] Access to pages restricted to loggedin user (google login is first page but I could just change url to dodge this login)

### Publish app

Approach to publish the app for my friends and potentially other groups

#### Hosting Online

- **Costs**: Yes, hosting an app online will typically involve some costs. However, there are affordable options, especially for small-scale applications. Providers like Heroku, AWS (Amazon Web Services), and Google Cloud Platform offer free tiers that might be sufficient for your initial needs. As your app grows, you can consider upgrading to paid plans.
- **Deployment**: For deployment, you'll need to package your Flask back-end and React front-end properly. Services like Heroku offer relatively straightforward deployment processes for both front-end and back-end applications.

### Login Functionality

- **Security**: Implementing a login functionality is essential for protecting user data and restricting access. You can use authentication services like Auth0, Firebase Authentication, or implement your own using Flask.
- **User Management**: This will also involve managing user accounts, which means you'll need a database to store user information securely.

### Lobby System

- **Real-time Interaction**: A lobby system for players to join and share data is a great feature. It implies some real-time data exchange, for which you might use WebSockets. Libraries like Socket.IO could be integrated with your Flask app.
- **Separation of Data**: Each lobby or group would have its own set of data. This requires a well-thought-out database schema to keep data separate and secure for each group.

#### Dummy Login for Portfolio Showcase

- **Demo Account**: Creating a demo account with pre-filled data is an excellent way to showcase your app to potential employers or stakeholders. It allows them to experience the functionality without needing to create an account.
- **Guided Tours**: Consider adding a guided tour or tooltips for first-time users to make the navigation intuitive.

#### General Considerations

- **User Experience**: Focus on creating a seamless and intuitive user interface. User experience is key in application design.
- **Feedback and Testing**: Get feedback from your friends and early users. Their input will be invaluable for making improvements.
- **Scalability**: Plan for scalability. If your app gains more users, you'll need to ensure it can handle increased traffic and data.
- **Legal and Privacy Considerations**: Be mindful of data privacy laws and regulations, especially if you plan to open the app to a broader audience.

### Modularization of Frontend

Given your application structure and components, a well-organized folder structure can greatly improve maintainability and readability. Here's a recommended structure tailored to your project:

### Root Directory
- **src/**
  - **components/**: Contains reusable UI components.
    - **common/**: For shared components like buttons, inputs, modals, etc.
    - **charts/**: Specific chart components used across the application.
    - **layout/**: Components related to the layout like headers, footers, navigation bars.
  - **views/**: Contains the main pages or views of your application.
    - **Login/**
    - **StartScreen/**
    - **CharacterManagement/**
    - **DsaStatsDashboard/**: Renamed from `CharacterData`.
  - **hooks/**: Custom React hooks for shared logic.
  - **services/**: For making API calls and handling other service-related logic.
  - **utils/**: Utility functions and constants.
  - **App.js**
  - **index.js**

### Detailed Breakdown

1. **src/components/common/**
   - Reusable UI elements like buttons, text inputs, loading spinners.

2. **src/components/charts/**
   - Chart components like `PieChart`, `BarChart`, `LineChart`.
   - Each chart component can have its own folder if they are complex.

3. **src/components/layout/**
   - `Header.js`, `Footer.js`, `NavigationBar.js`.
   - Could include `Home.js` if it becomes part of a menu bar or navbar.

4. **src/views/**
   - Each view

## Things to consider (from TOM)

- I added vscode extension recommendations in the `extensions.json` file. When you open the project in vscode, it should prompt you to install them. I recommend you do so, as they will help with formatting and linting. Also the settings in `.vscode/settings.json` will set the python interpreter to the virtual environment, so your dependencies actually resolve.
- Switch from CRA to Vite (low priority as you already have a working setup)
- Switch from Flask to FastAPI (low)
- Remove reportWebVitals (code in index, file, and also uninstall dependency) and instead use LightHouse (if really necessary)
- Why two charting libs? Seems unnecessary, better stick with one
- I think the python code needs some refactoring regarding the flow and format of the data. Come up with a universal data format for your app and then pass this around instead of working with raw files. What's good is that you already tried to separate business logic (in their own modules) from the HTTP controllers. In the end, the controllers act only as an interface between the client and business logic. They are responsible for request and response validation (body, query, path, parameters, response status code), and error handling. All other logic should be in the business logic modules. I recommend removing all file-related stuff into its own module and interface for the data.

## Where I left off last time

30.12.2023:
- I made the sorting for talents reusable and included it in the attacks table. That further allows to create the additional table columns for the attacks table and make them sortable as well.
- Made the column headers looking like clickable buttons.
- Tom introduced DTOs and encapsulation of functions. Need to revisit that

27.12.2023:
- Modularized last Chart (Pie Chart)

26.12.2023:
- I updated the talent table with other metrics (might remove them from the statistics of a single talent or at least reuse this for efficiency)
- I created two new bar charts which might need some slight improvement for characters with less than 10 talents with more than 10 uses.
- Next up is 100% creating a better structured front end modularity as the <mark>CharacterDashboard.js</mark> has already ~800 lines of code.
  - I started modularization with folder structure and removing Bar and Line charts into its own modules. Pie chart could be next, tables also possible to consider