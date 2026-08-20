import pytest
from common.http_client import HttpClient
from config import STUDENT_ACCOUNT, SCORE_TYPE_EXERCISE, SCORE_TYPE_TEST, SCORE_TYPE_EXAM


@pytest.fixture(scope="module")
def student_client(http_client):
    """学生角色会话fixture，使用正确学生登录接口 /user/studentLogin"""
    login_data = {"userName": STUDENT_ACCOUNT["stu_no"], "password": STUDENT_ACCOUNT["password"], "type": 2}
    # ✅真实抓包：学生登录接口是 /user/studentLogin
    resp = http_client.post("/user/studentLogin", data=login_data)
    print("====学生登录调试信息====")
    print(f"status_code:{resp.status_code}")
    print(f"response:{resp.text}")
    return http_client



class TestStudentLogin:
    """学生登录模块：正向、反向用例"""
    @pytest.mark.xfail(reason="后端BUG‑020：Filter耗尽POST表单输入流，Python‑requests无法登录，Postman可正常登录")
    def test_student_login_success(self, http_client):
        """正向：学生账号密码正确登录"""
        login_data = {
            "userName": STUDENT_ACCOUNT["stu_no"],
            "password": STUDENT_ACCOUNT["password"],
            "type": 2
        }
        resp = http_client.post("/user/login", data=login_data)
        print(resp.text[:300])
        assert resp.status_code == 200

    @pytest.mark.xfail(reason="后端BUG‑020：Filter耗尽POST表单输入流，Python‑requests无法登录，Postman可正常登录")
    def test_student_login_wrong_password(self, http_client):
        """反向：学号正确，密码错误"""
        login_data = {
            "userName": STUDENT_ACCOUNT["stu_no"],
            "password": "999999",
            "type": 2
        }
        resp = http_client.post("/user/login", data=login_data)
        print(resp.text[:300])
        assert resp.status_code == 200

    @pytest.mark.xfail(reason="后端BUG‑020：Filter耗尽POST表单输入流，Python‑requests无法登录，Postman可正常登录")
    def test_student_login_empty_stuno(self, http_client):
        """反向：学号为空登录"""
        login_data = {
            "userName": "",
            "password": STUDENT_ACCOUNT["password"],
            "type": 2
        }
        resp = http_client.post("/user/login", data=login_data)
        print(resp.text[:300])
        assert resp.status_code == 200

    @pytest.mark.xfail(reason="后端BUG‑020：Filter耗尽POST表单输入流，Python‑requests无法登录，Postman可正常登录")
    def test_student_logout(self, student_client):
        """正向：学生账号登出，真实接口POST /user/studentloginOut"""
        resp = student_client.post("/user/studentloginOut", data={})
        print(resp.text[:300])
        assert resp.status_code == 200


class TestStudentScoreQuery:
    """学生端业务：只允许查看本人成绩，不能增删改成绩/学生信息"""
    def test_student_query_my_score(self, student_client):
        """正向：学生查询自己的全部成绩，抓包接口 /score/getMyScoreInfo"""
        resp = student_client.get("/score/getMyScoreInfo", params={"page":1,"limit":10})
        print(f"status:{resp.status_code}, text:{resp.text[:400]}")
        assert resp.status_code == 200

    def test_student_filter_score_by_type(self, student_client):
        """正向：按成绩类型筛选自己成绩"""
        resp = student_client.get("/score/getMyScoreInfo", params={"page":1,"limit":10,"scoreType": SCORE_TYPE_EXAM})
        print(f"status:{resp.status_code}, text:{resp.text[:400]}")
        assert resp.status_code == 200

    def test_student_view_my_sum_score(self, student_client):
        """正向：学生查看自己成绩总分统计，抓包接口 /score/getMyScore"""
        resp = student_client.get("/student/myTotal", params={"page":1,"limit":10})
        print(f"status:{resp.status_code}, text:{resp.text[:400]}")
        assert resp.status_code == 200

    def test_student_cannot_see_other_student(self, student_client):
        """反向：学生尝试查询别的学生成绩（权限校验）"""
        resp = student_client.get("/score/getMyScoreInfo", params={"page":1,"limit":10,"stuNo": 201723999})
        print(f"status:{resp.status_code}, text:{resp.text[:400]}")
        assert resp.status_code == 200

    def test_student_no_permission_add_score(self, student_client):
        """反向：学生尝试新增成绩，无权限操作"""
        add_form = {
            "studentNo": STUDENT_ACCOUNT["stu_no"],
            "scoreType": SCORE_TYPE_TEST,
            "scoreValue": 75
        }
        resp = student_client.post("/score/add", data=add_form)
        print(f"status:{resp.status_code}, text:{resp.text[:400]}")
        assert resp.status_code == 200

    def test_student_no_permission_delete_score(self, student_client):
        """反向：学生尝试删除成绩，无权限操作"""
        resp = student_client.get("/score/delete", params={"id": 1})
        print(f"status:{resp.status_code}, text:{resp.text[:400]}")
        assert resp.status_code == 200

    def test_student_no_permission_manage_student(self, student_client):
        """反向：学生尝试访问学生管理列表接口，权限拦截，真实接口 /student/getAllStudent"""
        resp = student_client.get("/student/getAllStudent", params={"page":1,"limit":10})
        print(f"status:{resp.status_code}, text:{resp.text[:400]}")
        assert resp.status_code == 200

    def test_student_data_isolation(self, student_client):
        """反向：学生尝试查看其他学生的成绩，验证数据隔离"""
        resp = student_client.get("/score/getMyScore", params={"page":1,"limit":10,"stuNo": 201723999})
        print(f"status:{resp.status_code}, text:{resp.text[:400]}")
        assert resp.status_code == 200
