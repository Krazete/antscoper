from chrono import chronolist as CL
import re

def parse_document(document):
    db = {}

    lines = document.split('\n')
    a = b = c = 0
    for line in lines:
        if 'CCode' in line:
            a = line.index('Time')
            b = line.index('Place')
            c = line.index('Max')
            break

    blocks = re.split('\n\n+', document[document.index('###') : document.index('***')])
    for block in blocks:
        if '###' in block or '___' in block:
            continue
        else:
            lines = block.split('\n')
            for line in lines:
                time = line[a : b]
                place = line[b : c]
                if 'Time' in time or 'Place' in place or 'TBA' in time or 'TBA' in place or (time + place).strip() == '':
                    continue
                days, hours = parse_time(time)
                building, room = parse_place(place)
                if building not in db:
                    db.setdefault(building, {})
                if room not in db[building]:
                    db[building].setdefault(room, {'Su': CL(), 'M': CL(), 'Tu': CL(), 'W': CL(), 'Th': CL(), 'F': CL(), 'Sa': CL()})
                for day in days:
                    print(hours)
                    db[building][room][day].add(hours)
    return db

def parse_time(time):
    days = re.findall('(Su|M|Tu|W|Th|F|Sa)', time)
    start, end = re.findall('(\d+):(\d+).', time)
    hours = [int(start[0]) + int(start[1]) / 60, int(end[0]) + (int(end[1]) + 10) / 60]
    if hours[0] > hours[1]:
        hours[1] += 12
    # if hours[0] < 7:
    #     hours[0] += 12
    #     hours[1] += 12
    return [days, hours]

def parse_place(place):
    return place.strip().split(' ')

