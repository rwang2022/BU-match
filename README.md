# BU-match

## About
```
Select up to 5 students/alumni that you like.
If they select you too, you'll both be notified via B-mail after some time.
Until there is a match, you'll see a "no match found" message.
```
Interested? Visit \<Deployed Website\>

## Collaborators:

Name | Role
---- | -----
Ryan Wang | Frontend + Backend 
Erika Nelson | UI + CSS + Art

## For Developers: Getting Started
Be sure to have python3 and pip3 installed. 

1. Clone this repository.
```
$ git clone git@github.com:rwang2022/BU-match.git
$ cd BU-match
```

2. Create a new virtual environment.
```
$ python3 -m venv env
```
3. Activate virtual environment. 
```
# ======= Windows: activate env ========= #
$ .\env\Scripts\activate
# ======= Mac: activate env ============= #
$ source env/bin/activate
```

3. Install project dependencies.
```
(env) $ pip3 install -r requirements.txt
```

4. Run the app.
```
(env) $ python app.py
```

5. Deactivate when you're done
```
(env) $ deactivate
```

## NOTE TO SELF
```
When deploying, you must have action="/dev/sending_code" (in general, not specifically for sending_code)
The dev/ is crucial because dev is the name of the stage and is part of the URL
```
You'll be able to access the web app at http://127.0.0.1/5000/

