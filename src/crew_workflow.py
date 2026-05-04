from agents import run_extractor, run_triager, run_reviewer
from fallback import run_fallback_repair

def crew_workflow(text):
    print(f"--- Start Triager ---")
    triage = run_triager(text)
    
    print(f"--- Routing to Extractor ---")
    extraction = run_extractor(text, triage)
 
    print(f"--- Routing to Reviewer ---")
    attempts = 0
    repair = {} 
    
    while attempts < 2:
        review = run_reviewer(text, extraction)
        
        if review["verdict"] == "accept":
            return triage, extraction, review, repair 
            
        if review["verdict"] == "repair_needed": 
            print(f"Repair attempt {attempts + 1}")
            repair = run_fallback_repair(text, extraction, review["issues"])
            extraction = repair 
            attempts += 1
        else:
            break

    return triage, extraction, review, repair