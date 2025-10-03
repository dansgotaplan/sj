const btnAdicionar = document.getElementById("adicionar");
const modal = document.getElementById("modal");
const fechar = document.querySelector(".fechar");
const cancelar = document.getElementById("cancelar");
const formEvento = document.getElementById("eventoForm");

// Abrir modal
btnAdicionar.addEventListener("click", () => {
    modal.style.display = "block";
});

// Fechar modal
fechar.addEventListener("click", () => {
    modal.style.display = "none";
});

cancelar.addEventListener("click", () => {
    modal.style.display = "none";
});

// Fechar modal clicando fora
window.addEventListener("click", (e) => {
    if (e.target === modal) {
        modal.style.display = "none";
    }
});

// 🚨 Captura o submit e envia AJAX
formEvento.addEventListener("submit", function(e) {
    e.preventDefault();

    const dados = {
        handle: formEvento.handle.value,
        nome: formEvento.nome.value,
        descricao: formEvento.descricao.value,
        inicio: formEvento.inicio.value,
        fim: formEvento.fim.value,
        horario: formEvento.horario.value,
        endereco: formEvento.endereco.value,
        latitude: parseFloat(formEvento.latitude.value),
        longitude: parseFloat(formEvento.longitude.value),
        urlimagem: formEvento.urlimagem.value
    };

    fetch("/eventos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(dados)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            alert("Evento cadastrado com sucesso!");
            window.location.reload();
        } else {
            alert("Erro: " + result.error);
        }
    })
    .catch(error => console.error("Erro:", error));
});
