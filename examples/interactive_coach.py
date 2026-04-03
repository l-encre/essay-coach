#!/usr/bin/env python3
"""Interactive Essay Coach - Multi-turn conversation"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from essay_coach.main import EssayCoach

TRAINING_LABELS = {
    "opening":       "开头专训",
    "closing":       "结尾专训",
    "language":      "语言专训",
    "transitions":   "衔接过渡专训",
    "evidence":      "论据专训",
    "argumentation": "论证论述专训",
}

def main():
    coach = EssayCoach()
    conversation_history = None

    print("=" * 60)
    print("高考议论文专项教练")
    print("=" * 60)
    print("\n可用专训类型：")
    for key, label in TRAINING_LABELS.items():
        print(f"  {key:<16} {label}")

    training_type = input("\n请选择专训类型（直接回车默认 opening）：\n> ").strip() or "opening"
    if training_type not in TRAINING_LABELS:
        print(f"未知类型: {training_type}，使用默认 opening")
        training_type = "opening"

    print(f"\n正在加载【{TRAINING_LABELS[training_type]}】...\n")
    response = coach.train(training_type, "开始专训", conversation_history)
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
        response = coach.train(training_type, user_input, conversation_history)
        print("\n" + response["assistant_reply"])
        conversation_history = response["conversation_history"]

if __name__ == "__main__":
    main()
