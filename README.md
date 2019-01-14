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
Antscoper calls the CDN for data on every visit.
If it fails to load, Antscoper uses `geo_backup.json` instead.
#### Display
Antscoper displays the map via [Leaflet](https://leafletjs.com/), which the official UCI map also relies on.
To run a local copy of Antscoper, you must also download Leaflet and include it in the root directory.
### Schedules
#### Daily Updates
Room schedules are scraped daily from [WebSOC](https://www.reg.uci.edu/perl/WebSoc) every day at 6am.
Every scraping of WebSOC deletes all previously recorded schedules.
#### Database
Antscoper was initialized with all of WebSOC's data, meaning its database includes rooms from 1990 to now.
The website only shows rooms which have had some schedule in this year or the past year.
Rooms whose latest activity was two years ago or more are assumed to be presently nonexistent.
The entire database can be accessed from `data.json`, though this is avoided due to quota limits.
If the database ever fails to load, Antscoper uses `database_backup.json` instead.
#### Legend
The legend displays schedules from the database.
Due to quota limits, the legend will not activate until a query is entered in the search box.
Clicking a map popup also automatically enters a query and thus activates the legend.
An active legend will show schedule information for the relevant building on the selected day.

A query must consist of a building's abbreviated name.
The full building name will likely not bring up any results.
All results are stored until the page is closed.
