# Audit Summary — Lab 12 (Tool-grounded single-agent)
## Який use case
Topic modeling assistant
Агент отримує top words + top documents по темі і має:
* запропонувати назву теми;
* перевірити, чи тема не noise;
* класифікувати тему як good / mixed / bad.

## Які tools реалізовано
* suggest_topic_label(top_words, top_docs) – визначення назви теми;
* detect_noise_words(top_words) – пошук noisy або нерелевантних слів;
* score_topic_quality(top_words, top_docs) – оцінка якості теми.

## Скільки test cases
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

## Tool call success rate

Tool Call Success Rate: 100.00%

## Average tool calls per task

Average Tool Calls per Task: 2.20

## Скільки задач реально виграли від tools

Tasks with Useful Tool Use: 3

## Скільки було unnecessary tool calls

Unnecessary Tool Calls: 1

## 2–3 найкращі приклади tool use
1. case_005: Tools дали повністю структурований pipeline: detect_noise_words, suggest_topic_label, score_topic_quality. 
Результат: sports + good + no noise

2. case_006: Тут tools явно покращили результат: baseline видав беззмістовий label "two"; suggest_topic_label правильно визначив тему як technology.

## 2–3 проблемні приклади
1. case_009: Tool пов'язує слово "висадка" з садівництвом ('classification': 'science/gardening'). 

2. case_010: Tool suggest_topic_label повернув gardening, ігноруючи technology тематику.

## Що б ви покращували далі

Варто додати confidence score та conditional tool calling, щоб використовувати baseline-відповідь у випадках високої впевненості моделі та уникати зайвих викликів tools. Також доцільно покращити роботу detect_noise_words, оскільки наразі tool може noise. Крім того, необхідно впровадити fixed label set для уніфікації класифікації та уникнення неузгоджених topic labels.