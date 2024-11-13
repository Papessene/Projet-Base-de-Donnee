import os
import platform
import pyodbc
import random
from tabulate import tabulate
from datetime import datetime

# Configuration de la connexion à SQL Server avec authentification Windows
connexion = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-4V10MTB;'
    'DATABASE=GestionEtudiants;'
    'Trusted_Connection=yes;'
)

def gererEtudiants():
    x = "#" * 30
    y = "=" * 28
    global auRevoir
    auRevoir = "\n {}\n# {} #\n# ===> Système de gestion des étudiants <===  #\n# {} #\n {}".format(x, y, y, x)

    print("""

  --------------------------------------------------------------------
 |====================================================================|
 |======== Bienvenue dans le Système de Gestion des Étudiants ========|
 |====================================================================|
  --------------------------------------------------------------------

Entrez 1 : Pour voir la liste des étudiants
Entrez 2 : Pour ajouter un nouvel étudiant
Entrez 3 : Pour rechercher un étudiant
Entrez 4 : Pour supprimer un étudiant
Entrez 5 : Pour ajouter une nouvelle filière
Entrez 6 : Pour ajouter une nouvelle promotion
Entrez 7 : Pour quitter

		""")

    try:
        choixUtilisateur = int(input("Veuillez sélectionner une option ci-dessus : "))
    except ValueError:
        exit("\nErreur : ce n'est pas un nombre valide.")
    else:
        print("\n")

    if choixUtilisateur == 1:
        afficherEtudiants()
    elif choixUtilisateur == 2:
        ajouterEtudiant()
    elif choixUtilisateur == 3:
        rechercherEtudiant()
    elif choixUtilisateur == 4:
        supprimerEtudiant()
    elif choixUtilisateur == 5:
        ajouterFiliere()
    elif choixUtilisateur == 6:
        ajouterPromotion()
    elif choixUtilisateur == 7:
        quitter()
    else:
        print("Veuillez entrer une option valide")
        gererEtudiants()

def afficherEtudiants():
    cursor = connexion.cursor()
    query = """
    SELECT e.id, e.ine, e.nom, e.prenom, e.date_naissance, e.adresse, e.telephone, e.email, e.email_institutionnel,
           p.annee, f.nom_filiere
    FROM Etudiants e
    LEFT JOIN Promotion p ON e.promotion_id = p.id
    LEFT JOIN Filiere f ON e.filiere_id = f.id
    """
    cursor.execute(query)
    etudiants = cursor.fetchall()

    # Définir les en-têtes du tableau
    headers = ["ID", "INE", "Nom", "Prénom", "Date de Naissance", "Adresse", "Téléphone", "Email", "Email Institutionnel", "Promotion", "Filière"]

    # Afficher le tableau
    print("Liste des Étudiants\n")
    print(tabulate(etudiants, headers=headers, tablefmt="grid"))

def ajouterFiliere():
    nom_filiere = input("Entrez le nom de la filière : ")
    cursor = connexion.cursor()
    cursor.execute("INSERT INTO Filiere (nom_filiere) VALUES (?)", (nom_filiere,))
    connexion.commit()
    print(f"Filière '{nom_filiere}' ajoutée avec succès.")

def ajouterPromotion():
    annee = input("Entrez l'année de la promotion (exemple : 2023-2024) : ")

    # Vérifier le format de l'année si nécessaire
    if not annee or len(annee) != 9 or '-' not in annee:
        print("Format d'année invalide. Veuillez entrer une année au format '2023-2024'.")
        return

    cursor = connexion.cursor()
    try:
        cursor.execute("INSERT INTO Promotion (annee) VALUES (?)", (annee,))
        connexion.commit()
        print(f"Promotion '{annee}' ajoutée avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'ajout de la promotion : {e}")

def afficherPromotions():
    cursor = connexion.cursor()
    cursor.execute("SELECT id, annee FROM Promotion")
    promotions = cursor.fetchall()
    print("\nListe des promotions :")
    for promotion in promotions:
        print(f"ID: {promotion[0]}, Année: {promotion[1]}")

def generer_email_institutionnel(prenom, nom):
    cursor = connexion.cursor()
    query = "SELECT COUNT(*) FROM Etudiants WHERE prenom = ? AND nom = ?"
    cursor.execute(query, (prenom, nom))
    count = cursor.fetchone()[0]
    if count > 0:
        return f"{prenom.lower()}.{nom.lower()}{count + 1}@edu.sn"
    else:
        return f"{prenom.lower()}.{nom.lower()}@edu.sn"

