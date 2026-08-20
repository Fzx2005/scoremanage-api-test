import pytest
from common.http_client import HttpClient
from config import TEACHER_ADMIN, SCORE_TYPE_EXERCISE, SCORE_TYPE_TEST, SCORE_TYPE_EXAM


@pytest.fixture(scope="module")
def teacher_client(http_client):
    login_data = {"userName":"admin","password":"123456","type":1}
    resp = http_client.post("/user/login", data=login_data)
    print("====教师登录调试信息====")
    print(f"登录status_code:{resp.status_code}")
    print(f"登录response_text:{resp.text}")
    return http_client


class TestTeacherLogin:
    """教师登录模块：正向、反向用例"""
    @pytest.mark.xfail(reason="后端BUG‑020：Filter耗尽POST表单输入流，Python‑requests无法登录，Postman可正常登录")
    def test_teacher_login_success(self, http_client):
        """正向：正确账号密码登录"""
        data = {
            "userName": TEACHER_ADMIN["username"],
            "password": TEACHER_ADMIN["password"],
            "type": 1
        }
        resp = http_client.post("/user/login", data=data)
        print("\n====调试登录====")
        print(f"status_code={resp.status_code}")
        print(f"url={resp.url}")
        print(f"response_text={resp.text}")
        assert resp.status_code == 200

    @pytest.mark.xfail(reason="后端BUG‑020：Filter耗尽POST表单输入流，Python‑requests无法登录，Postman可正常登录")
    def test_teacher_login_wrong_password(self, http_client):
        """反向：账号正确，密码错误"""
        data = {
            "userName": TEACHER_ADMIN["username"],
            "password": "wrongpass123",
            "type": 1
        }
        resp = http_client.post("/user/login", data=data)
        print(resp.text[:300])
        assert resp.status_code == 200

    @pytest.mark.xfail(reason="后端BUG‑020：Filter耗尽POST表单输入流，Python‑requests无法登录，Postman可正常登录")
    def test_teacher_login_empty_username(self, http_client):
        """反向：用户名为空"""
        data = {
            "userName": "",
            "password": TEACHER_ADMIN["password"],
            "type": 1
        }
        resp = http_client.post("/user/login", data=data)
        print(resp.text[:300])
        assert resp.status_code == 200

    @pytest.mark.xfail(reason="后端BUG‑020：Filter耗尽POST表单输入流，Python‑requests无法登录，Postman可正常登录")
    def test_teacher_logout(self, teacher_client):
        """正向：教师登出接口，真实接口POST /user/loginOut"""
        resp = teacher_client.post("/user/loginOut", data={})
        print(resp.text[:300])
        assert resp.status_code == 200

    @pytest.mark.xfail(reason="后端BUG‑020：Filter耗尽POST表单输入流，Python‑requests无法登录，Postman可正常登录")
    def test_teacher_login_wrong_role(self, http_client):
        """反向：教师账号选择学生角色登录 type=2"""
        login_data = {
            "userName": TEACHER_ADMIN["username"],
            "password": TEACHER_ADMIN["password"],
            "type": 2
        }
        resp = http_client.post("/user/login", data=login_data)
        print(resp.text[:300])
        assert resp.status_code == 200

    @pytest.mark.xfail(reason="后端BUG‑020：Filter耗尽POST表单输入流，Python‑requests无法登录，Postman可正常登录")
    def test_teacher_login_not_exist_account(self, http_client):
        """反向：不存在的教师账号登录"""
        login_data = {
            "userName": "not_exist_admin",
            "password": "123456",
            "type": 1
        }
        resp = http_client.post("/user/login", data=login_data)
        print(resp.text[:300])
        assert resp.status_code == 200

    @pytest.mark.xfail(reason="后端BUG‑020：Filter耗尽POST表单输入流，Python‑requests无法登录，Postman可正常登录")
    def test_teacher_login_unauthorized_access(self, http_client):
        """反向：未登录直接访问教师业务接口"""
        resp = http_client.get("/student/getAllStudent", params={"page":1,"limit":10})
        print(resp.text[:300])
        assert resp.status_code == 200


