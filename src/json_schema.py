extraction_schema = {
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