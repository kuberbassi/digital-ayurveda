// This file is in: /static/js/script.js

document.addEventListener('DOMContentLoaded', () => {

    // --- 1. Fade-in on Scroll Animation ---
    const scrollObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.reveal-on-scroll').forEach(el => {
        scrollObserver.observe(el);
    });

    
    // --- 2. Active Nav Dot Scrolling ---
    const sections = document.querySelectorAll('section[id]');
    const navDots = document.querySelectorAll('.scroll-indicator .dot');

    if (navDots.length > 0) {
        const dotObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.getAttribute('id');
                    const activeDot = document.querySelector(`.scroll-indicator a[href="#${id}"]`);
                    navDots.forEach(dot => dot.classList.remove('active'));
                    if (activeDot) { 
                        activeDot.classList.add('active'); 
                    }
                }
            });
        }, { rootMargin: '-50% 0px -50% 0px', threshold: 0 });

        sections.forEach(section => { dotObserver.observe(section); });
    }

    // --- 3. Journal Form (Connects to Backend API) ---
    const journalForm = document.getElementById('journalForm');
    if (journalForm) {
        journalForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const mood = document.getElementById('mood').value;
            const entry = document.getElementById('entry').value;
            try {
                const response = await fetch('/api/journal', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ mood: mood, entry: entry }),
                });
                const result = await response.json();
                if (result.success) {
                    alert('Journal entry saved to database!');
                    journalForm.reset();
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                console.error('Failed to send entry:', error);
                alert('Error connecting to the server.');
            }
        });
    }

    
    // --- 4. Hero Mouse-Move Parallax ---
    const hero = document.querySelector('.hero-section');
    const parallaxElements = document.querySelectorAll('[data-parallax]');

    if (hero) {
        hero.addEventListener('mousemove', (e) => {
            const x = (e.clientX - window.innerWidth / 2) / window.innerWidth;
            const y = (e.clientY - window.innerHeight / 2) / window.innerHeight;
            parallaxElements.forEach(el => {
                const strength = el.dataset.parallaxStrength || 20;
                el.style.transform = `translate(${x * strength}px, ${y * strength}px)`;
            });
        });
    }
    
    // --- 5. 3D Card Tilt ---
    document.querySelectorAll('.tilt-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            const rotateX = (y / (rect.height / 2)) * -5;
            const rotateY = (x / (rect.width / 2)) * 10;
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(1)';
        });
    });

    // --- NEW: 6. Click Ripple Effect ---
    document.addEventListener('click', (e) => {
        // Create the ripple element
        const ripple = document.createElement('span');
        ripple.classList.add('click-ripple');
        
        // Set position to the cursor's location
        // We use clientX/Y for viewport-relative positioning
        ripple.style.left = e.clientX + 'px';
        ripple.style.top = e.clientY + 'px';
        
        // Center the ripple on the cursor
        ripple.style.marginLeft = '-25px'; // Half of the 50px width
        ripple.style.marginTop = '-25px'; // Half of the 50px height
        
        document.body.appendChild(ripple);
        
        // Remove the ripple after the animation finishes
        setTimeout(() => {
            ripple.remove();
        }, 600); // Must match the animation-duration in CSS
    });

});