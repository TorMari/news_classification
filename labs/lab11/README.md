# Lab 11 - LLM extraction як інженерія (schema-first)

## Extraction-задача
**Кейс:** витяг інформації про економічні/бізнес-події з новин

Потрібно отримати:
* `company` (організація/компанія)
* `event_type` (тип події)
* `amount` (сума угоди/інвестиції)
* `currency` (валюта)
* `date` (дата події)
* `location` (локація)

---

## JSON schema

```
{
  "type": "object",
  "properties": {
    "company": {
      "type": "string",
      "description": "Назва компанії або організації"
    },
    "event_type": {
      "type": "string",
      "enum": ["acquisition", "investment", "partnership", "launch", "sanctions", "other"],
      "description": "Тип події"
    },
    "amount": {
      "type": ["number", "null"],
      "description": "Сума (нормалізоване число без тексту)"
    },
    "currency": {
      "type": ["string", "null"],
      "enum": ["USD", "EUR", "UAH", None],
      "description": "Валюта"
    },
    "date": {
      "type": ["string", "null"],
      "format": "date",
      "description": "Дата у форматі YYYY-MM-DD"
    },
    "location": {
      "type": ["string", "null"],
      "description": "Локація події"
    }
  },
  "required": ["company", "event_type"],
  "additionalProperties": False
}
```

---

## Як виглядає baseline prompt
```
messages = [
      {"role": "system", "content": "You are a precise information extraction system. Respond ONLY with valid JSON."},
      {"role": "user", "content": f"""Extract data from the text below. 
      
  Rules:
  - If missing → null
  - Use YYYY-MM-DD for dates if possible
  - Amount must be a number
  - Extract only the core brand name
  - event_type must be one of ["acquisition", "investment", "partnership", "launch", "sanctions", "other"]
  - Normalize currency (e.g., "доларів" → USD, "€" -> EUR, "$" -> USD)
  - Choose the main company which mentioned first if multiple are mentioned


  Output schema:
  {{
    "company": string,
    "event_type": lowercase string,
    "amount": number or null,
    "currency": string or null,
    "date": string or null,
    "location": string or null
  }}

  Text: {item['text']}"""}
  ]
```

---

## Який validator використано
Validator здійснює перевірку на валідність JSON та на відповідність схемі.

---

## Як працює repair loop
На кожній ітерації відбувається генерація відповіді моделлю на основі поточного prompt. Отриманий результат перевіряється у два етапи: спочатку на валідність JSON (парсинг), а потім на відповідність схемі (schema validation). Якщо відповідь є коректною, процес завершується успішно.

Якщо ж відповідь не проходить валідацію, до діалогу додається попередній (помилковий) результат разом із повідомленням про помилку. Модель отримує інструкцію виправити відповідь з урахуванням конкретної причини помилки та згенерувати новий, виправлений JSON.

Цей процес повторюється до досягнення валідного результату або до вичерпання максимальної кількості спроб (MAX_REPAIR_ATTEMPTS=2). Якщо після всіх ітерацій результат залишається невалідним, повертається остання відповідь разом із інформацією про помилку.

---

## Який valid JSON rate до і після repair
* Raw valid JSON rate (до repair): 100.00%
* Post-repair valid JSON rate: 100.00%

---

## Які проблеми залишаються
Repair loop не покриває:
* не виправляє semantic помилки (наприклад, неправильний `event_type`)
* не запобігає галюцинаціям (особливо `date`)
* не гарантує правильний вибір `company`
* не контролює відповідність значень тексту