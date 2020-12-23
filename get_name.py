import requests

headers = {}
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"

url = "https://wiki.52poke.com/zh-hans/%E5%AE%9D%E5%8F%AF%E6%A2%A6%E5%88%97%E8%A1%A8%EF%BC%88%E6%8C%89%E5%85%A8%E5%9B%BD%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%EF%BC%89/%E7%AE%80%E5%8D%95%E7%89%88"

r = requests.get(url, headers=headers)
r.encoding = 'utf-8'
data = r.text
fw = open("1.csv", "w", encoding='utf-8')
for i in range(1, 899):
    number = '#' + "%03d" % i
    t = data.find(number)
    start = data.find("title=\"", t)
    end = data.find("\"", start+7)
    name = data[start + 7:end]
    fw.write(name+"\n")
    print(name)

fw.close()
