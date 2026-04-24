import stanza
from evaluation_set import evaluation_set
from ner_rules import apply_hybrid_rules

stanza.download("uk")  
nlp = stanza.Pipeline("uk", processors="tokenize,ner")

def run_ner_stanza(text):
    doc = nlp(text)
    entities = []
    
    for ent in doc.ents:
        entities.append((ent.text, ent.type))
    
    return entities

results_baseline = []

for item in evaluation_set:
    predicted = run_ner_stanza(item["text"])
    
    results_baseline.append({
        "id": item["id"],
        "text": item["text"],
        "predicted": predicted,
        "expected": item["expected_entities"]
    })

for item in results_baseline:
    predicted = item["predicted"]
    expected = item["expected"]
    
    print(f"\n=== Example {item['id']} ===")
    print(f"Text: {item['text']}\n")
    
    print("Predicted:")
    if predicted:
        for ent, label in predicted:
            print(f"  - {ent} ({label})")
    else:
        print("  - None")
    
    print("\nExpected:")
    for ent, label in expected:
        print(f"  - {ent} ({label})")


results_hybrid = []

for item in evaluation_set:
    text = item["text"]
    
    predicted = apply_hybrid_rules(text, run_ner_stanza(text))

    results_hybrid.append({
        "id": item["id"],
        "text": text,
        "predicted": predicted,
        "expected": item["expected_entities"]
    })

for item in results_hybrid:
    predicted = item["predicted"]
    expected = item["expected"]
    
    print(f"\n=== Example {item["id"]} ===")
    print(f"Text: {item['text']}\n")
    
    print("Predicted:")
    if predicted:
        for ent, label in predicted:
            print(f"  - {ent} ({label})")
    else:
        print("  - None")
    
    print("\nExpected:")
    for ent, label in expected:
        print(f"  - {ent} ({label})")