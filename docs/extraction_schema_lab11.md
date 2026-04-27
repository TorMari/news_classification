# Extraction schema summary

## 1. Яка extraction-задача
**Кейс:** витягування інформації про економічні та бізнес-події з новинних текстів.

## 2. Які поля у JSON
Необхідно отримати такі поля:
* `company` (організація/компанія)
* `event_type` (тип події)
* `amount` (сума угоди/інвестиції)
* `currency` (валюта)
* `date` (дата події)
* `location` (локація)

## 3. Які поля required
Обов'язкові поля: `company`, `event_type`

## 4. Як виглядає JSON schema
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
## 5. Які правила для null / missing values
* Якщо значення відсутнє у тексті -> використовується null
* Значення null повинно бути типом, а не рядком ("null" — некоректно)

## 6. Які поля найчастіше проблемні
1. `event_type`: модель плутає partnership, acquisition та investment
2. `company`: вибір не тієї сутності, спотворення назви
3. `location`: погана нормалізація (ФРН vs Німеччина), іноді пропуски

## 7. Що repair loop реально виправляє
Repair loop ефективно покриває:
* синтаксичні помилки JSON
* відповідність схемі (типи, required поля)
* нормалізацію типів (number, null)

Але має обмеження:
* не виправляє semantic помилки (наприклад, неправильний `event_type`)
* не запобігає галюцинаціям (особливо `date`)
* не гарантує правильний вибір `company`
* не контролює відповідність значень тексту
