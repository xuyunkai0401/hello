import pytest
import os

if __name__ == "__main__":
    # 删除旧的测试结果
    if os.path.isdir('allure-results'):
        os.system('rmdir /s /q allure-results')
    
    # 运行pytest并指定测试用例目录和Allure结果目录
    pytest.main([
        'testCase/',  # 指定测试用例目录
        '--alluredir', 'allure-results',  # 指定Allure报告的结果目录
        '--clean-alluredir',  # 在生成报告前清理结果目录
        '-vv',  # 增加详细输出的篇幅
    ])
    
    # 使用Allure命令行工具生成报告
    os.system('allure generate allure-results --clean -o allure-report')