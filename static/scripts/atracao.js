const btnAdicionar = document.getElementById("adicionar");
const modal = document.getElementById("modal");
const fechar = document.querySelector(".fechar");
const cancelar = document.getElementById("cancelar");
const formEvento = document.getElementById("atracaoForm");

// Abrir modal
btnAdicionar.addEventListener("click", () => {
  modal.style.display = "block";
});

// Fechar modal clicando no X
fechar.addEventListener("click", () => {
  modal.style.display = "none";
});

// Fechar modal clicando em cancelar
cancelar.addEventListener("click", () => {
  modal.style.display = "none";
});

// Fechar modal clicando fora
window.addEventListener("click", (e) => {
  if (e.target === modal) modal.style.display = "none";
});

// Envio do formulário
formEvento.addEventListener("submit", async (e) => {
  e.preventDefault();

  const dados = {
    handle: formEvento.handle.value,
    nome: formEvento.nome.value,
    ordem: parseInt(formEvento.ordem.value),
    fk: parseInt(formEvento.fk.value),
    descricao: formEvento.descricao.value,
    urlimagem: formEvento.urlimagem.value,
    principal: formEvento.principal.checked,
  };

  try {
    const response = await fetch("/atracao", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    });

    const json = await response.json();
    if (json.success) {
      location.reload();
    } else {
      alert("Erro: " + json.error);
    }
  } catch (error) {
    console.error("Erro na requisição:", error);
    alert("Erro ao cadastrar atração.");
  }

  formEvento.reset();
  modal.style.display = "none";
});
