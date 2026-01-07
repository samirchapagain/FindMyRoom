// Theme Toggle
const themeToggle = document.getElementById('themeToggle');
const body = document.body;

// Check for saved theme preference
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'dark') {
    body.classList.add('dark-mode');
    if (themeToggle) themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
}

if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-mode');
        
        if (body.classList.contains('dark-mode')) {
            localStorage.setItem('theme', 'dark');
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        } else {
            localStorage.setItem('theme', 'light');
            themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        }
    });
}

// Dashboard Tabs Navigation
const tabButtons = document.querySelectorAll('.tab-btn');

tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        const tabName = button.getAttribute('data-tab');
        if (tabName === 'client') {
            window.location.href = '/';
        } else if (tabName === 'owner') {
            window.location.href = '/owner/';
        }
    });
});

// Unlock Buttons - Disabled for direct chat access
// const unlockButtons = document.querySelectorAll('.unlock-btn');
// Payment system removed - chat access is now direct

// Google-like Voice Search with Real-time Display
const voiceSearchBtn = document.getElementById('voiceSearchBtn');
const searchWrapper = document.getElementById('searchWrapper');
const voiceStatus = document.getElementById('voiceStatus');
const searchInput = document.getElementById('searchInput');
let recognition;

if (voiceSearchBtn && 'webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en-US';
    
    voiceSearchBtn.addEventListener('click', function() {
        startVoiceRecognition();
    });
    
    function startVoiceRecognition() {
        // Visual feedback - Google style
        voiceSearchBtn.classList.add('listening');
        searchWrapper.classList.add('listening');
        voiceStatus.classList.add('show');
        voiceStatus.textContent = 'Listening...';
        
        recognition.start();
    }
    
    recognition.onresult = function(event) {
        let interimTranscript = '';
        let finalTranscript = '';
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
            } else {
                interimTranscript += transcript;
            }
        }
        
        // Real-time display like Google
        searchInput.value = finalTranscript + interimTranscript;
        
        if (finalTranscript) {
            voiceStatus.textContent = 'Processing...';
            processVoiceSearch(finalTranscript);
        }
    };
    
    function processVoiceSearch(transcript) {
        // Send to backend for intelligent processing
        fetch('/voice-search/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({transcript: transcript})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                voiceStatus.textContent = `Found ${data.count} rooms`;
                
                // Auto-apply filters without page reload
                setTimeout(() => {
                    const url = new URL(window.location);
                    url.searchParams.set('q', transcript);
                    
                    Object.keys(data.filters).forEach(key => {
                        if (key.includes('location')) {
                            const location = data.filters[key];
                            if (location.includes('downtown')) url.searchParams.set('location', 'Downtown');
                            else if (location.includes('university')) url.searchParams.set('location', 'Near University');
                            else if (location.includes('business')) url.searchParams.set('location', 'Business District');
                        }
                        if (key.includes('room_type')) url.searchParams.set('room_type', data.filters[key]);
                        if (key.includes('price__lte')) url.searchParams.set('price_max', data.filters[key]);
                    });
                    
                    window.location.href = url.toString();
                }, 1000);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            voiceStatus.textContent = 'Search failed';
        })
        .finally(() => {
            setTimeout(resetVoiceUI, 2000);
        });
    }
    
    function resetVoiceUI() {
        voiceSearchBtn.classList.remove('listening');
        searchWrapper.classList.remove('listening');
        voiceStatus.classList.remove('show');
    }
    
    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
        voiceStatus.textContent = 'Voice recognition failed';
        setTimeout(resetVoiceUI, 2000);
    };
    
    recognition.onend = function() {
        if (!voiceStatus.textContent.includes('Processing') && !voiceStatus.textContent.includes('Found')) {
            resetVoiceUI();
        }
    };
} else if (voiceSearchBtn) {
    // Fallback for browsers without speech recognition
    voiceSearchBtn.addEventListener('click', function() {
        const transcript = prompt('Enter your search (voice recognition not supported):');
        if (transcript) {
            searchInput.value = transcript;
            document.getElementById('searchForm').submit();
        }
    });
}

