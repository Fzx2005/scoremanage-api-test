import pytest
from common.http_client import HttpClient

class TestUnAuthAccess:
    """未登录权限拦截专项测试：无会话Cookie访问所有核心业务接口"""
    def setup_class(self):
        self.client = HttpClient()

    def test_no_login_access_student_list(self):
        """未登录访问学生列表接口"""
        resp = self.client.get("/student/list")
        print(f"未登录访问学生列表响应：{resp.text[:300]}")
        assert resp.status_code == 200

    def test_no_login_access_score_list(self):
        """未登录访问成绩列表接口"""
        resp = self.client.get("/score/list")
        print(f"未登录访问成绩列表响应：{resp.text[:300]}")
        assert resp.status_code == 200

    def test_no_login_access_sum_score(self):
        """未登录访问总成绩统计接口"""
        resp = self.client.get("/score/sum")
        print(f"未登录访问总成绩接口响应：{resp.text[:300]}")
        assert resp.status_code == 200

    def test_no_login_add_student(self):
        """未登录调用新增学生接口"""
        data = {"studentNo":"20260901","studentName":"游客新增","gender":"男"}
        resp = self.client.post("/student/add", data=data)
        assert resp.status_code == 200

    def test_no_login_add_score(self):
        """未登录调用新增成绩接口"""
        data = {"studentNo":"201723131","scoreType":2,"scoreValue":80}
        resp = self.client.post("/score/add", data=data)
        assert resp.status_code == 200

    def test_no_login_delete_data(self):
        """未登录调用删除成绩接口"""
        resp = self.client.get("/score/delete", params={"id":999})
        assert resp.status_code == 200
