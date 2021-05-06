from csv import reader
hourefile = open("bnb1h.csv")
minutefile = open("bnb1m.csv")
houreader = reader(hourefile , delimiter = ',')
minutereader = reader(minutefile , delimiter = ',')

unix_start = 1599858000000 
unix_time = unix_start
hours = 5607
next(minutereader) # skip first row 
next(houreader)  # skip first row
failcnt = 0 
for hour in range(hours):
    h = next(houreader)
    if unix_time != int(h[0]):
        failcnt += 1 
        print(h[0] , '---', unix_time)
        unix_time = int(h[0])
    # for i in range(60):
    #     hh=next(minutereader)
    #     if int(hh[0]) != (unix_time):
    #         print(hh[0] , '---' ,  unix_time )
    #         exit(0)
    unix_time += 3600000    
    # break
    # print(h[0])
    
    # for i in range(60):
    #     unix_time += 60000 * i
    #     next(houreader)
    


