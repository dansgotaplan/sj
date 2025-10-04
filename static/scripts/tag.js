const btnAdicionar = document.getElementById("adicionar");
const modal = document.getElementById("modal");
const fechar = document.querySelector(".fechar");
const cancelar = document.getElementById("cancelar");
const formTag = document.getElementById("tagForm");
const tituloModal = document.getElementById("titulo-modal");

let modoEdicao = false;
let tagEditandoId = null;

// abrir modal em modo "adicionar"
btnAdicionar.addEventListener("click", () => {
  modoEdicao = false;
  tagEditandoId = null;
  formTag.reset();
  tituloModal.textContent = "Adicionar Tag";
  modal.style.display = "block";
});

// fechar modal
fechar.addEventListener("click", () => (modal.style.display = "none"));
cancelar.addEventListener("click", () => (modal.style.display = "none"));
window.addEventListener("click", (e) => {
  if (e.target === modal) modal.style.display = "none";
});

// enviar form (adicionar ou editar)
formTag.addEventListener("submit", async (e) => {
  e.preventDefault();

  const dados = {
    handle: formTag.handle.value,
    nome: formTag.nome.value,
  };

  const url = modoEdicao ? `/tag/${tagEditandoId}` : "/tag";
  const method = modoEdicao ? "PUT" : "POST";

  try {
    const resposta = await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(dados),
    });

    const resultado = await resposta.json();
    if (resultado.success) {
      alert(modoEdicao ? "Tag atualizada!" : "Tag cadastrada com sucesso!");
      location.reload();
    } else {
      alert("Erro: " + resultado.error);
    }
  } catch (err) {
    console.error("Erro:", err);
  }

  modal.style.display = "none";
});

// abrir modal em modo "editar"
document.querySelectorAll(".editar").forEach((btn) => {
  btn.addEventListener("click", (e) => {
    const li = e.target.closest("li");
    const code = li.dataset.code;
    const handle = li.dataset.handle;
    const nome = li.dataset.nome;

    modoEdicao = true;
    tagEditandoId = code;
    tituloModal.textContent = "Editar Tag";

    formTag.handle.value = handle;
    formTag.nome.value = nome;

    modal.style.display = "block";
  });
});
