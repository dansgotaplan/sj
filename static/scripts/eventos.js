const btnAdicionar = document.getElementById("adicionar");
const modal = document.getElementById("modal");
const fechar = document.querySelector(".fechar");
const cancelar = document.getElementById("cancelar");
const formEvento = document.getElementById("eventoForm");
let editingId = null; // Id do evento que está sendo editado

// Abrir modal Adicionar
btnAdicionar.addEventListener("click", () => {
    editingId = null;
    formEvento.reset();
    modal.style.display = "block";
});

// Fechar modal
fechar.addEventListener("click", () => modal.style.display = "none");
cancelar.addEventListener("click", () => modal.style.display = "none");
window.addEventListener("click", (e) => { if (e.target === modal) modal.style.display = "none"; });

// Função enviar POST/PUT
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

    let url = "/eventos";
    let method = "POST";

    if (editingId) {  // Se estiver editando
        url = `/eventos/${editingId}`;
        method = "PUT";
    }

    fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            alert(editingId ? "Evento atualizado com sucesso!" : "Evento cadastrado com sucesso!");
            window.location.reload();
        } else {
            alert("Erro: " + result.error);
        }
    })
    .catch(error => console.error("Erro:", error));
});

// Botões Editar
document.querySelectorAll(".editar").forEach(btn => {
    btn.addEventListener("click", () => {
        const code = btn.dataset.code;
        editingId = code;

        // Preenche modal com os dados do evento
        const li = btn.closest("li");
        formEvento.handle.value = li.querySelector("#card-topo").textContent; // Ajustar se handle for diferente do nome
        formEvento.nome.value = li.querySelector("#card-topo").textContent;
        formEvento.descricao.value = li.querySelector("#card-descricao").textContent;
        formEvento.inicio.value = li.querySelector("#card-datas").dataset.inicio;
        formEvento.fim.value = li.querySelector("#card-datas").dataset.fim;
        formEvento.horario.value = li.querySelector("#card-datas").dataset.horario;
        formEvento.endereco.value = li.querySelector("#card-local").textContent;
        formEvento.latitude.value = li.querySelector("#card-coords").dataset.lat;
        formEvento.longitude.value = li.querySelector("#card-coords").dataset.lng;
        formEvento.urlimagem.value = li.querySelector("img").src;

        modal.style.display = "block";
    });
});
