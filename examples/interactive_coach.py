#!/usr/bin/env python3
"""Interactive Essay Coach - Multi-turn conversation"""

from essay_coach.main import EssayCoach

def main():
    coach = EssayCoach()
    conversation_history = None
    
    print("=" * 60)
    print("高考议论文开头专项教练")
    print("=" * 60)
    
    # First message - start the training
    print("\n正在加载训练题目...\n")
    response = coach.opening_training("开始开头专训", conversation_history)
    print(response['assistant_reply'])
    conversation_history = response['conversation_history']
    
    # Multi-turn conversation
    while True:
        print("\n" + "-" * 60)
        user_input = input("你的输入（输入 'exit' 退出）：\n> ").strip()
        
        if user_input.lower() in ['exit', 'quit', '退出']:
            print("\n感谢使用高考议论文开头专项教练！")
            break
        
        if not user_input:
            print("请输入内容")
            continue
        
        print("\n正在批改...")
        response = coach.opening_training(user_input, conversation_history)
        print("\n" + response['assistant_reply'])
        conversation_history = response['conversation_history']

if __name__ == "__main__":
    main()
