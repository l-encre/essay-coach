#!/usr/bin/env python3
"""Interactive Essay Coach - Multi-turn conversation"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from essay_coach.main import EssayCoach

def main():
    coach = EssayCoach()
    conversation_history = None

    print("=" * 60)
    print("高考议论文专项教练")
    print("=" * 60)


    print("\n正在加载训练...\n")
    response = coach.chat("帮我开始作文专项训练", conversation_history)
    print(response["assistant_reply"])
    conversation_history = response["conversation_history"]

    while True:
        print("\n" + "-" * 60)
        user_input = input("你的输入（输入 exit 退出）：\n> ").strip()

        if user_input.lower() in ["exit", "quit", "退出"]:
            print("\n感谢使用高考议论文专项教练！")
            break

        if not user_input:
            print("请输入内容")
            continue

        print("\n正在处理...")
        response = coach.chat(user_input, conversation_history)
        print("\n" + response["assistant_reply"])
        conversation_history = response["conversation_history"]

if __name__ == "__main__":
    main()
