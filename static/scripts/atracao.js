const btnAdicionar = document.getElementById("adicionar");
const modal = document.getElementById("modal");
const fechar = document.querySelector(".fechar");
const cancelar = document.getElementById("cancelar");
const formAtracao = document.getElementById("atracaoForm");

// Abrir modal
btnAdicionar.addEventListener("click", () => {
  modal.style.display = "block";
});

// Fechar modal
fechar.addEventListener("click", () => modal.style.display = "none");
cancelar.addEventListener("click", () => modal.style.display = "none");
window.addEventListener("click", (e) => { if(e.target === modal) modal.style.display = "none"; });

// Envio do formulário
formAtracao.addEventListener("submit", async (e) => {
  e.preventDefault();

  // Pega todas as tags selecionadas (checkboxes)
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

  try {
    const response = await fetch("/atracao", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    });

    const json = await response.json();
    if (json.success) location.reload();
    else alert("Erro: " + json.error);

  } catch (error) {
    console.error("Erro na requisição:", error);
    alert("Erro ao cadastrar atração.");
  }

  formAtracao.reset();
  modal.style.display = "none";
});
