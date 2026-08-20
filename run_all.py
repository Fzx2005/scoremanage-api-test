import pytest

if __name__ == '__main__':
    # 执行全部用例，生成报告输出到reports文件夹
    pytest.main([
        "./testcases/",
        "-s",
        "-v",
        "--html=reports/report.html",
        "--self-contained-html"
    ])
