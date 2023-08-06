from html.parser import HTMLParser
import os

class MyHTMLParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super(MyHTMLParser, self).__init__(*args, **kwargs)
        self.lines = []

    def handle_data(self, data):
        data = ' '.join(data.split())
        if len(data)>0:
            self.lines.append(data)


def extract(lines, key, N):
    for k, line in enumerate(lines):
        if key in line:
            return "|".join(" ".join(lines[k:k+1+N]).split(","))

def main():
    parser = MyHTMLParser()
    os.system("curl 10.13.13.2:8080 > /tmp/.spark-master")
    data = "".join(open("/tmp/.spark-master", "r").readlines()).replace("\n", "").replace("\t", " ")
    parser.feed(data)

    print(extract(parser.lines, "URL", N=1))
    print(extract(parser.lines, "Alive Workers:", N=1))
    print(extract(parser.lines, "Cores in use:", N=1))
    print(extract(parser.lines, "Memory in use:", N=1))
    print(extract(parser.lines, "Applications:", N=5))
    print(extract(parser.lines, "Drivers:", N=1))
    print(extract(parser.lines, "Status:", N=1))
    workers = {}
    for line in parser.lines:
        if line.__contains__("worker-"):
            ip_worker = line.split("-")[-2]
            port_worker = line.split("-")[-1]
            id_worker = line.split("-")[1]
            try:
                workers[ip_worker].append([port_worker,id_worker])
            except:
                workers[ip_worker] = [(port_worker,id_worker)]
    print("====WORKERS====")
    for k, (worker, d) in enumerate(workers.items()):
        print(f"@{worker} : {len(d)} up ({'-'.join([v[0] for v in d])})")