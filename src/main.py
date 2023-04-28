from analyzer import Analyzer
from web_server import WebServer

def main():
    analyzer = Analyzer()
    web_server = WebServer(analyzer)
    web_server.start()

if __name__ == "__main__":
    main()