# Assignment
The project is using virtual environment with python version 3.7.6
Steps for Running the Project:
1. Activate the virtual environment

2. Install the dependencies from requirements.txt file 
   pip install requirements.txt

3. Run the dev server
   python manage.py runserver
   
4. Request endpoint => http://127.0.0.1:8000/server/v1/initiate_request , Method => GET

The resulting endpoint request takes retries with exponential time in case of failures occurred while fetching response form third party api.


   
