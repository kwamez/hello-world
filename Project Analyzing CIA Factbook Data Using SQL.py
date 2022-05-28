#!/usr/bin/env python
# coding: utf-8

# In this project we'll be working with SQL in combination with Python. Specifically we'll use sqlite3. We will analyze the database file "factbook.db" which is the CIA World Factbook. We will write queries to look at the data and see if we can draw any interesting insights.

# In[19]:


#import sql3, pandas and connect to the databse.
import sqlite3
import pandas as pd
conn = sqlite3.connect("factbook.db")

#activates the cursor
cursor = conn.cursor()

#the SQL query to look at the tables in the databse
q1 = "SELECT * FROM sqlite_master WHERE type='table';"

#execute the query and read it in pandas, this returns a table in pandas form
database_info = pd.read_sql_query(q1, conn)
database_info


# Let's begin exploring the data, we can use pd.read_sql_query to see what the first table looks like

# In[20]:


q2 = "SELECT * FROM facts"

data = pd.read_sql_query(q2, conn)
data.head()


# In[21]:


q3 = "SELECT MIN(population), MAX(population), MIN(population_growth), MAX(population_growth) FROM facts"
data = pd.read_sql_query(q3, conn)
data.head()


# In[22]:


q4 = "select * from facts where population == (select min(population) from facts)"
data = pd.read_sql_query(q4, conn)
data.head()


# In[23]:


q5 = "select * from facts where population == (select max(population) from facts)"
data = pd.read_sql_query(q5, conn)
data.head()


# It doesn't make much sense to include Antarctica and the entire world as a part of our data analysis, we should definitely exlude this from our analysis.
# 
# We can write a SQL query along with subqueries to exlude the min and max population from the data.

# In[24]:


import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().magic('matplotlib inline')

q6 = '''
SELECT population, population_growth, birth_rate, death_rate
FROM facts
WHERE population != (SELECT MIN(population) from facts)
AND population != (SELECT MAX(population) from facts)
'''

data = pd.read_sql_query(q6, conn)
data.head()


# In[25]:


q6 = "select avg(population), avg(area) from facts"
data = pd.read_sql_query(q6, conn)
data.head()


# In[27]:


q7 = "select * from facts where population > (select avg(population) from facts)"
data = pd.read_sql_query(q7, conn)
data.head()


# In[28]:


q8 = "select * from facts where area < (select avg(area) from facts)"
data = pd.read_sql_query(q8, conn)
data.head()


# Suppose we are the CIA and we are interested in the future prospects of the countries arround the world. We can plot histograms of the birth rate, death rate, and population growth of the countries.

# In[29]:


fig = plt.figure(figsize=(10,10))
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
ax4 = fig.add_subplot(2,2,4)

data["birth_rate"].hist(ax=ax1)
ax1.set_xlabel("birth_rate")
data["death_rate"].hist(ax=ax2)
ax2.set_xlabel("death_rate")
data["population_growth"].hist(ax=ax3)
ax3.set_xlabel("population_growth")
data["population"].hist(ax=ax4)
ax4.set_xlabel("population")

plt.show()


# The birth_rate and population growth plot both show a right-skewed distribution, This makes sense as birth rate and population growth are directly related. The death_rate plot shows a normal distribution, almost a double peaked distribution. The population plot is a bit hard to read due to outliers.
# 
# Next we are interested to see what city has the highest population density

# In[30]:


q7 = '''
SELECT name, CAST(population as float)/CAST(area as float) "density"
FROM facts
WHERE population != (SELECT MIN(population) from facts)
AND population != (SELECT MAX(population) from facts)
ORDER BY density DESC
'''

data = pd.read_sql_query(q7, conn)
data.head()


# Looks like Macau has the highest population density in the world, not too surprising because Macau is a tourist heavy town with tons of casinos.

# In[31]:


fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(1,1,1)

data['density'].hist()

plt.show()


# Again there are several outliers making the data hard to read, let's limit the histogram and increase the number of bins.

# In[32]:


fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)

data['density'].hist(bins=500)
ax.set_xlim(0, 2000)
plt.show()


# This table includes cities along with countries. The cities will obviously have way higher density than the countries. So plotting them both together in one histogram doesn't make much sense
# 
# This explains why the population histogram we did earlier showed a similar trend.
