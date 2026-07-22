from typing import TypedDict

class AgentState(TypedDict):
##项目类型
    project_path:str
##   测试结果 
    test_result:str
#错误信息
    error_message:str
##测试次数
    fix_count:int
###最终报告
    final_report:str
