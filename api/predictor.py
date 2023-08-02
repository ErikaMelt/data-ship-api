import pickle
from flask import jsonify

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

def validate_input(data):
    try:
        required_keys = ["passenger_class", "gender",
                         "embarked_from", "family_size", "fare", "age"]
        for key in required_keys:
            if key not in data:
                return jsonify({"error": f"Missing required key: {key}"}), 400

        valid_passenger_classes = ["first", "second", "third"]
        valid_genders = ["male", "female"]
        valid_ports = ["southampton", "queenstown", "cherbourg"]

        if not isinstance(data["family_size"], int):
            return {"error": "Invalid data type for 'Family Size'. Expected an integer."}, 400

        if not isinstance(data["passenger_class"], str) or data["passenger_class"].lower() not in valid_passenger_classes:
            return {"error": "Invalid data type for 'passenger_class'. Expected 'first', 'second', or 'third'."}, 400

        if not isinstance(data["gender"], str) or data["gender"].lower() not in valid_genders:
            return {"error": "Invalid data type for 'Gender'. Expected 'male' or 'female'."}, 400

        if not isinstance(data["embarked_from"], str) or data["embarked_from"].lower() not in valid_ports:
            return {"error": "Invalid data type for 'Embarked Port'. Expected 'Southampton', 'Queenstown', or 'Cherbourg'."}, 400

        if not isinstance(data["fare"], (int, float)):
            return {"error": "Invalid data type for 'Fare'. Expected an integer or float."}, 400

        if not isinstance(data["age"], int):
            return {"error": "Invalid data type for 'Age'. Expected an integer."}, 400

        return None

    except Exception as e:
        return {"error": f"An error occurred during input validation: {str(e)}"}, 400
