const btnAdicionar = document.getElementById("adicionar");
const modal = document.getElementById("modal");
const fechar = document.querySelector(".fechar");
const cancelar = document.getElementById("cancelar");
const formLocal = document.getElementById("localForm");

let editarId = null; // Para armazenar o ID quando for editar

// Abrir modal para adicionar
btnAdicionar.addEventListener("click", () => {
    editarId = null;
    formLocal.reset();
    modal.style.display = "block";
});

// Fechar modal
fechar.addEventListener("click", () => modal.style.display = "none");
cancelar.addEventListener("click", () => modal.style.display = "none");
window.addEventListener("click", (e) => { if(e.target === modal) modal.style.display = "none"; });

// Função para preencher modal para edição
document.querySelectorAll(".editar").forEach(btn => {
    btn.addEventListener("click", (e) => {
        e.preventDefault();
        editarId = btn.dataset.id;
        const card = btn.closest("li");

        // Preencher formulário
        formLocal.handle.value = card.querySelector('strong').textContent.toLowerCase().replace(/\s/g,'');
        formLocal.nome.value = card.querySelector('strong').textContent;
        formLocal.descricao.value = card.querySelector('#card-descricao').textContent;
        formLocal.dias.value = card.querySelector('#card-dias').textContent.match(/\((.*?)\)/)[1].split('-')[0].trim();
        formLocal.inicio.value = card.querySelector('#card-dias').textContent.match(/\((.*?)\)/)[1].split('-')[0].trim();
        formLocal.fim.value = card.querySelector('#card-dias').textContent.match(/\((.*?)\)/)[1].split('-')[1].trim();
        formLocal.endereco.value = card.querySelector('#card-endereco').textContent;
        formLocal.latitude.value = card.querySelector('#card-local').textContent.split(',')[0].replace('Latitude: ','').trim();
        formLocal.longitude.value = card.querySelector('#card-local').textContent.split(',')[1].replace('Longitude: ','').trim();

        // Resetar checkboxes
        formLocal.querySelectorAll('input[name="tags"]').forEach(t => t.checked = false);
        const tagsText = card.querySelector('#card-tags').textContent.replace('Tags:','').split(',').map(t => t.trim());
        formLocal.querySelectorAll('input[name="tags"]').forEach(t => {
            if(tagsText.includes(t.nextSibling.textContent.trim())) t.checked = true;
        });

        modal.style.display = "block";
    });
});

// Submeter formulário (adicionar ou editar)
formLocal.addEventListener("submit", async (e) => {
    e.preventDefault();

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

    let url = "/locais";
    let method = "POST";

    if(editarId){
        url = `/locais/${editarId}`;
        method = "PUT";
    }

    try {
        const response = await fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados),
        });

        const json = await response.json();
        if (json.success) location.reload();
        else alert("Erro: " + json.error);

    } catch (error) {
        console.error("Erro na requisição:", error);
        alert("Erro ao salvar local.");
    }

    formLocal.reset();
    modal.style.display = "none";
});

// Excluir local
document.querySelectorAll(".excluir").forEach(btn => {
    btn.addEventListener("click", async (e) => {
        e.preventDefault();
        if(!confirm("Tem certeza que deseja excluir este local?")) return;

        const localId = btn.closest("li").querySelector(".editar").dataset.id;

        try {
            const response = await fetch(`/locais/${localId}`, { method: "DELETE" });
            const json = await response.json();
            if(json.success) location.reload();
            else alert("Erro: " + json.error);
        } catch (error) {
            console.error("Erro ao excluir:", error);
            alert("Erro ao excluir local.");
        }
    });
});
