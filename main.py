import os
import requests
from datetime import datetime
import json


class GetHot():
    def __init__(self, url):
        self.url = url
        self.list = []

    def format_list(self, origin):
        newList = map(lambda x:{"title": x['target']['title'], "excerpt": x['target']['excerpt'], "url": f"https://www.zhihu.com/question/{x['target']['id']}"}, origin)
        return list(newList)

    def getList(self):
        response = requests.get(self.url)
        self.list = json.loads(response.text)['data']
        return self.format_list(self.list)
    
    def read_old_list(self, datetime_str):
        try:
            with open(datetime_str, 'r') as f:
                oldList = json.load(f)
                return oldList
        except FileNotFoundError:
            with open(datetime_str, "w") as f:
                return []
    
    def write_list(self):
        if not os.path.exists('./data'):
            os.makedirs('./data')
        dir_path = os.path.dirname(os.path.realpath(__file__)) + '/data'
        datetime_str = f"{dir_path}/{datetime.now().strftime('%Y-%m-%d')}.json";
        current_list = self.getList()
        oldList = self.read_old_list(datetime_str)
        # 写数据之前判断这个数据是否存在
        mergeList = []
        
        if len(oldList) == 0:
             with open(datetime_str, "w") as f:
                json.dump(current_list, f, ensure_ascii=False, indent=4)
                print(f"写入文件成功，文件名为{datetime_str}")
        else:
            mergeList = oldList + current_list
            # 去掉重复的数据
            result = [dict(t) for t in {tuple(d.items()) for d in mergeList}]
            with open(datetime_str, "w") as f:
                json.dump(result, f, ensure_ascii=False, indent=4)
                self.create_readme(result)
                print(f"写入文件成功，文件名为{datetime_str}")
    
    def create_readme(self, newList):
        message = f"""# zhihu-trending-hot-questions
知乎热门话题，记录从 2023-7-19
日开始的知乎热门话题。每小时抓取一次数据，按天[归档](./data)。\n{self.create_readme_list(newList)}\n### License
[zhihu-trending-hot-questions](https://github.com/yaogengzhu/zhihu-trending-hot-questions)
的源码使用 MIT License 发布。具体内容请查看 [LICENSE](./LICENSE) 文件。
"""
        with open("./README.md", "w") as f:
            f.write(message)
    
    def create_readme_list(self, newList):
        question_list = "\n".join(f"1. [{x['title']}]({x['url']})" for x in newList)
        return f"<!-- BEGIN -->\n<!-- 最后更新时间 {datetime.now()} -->\n{question_list}\n<!-- END -->"


if __name__ == "__main__":
    url = 'https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=100'
    get = GetHot(url)
    get.write_list()
