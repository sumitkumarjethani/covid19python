For execute the covid19 graphics API do the following steps:
1. If it is first time that you are going to execute this API you have to retrieve the data with the next command:
	python covid19spider.py
   If you have already retrieved the data previously and you want to add to your database (covid.sqlite) the actual data you have to    use the same command mentioned above.
   But there are some countries like Spain who presents for example their data of 14/08/2020 on 15/08/2020 so if some country       does not have their data on the data base you can run the next command:
	python covid19spider -date dd/mm/yyyy (please follow the date format).
2. Make sure you run the  python covid19spider.py command every day for retriving the data correctly or the graphics showed won´t be
   the recent.
3. If you want to see the data of your covid DB on the cmd type the next command:
	python covid19basic.py
4. If you want to reset the covid DB type the next command:
	python covid19reset.py 

----------------------------------------------------------
USER INTERFACE NOT FINISHED YET IN THE SECOND COMMIT.