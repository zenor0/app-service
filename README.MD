# db-app-service

This is readme file

## deployment

1. Clone this repository:

   ```shell
   git clone

   ```
2. Enter the project directory:

   ```shell
   cd db-app-service
   ```
3. Create a virtual environment:

   ```shell
   python -m venv env
   ```
4. Activate the virtual environment:

   ```shell
   source env/bin/activate
   ```
5. Install dependencies:

   ```shell
   pip install -r requirements.txt
   ```
6. Init the database:
   
      ```shell
      make init-db
      ```

7. Run the app:

   ```shell
   python app-service.py
   ```
   or run in development mode:
   ```shell
   flask run --reload
   ```

