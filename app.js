document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const locationInput = document.getElementById('location-input');
    const sendBtn = document.getElementById('send-btn');
    
    // Add initial bot message
    addBotMessage("Hello! I'm your AI Wildlife Spotting Assistant. You can ask me to identify wildlife or find national parks. How can I help you today?");
    
    // Send message when button is clicked
    sendBtn.addEventListener('click', sendMessage);
    
    // Also send message when Enter is pressed
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    function sendMessage() {
        const message = userInput.value.trim();
        const location = locationInput.value.trim();
        
        if (message) {
            // Add user message to chat
            addUserMessage(message);
            
            // Clear input
            userInput.value = '';
            
            // Determine if the user is asking about parks or wildlife
            if (message.toLowerCase().includes('park') || message.toLowerCase().includes('visit')) {
                // Search for parks
                searchParks(message, location);
            } else {
                // Identify wildlife
                identifyWildlife(message, location);
            }
        }
    }
    
    function addUserMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message';
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function addBotMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function addBotHTML(html) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        messageDiv.innerHTML = html;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function identifyWildlife(query, location) {
        addBotMessage("Let me identify that for you...");
        
        fetch('/api/identify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                location: location
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success' && data.results.length > 0) {
                data.results.forEach(species => {
                    let html = `
                        <div class="species-card">
                            <h3>${species.common_name}</h3>
                            <p class="scientific-name">${species.scientific_name}</p>
                            <p>${species.description}</p>
                    `;
                    
                    if (species.image_url) {
                        html += `<img src="${species.image_url}" alt="${species.common_name}">`;
                    }
                    
                    html += `</div>`;
                    addBotHTML(html);
                });
            } else {
                addBotMessage("I couldn't find any matching species. Could you provide more details?");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            addBotMessage("Sorry, I encountered an error while trying to identify the species.");
        });
    }
    
    function searchParks(query, location) {
        addBotMessage("Looking for parks...");
        
        fetch('/api/parks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                location: location
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success' && data.parks.length > 0) {
                data.parks.forEach(park => {
                    let html = `
                        <div class="park-card">
                            <h3>${park.name}</h3>
                            <p>Location: ${park.location}</p>
                            <p>${park.description}</p>
                    `;
                    
                    if (park.image_url) {
                        html += `<img src="${park.image_url}" alt="${park.name}">`;
                    }
                    
                    html += `</div>`;
                    addBotHTML(html);
                });
            } else {
                addBotMessage("I couldn't find any parks matching your query. Try a different location or description.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            addBotMessage("Sorry, I encountered an error while searching for parks.");
        });
    }
});