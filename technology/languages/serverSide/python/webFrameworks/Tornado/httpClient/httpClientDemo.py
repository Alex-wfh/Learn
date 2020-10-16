from tornado.httpclient import HTTPClient


def synchronous_visit():
    http_client = HTTPClient()
    response = http_client.fetch('http://www.baidu.com')
    print(response.body[:100])


if __name__ == '__main__':
    synchronous_visit()