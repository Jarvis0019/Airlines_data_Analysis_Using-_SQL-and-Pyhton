#!/usr/bin/env python
# coding: utf-8

# In[25]:


import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# In[2]:


connection = sqlite3.connect('travel.sqlite')
cursor = connection.cursor()


# In[3]:


cursor.execute("""select name from sqlite_master where type = 'table';""")
print('List of tables present in the database')
table_list = [table[0] for table in cursor.fetchall()]
table_list


# In[4]:


aircrafts_data = pd.read_sql_query("select * from aircrafts_data", connection)
aircrafts_data


# In[5]:


airports_data = pd.read_sql_query("select * from airports_data",connection)
airports_data


# In[6]:


boarding_passes = pd.read_sql_query("select * from boarding_passes",connection)
boarding_passes


# In[7]:


bookings = pd.read_sql_query("select * from bookings",connection)
bookings


# In[8]:


flights = pd.read_sql_query("select * from flights",connection)
flights


# In[9]:


seats = pd.read_sql_query("select * from seats",connection)
seats


# In[10]:


ticket_flights = pd.read_sql_query("select * from ticket_flights",connection)
ticket_flights


# In[11]:


tickets = pd.read_sql_query("select * from tickets",connection)
tickets


# In[12]:


for table in table_list:
    print('\ntable:', table)
    column_info = connection.execute("PRAGMA table_info({})".format(table))
    for column in column_info.fetchall():
        print(column[1:3])


# In[13]:


for table in table_list:
    print('\ntable: ',table)
    df_table = pd.read_sql_query(f"select * from {table}",connection)
    print(df_table.isnull().sum())


#  How Many planes have more than 100 seats
#  

# In[14]:


pd.read_sql_query("""select aircraft_code,count(*) as num_seats from seats 
                        group by aircraft_code having num_seats >100""",connection)


# How the Number of Tickets booked and total amount earned changed with the Time?

# In[15]:


tickets = pd.read_sql_query("""select * from tickets inner join bookings
                        on tickets.book_ref = bookings.book_ref""",connection)
tickets['book_date'] = pd.to_datetime(tickets['book_date'])
tickets['date'] = tickets['book_date'].dt.date
tickets


# In[16]:


tickets.groupby('date')[['date']].count()


# In[17]:


x = tickets.groupby('date')[['date']].count()
plt.figure(figsize = (18,6))
plt.plot(x.index, x['date'], marker = '^')
plt.xlabel('Date', fontsize = 20)
plt.ylabel('Number of Tickets',fontsize = 20)
plt.grid('b')
plt.show()


# In[18]:


bookings = pd.read_sql_query("select * from bookings",connection)
bookings['book_date'] = pd.to_datetime(bookings['book_date'])
bookings['date'] = bookings['book_date'].dt.date
bookings


# In[19]:


bookings.groupby('date')[['total_amount']].sum()


# In[20]:


x = bookings.groupby('date')[['total_amount']].sum()
plt.figure(figsize = (18,6))
plt.plot(x.index, x['total_amount'], marker = '^')
plt.xlabel('Date', fontsize = 20)
plt.ylabel('Total Amount Earned',fontsize = 20)
plt.grid('b')
plt.show()


# Calculate the Average Charges for each aircrafts with different farre conditions?

# In[21]:


df = pd.read_sql_query("""select * from ticket_flights join flights on ticket_flights.flight_id = flights.flight_id""",connection)
df


# In[22]:


df = pd.read_sql_query("""select fare_conditions, aircraft_code, avg(amount)
                             from ticket_flights join flights on ticket_flights.flight_id = flights.flight_id
                             group by aircraft_code, fare_conditions""",connection)
df


# In[26]:


sns.barplot(data = df, x = 'aircraft_code', y ='avg(amount)', hue = 'fare_conditions')

