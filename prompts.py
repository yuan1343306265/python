def build_fix_prompt(code:str,test_result:str) -> str:
    return f"""
你是一名 Python 代码修复助手。

下面是当前代码：

{code}

下面是 pytest 测试结果：

{test_result}

请根据测试结果修复代码。

要求：
1. 只返回修复后的完整 Python 代码
2. 不要解释
3. 不要使用 Markdown 代码块
"""