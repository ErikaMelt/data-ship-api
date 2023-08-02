import pickle

def load_file(path):
    with open(path, "rb") as f:
        model = pickle.load(f)
    return model

def predict(model, data):
    data = apply_feature_engineering(data)
    data.drop('age', axis=1, inplace=True) 

    # Make predictions using the pipeline previously trained. 
    prediction = model.predict(data)
    probability = model.predict_proba(data)
    return prediction, probability


def get_age_category(data):
    age = data['age'].iloc[0] 

    if age <= 12:
        age_category = 'child'
    elif age <= 18:
        age_category = 'teenager'
    elif age <= 30:
        age_category = 'young adult'
    elif age <= 50:
        age_category = 'adult'
    else:
        age_category = 'elderly'

    data['age_category'] = age_category

    return data

def calculate_family_fare(data):
    print()
    data.rename(columns={'fare': 'winsorized_fare'}, inplace=True)
    data['fare_per_family_member'] = data['winsorized_fare'] / (data['family_size'] + 1)  
    return data 

def apply_feature_engineering(data): 
    data = get_age_category(data)
    data = calculate_family_fare(data)
    return data 

