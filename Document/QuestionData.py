import re
import json
import os

def parse_choice_questions(file_path):
    """解析选择题文件"""
    questions = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式匹配选择题
    pattern = r'(\d+)\.\.?\s+(.*?)\s+A[、.](.*?)\s+B[、.](.*?)\s+C[、.](.*?)\s+D[、.]?(.*?)(?=\n\d+\.\.|\n\s*$|$)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for i, match in enumerate(matches):
        question_id = f"q{int(match[0]):03d}"
        question_text = match[1].strip()
        options = {
            "A": match[2].strip(),
            "B": match[3].strip(),
            "C": match[4].strip(),
            "D": match[5].strip() if match[5].strip() else "无"
        }
        
        # 这里需要设置默认答案，实际应用中可能需要从其他地方获取
        # 由于题库中没有提供答案，这里暂时设置为A
        answer = "A"
        
        question_data = {
            "id": question_id,
            "type": "choice",
            "question": question_text,
            "options": options,
            "answer": answer
        }
        
        questions.append(question_data)
    
    return questions

def parse_true_false_questions(file_path):
    """解析判断题文件"""
    questions = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式匹配判断题
    pattern = r'(\d+)\.\s+(.*?)(?=\n\d+\.|\n\s*$|$)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for i, match in enumerate(matches):
        question_id = f"q{int(match[0])+1000:03d}"  # 使用1000+序号避免与选择题ID冲突
        question_text = match[1].strip()
        
        # 这里需要设置默认答案，实际应用中可能需要从其他地方获取
        # 由于题库中没有提供答案，这里暂时随机设置为true
        answer = True
        
        question_data = {
            "id": question_id,
            "type": "true_false",
            "question": question_text,
            "answer": answer
        }
        
        questions.append(question_data)
    
    return questions

def main():
    # 设置文件路径
    choice_file = os.path.join(os.path.dirname(__file__), "..", "Document", "选择题.txt")
    true_false_file = os.path.join(os.path.dirname(__file__), "..", "Document", "判断题.txt")
    output_file = os.path.join(os.path.dirname(__file__), "..", "Document", "questions.json")
    
    # 解析题目
    choice_questions = parse_choice_questions(choice_file)
    true_false_questions = parse_true_false_questions(true_false_file)
    
    # 合并题目
    all_questions = choice_questions + true_false_questions
    
    # 保存为JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)
    
    print(f"成功转换 {len(choice_questions)} 道选择题和 {len(true_false_questions)} 道判断题")
    print(f"结果已保存到 {output_file}")

if __name__ == "__main__":
    main()