def zusammenfassenprompt():
    with open("app/ai/prompts/prompte/Text_zusammenfassen_Promt.md", "r", encoding="utf-8") as promt:
        return promt.read()
    
def task_erstellenpromt():
    with open("app/ai/prompts/prompte/Aufgaben_erstellen_Promt.md", "r", encoding="utf-8") as promt:
        return promt.read()
    
def ordnerbericht_prompt():
    with open("app/ai/prompts/prompte/Ordnerbericht_zusammenstellen.md", "r", encoding="utf-8") as promt:
        return promt.read()
    
def ordnerstrkurbericht():
    with open("app/ai/prompts/prompte/Ordnerbericht_zusammenstellen.md", "r", encoding="utf-8") as promt:
        return promt.read()