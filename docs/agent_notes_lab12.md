# Agent Note Summary
## 1. Який use case обрано
Було реалізовано topic modeling assistant для аналізу тематичних кластерів. Агент отримує top_words та top_docs і має визначити тему, оцінити її якість та перевірити наявність noise.

## 2. Який agent task
Основні задачі агента:
* запропонувати назву теми;
* визначити, чи є тема noisy;
* класифікувати тему як good, mixed або bad;
* сформувати фінальну структуровану відповідь.

## 3. Які tools реалізовано
Було реалізовано три tools:
* suggest_topic_label(top_words, top_docs) – визначення назви теми;
* detect_noise_words(top_words) – пошук noisy або нерелевантних слів;
* score_topic_quality(top_words, top_docs) – оцінка якості теми.

## 4. Як агент вирішує, коли викликати tool
Agent використовує просту rule-based логіку:
* викликає detect_noise_words, якщо topic містить підозрілі або неоднозначні слова;
* викликає suggest_topic_label, якщо baseline-класифікація невпевнена;
* викликає score_topic_quality, якщо потрібно оцінити coherence теми.

## 5. Як логуються tool calls
Кожен tool call логувався у формат JSON Lines, наприклад:
```
{
    "timestamp": "2026-05-14T06:49:41",
    "tool_name": "detect_noise_words",
    "input": {
      "top_words": ["НАТО", "альянс", "оборона", "саміт", "Брюссель"]
    },
    "output": {
      "is_noise": false,
      "noise_words": []
    },
    "success": true,
    "error": null,
    "reason": "Found 0 noise words."
}
```

## 6. Що tools реально покращили
Tools покращили:
* якість класифікації у складних кейсах;
* структурованість reasoning pipeline;
* обробку noisy topics.

## 7. Де tools були зайві або не допомогли
У простих кейсах tools інколи дублювали baseline без покращення результату. Наприклад: case_001, case_005.

Також були випадки, коли quality = mixed, але tools повертали неповний список labels.

## 8. Які помилки лишилися
Основні типи помилок:
* over-trust до tool outputs;
* inconsistent taxonomy labels;
* unnecessary tool calls.
Також detect_noise_words інколи визначав stopwords як noise.

## 9. Що б ви фіксили далі
Варто додати confidence score та conditional tool calling, щоб використовувати baseline-відповідь у випадках високої впевненості моделі та уникати зайвих викликів tools. Також доцільно покращити роботу detect_noise_words, оскільки наразі tool може noise. Крім того, необхідно впровадити fixed label set для уніфікації класифікації та уникнення неузгоджених topic labels.