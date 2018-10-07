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
'''

import SimpleHTTPServer
import json


class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.getheader('content-length'))
        body = self.rfile.read(content_length)
        try:
            result = json.loads(body, encoding='utf-8')
            # process result as a normal python dictionary
            ...
            self.wfile.write('Request has been processed.')
        except Exception as exc:
            self.wfile.write('Request has failed to process. Error: %s', exc.message)
