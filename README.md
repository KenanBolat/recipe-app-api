# recipe-app-api
## Notes 
    - APIVIEW: 
       - focused around HTTP methods 
       - Class methods for HTTP methods:
        - GET, POST, PUT, PATCH, DELETE 
       - Provide flexibility over URLS and logic 
       - Useful for non CRUD APIs: 
       - Avoid for simple Create, Read, Update, Delete APIs 
       - Bespoke logic (eg: auth, jobs, external apis)

     - ViewSet:
       - focused around actions:
       - retrieve, list, update, partial update, destroy
       - Map to Django models  
       - Use Routers to generate URLs 
       - Great for CRUD operations on models

