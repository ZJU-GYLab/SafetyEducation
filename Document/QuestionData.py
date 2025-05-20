import re
import json
import os

def parse_choice_questions(file_path):
    """解析选择题文件"""
    questions = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式匹配选择题
    pattern = r'(\d+)\.\.?\s+(.*?)\s+A\.\s+(.*?)\s+B\.\s+(.*?)(?:\s+C\.\s+(.*?))?(?:\s+D\.\s+(.*?))?(?:\s+E\.\s+(.*?))?(?:\s+F\.\s+(.*?))?(?=\s+正确答案：|\n\d+\.\.?|\s*$)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for i, match in enumerate(matches):
        question_id = f"qx{i+1:03d}"  # 使用qx前缀和序号
        question_text = match[1].strip()
        
        # 构建选项字典
        options = {"A": match[2].strip()}
        if match[3].strip():
            options["B"] = match[3].strip()
        if len(match) > 4 and match[4].strip():
            options["C"] = match[4].strip()
        if len(match) > 5 and match[5].strip():
            options["D"] = match[5].strip()
        if len(match) > 6 and match[6].strip():
            options["E"] = match[6].strip()
        if len(match) > 7 and match[7].strip():
            options["F"] = match[7].strip()
        
        # 查找答案
        answer_pattern = rf'{match[0]}\.\.?\s+.*?正确答案：([A-F])'
        answer_match = re.search(answer_pattern, content, re.DOTALL)
        answer = answer_match.group(1) if answer_match else "A"  # 默认答案为A
        
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
    pattern = r'(\d+)\.\.?\s+(.*?)\s+正确答案：(对|错)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for i, match in enumerate(matches):
        question_id = f"qp{i+1:03d}"  # 使用qp前缀和序号
        question_text = match[1].strip()
        answer = True if match[2] == "对" else False
        
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
    choice_file = "/Users/chenhaotian/GYLab_SafetyEducation/Document/选择题带答案.txt"
    true_false_file = "/Users/chenhaotian/GYLab_SafetyEducation/Document/判断题带答案.txt"
    output_file = "/Users/chenhaotian/GYLab_SafetyEducation/Document/QuestionLibrary.json"
    
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