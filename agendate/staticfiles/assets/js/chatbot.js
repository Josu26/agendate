document.addEventListener('DOMContentLoaded', function() {
    const sendButton = document.getElementById('send-button');
    const userInput = document.getElementById('user-input');
    const messagesDiv = document.getElementById('messages');

    // Función para agregar mensajes al chat
    function addMessage(role, message) {
        const messageDiv = document.createElement('div');
        messageDiv.innerHTML = `<strong>${role}:</strong> ${message}`;
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight; // Desplazar al final
    }

    // Función para manejar el clic en el botón de enviar
    sendButton.addEventListener('click', async function() {
        const userMessage = userInput.value.trim();
        if (userMessage === '') return;

        // Añade el mensaje del usuario al chat
        addMessage('Tú', userMessage);
        userInput.value = '';

        try {
            // Enviar el mensaje al servidor
            const response = await fetch(`/chat/?message=${encodeURIComponent(userMessage)}`);
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }

            // Obtener la respuesta del bot
            const data = await response.json();
            const botResponse = data.response;

            // Añade la respuesta del bot al chat
            addMessage('Bot', botResponse);
        } catch (error) {
            console.error('Error al enviar el mensaje:', error);
            addMessage('Bot', 'Lo siento, hubo un problema con el servidor.');
        }
    });

    // Opcional: Manejar la tecla Enter para enviar el mensaje
    userInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            sendButton.click();
        }
    });
});
