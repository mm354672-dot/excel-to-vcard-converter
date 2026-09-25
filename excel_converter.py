import pandas as pd
import os

def clean_phone(phone):
    if pd.isna(phone):
        return ""
    cleaned = "".join(c for c in str(phone) if c.isdigit())
    if cleaned.startswith("8") and len(cleaned) == 11:
        cleaned = "7" + cleaned[1:]
    return "+" + cleaned if cleaned else ""

def convert_excel_to_vcard(excel_path, output_name="contacts.vcf"):
    if not os.path.exists(excel_path):
        print(f"[-] Ошибка: Файл {excel_path} не найден!")
        return False
        
    print(f"[+] Чтение файла: {excel_path}")
    df = pd.read_excel(excel_path)
    df.columns = [col.lower().strip() for col in df.columns]
    
    name_col = next((c for c in df.columns if "имя" in c or "name" in c or "фио" in c), None)
    phone_col = next((c for c in df.columns if "телефон" in c or "phone" in c or "номер" in c), None)
    
    if not name_col or not phone_col:
        print("[-] Ошибка: В таблице должны быть колонки с Именем и Телефоном!")
        return False
        
    vcard_content = ""
    saved_count = 0
    
    for index, row in df.iterrows():
        name = str(row[name_col]).strip()
        phone = clean_phone(row[phone_col])
        
        if not phone or name == "nan":
            continue
            
        vcard_content += "BEGIN:VCARD\n"
        vcard_content += "VERSION:3.0\n"
        vcard_content += f"FN:{name}\n"
        vcard_content += f"TEL;TYPE=CELL:{phone}\n"
        vcard_content += "END:VCARD\n"
        saved_count += 1
        
    with open(output_name, "w", encoding="utf-8") as f:
        f.write(vcard_content)
        
    print(f"[Успех] Конвертация завершена! Создан файл: {output_name}")
    print(f"[+] Успешно перенесено контактов: {saved_count}")
    return True

if __name__ == "__main__":
    test_data = {
        "Имя": ["Иван Продажи", "Алексей Поставщик", "Мария Клиент"],
        "Телефон": ["89991234567", "+7 (911) 765-43-21", "8 900 111 22 33"]
    }
    pd.DataFrame(test_data).to_excel("test_leads.xlsx", index=False)
    convert_excel_to_vcard("test_leads.xlsx", "business_leads.vcf")