def ajouterEtudiant():
    nom = input("Entrez le nom de l'étudiant : ")
    prenom = input("Entrez le prénom de l'étudiant : ")

    # Validation du format de la date de naissance
    while True:
        date_naissance = input("Entrez la date de naissance de l'étudiant (AAAA-MM-JJ) : ")
        try:
            # Vérification du format
            date_naissance = datetime.strptime(date_naissance, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Format de date invalide. Veuillez entrer la date au format AAAA-MM-JJ.")

    adresse = input("Entrez l'adresse de l'étudiant : ")
    telephone = input("Entrez le numéro de téléphone de l'étudiant : ")
    email = input("Entrez l'email de l'étudiant : ")

    # Génération de l'email institutionnel
    email_institutionnel = generer_email_institutionnel(prenom, nom)

    # Sélectionner une promotion par nom
    cursor = connexion.cursor()
    cursor.execute("SELECT id, annee FROM Promotion")
    promotions = cursor.fetchall()
    print("Choisissez une promotion (ID) :")
    for promotion in promotions:
        print(f"{promotion[0]}: {promotion[1]}")
    promotion_id = int(input("ID de la promotion : "))

    # Sélectionner une filière par nom
    cursor.execute("SELECT id, nom_filiere FROM Filiere")
    filieres = cursor.fetchall()
    print("Choisissez une filière (ID) :")
    for filiere in filieres:
        print(f"{filiere[0]}: {filiere[1]}")
    filiere_id = int(input("ID de la filière : "))

    # Génération de l'INE
    cursor.execute("SELECT COUNT(*) FROM Etudiants")
    count = cursor.fetchone()[0] + 1
    ine = f"INE{count:05}"

    # Insertion de l'étudiant
    cursor.execute("INSERT INTO Etudiants (ine, nom, prenom, date_naissance, adresse, telephone, email, email_institutionnel, promotion_id, filiere_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (ine, nom, prenom, date_naissance, adresse, telephone, email, email_institutionnel, promotion_id, filiere_id))
    connexion.commit()
    print("\n=> Nouvel étudiant ajouté avec succès !")
    afficherEtudiants()

def rechercherEtudiant():
    critere = input("Rechercher par nom ou prénom : ")
    cursor = connexion.cursor()
    query = """
    SELECT e.id, e.ine, e.nom, e.prenom, e.date_naissance, e.adresse, e.telephone, e.email, e.email_institutionnel,
           p.annee, f.nom_filiere
    FROM Etudiants e
    LEFT JOIN Promotion p ON e.promotion_id = p.id
    LEFT JOIN Filiere f ON e.filiere_id = f.id
    WHERE e.nom = ? OR e.prenom = ?
    """
    cursor.execute(query, (critere, critere))
    etudiants = cursor.fetchall()
    if etudiants:
        print("\nÉtudiants trouvés :")
        for etudiant in etudiants:
            print(f"ID: {etudiant[0]}, INE: {etudiant[1]}, Nom: {etudiant[2]}, Prénom: {etudiant[3]}, Date de Naissance: {etudiant[4]}, Adresse: {etudiant[5]}, Téléphone: {etudiant[6]}, Email: {etudiant[7]}, Email Institutionnel: {etudiant[8]}, Promotion: {etudiant[9]}, Filière: {etudiant[10]}")
    else:
        print(f"\nAucun étudiant trouvé avec le nom ou prénom '{critere}'.")

def supprimerEtudiant():
    etudiant_id = int(input("Entrez l'ID de l'étudiant à supprimer : "))
    cursor = connexion.cursor()
    cursor.execute("SELECT * FROM Etudiants WHERE id = ?", etudiant_id)
    etudiant = cursor.fetchone()
    if etudiant:
        cursor.execute("DELETE FROM Etudiants WHERE id = ?", etudiant_id)
        connexion.commit()
        print(f"\nÉtudiant avec ID {etudiant_id} supprimé avec succès.")
    else:
        print(f"\nAucun étudiant trouvé avec l'ID '{etudiant_id}'.")

def quitter():
    print(auRevoir)
    connexion.close()
    quit()

def relancer():
    while True:
        reponseRelancer = input("\nVoulez-vous continuer à utiliser le programme ? (o pour Oui, n pour Non) : ")
        if reponseRelancer.lower() == 'o':
            gererEtudiants()
        else:
            quitter()

# Lancer la gestion des étudiants
gererEtudiants()
relancer()
