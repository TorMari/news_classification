from embading_train import w2v_model
from embading_train import ft_model

def analyze_models(w2v_model, ft_model):

    test_words = [
        "фільм",        
        "дискваліфікація",       
        "євробачення",   
        "інфляція", 
        "фейки",    
        "оприлюднений", 
        "відновили",    
        "київ",      
        "Phillip Nova",  
        "сценарію"      
    ]

    print(f"{'Термін':<15} | {'Модель':<10} | {'Найближчі сусіди (Nearest Neighbors)'}")
    print("-" * 100)

    for term in test_words:
        print(f"{term:<15} | Word2Vec  | ", end="")
        if term in w2v_model.wv:
            w2v_neighbors = w2v_model.wv.most_similar(term, topn=5)
            print(", ".join([f"{n} ({s:.2f})" for n, s in w2v_neighbors]))
        else:
            print("Слово відсутнє у словнику W2V")

        print(f"{'':<15} | FastText  | ", end="")
        try:
            ft_neighbors = ft_model.wv.most_similar(term, topn=5)
            print(", ".join([f"{n} ({s:.2f})" for n, s in ft_neighbors]))
        except Exception as e:
            print(f"Помилка FastText: {e}")
        
        print("-" * 100)

analyze_models(w2v_model, ft_model)


def analyze_domain_specific_terms(w2v_model, ft_model):

    domain_terms = [
        "саундтрек", 
        "енергосистеми", 
        "санкції", 
        "законопроєкт", 
        "пенальті"
    ]

    print(f"{'Термін':<15} | {'Модель':<10} | {'Найближчі сусіди (Nearest Neighbors)'}")
    print("-" * 100)

    for term in domain_terms:
        print(f"{term:<15} | Word2Vec  | ", end="")
        if term in w2v_model.wv:
            w2v_neighbors = w2v_model.wv.most_similar(term, topn=5)
            print(", ".join([f"{n} ({s:.2f})" for n, s in w2v_neighbors]))
        else:
            print("Слово відсутнє у словнику W2V")

        print(f"{'':<15} | FastText  | ", end="")
        try:
            ft_neighbors = ft_model.wv.most_similar(term, topn=5)
            print(", ".join([f"{n} ({s:.2f})" for n, s in ft_neighbors]))
        except Exception as e:
            print(f"Помилка FastText: {e}")
        
        print("-" * 100)

analyze_domain_specific_terms(w2v_model, ft_model)