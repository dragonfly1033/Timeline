curShowName = ''
DAYS = ['Unknown'] + [i for i in range(1,32)]
MONTHS = ['Unknown','January', 'February', 'March', 'April', 'May', 'June',
 'July', 'August', 'September', 'October', 'November', 'December']
YEARS = [i for i in range(1, 2021)]
SIDE = True

def printall():
    print(timelineData)
    print(curShowName)
    print(days)
    print(months)
    #print(years)
    print(side)