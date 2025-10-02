const btnAdicionar = document.getElementById("adicionar");
const modal = document.getElementById("modal");
const fechar = document.querySelector(".fechar");
const cancelar = document.getElementById("cancelar");
const formLocal = document.getElementById("localForm");

btnAdicionar.addEventListener("click", () => modal.style.display = "block");
fechar.addEventListener("click", () => modal.style.display = "none");
cancelar.addEventListener("click", () => modal.style.display = "none");
window.addEventListener("click", (e) => { if(e.target === modal) modal.style.display = "none"; });

formLocal.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Pega todas as tags selecionadas
    const selectedTags = Array.from(formLocal.querySelectorAll('input[name="tags"]:checked')).map(el => parseInt(el.value));

    const dados = {
        handle: formLocal.handle.value,
        nome: formLocal.nome.value,
        descricao: formLocal.descricao.value,
        dias: formLocal.dias.value,
        inicio: formLocal.inicio.value,
        fim: formLocal.fim.value,
        endereco: formLocal.endereco.value,
        latitude: parseFloat(formLocal.latitude.value),
        longitude: parseFloat(formLocal.longitude.value),
        urlimage: formLocal.urlimage.value,
        urlicone: formLocal.urlicone.value,
        tags: selectedTags
    };

    try {
        const response = await fetch("/locais", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados),
        });

        const json = await response.json();
        if (json.success) location.reload();
        else alert("Erro: " + json.error);

    } catch (error) {
        console.error("Erro na requisição:", error);
        alert("Erro ao cadastrar local.");
    }

    formLocal.reset();
    modal.style.display = "none";
});
