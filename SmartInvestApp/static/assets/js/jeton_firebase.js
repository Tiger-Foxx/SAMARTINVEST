// Assurez-vous d'avoir inclus le SDK Firebase dans votre projet
// et d'avoir initialisé Firebase avec votre configuration

// Récupérer le token de l'appareil
function getTokenAndSendToServer() {
    const messaging = firebase.messaging();
  
    // Demander la permission pour les notifications push
    messaging.requestPermission()
      .then(function() {
        console.log('Permission accordée');
        // Obtenir le token actuel
        return messaging.getToken();
      })
      .then(function(token) {
        console.log('Token obtenu:', token);
        // Envoyer le token au serveur
        sendTokenToServer(token);
      })
      .catch(function(err) {
        console.log('Impossible d\'obtenir la permission', err);
      });
  }
  
  // Envoyer le token au serveur Django
  function sendTokenToServer(token) {
    // Remplacez cette URL par l'URL de votre point de terminaison Django
    const url = '/path/to/your/django/view/';
  
    // Utilisez fetch pour envoyer une requête POST à votre serveur
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Assurez-vous d'inclure le token CSRF si nécessaire
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({ token: token })
    })
    .then(response => {
      if (response.ok) {
        console.log('Token envoyé au serveur avec succès');
      } else {
        console.log('Erreur lors de l\'envoi du token au serveur');
      }
    })
    .catch(error => {
      console.log('Erreur lors de l\'envoi du token:', error);
    });
  }
  
  // Fonction pour obtenir le cookie CSRF de Django
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Est-ce que le cookie commence par le nom recherché ?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  
  // Appeler la fonction pour démarrer le processus
  getTokenAndSendToServer();
  