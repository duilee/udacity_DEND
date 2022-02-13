# Capstone Project

## Introduction
The main dataset will include data on immigration to the United States, and supplementary datasets will include data on airport codes, U.S. city demographics, and temperature data. 

## Datasets
I94 Immigration Data: This data comes from the US National Tourism and Trade Office. A data dictionary is included in the workspace. This is where the data comes from. There's a sample file so you can take a look at the data in csv format before reading it all in. You do not have to use the entire dataset, just use what you need to accomplish the goal you set at the beginning of the project.
World Temperature Data: This dataset came from Kaggle. You can read more about it [here](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data).
U.S. City Demographic Data: This data comes from OpenSoft. You can read more about it [here](https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/).
Airport Code Table: This is a simple table of airport codes and corresponding cities. It comes from [here](https://datahub.io/core/airport-codes#data).

## Database Schema

Immigrants Table holds the core information needed and dimension tables (temperature, demographics, airport) can be joined if additional information is  neccessary 

| Table |Description |
| --- |-----------|
| immigrants | Fact table for i94 immigrations data|
| temperature | Dimension table for temperature data|
| demographics| Dimension table for city demographics data|
| airport | Dimension table for airports information data|

### Immigrants

| Column |Type|
| --- |-----------|
|cicid  |  FLOAT PRIMARY KEY|
|    year  |   FLOAT|
|    month  |  FLOAT|
|    cit    |  FLOAT|
|    res    |  FLOAT|
|    iata   |  VARCHAR(3)|
|    arrdate | FLOAT|
|    mode   |  FLOAT|
|    addr   |  VARCHAR|
|    depdate | FLOAT|
|    bir     | FLOAT|
|    visa    | FLOAT|
|    count   | FLOAT|
|    dtadfile |VARCHAR|
|    entdepa | VARCHAR(1)|
|    entdepd | VARCHAR(1)|
|    matflag | VARCHAR(1)|
|    biryear | FLOAT|
|    dtaddto | VARCHAR|
|    gender  | VARCHAR(1)|
|    airline | VARCHAR|
|    admnum  | FLOAT |
|    fltno   | VARCHAR |
|   visatype | VARCHAR |

### Temperature

| Column |Type|
| --- |-----------|
|    timestamp              |        DATE|
|    average_temperature     |       FLOAT|
|    average_temperature_uncertainty | FLOAT|
|    city                      |     VARCHAR|
|    country                   |     VARCHAR|
|    latitude                   |    VARCHAR|
|    longitude                 |     VARCHAR|

### Demographics

| Column |Type|
| --- |-----------|
|    city           |        VARCHAR|
|    state          |        VARCHAR|
|    media_age      |        FLOAT|
|    male_population |       INT|
|    female_population  |    INT|
|    total_population   |    INT|
|    num_veterans       |    INT|
|    foreign_born       |    INT|
|    average_household_size | FLOAT|
|    state_code         |    VARCHAR(2)|
|    race               |    VARCHAR|
|    count              |    INT|

### Airports

| Column |Type|
| --- |-----------|
|    iata_code  |  VARCHAR PRIMARY KEY |
|    name       |  VARCHAR |
|    type       |  VARCHAR |
|    local_code  | VARCHAR |
|    coordinates | VARCHAR|
|    city        | VARCHAR|
|    elevation_ft | FLOAT|
|    continent  |  VARCHAR|
|    iso_country | VARCHAR|
|    iso_region  | VARCHAR|
|    municipality  | VARCHAR|
|    gps_code   |  VARCHAR|

## Mapping Out Data Pipelines
List the steps necessary to pipeline the data into the chosen data model
- execute create_tables.py to create tables
- create airports data
- insert data

## Complete Project Write Up
##### Who is going to use the data model
- Anyone interested in immigration data or those who needs immigration data in regular basis should be the core audience  
- i.e. government officials in immigration, data analysts working at NGO,... etc

##### What are the types of questions that can be answered
- location specific statstics including airports, city
- immigrations in certain period of time
- immigration information by visa tpye
- demographics of immigrants
- etc...

  
##### Clearly state the rationale for the choice of tools and technologies for the project.
- Pandas and Python is used for the convenience at data visualizing and data processing. When data get bigger to process, Spark or EMR, or other distributed service should be considered. Python is used as Jupyter notebook is the main programming environment.  

- Star Schema fits this project with immigration data at the center. As the project centers round immigration data, it is rational that immigration data serves as the core fact table. And dimension table such as temperature, demographics can be used if addtional information is needed
    
##### Propose how often the data should be updated and why.
- Since the immigration data is aggregated monthly according to the table. Monthly update is recommended

##### Write a description of how you would approach the problem differently under the following scenarios:
 * The data was increased by 100x.
     - Data should be processed in a distributed way, hence use Spark with EMR
 * The data populates a dashboard that must be updated on a daily basis by 7am every day.
     - Schedule a Dag using Airflow at the desired time and have it run daily.
 * The database needed to be accessed by 100+ people.
     - Use AWS Reshift to easily process data accessed by many people and use db role to assign appropriate roles

##### sample query with this dataset can answer
- immigrations by iata code  
    ''' SELECT iata, COUNT(cicid) AS cnt
        FROM immigrations
        ORDER BY 2 DESC'''
