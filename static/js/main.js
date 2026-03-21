/* ============================================================
   Eccentric Academy – Main JS
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

    // ---- NAVBAR SCROLL EFFECT ----
    const navbar = document.querySelector('.ea-navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar?.classList.add('scrolled');
        } else {
            navbar?.classList.remove('scrolled');
        }
    });

    // ---- COUNTDOWN TIMER ----
    const countdownEl = document.getElementById('ea-countdown');
    if (countdownEl) {
        const targetDate = new Date();
        targetDate.setHours(targetDate.getHours() + 47, targetDate.getMinutes() + 23, 0, 0);

        function updateCountdown() {
            const now = new Date();
            const diff = targetDate - now;

            if (diff <= 0) {
                countdownEl.innerHTML = '<span class="text-accent">Offer Expired</span>';
                return;
            }

            const hours = Math.floor(diff / (1000 * 60 * 60));
            const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((diff % (1000 * 60)) / 1000);

            document.getElementById('cd-hours').textContent = String(hours).padStart(2, '0');
            document.getElementById('cd-minutes').textContent = String(minutes).padStart(2, '0');
            document.getElementById('cd-seconds').textContent = String(seconds).padStart(2, '0');
        }

        updateCountdown();
        setInterval(updateCountdown, 1000);
    }

    // ---- AJAX CONTACT FORM ----
    const contactForm = document.getElementById('ea-contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            const btn = contactForm.querySelector('[type="submit"]');
            const originalText = btn.innerHTML;
            const feedback = document.getElementById('contact-feedback');

            btn.disabled = true;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Sending...';

            try {
                const formData = new FormData(contactForm);
                const response = await fetch(contactForm.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    }
                });

                const data = await response.json();

                if (data.success) {
                    feedback.className = 'alert alert-success mt-3';
                    feedback.innerHTML = `<i class="bi bi-check-circle-fill me-2"></i>${data.message}`;
                    feedback.style.display = 'block';
                    contactForm.reset();
                } else {
                    feedback.className = 'alert alert-danger mt-3';
                    const errorMessages = Object.values(data.errors || {}).flat().join(' ');
                    feedback.innerHTML = `<i class="bi bi-exclamation-triangle-fill me-2"></i>${errorMessages || 'Please fix the errors and try again.'}`;
                    feedback.style.display = 'block';
                }
            } catch (err) {
                feedback.className = 'alert alert-danger mt-3';
                feedback.innerHTML = '<i class="bi bi-exclamation-triangle-fill me-2"></i>Network error. Please try again.';
                feedback.style.display = 'block';
            } finally {
                btn.disabled = false;
                btn.innerHTML = originalText;

                // Scroll to feedback
                feedback.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        });
    }

    // ---- ANIMATE ON SCROLL ----
    const animElements = document.querySelectorAll('[data-animate]');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    animElements.forEach(el => observer.observe(el));

    // ---- SMOOTH SCROLL FOR ANCHOR LINKS ----
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // ---- TERMINAL TYPING EFFECT ----
    const terminal = document.getElementById('ea-terminal');
    if (terminal) {
        const lines = [
            { text: '$ nmap -sV 192.168.1.0/24', type: 'cmd', delay: 500 },
            { text: 'Starting Nmap 7.94...', type: 'output', delay: 800 },
            { text: '443/tcp  open  https   nginx', type: 'success', delay: 400 },
            { text: '$ sqlmap -u "https://target.ng/login"', type: 'cmd', delay: 600 },
            { text: '[INFO] testing connection to target', type: 'output', delay: 300 },
            { text: '[CRITICAL] SQL injection found!', type: 'error', delay: 400 },
            { text: '$ burpsuite --headless --config=api', type: 'cmd', delay: 700 },
            { text: '[+] Intercepting requests...', type: 'success', delay: 300 },
        ];

        let lineIndex = 0;
        const typingContainer = terminal.querySelector('.ea-terminal-body');

        function addLine() {
            if (lineIndex >= lines.length) return;

            const line = lines[lineIndex];
            const el = document.createElement('div');
            el.className = `ea-terminal-${line.type}`;
            el.textContent = line.text;
            el.style.opacity = '0';
            typingContainer.appendChild(el);

            requestAnimationFrame(() => {
                el.style.transition = 'opacity 0.3s ease';
                el.style.opacity = '1';
            });

            lineIndex++;
            if (lineIndex < lines.length) {
                setTimeout(addLine, lines[lineIndex].delay);
            }
        }

        setTimeout(addLine, 1000);
    }
});
