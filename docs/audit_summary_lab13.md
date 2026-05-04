# Audit Summary — Lab 13 (Multi-agent crew)

## Який extraction-кейс
**Кейс:** витяг структурованої інформації про економічні та бізнес-події з новинних текстів.

Потрібно отримати:
* `company` (організація/компанія)
* `event_type` (тип події)
* `amount` (сума угоди/інвестиції)
* `currency` (валюта)
* `date` (дата події)
* `location` (локація)

## Які агенти реалізовано
Реалізовано multi-agent pipeline:
1. Triager: визначає тип задачі, задає schema routing
2. Extractor: витягує дані відповідно до schema
3. Reviewer: перевіряє коректність extraction, виявляє помилки та галюцинації
4. Fallback (Repair loop): виправляє помилки після Reviewer

## Скільки test cases
Набір test cases складається з 10 прикладів, кожен з яких має JSON-розмітку з полями `case_id`, `description`, `input` та `expected_behavior`. Обрані кейси покривають коректні новини, відсутні поля, неявні дати, шум (відсотки, аналітика), помилки в тексті (опечатки).

## Valid final output rate
Valid Final Output Rate: 10.00%

## Reviewer catch rate
Reviewer Catch Rate: 0.00%

## Fallback activation rate
Fallback Activation Rate: 0.00%

## Fallback success rate
Fallback Success Rate: 0.00%

## Manual review rate
Manual Review Rate: 90.00%

## Single-agent vs crew comparison
| Rate | Single-agent | Crew |
|------|--------------|------|
|valid output rate|0%|10%|
|consistency error rate|100%|90%|
|hallucinated fields|10%|10%|
|missing required fields|0%|0%|
|cases needing manual review|100%|90%|

## Найкращі приклади роботи crew
**Case 009** 
* Правильно визначено company, amount, currency
* Коректна нормалізація (1 млрд -> 1000000000)

Простий, явний кейс без неоднозначностей

**Case 006** — Googlr (з шумом)
* Витягнуто суму: 500000000
* Валюта нормалізована -> USD
* location -> Париж

Попри помилку в назві, extraction загалом адекватний

## Проблемні кейси
**CASE 001**

Помилки:
* Дата 2024-03-15 (у тексті 2024-05-15)
* Reviewer повертає accept, ігноруючи помилку

**CASE 003**

Помилки:
* Неправильний event_type: investment (має бути acquisition)
* Неправильний date: "YYYY-MM-DD" (має бути null)
* Reviewer повертає accept, ігноруючи помилку

**CASE 008**

Помилки:
* amount: 0.055 (неправильна нормализація)
* currency: percent
* Reviewer повертає accept, ігноруючи помилку

## Що варто покращити
1. Посилити Reviewer
2. Заборонити placeholder значення

Never output: "YYYY-MM-DD", "unknown", "не розташовано"

3. Додати перевірку типів полів та enum для event_type
4. Покращити правила нормалізації та виправлення помилок у полях
