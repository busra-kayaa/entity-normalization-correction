import json
import os


def convert():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Elindeki 10.000'lik veya bölünmüş dosyaları buraya ekle
    input_files = ['train.json', 'validation.json', 'test.json']

    system_prompt = (
        "You are an expert text correction system. Correct the input text and provide a detailed JSON analysis. "
        "Use ONLY these 6 error types: 'deascii', 'typographic', 'terminology', 'lexical', 'grammar', 'punctuation'. "
        "Definitions: deascii (Turkish character issues), typographic (spelling/space/typos), "
        "terminology (official name changes), lexical (vocabulary errors), grammar (syntax/articles), "
        "punctuation (missing/wrong marks)."
    )

    for file_name in input_files:
        input_path = os.path.join(current_dir, file_name)
        output_path = os.path.join(current_dir, f"mizan_6class_{file_name.replace('.json', '.jsonl')}")

        if not os.path.exists(input_path): continue

        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        with open(output_path, 'w', encoding='utf-8') as f:
            for item in data:
                corrections = []
                if item['is_noisy'] and item['error_type'] != 'none':
                    # Kelime bazlı farkı modelin kendisinin bulması için
                    # başlangıçta tüm cümleyi veya farkı işaretliyoruz.
                    corrections.append({
                        "original": item['input'],
                        "corrected": item['target'],
                        "type": item['error_type'],
                        "explanation": f"Fixed {item['error_type']} error."
                    })

                response_json = {
                    "originalText": item['input'],
                    "correctedText": item['target'],
                    "corrections": corrections
                }

                # Llama 3 Fine-Tuning Formatı
                example = {
                    "instruction": system_prompt,
                    "input": item['input'],
                    "output": json.dumps(response_json, ensure_ascii=False)
                }
                f.write(json.dumps(example, ensure_ascii=False) + '\n')

        print(f"✅ {file_name} hazır: {output_path}")


if __name__ == "__main__":
    convert()