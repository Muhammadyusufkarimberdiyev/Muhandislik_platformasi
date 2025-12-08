
        // =========================
        // TOUCH GESTURES (TEAM SLIDER)
        // =========================
        let startX = 0;
        let isDragging = false;

        const teamSlider = document.querySelector('.team-slider');

        teamSlider.addEventListener('touchstart', function(e) {
            startX = e.touches[0].clientX;
            isDragging = true;
        });

        teamSlider.addEventListener('touchend', function(e) {
            if (!isDragging) return;
            
            const endX = e.changedTouches[0].clientX;
            const diffX = startX - endX;
            
            if (Math.abs(diffX) > 50) { // 50px dan ko'p siljiganda
                if (diffX > 0) {
                    moveSlide(1); // o'ngga
                } else {
                    moveSlide(-1); // chapga
                }
            }
            
            isDragging = false;
        });

        // =========================
        // AUTO-PLAY TEAM SLIDER
        // =========================
        function autoSlide() {
            const totalCards = document.getElementById("teamCards").children.length;
            const visibleCards = getVisibleCards();
            
            if (currentIndex >= totalCards - visibleCards) {
                currentIndex = -1;
            }
            moveSlide(1);
        }

        // Auto-play har 4 soniyada (ixtiyoriy)
        // setInterval(autoSlide, 4000);

        // =========================
        // LOADING ANIMATION
        // =========================
        window.addEventListener('load', function() {
            document.body.style.opacity = '0';
            document.body.style.transition = 'opacity 0.5s ease';
            
            setTimeout(() => {
                document.body.style.opacity = '1';
            }, 100);
        });

        // =========================
        // PERFORMANCE OPTIMIZATION
        // =========================
        // Debounce function for resize events
        function debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }

        // Optimized resize handler
        const optimizedResize = debounce(function() {
            toggleSearch();
            currentIndex = 0;
            const cards = document.getElementById("teamCards");
            cards.style.transform = 'translateX(0px)';
        }, 250);

        window.addEventListener('resize', optimizedResize);
 (function() {
            let currentIndex = 0;
            let isDragging = false;
            let startPos = 0;
            let currentTranslate = 0;
            let prevTranslate = 0;
            let animationID = 0;

            const cardsContainer = document.getElementById('teamCards');
            const prevBtn = document.getElementById('prevBtn');
            const nextBtn = document.getElementById('nextBtn');

            // Ko'rinadigan kartalar soni
            function getVisibleCards() {
                const width = window.innerWidth;
                if (width <= 768) return 1;
                if (width <= 1200) return 2;
                return 3;
            }

            // Card width + gap
            function getSlideWidth() {
                const width = window.innerWidth;
                const cards = cardsContainer.children;
                
                if (cards.length === 0) return 0;
                
                if (width <= 768) {
                    // Mobile: 100% width
                    return cardsContainer.parentElement.offsetWidth;
                } else {
                    // Desktop/Tablet: card width + gap
                    const card = cards[0];
                    const cardWidth = card.offsetWidth;
                    const computedStyle = window.getComputedStyle(cardsContainer);
                    const gap = parseFloat(computedStyle.gap) || 0;
                    return cardWidth + gap;
                }
            }

            // Progress dots yaratish
            function createDots() {
                const dotsContainer = document.getElementById('sliderDots');
                const totalCards = cardsContainer.children.length;
                const visibleCards = getVisibleCards();
                const totalSlides = Math.ceil(totalCards / visibleCards);
                
                dotsContainer.innerHTML = '';
                
                for (let i = 0; i < totalSlides; i++) {
                    const dot = document.createElement('div');
                    dot.className = 'dot';
                    if (i === 0) dot.classList.add('active');
                    dot.onclick = () => goToSlide(i);
                    dotsContainer.appendChild(dot);
                }
            }

            // Dots yangilash
            function updateDots() {
                const dots = document.querySelectorAll('.dot');
                const visibleCards = getVisibleCards();
                const currentSlide = Math.floor(currentIndex / visibleCards);
                
                dots.forEach((dot, index) => {
                    dot.classList.toggle('active', index === currentSlide);
                });
            }

            // Button holatini yangilash
            function updateButtons() {
                const totalCards = cardsContainer.children.length;
                const visibleCards = getVisibleCards();
                const maxIndex = totalCards - visibleCards;
                
                prevBtn.classList.toggle('disabled', currentIndex <= 0);
                nextBtn.classList.toggle('disabled', currentIndex >= maxIndex);
            }

            // Slider harakati
            function setSliderPosition() {
                const slideWidth = getSlideWidth();
                const offset = -(currentIndex * slideWidth);
                cardsContainer.style.transform = `translateX(${offset}px)`;
                updateButtons();
                updateDots();
            }

            // Slide ko'chirish
            window.moveSlide = function(direction) {
                const totalCards = cardsContainer.children.length;
                const visibleCards = getVisibleCards();
                const maxIndex = totalCards - visibleCards;
                
                const newIndex = currentIndex + direction;
                
                if (newIndex < 0 || newIndex > maxIndex) {
                    return;
                }
                
                currentIndex = newIndex;
                setSliderPosition();
            };

            // Ma'lum slide'ga o'tish
            function goToSlide(slideIndex) {
                const visibleCards = getVisibleCards();
                currentIndex = slideIndex * visibleCards;
                
                const totalCards = cardsContainer.children.length;
                const maxIndex = totalCards - visibleCards;
                
                if (currentIndex > maxIndex) {
                    currentIndex = maxIndex;
                }
                
                setSliderPosition();
            }

            // Touch/Mouse dragging
            function touchStart(index) {
                return function(event) {
                    isDragging = true;
                    startPos = getPositionX(event);
                    animationID = requestAnimationFrame(animation);
                    cardsContainer.style.cursor = 'grabbing';
                };
            }

            function touchMove(event) {
                if (isDragging) {
                    const currentPosition = getPositionX(event);
                    currentTranslate = prevTranslate + currentPosition - startPos;
                }
            }

            function touchEnd() {
                isDragging = false;
                cancelAnimationFrame(animationID);
                cardsContainer.style.cursor = 'grab';
                
                const movedBy = currentTranslate - prevTranslate;
                
                if (movedBy < -100 && currentIndex < cardsContainer.children.length - getVisibleCards()) {
                    moveSlide(1);
                }
                
                if (movedBy > 100 && currentIndex > 0) {
                    moveSlide(-1);
                }
                
                setSliderPosition();
                currentTranslate = 0;
                prevTranslate = 0;
            }

            function getPositionX(event) {
                return event.type.includes('mouse') ? event.pageX : event.touches[0].clientX;
            }

            function animation() {
                if (isDragging) requestAnimationFrame(animation);
            }

            // Event listeners
            cardsContainer.addEventListener('mousedown', touchStart(0));
            cardsContainer.addEventListener('mousemove', touchMove);
            cardsContainer.addEventListener('mouseup', touchEnd);
            cardsContainer.addEventListener('mouseleave', touchEnd);

            cardsContainer.addEventListener('touchstart', touchStart(0), { passive: true });
            cardsContainer.addEventListener('touchmove', touchMove, { passive: true });
            cardsContainer.addEventListener('touchend', touchEnd);

            // Keyboard navigation
            document.addEventListener('keydown', function(e) {
                if (e.key === 'ArrowLeft') moveSlide(-1);
                if (e.key === 'ArrowRight') moveSlide(1);
            });

            // Resize handler
            let resizeTimeout;
            window.addEventListener('resize', function() {
                clearTimeout(resizeTimeout);
                resizeTimeout = setTimeout(function() {
                    currentIndex = 0;
                    createDots();
                    setSliderPosition();
                }, 250);
            });

            // Initialize
            window.addEventListener('load', function() {
                createDots();
                setSliderPosition();
                console.log('✅ Mukammal Team Slider tayyor!');
            });

            // Auto-play (ixtiyoriy)
            setInterval(() => {
                const totalCards = cardsContainer.children.length;
                const visibleCards = getVisibleCards();
                if (currentIndex >= totalCards - visibleCards) {
                    currentIndex = 0;
                } else {
                    moveSlide(1);
                }
            }, 5000);

        })();