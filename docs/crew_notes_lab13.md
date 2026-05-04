# Crew Design Summary
## 1. Який use case обрано
**Кейс:** витяг структурованої інформації про економічні та бізнес-події з новинних текстів.

Потрібно отримати:
* `company` (організація/компанія)
* `event_type` (тип події)
* `amount` (сума угоди/інвестиції)
* `currency` (валюта)
* `date` (дата події)
* `location` (локація)

## 2. Які агенти є в crew
* Triager
* Extractor
* Reviewer
* Fallback (Repair Agent)

## 3. Роль кожного агента
1. Triager: визначає тип задачі, задає schema routing
2. Extractor: витягує дані відповідно до schema
3. Reviewer: перевіряє коректність extraction, виявляє помилки та галюцинації
4. Fallback (Repair loop): виправляє помилки після Reviewer

## 4. Правила делегування
1. Triager викликається першим.
2. Extractor викликається після Triager.
3. Reviewer перевіряє Extractor output.
4. Якщо Reviewer verdict = accept -> final output.
5. Якщо verdict = repair_needed -> fallback/repair attempt.
6. Якщо repair не допоміг -> manual_review.

## 5. Що перевіряє Reviewer
* Відповідність даних тексту
* Відсутність галюцинацій
* Коректність типів (number, string, null)
* Формат дати (YYYY-MM-DD)
* Валідність event_type (enum)

## 6. Коли спрацьовує fallback
Fallback має запускатися, якщо:
* verdict = repair_needed
* verdict = fallback_needed
* JSON невалідний
* є пропущені або суперечливі поля

## 7. Що crew покращив порівняно з single-agent
Потенційно crew дає:
* додатковий контроль якості (Reviewer)
* можливість виправлення помилок (repair loop)
* більш стабільний формат виходу

За отриманими результатами:
* покращення не досягнуто через недостатній Reviewer

## 8. Де multi-agent підхід був зайвий
* Прості кейси з явною структурою без неоднозначностей
* Короткі новини без шуму

## 9. Які помилки залишилися
* reviewer missed error
* wrong reviewer output,
* extractor hallucinated field,
* final output inconsistent with input
* fallback not triggered

## 10. Що б ви фіксили далі
1. Посилити Reviewer
2. Заборонити placeholder значення

Never output: "YYYY-MM-DD", "unknown", "не розташовано"

3. Додати перевірку типів полів та enum для event_type
4. Покращити правила нормалізації та виправлення помилок у полях