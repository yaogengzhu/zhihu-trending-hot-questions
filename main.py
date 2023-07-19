import requests
from datetime import datetime
import json

class GetHot():
    def __init__(self, url):
        self.url = url
        self.list = []

    def format_list(self, origin):
        newList = map(lambda x:{"title": x['target']['title'], "excerpt": x['target']['excerpt'], "url": f"https://zhihu.com/questions/{x['target']['id']}"}, origin)
        return list(newList)

    def getList(self):
        response = requests.get(self.url)
        self.list = json.loads(response.text)['data']
        return self.format_list(self.list)
    
    def read_old_list(self, datetime_str):
        try:
            with open(datetime_str, 'r') as f:
                oldList = json.load(f)
                if len(oldList) != 0:
                    return oldList
                return []
        except FileNotFoundError:
            return []
    
    def write_list(self):
        datetime_str = f"./data/{datetime.now().strftime('%Y-%m-%d')}.json";
        newlist = self.getList()
        oldList = self.read_old_list(datetime_str)
        # 写数据之前判断这个数据是否存在
        mergeList = []
        if len(oldList) == 0:
             with open(datetime_str, "w") as f:
                json.dump(newlist, f, ensure_ascii=False, indent=4)
                print(f"写入文件成功，文件名为{datetime_str}")
        else:
            for item in oldList:
                if item['title'] not in newlist:
                    mergeList.append(item)
            with open(datetime_str, "w") as f:
                json.dump(mergeList, f, ensure_ascii=False, indent=4)
            print(f"写入文件成功，文件名为{datetime_str}")

if __name__ == "__main__":
    url = 'https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=100'
    get = GetHot(url)
    get.write_list()
