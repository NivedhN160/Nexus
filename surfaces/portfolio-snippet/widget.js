// Nexus Lead Widget Embed Script
(function() {
    console.log("Nexus Lead Widget init...");

    const widgetId = document.currentScript.getAttribute('data-widget-id');
    const apiUrl = document.currentScript.getAttribute('data-api-url') || 'http://localhost:8000';

    if (!widgetId) {
        console.error("Nexus Widget: No data-widget-id provided.");
        return;
    }

    // Load CSS
    const style = document.createElement('style');
    style.innerHTML = `
        .nexus-widget-btn {
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: #00F0FF;
            color: #0B0F14;
            border: none;
            border-radius: 50%;
            width: 56px;
            height: 56px;
            box-shadow: 0 4px 12px rgba(0, 240, 255, 0.3);
            cursor: pointer;
            z-index: 999999;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.2s;
        }
        .nexus-widget-btn:hover {
            transform: scale(1.05);
        }
        .nexus-widget-btn svg {
            width: 24px;
            height: 24px;
        }
        .nexus-widget-modal {
            display: none;
            position: fixed;
            bottom: 90px;
            right: 24px;
            width: 320px;
            background: #111827;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.5);
            z-index: 999999;
            overflow: hidden;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            color: #fff;
        }
        .nexus-widget-modal.open {
            display: block;
        }
        .nexus-widget-header {
            background: rgba(0, 240, 255, 0.1);
            padding: 16px;
            border-bottom: 1px solid rgba(0, 240, 255, 0.2);
        }
        .nexus-widget-header h3 {
            margin: 0;
            font-size: 16px;
            color: #00F0FF;
        }
        .nexus-widget-body {
            padding: 16px;
        }
        .nexus-widget-form {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .nexus-widget-input {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 6px;
            padding: 8px 12px;
            color: #fff;
            outline: none;
            font-size: 14px;
        }
        .nexus-widget-input:focus {
            border-color: #00F0FF;
        }
        textarea.nexus-widget-input {
            resize: vertical;
            min-height: 80px;
        }
        .nexus-widget-submit {
            background: #00F0FF;
            color: #0B0F14;
            border: none;
            padding: 10px;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 8px;
        }
        .nexus-widget-submit:hover {
            background: #00D0E0;
        }
        .nexus-hp {
            display: none !important;
        }
    `;
    document.head.appendChild(style);

    // Create UI
    const container = document.createElement('div');
    container.innerHTML = `
        <button class="nexus-widget-btn" id="nexus-widget-toggle">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
        </button>
        <div class="nexus-widget-modal" id="nexus-widget-modal">
            <div class="nexus-widget-header">
                <h3>Contact</h3>
            </div>
            <div class="nexus-widget-body">
                <form class="nexus-widget-form" id="nexus-widget-form">
                    <input type="text" class="nexus-widget-input" name="name" placeholder="Name" required>
                    <input type="email" class="nexus-widget-input" name="email" placeholder="Email" required>
                    <textarea class="nexus-widget-input" name="message" placeholder="Message" required></textarea>
                    
                    <!-- Honeypot -->
                    <input type="text" class="nexus-hp" name="honeypot" tabindex="-1" autocomplete="off">
                    
                    <button type="submit" class="nexus-widget-submit">Send Message</button>
                </form>
            </div>
        </div>
    `;
    document.body.appendChild(container);

    // Logic
    const toggleBtn = document.getElementById('nexus-widget-toggle');
    const modal = document.getElementById('nexus-widget-modal');
    const form = document.getElementById('nexus-widget-form');

    toggleBtn.addEventListener('click', () => {
        modal.classList.toggle('open');
    });

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        const btn = form.querySelector('button[type="submit"]');
        btn.textContent = 'Sending...';
        btn.disabled = true;

        fetch(`${apiUrl}/leads/widgets/${widgetId}/submissions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(res => {
            btn.textContent = 'Sent!';
            btn.style.background = '#10B981';
            btn.style.color = 'white';
            setTimeout(() => {
                modal.classList.remove('open');
                form.reset();
                btn.textContent = 'Send Message';
                btn.style.background = '#00F0FF';
                btn.style.color = '#0B0F14';
                btn.disabled = false;
            }, 2000);
        })
        .catch(err => {
            console.error(err);
            btn.textContent = 'Error';
            btn.style.background = '#EF4444';
            btn.style.color = 'white';
            setTimeout(() => {
                btn.textContent = 'Send Message';
                btn.style.background = '#00F0FF';
                btn.style.color = '#0B0F14';
                btn.disabled = false;
            }, 2000);
        });
    });
})();
