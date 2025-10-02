const btnAdicionar = document.getElementById("adicionar");
const modal = document.getElementById("modal");
const fechar = document.querySelector(".fechar");
const cancelar = document.getElementById("cancelar");
const formTag = document.getElementById("tagForm");

// abrir modal
btnAdicionar.addEventListener("click", () => {
  modal.style.display = "block";
});

// fechar modal
fechar.addEventListener("click", () => {
  modal.style.display = "none";
});
cancelar.addEventListener("click", () => {
  modal.style.display = "none";
});
window.addEventListener("click", (e) => {
  if (e.target === modal) {
    modal.style.display = "none";
  }
});

// envio do form
formTag.addEventListener("submit", async (e) => {
  e.preventDefault();

  const dados = {
    handle: formTag.handle.value,
    nome: formTag.nome.value,
  };

  try {
    const resposta = await fetch("/tag", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(dados)
    });

    const resultado = await resposta.json();
    if (resultado.success) {
      alert("Tag cadastrada com sucesso!");
      location.reload(); // recarrega a página pra mostrar a nova tag
    } else {
      alert("Erro: " + resultado.error);
    }
  } catch (err) {
    console.error("Erro ao salvar tag:", err);
  }

  formTag.reset();
  modal.style.display = "none";
});
