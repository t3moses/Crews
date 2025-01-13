working_directory = "/Users/timmoses/Documents/Tech/Projects/Version_controlled/Assignment/"
event_dates = ["Fri Jun 6","Fri Jun 13","Fri Jun 20","Sat Jun 28","Fri Jul 4","Fri Jul 11","Sat Jul 19","Fri Jul 25","Fri Aug 1","Sat Aug 9","Fri Aug 15","Fri Aug 22","Sat Aug 30","Fri Sep 5","Fri Sep 12","Fri Sep 19","Fri Sep 26"]
boat_header_row = ["key","owner key","display name","email address","mobile","female","min occupancy","max occupancy","assistance"]
sailor_header_row = ["key","display name","partner key","email address","member","skill","experience","request female","whitelist"]
default_boat = { "key" : "", "owner key" : "", "display name" : "", "email address" : "","mobile" : "", "female" : "", "min occupancy" : "1", "max occupancy" : "1", "assistance" : "False" }
default_sailor = { "key" : "", "display name" : "", "partner key" : "", "email address" : "", "member" : "False", "skill" : "0", "experience" : "", "request female" : "N","whitelist" : ""}
rules = ["assist", "whitelist", "skill", "partner", "repeat"]
streak = 1 # Minimum compliant gap between repeats.
