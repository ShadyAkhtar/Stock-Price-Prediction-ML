import csv
import nsepy as ns
from datetime import date

df = ns.get_history(symbol="AUROPHARMA", start = date(2010,1,1), end = date.today())

print(df)
df.to_csv('df.csv',index = True , header = True )   
# f = open('../datasets/data/TATAMOTORS.csv', 'w')

# create the csv writer
# writer = csv.writer(f)

# write a row to the csv file
# writer.writerows(df)

# close the file
# f.close()