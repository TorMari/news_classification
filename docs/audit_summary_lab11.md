# Audit Summary — Lab 11 (LLM extraction як інженерія (schema-first))

## Який extraction-кейс
**Кейс:** витяг інформації про економічні/бізнес-події з новин

Потрібно отримати:
* `company` (організація/компанія)
* `event_type` (тип події)
* `amount` (сума угоди/інвестиції)
* `currency` (валюта)
* `date` (дата події)
* `location` (локація)

## Кількість прикладів у evaluation set
Evaluation set складається з 16 текстів, кожен з яких має вручну створену еталонну (gold) JSON-розмітку з полями `text` та `expected`.

## Який raw valid JSON rate
Raw valid JSON rate (до repair): 100.00%

## Який post-repair valid JSON rate
Post-repair valid JSON rate: 100.00%

## Який schema-valid JSON rate
Schema-valid JSON rate: 100.00%

## Поля, що ламаються найчастіше
1. `event_type`: модель плутає partnership, acquisition та investment
2. `company`: вибір не тієї сутності, спотворення назви
3. `location`: погана нормалізація (ФРН vs Німеччина), іноді пропуски

## Наймасовіші категорії помилок
1. hallucinated field/value (найчастище у `date`)
2. semantic extraction error (`event_type`, `company`)
3. normalization issues (`location`, `company`)
4. null handling issue

## Чи schema-first підхід спрацював добре
Schema-first підхід добре спрацював для забезпечення коректної структури та типів даних (валидний JSON майже у всіх випадках). Водночас він не вирішує змістовні помилки — модель продовжує галюцинувати та неправильно інтерпретувати події і сутності.