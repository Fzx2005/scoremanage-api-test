import requests
from config import BASE_URL


class HttpClient:
    def __init__(self, base_url: str = None):
        if base_url is None:
            self.base_url = BASE_URL
        else:
            self.base_url = base_url
        self.session = requests.Session()

    def post(self, uri, data=None, **kwargs):
        if self.base_url:
            url = self.base_url + uri
        else:
            url = uri

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "PostmanRuntime/7.29.0",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }
        # 合并外部传入headers
        if "headers" in kwargs:
            headers.update(kwargs["headers"])
            kwargs["headers"] = headers
        else:
            kwargs["headers"] = headers

        resp = self.session.post(url, data=data,** kwargs)
        # 调试打印真实请求头
        print("\n====Python发送请求头====")
        print(resp.request.headers)
        print("====响应内容====")
        print(resp.text)
        return resp

    def get(self, uri, params=None, headers=None, **kwargs):
        if self.base_url:
            full_url = self.base_url + uri
        else:
            full_url = uri

        default_headers = {
            "User-Agent": "PostmanRuntime/7.29.0",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }
        if headers:
            default_headers.update(headers)
        resp = self.session.get(full_url, params=params, headers=default_headers, **kwargs)
        return resp

    def clear_cookie(self):
        """清空会话Cookie，模拟退出登录/未登录状态"""
        self.session.cookies.clear()

    def close(self):
        self.session.close()
