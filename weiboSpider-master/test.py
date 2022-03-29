from datetime import date, datetime, timedelta
import os
file_dir = 'D:\data\spider\weibo'
print(file_dir)
if not os.path.isdir(file_dir):
    os.makedirs(file_dir)