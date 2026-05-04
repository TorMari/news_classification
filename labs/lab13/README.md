# Lab 13 - Multi-agent crew

## Use case
**Кейс:** витяг структурованої інформації про економічні та бізнес-події з новинних текстів.

Потрібно отримати:
* `company` (організація/компанія)
* `event_type` (тип події)
* `amount` (сума угоди/інвестиції)
* `currency` (валюта)
* `date` (дата події)
* `location` (локація)

---

## Агенти
* Triager
* Extractor
* Reviewer
* Fallback (Repair Agent)

---

## Workflow
Input -> Triager -> Extractor -> Reviewer -> Fallback (Repair) 

---

## Delegation rules
1. Triager викликається першим.
2. Extractor викликається після Triager.
3. Reviewer перевіряє Extractor output.
4. Якщо Reviewer verdict = accept -> final output.
5. Якщо verdict = repair_needed -> fallback/repair attempt.
6. Якщо repair не допоміг -> manual_review.

---

## Як працює Reviewer
Перевіряє:
* відповідність тексту  
* відсутність галюцинацій  
* формат і типи полів  
* валідність event_type  
* коректність дат  

---

## Як працює fallback
- отримує помилки від Reviewer  
- перегенеровує JSON  
- виправляє некоректні поля  
- повторно проходить Reviewer  

---

## Як запускати notebook
1. Відкрити `lab13_multi_agent_crew_triager_extractor_reviewer.ipynb` у Google Colab.
2. Запустити всі блоки.

---

## Де лежать logs
Crew logs лежать у файлі `crew_logs_lab13.jsonl`.

---

## Які метрики
Valid Final Output Rate: 10.00%
Reviewer Catch Rate: 0.00%
Fallback Activation Rate: 0.00%
Fallback Success Rate: 0.00%
Manual Review Rate: 90.00%

Single-agent vs Crew comparison
| Rate | Single-agent | Crew |
|------|--------------|------|
|valid output rate|0%|10%|
|consistency error rate|100%|90%|
|hallucinated fields|10%|10%|
|missing required fields|0%|0%|
|cases needing manual review|100%|90%|

---

## Головний висновок

Multi-agent підхід не забезпечив значного покращення якості через слабку валідацію на етапі Reviewer, що призводить до відсутності коректного запуску fallback. Як наслідок, система не виправляє помилки та не покращує якість single-agent рішення.