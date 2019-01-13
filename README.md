# Antscoper
Antscoper is a tool for viewing the class schedule of every single classroom and lecture hall at UCI.

It can be used to easily find vacant classrooms to use as study rooms or theater rooms.

Please note that rooms are typically closed on weekends and holidays.
On days when rooms are open, they are usually open from 7am to 10pm.
Rooms are sometimes reserved (especially before exams), so be prepared to leave a vacant classroom if asked.

<img src="sample.png">

## Inner Workings
### Map
#### Data
Map data is taken from the same source that [UCI's official Interactive Map](https://map.uci.edu) uses.
I probably should keep a copy for backup, but Antscoper currently calls the CDN for data on every visit.
#### Display
Antscoper displays the map via [Leaflet](https://leafletjs.com/), which the official UCI map also relies on.
To run a local copy of Antscoper, you must also download Leaflet and include in the root directory.
### Schedules
#### Daily Updates
Room schedules are scraped daily from [WebSOC](https://www.reg.uci.edu/perl/WebSoc) every day at 6am.
Every scraping of WebSOC deletes all previously recorded schedules.
Every time the website is opened, Antscoper queries the entire database. It probably shouldn't do this.
#### Database
Antscoper was initialized with all of WebSOC's data, meaning its database includes rooms from 1990 to now.
The website only shows rooms which have had some schedule this year or the past year.
Rooms whose latest activity was two years ago or more are assumed to be presently nonexistent.
