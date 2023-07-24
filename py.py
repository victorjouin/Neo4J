import pandas as pd

# Lecture du fichier CSV
df = pd.read_csv("recettes_avec_ingredients.csv")

# Création du nouveau DataFrame
new_df = pd.DataFrame(columns=["recette_id", "recette_nom", "ingredient_id", "ingredient_nom"])

# Itération sur les lignes du DataFrame d'origine
for _, row in df.iterrows():
    ingredient_ids = row["ingredient_ids"].split(",")
    ingredients = row["ingredients"].split(",")
    
    # Vérifier si les deux listes ont la même longueur
    if len(ingredient_ids) == len(ingredients):
        for i in range(len(ingredient_ids)):
            new_row = {
                "recette_id": row["recette_id"],
                "recette_nom": row["recette_nom"],
                "ingredient_id": ingredient_ids[i],
                "ingredient_nom": ingredients[i]
            }
            new_df = pd.concat([new_df, pd.DataFrame([new_row])], ignore_index=True)

# Enregistrement du nouveau DataFrame en tant que fichier CSV
new_df.to_csv("nouveau_recette.csv", index=False)
