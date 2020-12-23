import requests

headers = {}
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"

fr = open("name.csv", "r", encoding='utf-8')
fw = open("test.txt", "w", encoding='utf-8')
for line in fr:
    url = "http://wiki.52poke.com/index.php?title=" + \
        line.strip("\n") + "&action=edit"
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    fw.write(r.text)
    break

fw.close()
