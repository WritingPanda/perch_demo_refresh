# Demo Refresh

The way this works is to close all alerts within an organization's queue. The purpose is for refreshing the demo environment for company purposes. 

The first thing you will need to do is create a virtual environment for Python 3 and install all packages:

    pip install -r requirements.txt

Next, you will need to create a `.env` file with the following information:

    USER=STR
    PASSWORD=STR
    API_KEY=STR
    URL=STR
    TEAM_ID=INT

    QA_USER=STR
    QA_PASSWORD=STR
    QA_API_KEY=STR
    QA_URL=STR
    QA_TEAM_ID=INT

I am using `python-dotenv` to load the environment files without editing my virtual environment. 

The script accepts one argument to determine if we will be using the production environment or the QA environment:

    <!-- Production -->
    python main.py prod

    <!-- QA -->
    python main.py test

TODO: Write tests
