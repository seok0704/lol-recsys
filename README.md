# League of Legends Recommender System
![image](https://user-images.githubusercontent.com/17075250/116634200-6cdb5980-a929-11eb-92d2-230ab3da1354.png)

Champ2Play is a League of legends recommender system  built using Python and recommender system algorithm for the game of League of Legends. League of legend is a multiplayer online game that competes in two teams made of five players each. Each player selects a champion (or game character) that matches its role (Every player is given a role), and play that champion throughout the game. The problem with league of legends right now is that it is very hard for new users to join due to level of complexity and the diversity in champions. There are more than 155 champions in the game, making the new users hard to find their character that matches their playstyle.

The recommender system can provide recommendations for each user based on their match history.

![image](https://user-images.githubusercontent.com/17075250/116634343-c0e63e00-a929-11eb-8468-c11f7e43e6ec.png)
*Example of Recommendation Per User History (Shows up to top 100)*

The recommender system can also provide recommendations based on specific champion.

![image](https://user-images.githubusercontent.com/17075250/116634411-ef641900-a929-11eb-9cde-80ed6348c291.png)
*Example of Recommendation Per Champion (Shows up to top 100)*

## How it Works
The algorithm uses a collaborative recommender system to power the recommendations. Collaborative filtering is a method that use the  champions commonly by each user and determine which champions are similar to each other. For this model, it utilizes item-item similarity as it yielded the best outcome.

### Data Collection / Web Scraping
In the League of Legends API (RIOT API), it only provides leaderboards from Masters Tier which is 0.1 percentile of the players. Instead of querying data from the API, the username of the game is collected using a site called OP.GG which is an analytic site which contains the leaderboard of all users. Using Beautifulsoup Library, it extracted users above Platinum tier (Top 10%) from the leaderboard https://na.op.gg/ranking/ladder/. After extracting all users above Platinum, the algorithm browsed to individual profile of the users it extracted and scraped the number of times played for each champion and normalized the number of times played for each champion with total matches played. The higher the normalized value, the user played more frequently of that specific champion.

![image](https://user-images.githubusercontent.com/17075250/116634804-153ded80-a92b-11eb-9928-a02e7e9ad351.png)

*Table after webscraping*

### Model Implementation
Since all users have different total matches played, using the normalized value would provide consistent scale throughout users. The rating matrix is constructed using the normalized matches played per champion for each users.

As with any machine learning algorithms, various approaches were taken to achieve the best performance. The following parameters were validated:
1. Similarity: Jaccard, Cosine, Euclidean
2. Collaborative Filtering: PMF, User-User KNN, Item-Item KNN, Popularity

Evaluation is critical in machine learning projects, because it allows us to compare different algorithms and hyperparameter choices for these models.

One key aspect of evaluation is to ensure that the trained model generalizes for data it was not trained on, using Cross-validation techniques. The system utilizes 5 fold for evaluation.

In recommender system, the common evaluation metrics are R@K, P@K and RMSE. Even though the code evaluates for all three metrics, the highest priority will be R@K as we want recommender system to recommend most or all champions that users would prefer.

|                 | RMSE Mean	      | P@5 Mean        | R@5 Mean      |
| --------------- | --------------- | --------------- |---------------|
| Popularity      | 0.48374	        | 0.0572484       |0.304603       |
| User - Cosine   | 0.0960986	      | 0.00556688	    |0.0265991      |
|**Item - Cosine**| **0.0888415**  | **0.0561146**   |**0.324303**   |
| PMF             | 0.0896907       |0.0390828        | 0.239742      |

Our final model uses the item-item KNN using cosine similarity as this showed the best performance in all metrics, and the recommendation it gave made perfect sense. Additionally, the recommendation computation time is exteremely fast since the item-item rating matrix is constructed between champions whereas for user-user, the similarity matrix is constructed throughout different users, making the predictions computationally expensive.

### Recommendation Pipeline
In order to have better control over the recommendations, recommendation pipeline is built on our own. When the user searches its username, the pipeline gets user data from RIOT API (Using RiotWatcher Library) and constructs a user vector which then uses the item-item similarity matrix to receive the top 100 champion recommendations. If the user selects a champion, the tool recommends the top 100 champions based on the item-item matrix stored in the recommender system. The code can be found in the Util folder for both user recommendation and champion recommendation.

### Web App
The web application is powered by Django, a popular Python web framework. 

### Tools / Libraries Used
The major tools and libraries used are as follows:
* **Visual Studio**: Used to develop web
* **Jupyter Notebook**: For developing and testing the model. Major code in Model Implementation and Data Collection
* **Pandas**: Used to store meta-data
* **Beautiful Soup**: Webscraping for Data Collection
* **RIOT API**: Querying the live data
* **Django**: Used as the web framework
* **Numpy**: Used for matrix storing and calculation
