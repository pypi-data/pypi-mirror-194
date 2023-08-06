## Data pipeline using Delta Lake tables
We have implemented the medallion architecture by using Delta Lake tables to store and analyse our Trello data.

Bronze Delta Lake tables (Ingestion) - The raw data of all the cards of Trello boards and the Trello board members is ingested into these tables
Silver Delta Lake tables (Refinement) - The data from the Bronze tables is refined to pick required columns, join with the members lookup delta table and add board info
Gold Delta Lake tables (Aggregation) - Built based on specific use case. Eg: One of the tables consist of all the cards that are in doing list have no activity for specified number of days