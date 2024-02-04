# 1. Title and Author

- **Project Title:** Movie Recommendation System
- **Prepared for:** UMBC Data Science Master Degree Capstone by Dr. Chaojie (Jay) Wang
- **Author:** Murali krishna Avula
- **GitHub:** https://github.com/muralikrishna02
- **LinkedIn:** https://linkedin.com/in/murali-krishna-avula
- **PowerPoint Presentation:** 
- **YouTube Video:** 

# 2. Background

The movie recommendation system aims to provide personalized movie recommendations to users based on their preferences and behavior.
With the increasing popularity of streaming platforms, such systems play a crucial role in enhancing user experience and engagement.

**Research Questions:**
1. How can we leverage user preferences and movie attributes to generate accurate recommendations?
2. What machine learning algorithms and techniques are most effective for building a movie recommendation system?
3. How can we evaluate the performance and effectiveness of the recommendation system?

# 3. Data

## Data Sources
- The primary data source for this project is the https://www.themoviedb.org/ , which contains information about Movies,budget,production house and more.
- Additional data sources may include movie credits, and cast.

## Data Size
- The dataset is approximately 45 MB.
- It consists of 4804 rows and 20 columns.

## Data Dictionary

| Column Name       | Data Type    | Definition                                   | Potential Values         |
|-------------------|--------------|----------------------------------------------|--------------------------|
| movie_id          | int          | Unique identifier for each movie             |                          |
| title             | str          | Title of the movie                           |                          |
| overview          | str          | Summary or description of the movie          |                          |
| genres            | str          | Genres of the movie                          | Action, Drama, Comedy, etc. |
| keywords          | str          | Keywords associated with the movie            |                          |
| original_language | str          | Language of the movie                        | English, French, Spanish, etc. |
| popularity        | float        | Popularity score of the movie                |                          |
| release_date      | datetime     | Release date of the movie                    |                          |
| production_companies | str       | Production companies involved in the movie   |                          |

## Features/Predictors
- Potential features for the ML models include:
  - Overview
  - Genres
  - Keywords
  - Original Language
  - Popularity
  - Release Date
  - Production Companies
