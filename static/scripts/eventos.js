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

// Capturar submissão do formulário
formEvento.addEventListener("submit", (e) => {
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
.then(res => res.json())
.then(response => {
    if (response.success) {
        console.log("Evento cadastrado com sucesso!");
        // recarrega a página pra mostrar o novo evento
        window.location.reload();
    } else {
        console.error("Erro ao cadastrar evento:", response.error);
        alert("Erro: " + response.error);
    }
})
.catch(err => console.error("Erro de rede:", err));

formEvento.reset();
modal.style.display = "none";

});
