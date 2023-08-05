# Fill Datetime Data

This is a simple python script which fills in data using Pandas in Python using the aggregate mean of the data you wish to fill. 

Importing should look like:

from fill_dt_data import fill_data

The script requires two columns, one labelled exactly "data" (case sensitive) that contains datetime data in YYYYmmdd format and at least one other column that contains data that you wish to replace.

The function takes in a DataFrame, the name of the column that you wish to fill, and the starting and ending dates for the time frame that you wish to fill. It then uses up to the decade of time surrounding your dates and takes the average value for each day in each month, then fills your dates with those averages.