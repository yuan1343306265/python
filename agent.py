import os

from dotenv import load_dotenv
from openai import OpenAI

from tools import run_tests, read_file, write_file, backup_file
from prompts import build_fix_prompt


load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise ValueError("没有读取到 DEEPSEEK_API_KEY，请检查 .env 文件。")


client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",
)


def run_code_inspector(project_path: str):
    print("CodeInspector Agent 已启动")
    print("正在运行测试……")

    test_result = run_tests(project_path)
    print(test_result)

    test_result_lower = test_result.lower()

    if "failed" not in test_result_lower and "error" not in test_result_lower:
        print("测试全部通过，不需要修复。")
        return

    target_file = f"{project_path}/calculator.py"
    source_code = read_file(target_file)

    print("已读取需要检查的代码：")
    print(source_code)

    fix_prompt = build_fix_prompt(
        source_code,
        test_result,
    )

    print("正在请求大模型分析并修复代码……")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "user",
                "content": fix_prompt,
            }
        ],
    )

    fixed_code = response.choices[0].message.content

    fixed_code = (
        fixed_code
        .replace("```python", "")
        .replace("```", "")
        .strip()
    )

    backup_path = f"{target_file}.bak"
    backup_file(target_file, backup_path)
    print(f"原文件已备份到：{backup_path}")

    write_file(target_file, fixed_code)
    print("修复后的代码已写回原文件。")

    print("正在重新运行测试……")

    final_test_result = run_tests(project_path)
    print(final_test_result)

    final_test_result_lower = final_test_result.lower()

    if (
        "failed" not in final_test_result_lower
        and "error" not in final_test_result_lower
    ):
        final_status = "修复成功，所有测试已通过。"
    else:
        final_status = "修复后仍有测试失败，需要继续检查。"

    final_report = f"""
========== CodeInspector 最终报告 ==========
目标文件：{target_file}
备份文件：{backup_path}

首次测试结果：
{test_result}

修复后测试结果：
{final_test_result}

最终状态：{final_status}
===========================================
"""

    print(final_report)


if __name__ == "__main__":
    run_code_inspector(".")