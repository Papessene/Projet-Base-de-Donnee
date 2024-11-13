-- Création de la base de données
CREATE DATABASE GestionEtudiants;
GO

-- Utilisation de la base de données
USE GestionEtudiants;
GO

-- Création de la table Filiere
CREATE TABLE Filiere (
    id INT PRIMARY KEY IDENTITY(1,1),
    nom_filiere VARCHAR(255) NOT NULL
);
GO

-- Création de la table Promotion
CREATE TABLE Promotion (
    id INT PRIMARY KEY IDENTITY(1,1),
    annee VARCHAR(9) NOT NULL
);
GO

-- Création de la table Etudiants
CREATE TABLE Etudiants (
    id INT PRIMARY KEY IDENTITY(1,1),
    ine VARCHAR(10) NOT NULL,
    nom VARCHAR(255) NOT NULL,
    prenom VARCHAR(255) NOT NULL,
    date_naissance DATE NOT NULL,
    adresse VARCHAR(255) NOT NULL,
    telephone VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    email_institutionnel VARCHAR(255),
    promotion_id INT,
    filiere_id INT,
    FOREIGN KEY (promotion_id) REFERENCES Promotion(id),
    FOREIGN KEY (filiere_id) REFERENCES Filiere(id)
);
GO
