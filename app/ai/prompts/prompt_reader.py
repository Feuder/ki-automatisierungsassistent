def zusammenfassenprompt():
    with open("app/ai/prompts/prompte/Text_zusammenfassen_Promt.md", "r", encoding="utf-8") as prompt_datei:
        return prompt_datei.read()

def task_erstellenpromt():
    with open("app/ai/prompts/prompte/Aufgaben_erstellen_Promt.md", "r", encoding="utf-8") as prompt_datei:
        return prompt_datei.read()

def ordnerbericht_prompt():
    with open("app/ai/prompts/prompte/Ordnerbericht_zusammenstellen.md", "r", encoding="utf-8") as prompt_datei:
        return prompt_datei.read()

def dateiablage_prompt():
    with open("app/ai/prompts/prompte/Ordneranalyse.md", "r", encoding="utf-8") as prompt_datei:
        return prompt_datei.read()