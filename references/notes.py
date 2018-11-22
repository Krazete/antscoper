'''
+-------------------------------------+
|                IDEAS                |
+-------------------------------------+
| General Classroom Information       |
|   Include a disclaimer for warning  |
|   about official bookings and the   |
|   general closing time for classes. |
| WebSOC Viewer                       |
|   Search through WebSOC without     |
|   having to reload for each search  |
|   query.                            |
| WebSOC Class Compiler               |
|   From a chosen combination of      |
|   classes all possible schedules    |
|   are generated. Incompatible       |
|   combinations can also be          |
|   instantly revealed.               |
| Classroom Availability Checker      |
|   Display the times when a class is |
|   held for a chosen classroom.      |
+-------------------------------------+
janitors come invariably between 8:00 and 11:00
doors lock at 9:20?
some systems shut down at 11:50???
some systems restart at 1:00
painter/maintenance at 2:45?
doors unlock at 7

TODO:
    fix Schedule queries
        request by building?
        request by proximity?
        request by day?
    fix gui
        stop going by 30-minute blocks
        add some search feature
        allow building to be clicked
        etc
        
// optimize database requests (for quota limit)
// change last_active to active_quarters
// only request last four quarters from database
// keep copy of mapbox data
// only request rooms database with building abbreviations found in mapbox data

'''
