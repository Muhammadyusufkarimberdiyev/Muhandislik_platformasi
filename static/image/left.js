// Modalni ochish
function openModal(id) {
    document.getElementById(id).style.display = "block";
}

// Tugmalarni ulash
document.getElementById("schemaBtn").addEventListener("click", () => openModal("schemaModal"));
document.getElementById("codeBtn").addEventListener("click", () => openModal("codeModal"));
document.getElementById("componentsBtn").addEventListener("click", () => openModal("componentsModal"));
document.getElementById("infoFloatingBtn").addEventListener("click", () => openModal("infoModal"));

// Yopish tugmalari
document.querySelectorAll(".close").forEach(btn => {
    btn.addEventListener("click", function() {
        this.closest(".modal").style.display = "none";
    });
});

// Tab switching (Kod uchun)
document.querySelectorAll(".tab-btn").forEach(button => {
    button.addEventListener("click", function() {
        const tab = this.dataset.tab;
        document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));
        this.classList.add("active");
        document.querySelectorAll(".tab-content").forEach(content => {
            content.classList.remove("active");
            if (content.id === tab) content.classList.add("active");
        });
    });
});