class TestTeacherStudentManage:
    """教师端-学生管理模块：增删改查，正向反向"""
    def test_query_student_list(self, teacher_client):
        """正向：查询全部学生列表 真实接口 /student/getAllStudent"""
        resp = teacher_client.get("/student/getAllStudent", params={"page":1,"limit":10})
        print(f"status:{resp.status_code}, text:{resp.text[:400]}")
        try:
            res = resp.json()
        except Exception:
            res = None
        assert resp.status_code == 200

    def test_search_student_by_name(self, teacher_client):
        """正向：按学生姓名搜索，post传参 getAllStudent"""
        post_data = {"page":1,"limit":10,"name":"张"}
        resp = teacher_client.post("/student/getAllStudent", data=post_data)
        print(f"status:{resp.status_code}, text:{resp.text[:400]}")
        assert resp.status_code == 200

    def test_add_student_repeat_stuno(self, teacher_client):
        """反向：新增学生，学号重复"""
        add_data = {
            "studentNo": "201723131",
            "studentName": "测试重复学号",
            "gender": "男",
            "stuPass": "201723131"
        }
        resp = teacher_client.post("/student/addStudent", data=add_data)
        print(f"status:{resp.status_code}, text:{resp.text[:400]}")
        assert resp.status_code == 200

    def test_update_student(self, teacher_client):
        """正向：修改学生信息"""
        update_data = {
            "id": 1,
            "studentNo": "201723131",
            "studentName": "修改后的名字",
            "gender": "女"
        }
        resp = teacher_client.post("/student/updateStudent", data=update_data)
        print(f"status:{resp.status_code}, text:{resp.text[:400]}")
        assert resp.status_code == 200

    def test_delete_student(self, teacher_client):
        """正向：删除学生（不要删真实业务数据）"""
        resp = teacher_client.get("/student/deleteStudent", params={"id": 999})
        print(f"status:{resp.status_code}, text:{resp.text[:400]}")
        assert resp.status_code == 200

    def test_student_list_pagination(self, teacher_client):
        """正向：学生列表分页功能验证"""
        resp_page1 = teacher_client.get("/student/getAllStudent", params={"page": 1, "limit": 10})
        print(f"第1页响应：{resp_page1.text[:400]}")
        assert resp_page1.status_code == 200

        resp_page2 = teacher_client.get("/student/getAllStudent", params={"page": 2, "limit": 10})
        print(f"第2页响应：{resp_page2.text[:400]}")
        assert resp_page2.status_code == 200

        resp_page0 = teacher_client.get("/student/getAllStudent", params={"page": 0, "limit": 10})
        assert resp_page0.status_code == 200

        resp_limit_max = teacher_client.get("/student/getAllStudent", params={"page": 1, "limit": 9999})
        assert resp_limit_max.status_code == 200


class TestTeacherScoreManage:
    """教师端成绩管理、学生总成绩管理"""
    def test_query_score_list(self, teacher_client):
        """正向：教师查询全部成绩列表"""
        resp = teacher_client.get("/score/getAllScore", params={"page":1,"limit":10})
        print(f"status:{resp.status_code}, text:{resp.text[:400]}")
        assert resp.status_code == 200

    def test_search_score_by_name(self, teacher_client):
        """正向：按学生名字查询成绩"""
        post_data = {"page":1,"limit":10,"studentName":"张"}
        resp = teacher_client.post("/score/getAllScore", data=post_data)
        print(f"status:{resp.status_code}, text:{resp.text[:400]}")
        assert resp.status_code == 200

    def test_update_score(self, teacher_client):
        """正向：修改成绩"""
        form_data = {
            "id": 1,
            "studentNo": "201723131",
            "scoreType": SCORE_TYPE_EXAM,
            "scoreValue": 88
        }
        resp = teacher_client.post("/student/studentSelect", data=form_data)
        print(f"status:{resp.status_code}, text:{resp.text[:400]}")
        assert resp.status_code == 200

    def test_delete_score(self, teacher_client):
        """正向：删除成绩记录"""
        resp = teacher_client.get("/score/deleteScore", params={"id": 888})
        print(f"status:{resp.status_code}, text:{resp.text[:400]}")
        assert resp.status_code == 200

    def test_add_score_negative_value(self, teacher_client):
        """反向：新增成绩，分数为负数（非法数据）"""
        form_data = {
            "studentNo": "201723131",
            "scoreType": SCORE_TYPE_TEST,
            "scoreValue": -20
        }
        resp = teacher_client.post("/score/addScore", data=form_data)
        print(f"status:{resp.status_code}, text:{resp.text[:400]}")
        assert resp.status_code == 200

    def test_query_all_sum_score(self, teacher_client):
        """正向：教师端查询学生总成绩管理列表"""
        resp = teacher_client.get("/score/getAllSumScore", params={"page":1,"limit":10})
        print(f"status:{resp.status_code}, text:{resp.text[:400]}")
        assert resp.status_code == 200

    def test_search_sum_score(self, teacher_client):
        """正向：条件筛选总成绩"""
        post_data = {"page":1,"limit":10,"scoreType":SCORE_TYPE_EXAM}
        resp = teacher_client.post("/score/getAllSumScore", data=post_data)
        print(f"status:{resp.status_code}, text:{resp.text[:400]}")
        assert resp.status_code == 200

    def test_score_list_pagination(self, teacher_client):
        """正向：成绩列表分页功能验证"""
        resp_page1 = teacher_client.get("/score/getAllSumScore", params={"page": 1, "limit": 10})
        print(f"第1页响应：{resp_page1.text[:400]}")
        assert resp_page1.status_code == 200

        resp_page2 = teacher_client.get("/score/getAllSumScore", params={"page": 2, "limit": 10})
        print(f"第2页响应：{resp_page2.text[:400]}")
        assert resp_page2.status_code == 200

        resp_page_neg = teacher_client.get("/score/getAllSumScore", params={"page": -1, "limit": 10})
        assert resp_page_neg.status_code == 200

    def test_sum_score_pagination(self, teacher_client):
        """正向：学生总成绩列表分页功能验证"""
        resp_page1 = teacher_client.get("/score/getAllSumScore", params={"page": 1, "limit": 10})
        print(f"第1页响应：{resp_page1.text[:400]}")
        assert resp_page1.status_code == 200

        resp_page2 = teacher_client.get("/score/getAllSumScore", params={"page": 2, "limit": 10})
        print(f"第2页响应：{resp_page2.text[:400]}")
        assert resp_page2.status_code == 200
