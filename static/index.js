
let currentIndex = 0;
const cards = document.querySelectorAll(".team-card");
const totalCards = cards.length;
const visibleCards = 3; // nechta ko‘rinadi
const cardWidth = 300; // (280px + margin)

function moveSlide(direction) {
  currentIndex += direction;
  if (currentIndex < 0) currentIndex = 0;
  if (currentIndex > totalCards - visibleCards) {
    currentIndex = totalCards - visibleCards;
  }
  const offset = -(cardWidth * currentIndex);
  document.getElementById("teamCards").style.transform = `translateX(${offset}px)`;
}



  window.moveSlide = function(direction) {
  currentIndex += direction;

  // Infinite loop qilish
  if (currentIndex < 0) {
    currentIndex = totalCards - visibleCards; // oxirga qaytadi
  }
  if (currentIndex > totalCards - visibleCards) {
    currentIndex = 0; // boshiga qaytadi
  }

  const offset = -(cardWidth * currentIndex);
  document.getElementById("teamCards").style.transform = `translateX(${offset}px)`;
}

  document.addEventListener("DOMContentLoaded", function() {
  let currentIndex = 0;
  const cards = document.querySelectorAll(".team-card");
  const totalCards = cards.length;
  const visibleCards = 3; // nechta ko‘rinadi
  const cardWidth = 280 + 20; // width + margin

  window.moveSlide = function(direction) {
    currentIndex += direction;
    if (currentIndex < 0) currentIndex = 0;
    if (currentIndex > totalCards - visibleCards) {
      currentIndex = totalCards - visibleCards;
    }
    const offset = -(cardWidth * currentIndex);
    document.getElementById("teamCards").style.transform = `translateX(${offset}px)`;
  }
});
  const menuToggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('nav ul');
  
  menuToggle.addEventListener('click', function() {
    nav.classList.toggle('active');
    this.classList.toggle('active');
  });
  // Wait for DOM to be fully loaded
 
    // ===== Utility: Typewriter for plain text or HTML (keeps tags like <br>)
    function typeHTML(el, html, speed = 28) {
      // Split by tags to preserve <br> and entities
      const parts = html
        .replace(/\n/g, '<br>')
        .match(/<[^>]+>|[^<]+/g) || [];
      let out = '';
      let i = 0;

      return new Promise(resolve => {
        function step(){
          if(i >= parts.length){ el.innerHTML = out; el.classList.remove('caret'); return resolve(); }
          const chunk = parts[i++];
          if(/<[^>]+>/.test(chunk)){
            out += chunk; // write tags immediately
          } else {
            // type characters from this text chunk
            const chars = [...chunk];
            let j = 0;
            const write = () => {
              out += chars[j++]; el.innerHTML = out;
              if(j < chars.length) setTimeout(write, speed);
              else setTimeout(step, speed);
            };
            return write();
          }
          setTimeout(step, speed);
        }
        el.classList.add('caret');
        step();
      });
    }
      const slider = document.getElementById("teamSlider");
    const members = document.querySelectorAll(".team-member");
    let index = 0;
    const perPage = 3;

    function showMember() {
      slider.style.transform = `translateX(${-index * (100 / perPage)}%)`;
    }

    function nextMember() {
      if (index < members.length - perPage) {
        index++;
        showMember();
      }
    }

    function prevMember() {
      if (index > 0) {
        index--;
        showMember();
      }
    }
    const RUN_KEY = 'mmp-once-loader';

    window.addEventListener('load', async () => {
      const loader = document.getElementById('loader');
      const robot  = document.getElementById('robot');
      const title  = document.getElementById('title');
      const subtitle = document.getElementById('subtitle');
      const flyover = document.getElementById('flyover');

      // Simulate small delay for loader aesthetic (optional)
      await new Promise(r => setTimeout(r, 900));

      // Hide loader
      loader.classList.add('hidden');

      // Start one-time animations
      const firstTime = !sessionStorage.getItem(RUN_KEY);
      sessionStorage.setItem(RUN_KEY, '1');

      // Robot fade-in after a short delay
      setTimeout(() => robot.classList.add('show'), 300);

      // Typing title then subtitle
      await typeHTML(title, title.dataset.text, 26);
      await new Promise(r => setTimeout(r, 120));
      await typeHTML(subtitle, subtitle.dataset.text, 14);

      // Rocket flyover + tagline (run once per tab open)
      if(firstTime){
        setTimeout(() => flyover.classList.add('run'), 200);
      }
    });

    window.addEventListener("load", function() {
  document.querySelector(".loader-overlay").classList.add("hidden");
});