// SMS Button with Backend Integration
const smsBtn = document.querySelector('.sms-btn');
if (smsBtn) {
    smsBtn.addEventListener('click', function() {
        const roomCards = document.querySelectorAll('.room-card');
        if (roomCards.length > 0) {
            const message = prompt('Enter your inquiry message:');
            if (message) {
                const firstRoomId = roomCards[0].querySelector('.unlock-btn').getAttribute('data-room-id');
                
                fetch('/sms-inquiry/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        room_id: firstRoomId,
                        message: message
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert(data.message);
                    } else {
                        alert('Failed to send SMS inquiry.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error sending SMS inquiry.');
                });
            }
        } else {
            alert('No rooms available for inquiry.');
        }
    });
}

// Enhanced Voice Filter Button
const voiceBtn = document.querySelector('.voice-btn');
if (voiceBtn && recognition) {
    voiceBtn.addEventListener('click', function() {
        this.style.transform = 'scale(1.2)';
        
        // Use the same recognition instance
        const filterRecognition = new webkitSpeechRecognition();
        filterRecognition.continuous = false;
        filterRecognition.interimResults = false;
        filterRecognition.lang = 'en-US';
        
        filterRecognition.start();
        
        filterRecognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            
            fetch('/voice-search/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({transcript: transcript})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show floating notification
                    showNotification(`Voice: "${transcript}" - ${data.message}`);
                    
                    // Auto-apply filters
                    const url = new URL(window.location);
                    Object.keys(data.filters).forEach(key => {
                        if (key.includes('location')) {
                            const location = data.filters[key];
                            if (location.includes('downtown')) url.searchParams.set('location', 'Downtown');
                            else if (location.includes('university')) url.searchParams.set('location', 'Near University');
                            else if (location.includes('business')) url.searchParams.set('location', 'Business District');
                        }
                        if (key.includes('room_type')) url.searchParams.set('room_type', data.filters[key]);
                        if (key.includes('price__lte')) url.searchParams.set('price_max', data.filters[key]);
                    });
                    
                    setTimeout(() => window.location.href = url.toString(), 1500);
                }
            });
            
            voiceBtn.style.transform = '';
        };
        
        filterRecognition.onerror = function(event) {
            voiceBtn.style.transform = '';
            showNotification('Voice command failed. Please try again.');
        };
    });
} else if (voiceBtn) {
    voiceBtn.addEventListener('click', function() {
        showNotification('Voice command activated. Say "Show apartments under ₹20,000" or similar.');
    });
}

// Notification helper
function showNotification(message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: var(--light-accent);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1001;
        max-width: 300px;
        font-size: 0.9rem;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Image Upload
const imageUpload = document.querySelector('.image-upload');

if (imageUpload) {
    imageUpload.addEventListener('click', function() {
        const fileInput = this.querySelector('input[type="file"]');
        if (fileInput) {
            fileInput.click();
        }
    });
}

// Profile Dropdown
const profileBtn = document.getElementById('profileBtn');
const profileMenu = document.getElementById('profileMenu');

if (profileBtn && profileMenu) {
    profileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        profileBtn.classList.toggle('active');
        profileMenu.classList.toggle('show');
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!profileBtn.contains(e.target) && !profileMenu.contains(e.target)) {
            profileBtn.classList.remove('active');
            profileMenu.classList.remove('show');
        }
    });
}

// Auto-hide messages
setTimeout(() => {
    const messages = document.querySelector('.messages');
    if (messages) {
        messages.style.opacity = '0';
        setTimeout(() => messages.remove(), 500);
    }
}, 3000);

// SMS Inquiry Helper Function
function sendSMSInquiry(roomId) {
    const message = prompt('Enter your inquiry message:');
    if (message) {
        fetch('/sms-inquiry/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                room_id: roomId,
                message: message
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
            } else {
                alert('Failed to send SMS inquiry.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error sending SMS inquiry.');
        });
    }
}

// CSRF Token helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}