# Data PackRat

This project is to be able to download things locally durning non-internet usage times. It is starting with videos that can be downloaded with `youtube-dl`, but can later be expanded to other things.

## Initial Goal

The initial goal is to be able to download youtube videos at night while I am asleep, and then I can watch them with plex later. That way during the day while working I am not sucking up bandwidth that I can use for work. It is a way to maximize bandwidth usage.

## Setup/Run

Download and run the project.

### Setup Website

```
git clone https://github.com/buddylindsey/data-packrat.git ~/Programming/data-packrat
cd data-packrat/datapackrat
python3 -m venv ~/.virtualenvs/data-packrat
source ~/.virtualenvs/data-packrat/bin/activate
```

Set custom settings at bottom of `datapackrat/settings.py`

```
./manage.py createsuperuser
# follow the prompts
./manage.py runserver
```

Visit http://localhost:8000/admin to login and start adding videos to download.

### Setup Downloader

Setup crontab

```bash
crontab -e
```

Add the following.

```
5 0 * * * cd ~/Programming/data-packrat/datapackrat && ~/.virtualenvs/data-packrat/bin/python manage.py pulldata
```

It might be better to create a script that calls those commands.
