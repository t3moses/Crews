event_dates = ["Fri Jun 6","Fri Jun 13","Fri Jun 20","Sat Jun 28","Fri Jul 4","Fri Jul 11","Sat Jul 19","Fri Jul 25","Fri Aug 1","Sat Aug 9","Fri Aug 15","Fri Aug 22","Sat Aug 30","Fri Sep 5","Fri Sep 12","Fri Sep 19","Fri Sep 26"]
boat_header_row = ["key","owner key","display name","email address","mobile","female","min occupancy","max occupancy","assistance"]
sailor_header_row = ["key","display name","partner key","email address","member","skill","experience","request female","whitelist"]
default_boat = { "key" : "", "owner key" : "", "display name" : "", "email address" : "","mobile" : "", "female" : "", "min occupancy" : "1", "max occupancy" : "1", "assistance" : "False" }
default_sailor = { "key" : "", "display name" : "", "partner key" : "", "email address" : "", "member" : "False", "skill" : "0", "experience" : "", "request female" : "N","whitelist" : ""}
inner_epochs = 5 # Gradient descent iterations to find 'local' minimum.
outer_epochs =5 # Iterations to find 'global' minimum.
loss_threshold = 4
whitelist_weight = 10
partner_weight = 8
assist_weight = 8
skill_weight = 5
repeat_weight = 6
repeat_exponent = -1.7 # Must be <= 0. Significance of repeats according to how recently they occurred. 0 makes all repeats equally significant.