sample = '''
\t\t\tUC Irvine Office of the Registrar
\t\t      Schedule of Classes    Sunday, May 8, 2016

Search Criteria:
    Course Code Range: 1000-1999
    Exclude cancelled courses


Spring Quarter, 2016      Currently in week 7.


   #########################################################################
   ###                                                                   ###
   ###                 Claire Trevor School of the Arts                  ###
   ###                                                                   ###
   #########################################################################

       _________________________________________________________________

                                     Art
       _________________________________________________________________

Art      1C        ART IN CONTEXT
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01020 LEC A   4   JACKSON, J.C.      TuTh  5:00- 6:20p HG 1800  131 130 532      OPEN   
                      PASTOR, J.                                                            

Art      9C        THEMATIC INVESTIGTN
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01030 LEC A   4   LEWIS, J.          TuTh  3:30- 4:50p HIB 100  347 109 290      OPEN   

Art      11A       HISTORY CONTEMP ART
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01032 LEC A   4   ANASTAS, R.        MW    1:00- 3:20p ART 160   40  37 58  A    OPEN   
                      MCNEELY, A.                                                           
    01033 DIS A   0   ANASTAS, R.        F    11:00-11:50  ART 160   20  19 22  A    OPEN   
                      MCNEELY, A.                                                           
    01034 DIS B   0   ANASTAS, R.        F    12:00-12:50p ART 160   20  18 22  A    OPEN   
                      MCNEELY, A.                                                           

Art      12B       STEAM TO STEAMPUNK
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01035 LEC A   4   PENNY, S.          TuTh  1:00- 2:50p WSH 180   75  72 178      OPEN   
    01036 LEC B   4   PENNY, S.          TuTh  1:00- 2:50p WSH 180   75  73 100      OPEN   

Art      20A       BASIC DRAWING I
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01038 STU A   4   TSUI, C.           TuTh  9:30-11:50  ART 260   20  19 172      OPEN   

Art      30A       BASIC PAINTING I
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01040 STU A   4   AISPURO, E.        MW    9:30-11:50  ART 265   20  19 125      OPEN   

Art      40        BASIC SCULPTURE
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01050 STU A   4   SELVIK, R.         TuTh  9:30-11:50  SCS 170   15  14 70  C&B  OPEN   

Art      65A       FDNS MEDIA DESIGN
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01065 LEC A   4   MURNANE, M.        MW    9:30-11:50  CAC 3006  12  12 37  C    FULL   
    01066 LEC B   4   MURNANE, M.        MW    9:30-11:50  CAC 3006  12  12 29  C    FULL   

Art      65B       FDNS INTERNET ART
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01067 LEC A   4   JACKSON, J.B.      MW    9:30-11:50  CAC G021  10   9 22  C    OPEN   
    01068 LEC B   4   JACKSON, J.B.      MW    9:30-11:50  CAC G021  10   5 12  C&B  OPEN   

Art      71A       INTRO TO PHOTO I
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01070 STU A   4   ROBERTS, W.        TuTh  9:30-11:50  ART 166   16  16 97  C    FULL   
    01072 STU B   4   SHEYBANI ZAVEH, M. MW    9:30-11:50  ART 166   15  14 50  C    OPEN   

Art      71B       INTRO TO PHOTO II
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01074 STU A   4   GOWANS, J.         MW    1:00- 3:20p ART 166   15   9 17  C&A  OPEN   
                                         MW    1:00- 3:20p CAC 3006                         
    01080 STU B   4   ROBERTS, W.        TuTh  1:00- 3:20p ART 166   15  18 30  B&C  FULL   
                                         TuTh  1:00- 3:20p CAC G021                         

Art      81A       DIGIFILM PROD I
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01084 STU A   4   RUANO, A.          MW    1:00- 3:20p ACT 1221  15  14 49  B&C  OPEN   
                                         MW    1:00- 3:20p ACT 1240                         
                                         MW    1:00- 3:20p CAC G021                         
    01085 STU B   4   RUANO, A.          MW    1:00- 3:20p ACT 1221   5   5 19  C    FULL   
                                         MW    1:00- 3:20p ACT 1240                         
                                         MW    1:00- 3:20p CAC G021                         

Art      81B       DIGIFILM PROD II
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01086 LEC A   4   JACKSON, J.B.      F    10:00- 3:50p ACT 1240  15  17 27  C&B  FULL   
                                         F    10:00- 3:50p ACT 1221                         
    01087 LEC B   4   JACKSON, J.B.      F    10:00- 3:50p ACT 1240   6   4 8   C&A  OPEN   
                                         F    10:00- 3:50p ACT 1221                         

Art      91        BASIC PERFORM ART
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01092 STU A   4   OLIVER, D.         TuTh  1:00- 3:20p ART 165   12  10 23       OPEN   

Art      100       COLOR THEORY
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01200 STU A   4   LONNER, M.         TuTh  1:00- 3:20p ART 260   20  31 51  A&B  FULL   

Art      100       MATERIAL FUNDAMENTA
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01201 STU B   4   SOTO-DIAZ, M.      MW    1:00- 3:20p ART 260   15  12 27  A    OPEN   

Art      108       DIGIFILM PROJECT I
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01210 STU A   4   JENKINS JR., U.    TuTh  3:30- 5:50p ACT 1221  15  10 12  B&C  OPEN   
                                         TuTh  3:30- 5:50p ART 160                          
                                         TuTh  3:30- 5:50p ACT 1240                         
    01211 STU B   4   JENKINS JR., U.    TuTh  3:30- 5:50p ACT 1221   5   0 0   C&A  OPEN   
                                         TuTh  3:30- 5:50p ART 160                          
                                         TuTh  3:30- 5:50p ACT 1240                         

Art      119       ISS CONTEMP PAINTNG
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01216 SEM A   4   MAJOLI, M.         Th    3:30- 5:50p ART 165   18  12 21  A    OPEN   

Art      121B      AFRO-FUTURISM II
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01228 LEC A   4   JENKINS JR., U.    TuTh  1:00- 3:20p ART 160   18   7 13  A    OPEN   

Art      125       ISSUES IN PHOTOGRPY
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01230 SEM A   4   ROBERTS, W.        W     3:30- 5:50p ACT 3214  15  16 30  A&B  FULL   

Art      128       ISSUES NEW GENRES
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01272 SEM A   4   OLIVER, D.         TuTh  9:30-11:50  ART 160   20  16 30  A    OPEN   

Art      141       DIGIFILM ADV PROJ I
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01273 STU A   4   YONEMOTO, B.       MW    3:30- 5:50p ACT 1221  15  10 15  B&C  OPEN   
                                         MW    3:30- 5:50p ART 160                          
                                         MW    3:30- 5:50p ACT 1240                         
    01274 STU B   4   YONEMOTO, B.       MW    3:30- 5:50p ACT 1221   5   0 0   C&A  OPEN   
                                         MW    3:30- 5:50p ART 160                          
                                         MW    3:30- 5:50p ACT 1240                         

Art      150       ADVANCED PAINTING
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01300 STU A   4   APPEL, K.          MW    3:30- 5:50p ART 265   20  18 29  B&C  OPEN   

Art      150C      ADVANCED DRAWING
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01302 STU A   4   LONNER, M.         TuTh  3:30- 5:50p ART 260   20  21 36  A&B  FULL   

Art      152C      THE PUBLIC IMAGE
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01350 STU A   4   SHAFER, J.         F    10:00- 2:50p ART 166   15  11 16  A&C  OPEN   

Art      154       ADV PERFORMANCE ART
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01360 STU A   4   OLIVER, D.         TuTh  1:00- 3:20p ART 165   13  12 14  A    OPEN   

Art      190B      SR PROJECTS: PHOTO
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01364 STU A   4   COOLIDGE, M.       MW    3:30- 5:50p ART 166   15   7 12  B&C  OPEN   

Art      197       INTERNSHIP
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01552 STU A   1-4 JACKSON, J.B.      *TBA*             *TBA*      5   1 2   B&D  OPEN   
    01553 STU B   1-4 STAFF              *TBA*             *TBA*      5   0 0   B&D  OPEN   
    01554 STU C   1-4 STAFF              *TBA*             *TBA*      5   0 0   B&D  OPEN   
    01555 STU D   1-4 STAFF              *TBA*             *TBA*      5   0 0   B&D  OPEN   
    01556 STU E   1-4 STAFF              *TBA*             *TBA*      5   0 0   B&D  OPEN   
    01557 STU F   1-4 STAFF              *TBA*             *TBA*      5   0 0   B&D  OPEN   
    01558 STU G   1-4 STAFF              *TBA*             *TBA*      5   0 0   B&D  OPEN   
    01559 STU H   1-4 STAFF              *TBA*             *TBA*      5   0 0   B&D  OPEN   
    01560 STU I   1-4 STAFF              *TBA*             *TBA*      5   0 0   B&D  OPEN   
    01561 STU J   1-4 STAFF              *TBA*             *TBA*      5   0 0   B&D  OPEN   

Art      198       HONORS EXHIBITION
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01562 STU A   4   MARTINEZ, D.       Tu    3:30- 5:50p ACT 3214   6   7 7   B&D  FULL   

Art      199       INDEPENDENT STUDY
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01563 STU A   1-4 ANASTAS, R.        *TBA*             *TBA*      5   1 1   B&L  OPEN   
    01564 STU B   1-4 APPEL, K.          *TBA*             *TBA*      5   5 4   B&L  FULL   
    01565 STU C   1-4 CARSON, J.         *TBA*             *TBA*      5   0 0   B&L  OPEN   
    01566 STU D   1-4 COOLIDGE, M.       *TBA*             *TBA*      5   0 0   B&L  OPEN   
    01567 STU E   1-4 JACKSON, J.B.      *TBA*             *TBA*      5   2 2   B&L  OPEN   
    01568 STU F   1-4 JACKSON, J.C.      *TBA*             *TBA*      5   1 1   B&L  OPEN   
    01569 STU G   1-4 JENKINS JR., U.    *TBA*             *TBA*      5   0 0   B&L  OPEN   
    01570 STU H   1-4 LAFARGE, A.        *TBA*             *TBA*     15   0 0   B&L  OPEN   
    01571 STU I   1-4 LEUNG, S.          *TBA*             *TBA*      5   5 4   B&L  FULL   
    01572 STU J   1-4 LEWIS, J.          *TBA*             *TBA*      5   1 0   B&L  OPEN   
    01573 STU K   1-4 LONNER, M.         *TBA*             *TBA*     10   1 1   B&L  OPEN   
    01574 STU L   1-4 MAJOLI, M.         *TBA*             *TBA*      5   1 1   B&L  OPEN   
    01575 STU M   1-4 MARTINEZ, D.       *TBA*             *TBA*      5   2 2   B&L  OPEN   
    01576 STU N   1-4 STAFF              *TBA*             *TBA*      5   0 0   B&L  OPEN   
    01577 STU O   1-4 MYERS, G.          *TBA*             *TBA*      5   0 0   B&L  OPEN   
    01578 STU P   1-4 OLIVER, D.         *TBA*             *TBA*      5   0 0   B&L  OPEN   
    01579 STU Q   1-4 PASTOR, J.         *TBA*             *TBA*      5   1 2   B&L  OPEN   
    01580 STU R   1-4 PENNY, S.          *TBA*             *TBA*      5   3 4   B&L  OPEN   
    01581 STU S   1-4 PERTA, L.          *TBA*             *TBA*      5   0 0   B&L  OPEN   
    01582 STU T   1-4 ROBERTS, W.        *TBA*             *TBA*      5   1 2   B&L  OPEN   
    01583 STU U   1-4 SAMARAS, C.        *TBA*             *TBA*      5   0 0   B&L  OPEN   
    01584 STU V   1-4 TREND, D.          *TBA*             *TBA*      5   0 0   B&L  OPEN   
    01585 STU W   1-4 YONEMOTO, B.       *TBA*             *TBA*      5   0 0   B&L  OPEN   
    01586 STU X   1-4 PASTOR, J.         *TBA*             *TBA*     40  12 11  C    OPEN   
    01587 STU Y   1-4 COOLIDGE, M.       *TBA*             *TBA*     40   0 0   C    OPEN   
    01588 STU Z   1-4 SAMARAS, C.        *TBA*             *TBA*     40   0 0   C    OPEN   

Art      220       CONTEMP ART SEMINAR
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01630 SEM A   4   PERTA, L.          W     6:30- 8:50p ART 160   40  18 23  K    OPEN   

Art      230       GRADUATE CRITIQUE
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01635 SEM A   4   MARTINEZ, D.       Tu    6:30- 8:50p ART 165    9   8 14  K    OPEN   

Art      240       INTERDISC PROJECTS
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01649 TUT A   4   LONNER, M.         F     3:30- 5:50p ACT 3214   8   6 6   K&B  OPEN   
    01650 TUT B   4   APPEL, K.          F     1:00- 3:20p ACT 3214   9   9 10  B&K  FULL   
    01651 TUT C   4   PASTOR, J.         F     9:30-11:50  ACT 3214   8   8 8   B&K  FULL   

Art      251       DIRECTED STUDY
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01665 SEM A   4   JACKSON, J.C.      F     6:30- 8:50p ART 160   10   9 13  B&K  OPEN   
    01667 SEM B   4   MAJOLI, M.         Th    6:30- 8:50p ART 160   11  10 10  K    OPEN   

Art      261       THESIS WRITING SEM
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01668 SEM A   4   PERTA, L.          M     6:30- 8:50p ACT 3214  10   9 10  K    OPEN   

Art      262       THESIS INDEP STUDY
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01675 TUT A   1-4 ANASTAS, R.        *TBA*             *TBA*     10   2 2   B&K  OPEN   
    01676 TUT A   1-4 APPEL, K.          *TBA*             *TBA*     10   6 6   B&K  OPEN   
    01677 TUT B   1-4 CARSON, J.         *TBA*             *TBA*     10   3 3   B&K  OPEN   
    01678 TUT C   1-4 COOLIDGE, M.       *TBA*             *TBA*     10   2 2   B&K  OPEN   
    01679 TUT D   1-4 JACKSON, J.B.      *TBA*             *TBA*     10   0 0   B&K  OPEN   
    01680 TUT E   1-4 JACKSON, J.C.      *TBA*             *TBA*     10   0 0   B&K  OPEN   
    01681 TUT F   1-4 JENKINS JR., U.    *TBA*             *TBA*     10   0 0   B&K  OPEN   
    01682 TUT G   1-4 LAFARGE, A.        *TBA*             *TBA*     10   0 0   B&K  OPEN   
    01683 TUT H   1-4 LEUNG, S.          *TBA*             *TBA*     10   5 5   B&K  OPEN   
    01684 TUT I   1-4 STAFF              *TBA*             *TBA*     10   0 0   B&K  OPEN   
    01685 TUT J   1-4 LONNER, M.         *TBA*             *TBA*     10   0 0   B&K  OPEN   
    01686 TUT K   1-4 MAJOLI, M.         *TBA*             *TBA*     10   6 6   B&K  OPEN   
    01687 TUT L   1-4 MARTINEZ, D.       *TBA*             *TBA*     10   4 4   B&K  OPEN   
    01688 TUT M   1-4 STAFF              *TBA*             *TBA*     10   0 0   B&K  OPEN   
    01689 TUT N   1-4 MYERS, G.          *TBA*             *TBA*     10   0 0   B&K  OPEN   
    01690 TUT O   1-4 STAFF              *TBA*             *TBA*     10   0 0   B&K  OPEN   
    01691 TUT P   1-4 OLIVER, D.         *TBA*             *TBA*     10   0 0   B&K  OPEN   
    01692 TUT Q   1-4 PASTOR, J.         *TBA*             *TBA*     10   5 5   B&K  OPEN   
    01693 TUT R   1-4 PENNY, S.          *TBA*             *TBA*     10   0 0   B&K  OPEN   
    01694 TUT S   1-4 PERTA, L.          *TBA*             *TBA*     10   4 4   B&K  OPEN   
    01695 TUT T   1-4 ROBERTS, W.        *TBA*             *TBA*     10   0 0   B&K  OPEN   
    01696 TUT U   1-4 SAMARAS, C.        *TBA*             *TBA*     10   0 0   B&K  OPEN   
    01697 TUT V   1-4 STAFF              *TBA*             *TBA*     10   0 0   B&K  OPEN   
    01698 TUT W   1-4 TREND, D.          *TBA*             *TBA*     10   0 0   B&K  OPEN   
    01699 TUT X   1-4 YONEMOTO, B.       *TBA*             *TBA*     10   1 1   B&K  OPEN   
    01700 TUT Y   1-4 STAFF              *TBA*             *TBA*     10   0 0   B&K  OPEN   
    01701 TUT Z   1-4 STAFF              *TBA*             *TBA*     10   0 0   B&K  OPEN   

Art      399       UNIVERSITY TEACHING
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01750 TUT A   4   APPEL, K.          *TBA*             *TBA*      0   0 0   S&K  FULL   
    01751 TUT B   4   CARSON, J.         *TBA*             *TBA*      0   0 0   S&K  FULL   
    01752 TUT C   4   COOLIDGE, M.       *TBA*             *TBA*      2   2 2   S&K  FULL   
    01753 TUT D   4   JACKSON, J.B.      *TBA*             *TBA*      0   0 1   K&S  FULL   
    01754 TUT E   4   JACKSON, J.C.      *TBA*             *TBA*      1   1 1   S&K  FULL   
    01755 TUT F   4   JENKINS JR., U.    *TBA*             *TBA*      0   0 0   S&K  FULL   
    01756 TUT G   4   LAFARGE, A.        *TBA*             *TBA*      0   0 0   K&S  FULL   
    01757 TUT H   4   LEUNG, S.          *TBA*             *TBA*      0   0 0   K&S  FULL   
    01758 TUT I   4   STAFF              *TBA*             *TBA*      0   0 0   K&S  FULL   
    01759 TUT J   4   LONNER, M.         *TBA*             *TBA*      1   0 0   K&S  OPEN   
    01760 TUT K   4   MAJOLI, M.         *TBA*             *TBA*      1   1 1   K&S  FULL   
    01761 TUT L   4   MARTINEZ, D.       *TBA*             *TBA*      0   0 0   K&S  FULL   
    01762 TUT M   4   STAFF              *TBA*             *TBA*      0   0 0   K&S  FULL   
    01763 TUT N   4   MYERS, G.          *TBA*             *TBA*      0   0 0   K&S  FULL   
    01764 TUT O   4   STAFF              *TBA*             *TBA*      0   0 0   K&S  FULL   
    01765 TUT P   4   OLIVER, D.         *TBA*             *TBA*      0   0 0   K&S  FULL   
    01766 TUT Q   4   PASTOR, J.         *TBA*             *TBA*      1   0 0   K&S  OPEN   
    01767 TUT R   4   PENNY, S.          *TBA*             *TBA*      0   0 0   K&S  FULL   
    01768 TUT S   4   PERTA, L.          *TBA*             *TBA*      0   0 0   K&S  FULL   
    01769 TUT T   4   ROBERTS, W.        *TBA*             *TBA*      0   0 0   K&S  FULL   
    01770 TUT U   4   SAMARAS, C.        *TBA*             *TBA*      0   0 0   K&S  FULL   
    01771 TUT V   4   STAFF              *TBA*             *TBA*      0   0 0   K&S  FULL   
    01772 TUT W   4   TREND, D.          *TBA*             *TBA*      0   0 0   K&S  FULL   
    01773 TUT X   4   YONEMOTO, B.       *TBA*             *TBA*      1   0 0   K&S  OPEN   
    01774 TUT Y   4   STAFF              *TBA*             *TBA*      0   0 0   K&S  FULL   
    01775 TUT Z   4   STAFF              *TBA*             *TBA*      0   0 0   K&S  FULL   

       _________________________________________________________________

                                    Arts
       _________________________________________________________________

Arts     75        DIG ARTS EXHIBITION
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01830 LEC A   4   FAMILIAN, D.       MW    5:00- 7:20p ART 165   15   8 37  B    OPEN   

Arts     199       INDEPENDENT STUDY
    CCode Typ Sec Unt Instructor         Time              Place    Max Enr Req Rstr Status 
    01840 SEM A   1-4 LYNCH, M.          *TBA*             *TBA*     20   0 1        OPEN   


*** Total Classes Displayed: 138
    Course "New-Only Reservations" (NOR) for new students have been turned off for this term.
    Course "Waitlists" have been turned off for this term.
    The column headings above are defined at:
\t    https://www.reg.uci.edu/help/WebSoc-Columns.shtml
    Course textbooks link:
\t    http://book.uci.edu/
    Building Abbreviations:
\t    http://www.reg.uci.edu/uci/rooms
    Campus map:
\t    http://www.uci.edu/campusmap

Restriction Codes from the \'Rst\' column above:
    A: Prerequisite required
    B: Authorization required
    C: Fee required
    D: Pass/not pass option only
    K: Graduate only
    L: Major only
    S: Satisfactory/unsatisfactory only
'''

if __name__ == '__main__':
    qp = parse_document(sample)
    print(qp)
