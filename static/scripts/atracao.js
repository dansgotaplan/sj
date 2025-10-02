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
  if (e.target === modal) {
    modal.style.display = "none";
  }
});

// Envio do formulário
formEvento.addEventListener("submit", async (e) => {
  e.preventDefault(); // impede envio normal do form

  // Pega os dados do formulário
  const dados = {
    handle: formEvento.handle.value,
    nome: formEvento.nome.value,
    ordem: formEvento.ordem.value,
    fk: formEvento.fk.value,
    descricao: formEvento.descricao.value,
    urlimagem: formEvento.urlimagem.value,
    principal: formEvento.principal.checked,
  };

  try {
    // Envia os dados via POST para o Flask
    const response = await fetch("/atracao", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    });

    if (response.ok) {
      location.reload(); // recarrega a página para mostrar a nova atração
    } else {
      console.error("Erro ao salvar atração");
    }
  } catch (error) {
    console.error("Erro na requisição:", error);
  }

  // Limpa o formulário e fecha o modal
  formEvento.reset();
  modal.style.display = "none";
});
