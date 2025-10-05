const btnAdicionar = document.getElementById("adicionar");
const modal = document.getElementById("modal");
const fechar = document.querySelector(".fechar");
const cancelar = document.getElementById("cancelar");
const formAtracao = document.getElementById("atracaoForm");
let editando = false;
let atracaoEditId = null;

// Abrir modal de adicionar
btnAdicionar.addEventListener("click", () => {
  editando = false;
  formAtracao.reset();
  document.getElementById("salvar").textContent = "Salvar";
  modal.style.display = "block";
});

// Fechar modal
fechar.addEventListener("click", () => modal.style.display = "none");
cancelar.addEventListener("click", () => modal.style.display = "none");
window.addEventListener("click", (e) => { if (e.target === modal) modal.style.display = "none"; });

// Envio do formulário (POST ou PUT)
formAtracao.addEventListener("submit", async (e) => {
  e.preventDefault();

  const selectedTags = Array.from(formAtracao.querySelectorAll('input[name="tags"]:checked'))
                            .map(el => parseInt(el.value));

  const dados = {
    handle: formAtracao.handle.value,
    nome: formAtracao.nome.value,
    ordem: parseInt(formAtracao.ordem.value),
    fk: formAtracao.fk.value ? parseInt(formAtracao.fk.value) : null,
    descricao: formAtracao.descricao.value,
    urlimagem: formAtracao.urlimagem.value,
    principal: formAtracao.principal.checked,
    tags: selectedTags
  };

  const url = editando ? `/atracao/${atracaoEditId}` : "/atracao";
  const metodo = editando ? "PUT" : "POST";

  try {
    const response = await fetch(url, {
      method: metodo,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    });

    const json = await response.json();
    if (json.success) location.reload();
    else alert("Erro: " + json.error);

  } catch (error) {
    console.error("Erro na requisição:", error);
    alert("Erro ao salvar atração.");
  }

  formAtracao.reset();
  modal.style.display = "none";
});

// ---- Função para editar ----
document.querySelectorAll(".editar").forEach(botao => {
  botao.addEventListener("click", () => {
    editando = true;
    atracaoEditId = botao.dataset.id;
    document.getElementById("salvar").textContent = "Atualizar";

    formAtracao.handle.value = botao.dataset.handle;
    formAtracao.nome.value = botao.dataset.nome;
    formAtracao.ordem.value = botao.dataset.ordem;
    formAtracao.descricao.value = botao.dataset.descricao;
    formAtracao.urlimagem.value = botao.dataset.urlimagem;
    formAtracao.principal.checked = botao.dataset.principal === "true";
    formAtracao.fk.value = botao.dataset.fk;

    modal.style.display = "block";
  });
});
