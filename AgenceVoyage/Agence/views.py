from django.shortcuts import render, redirect
from .models import Client, Voyage, Reservation
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def liste_clients(request):
    clients = Client.objects.all()
    return render(request, 'liste_clients.html', {'clients': clients})

def register(request):
    if request.method == 'POST':
        prenom = request.POST['prenom']
        nom = request.POST['nom']
        email = request.POST['email']
        password = request.POST['password']

        # Créer un nouveau client dans la base de données
        client = Client(prenom=prenom, nom=nom, email=email)
        client.save()

        # Créer un utilisateur Django (si vous utilisez le système d'authentification intégré)
        user = User.objects.create_user(username=email, password=password)
        user.save()

        messages.success(request, 'Votre compte a été créé avec succès!')
        return redirect('home')  # Redirige vers la page d'accueil après inscription
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Authentification
        user = authenticate(username=email, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Vous êtes maintenant connecté!')
            return redirect('home')
        else:
            messages.error(request, 'Email ou mot de passe incorrect')
            return render(request, 'login.html')
    return render(request, 'login.html')

def reserver(request):
    if request.method == "POST":
        # Remplacez par la logique nécessaire pour enregistrer la réservation
        client_id = request.POST.get("client_id")  # Exemple de récupération de client_id
        voyage_id = request.POST.get("voyage_id")  # Exemple de récupération de voyage_id

        if client_id and voyage_id:
            Reservation.objects.create(client_id=client_id, voyage_id=voyage_id)
            messages.success(request, 'Votre réservation a été effectuée avec succès!')
            return redirect("confirmation")  # Redirigez vers une page de confirmation
    return render(request, "reserver.html")

def visite(request):
    if request.method == "POST":
        # Remplacez par la logique nécessaire pour enregistrer la réservation
        client_id = request.POST.get("client_id")  # Exemple de récupération de client_id
        voyage_id = request.POST.get("voyage_id")  # Exemple de récupération de voyage_id

        if client_id and voyage_id:
            Reservation.objects.create(client_id=client_id, voyage_id=voyage_id)
            messages.success(request, 'Votre réservation a été effectuée avec succès!')
            return redirect("confirmation")  # Redirigez vers une page de confirmation
    return render(request, "visite.html")
