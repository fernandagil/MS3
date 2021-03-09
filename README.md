# MS3
 
![]()
 
You can visit the deployed website [here](https://fernandagil.github.io/ms2-olespanish-game/).
 
---
 
## 1. UX
 
### 1.1. Project Goals

 
### 1.2. User Stories
- As a user, I want to immediately understand the purpose of the site.
- As a user, I want to be able to leave a review about a tv show I liked or disliked.
- As a user, I want to be able to edit the reviews I alredy created.
- As a user, I want to be able to delete the reviews I created.
- As a user, I want to be able to see reviews that other users have created.
- As a user, I want to be able to search for a movie or genre.
- As a user, I want to keep track of all the tv shows, movies and documentaries I’m watching at the moment.
- As a user, I want to keep track of all the tv shows, movies and documentaries I’d like to watch.
- As a user, I want to keep track of all the tv shows, movies and documentaries I already watched.
- As a user, I want to see where I could watch the shows I'm interested in.

---
 
## 2. Features
 
### 2.1. Existing features
 
### 2.2. Potential Features
 
---
 
## 3. Technologies used
 
- [HTML5](https://html.com/) - provides the content and structure for my website.
- [CSS3](http://www.css3.info/) - provides the styling.
- [Bootstrap](https://getbootstrap.com/) - used to create the layout of the project and some styling.
- [Python]() - 
- [Flask]() - used in conjunction with the Jinja2 templating language to generate the HTML templates on the backend. It was also used to access and process the data sent from the frontend to the server.
- [MongoDB]() - 
- [Balsamiq](https://balsamiq.com/) - used to create the project's wireframes.
- [Gitpod](https://gitpod.io/) - used to develop the website.
- [GitHub](https://github.com/) - 


---
 
## 4. Testing
 
The testing process can be seen [here](TESTING.md).
 
---
 
## 5. Deployment
 
###### Heroku deployment

Heroku needs some application and dependencies to run the app
1. Create a **requirements.txt** file using the terminal command  `pip freeze > requirements.txt`.
2. Create a  **Procfile ** with the terminal command  `echo web: python app.py > Procfile`.
3. Push these files to GitHub
* The Procfile might add a blank line at the bottom, and sometimes this can cause problems when running our app on Heroku, so just delete that line and save the file.
4. Go to [Heroku](https://www.heroku.com/) and once you're logged in on your dashboard, click on the **New** button and there click **Create a New App**.
5. Give the new app a name and set the region closest to you, then click the **Create App** 
6. This will take you to the **Deploy** tab of your newly created app. There go to **Deployment method** and select **GitHub**. 
7. In **Connect to GitHub**, search for your repository and click **Connect** to connect it to this app.
8. In the Heroku dashboard for the app, go to **Settings**, and then scroll down and click on **Reveal Config Vars**. Set the following config vars:
|  Key  |  Value  |
| :-------------: | :-------------: |
|  IP |  0.0.0.0  |
|  PORT  |  5000  |
|  SECRET_KEY  |  <your_secret_key>  |
|  MONGO_URI  |    |
mongodb+srv://<username>:<password>@<cluster_name>-qtxun.mongodb.net/<database_name>?retryWrites=true&w=majority
|  MONGO_DBNAME  |  movies  |

9. In the Heroku dashboard for the app, go to **Deploy**, scroll down and click on **Enable Automatic Deployment**
10. Below that select the branch that you want to deploy (in this case *master*) and click **Deploy Branch**
11. Once that’s done, you can click **View** to launch your app


---
 
## 6. Credits
 
### 6.1. Content
 
### 6.2. Media
 
### 6.1. Acknowledgments
