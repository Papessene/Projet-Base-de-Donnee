from django.db import models

class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15)

    class Meta:
        db_table = 'Client'  # Nom de la table SQL Server

class Voyage(models.Model):
    destination = models.CharField(max_length=100)
    date_depart = models.DateField()
    date_retour = models.DateField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'Voyage'

class Reservation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    date_reservation = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Reservation'