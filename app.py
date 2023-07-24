import tkinter as tk
from tkinter import messagebox
from neo4j import GraphDatabase
from collections import Counter
from fpdf import FPDF
import os
from dotenv import load_dotenv
load_dotenv()
neo4j_password = os.environ.get("NEO4J_PASSWORD")
# Informations de connexion à la base de données Neo4j
uri = os.environ.get("NEOAJ_URI")
driver = GraphDatabase.driver(uri, auth=("neo4j", neo4j_password))

def get_all_ingredients():
    with driver.session() as session:
        query = "MATCH (i:ingredient) RETURN i.ingredient_nom AS ingredient_nom"
        result = session.run(query)
        ingredients = [record["ingredient_nom"] for record in result]
    return ingredients

def get_ingredients(recette_ids):
    with driver.session() as session:
        recette_ids_str = ', '.join(str(recette_id) for recette_id in recette_ids)
        query = f"MATCH (i:ingredient)-[:contient]->(r:recette) WHERE r.recette_id IN [{recette_ids_str}] RETURN i.ingredient_nom AS ingredient_nom"
        result = session.run(query)
        ingredients = [record["ingredient_nom"] for record in result]
    return ingredients

recettes = {
    1: "saumon sauce à l'estragon & asperges verts",
    2: "pizza turque au boeuf & persil",
    3: "Poulet & sauce fraise balsamique",
    4: "Rigatoni & endive poélées",
    5: "filet de saumon & sauce à l'oseille",
    6: "Conchiglie & fricassé de champignons",
    7: "Rigatoni au pesto verde & tomates confites",
    8: "Salade de penne, burrata & tomates cerise",
    9: "Conchiglie au pesto rosso et a la feta",
    10: "Farfamme & pesto aux champignons des bois",
}

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Liste de courses", 0, 1, "C")
    
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def generate_shopping_list():
    selected_recipes = []
    for recette_id, recette_nom in recettes.items():
        if recette_vars[recette_id].get() == 1:
            selected_recipes.append(recette_id)
    
    produits = get_ingredients(selected_recipes)
    liste_courses = Counter(produits)
    
    # Générer le PDF de la liste de courses
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Liste de courses", 0, 1, "C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    for ingredient, count in liste_courses.items():
        pdf.cell(0, 10, f"{ingredient} ({count})", 0, 1)
    pdf.output("liste_courses.pdf")

    messagebox.showinfo("Liste de courses", "La liste de courses a été générée avec succès.")

# Créer la fenêtre principale
window = tk.Tk()
window.title("Sélection de recettes")

# Créer les radio buttons pour chaque recette
recette_vars = {}
for recette_id, recette_nom in recettes.items():
    recette_vars[recette_id] = tk.IntVar()
    recette_checkbox = tk.Checkbutton(window, text=recette_nom, variable=recette_vars[recette_id])
    recette_checkbox.pack()

# Créer le bouton pour générer la liste de courses
generate_button = tk.Button(window, text="Générer la liste de courses", command=generate_shopping_list)
generate_button.pack()

# Lancer la boucle principale de l'interface graphique
window.mainloop()

driver.close()
