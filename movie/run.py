import threading
import subprocess
import datetime
import os
import time


def run(movie_type, page):
    today = datetime.date.today()
    log_path = os.getcwd() + '/' + str(today) + '/log/'
    data_path = os.getcwd() + '/' + str(today) + '/data/'
    log_folder = os.path.exists(log_path)
    data_folder = os.path.exists(log_path)
    print(log_path)
    if not log_folder:
        os.makedirs(log_path)
    else:
        pass
    if not data_folder:
        os.makedirs(data_path)
    else:
        pass

    output_file = open(log_path + '/movie_page_' + str(page) + '.log', 'w')
    command = 'scrapy crawl movie_spider -o ' + data_path + '/' + str(movie_type) + 'movie_page_' + str(page) + '.json -a movie_type=' + str(movie_type) + ' -a page=' + str(page)
    try:
        subprocess.run(command, shell=True, stdout=output_file, check=True)
    except subprocess.CalledProcessError as e:
        print('ERROR:' + e.stderr)

# 影片类型对照
# 电影：
# 5-动作片
# 6-喜剧片
# 7-爱情片
# 8-科幻片
# 9-恐怖片
# 10-剧情片
# 11-战争片
#
# 电视剧：
# 12-国产剧
# 13-台湾剧
# 14-韩国剧
# 15-欧美剧
# 16-香港剧
# 17-泰国剧
# 18-日本剧
# 19-福利


MOVIE_TYPE = 7      # 影片类型
START = 1           # 起始页
END = 4             # 结束页/10
LIMIT = 10          # 单次爬取页数
for i in range(START, END):
    # 单次爬取10页，每个线程爬取1页
    PAGE = i * LIMIT + 1
    for j in range(0, 10):
        t = threading.Thread(target=run, args=(MOVIE_TYPE, PAGE,))
        t.start()
        PAGE += 1
        time.sleep(2)
    time.sleep(1200)
