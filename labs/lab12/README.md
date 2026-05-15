# Lab 12 — Tool-grounded Single-Agent

## Use Case
Було реалізовано topic modeling assistant для аналізу тематичних кластерів. Агент отримує top_words та top_docs і має визначити тему, оцінити її якість та перевірити наявність noise.

---

## Agent Task
Agent повинен:
- визначити назву теми;
- перевірити тему на noise;
- оцінити якість теми (`good`, `mixed`, `bad`);
- сформувати фінальну структуровану відповідь.

---

## Реалізовані Tools
Було реалізовано три tools:
* suggest_topic_label(top_words, top_docs) – визначення назви теми;
* detect_noise_words(top_words) – пошук noisy або нерелевантних слів;
* score_topic_quality(top_words, top_docs) – оцінка якості теми.

---

## Як запускати notebook
1. Відкрити `lab12_tool_grounded_single_agent.ipynb` у Google Colab.
2. Запустити всі блоки.

---

## Де лежать logs
Tools logs лежать у файлі `tool_logs_lab12.jsonl`.

---

## Test Cases
Набір test cases складається з 10 прикладів, кожен з яких має JSON-розмітку з полями `case_id`, `case_type`, `top_words`, `top_docs` та `expected`. Обрані кейси покривають такі випадки:
1. простий кейс, де tools очевидно допомагають;
2. кейс із missing data;
3. кейс із noisy text;
4. кейс, де tool повертає порожній результат;
5. кейс, де агент не мав би викликати зайвий tool;
6. кейс із неоднозначністю;
7. кейс, де потрібно два tools підряд;
8. кейс, де validator знаходить проблему;
9. кейс, де фінальна відповідь має послатися на tool output;
10. кейс, де агент помилився або tool не допоміг.

---

## Метрики
1. Tool Call Success Rate: 100.00%
2. Average Tool Calls per Task: 2.20
3. Tasks with Useful Tool Use: 3
4. Unnecessary Tool Calls: 1
5. Tool Error Rate: 0.00%
6. 3 Tools Used in Task: 50.00%
7. Tool Output Ignored: 8
8. Final Answer Contradicts Tool: 2
9. Manual Ratings: {'correct': 2, 'partly_correct': 7, 'wrong': 1}

---

## Головний Висновок

Tool-grounded підхід покращив структурованість reasoning та допоміг у складних classification cases. Найкращий результат tools показали у noisy та ambiguous topics, але залишились проблеми з over-trust до tool outputs, inconsistent labels та unnecessary tool calls.