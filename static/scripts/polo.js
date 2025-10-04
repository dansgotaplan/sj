const btnAdicionar = document.getElementById("adicionar");
const modal = document.getElementById("modal");
const fechar = document.querySelector(".fechar");
const cancelar = document.getElementById("cancelar");
const formPolo = document.getElementById("poloForm");
const modalTitulo = document.getElementById("modalTitulo");

let modoEdicao = false;
let poloEditandoId = null;

// função pra trocar o título com animação suave
function alterarTituloModal(texto) {
  modalTitulo.style.opacity = 0;
  setTimeout(() => {
    modalTitulo.textContent = texto;
    modalTitulo.style.opacity = 1;
  }, 200);
}

// abrir modal (adicionar)
btnAdicionar.addEventListener("click", () => {
  modoEdicao = false;
  poloEditandoId = null;
  formPolo.reset();
  alterarTituloModal("Adicionar Polo");
  modal.style.display = "block";
});

// fechar modal
fechar.addEventListener("click", () => (modal.style.display = "none"));
cancelar.addEventListener("click", () => (modal.style.display = "none"));
window.addEventListener("click", (e) => {
  if (e.target === modal) modal.style.display = "none";
});

// enviar formulário
formPolo.addEventListener("submit", async (e) => {
  e.preventDefault();

  const dados = {
    handle: formPolo.handle.value,
    nome: formPolo.nome.value,
    descricao: formPolo.descricao.value,
    inicio: formPolo.inicio.value,
    fim: formPolo.fim.value,
    endereco: formPolo.endereco.value,
    latitude: formPolo.latitude.value,
    longitude: formPolo.longitude.value,
    urlimagem: formPolo.urlimagem.value,
    ismultilocal: formPolo.ismultilocal.checked,
  };

  const url = modoEdicao ? `/polo/${poloEditandoId}` : "/polo";
  const method = modoEdicao ? "PUT" : "POST";

  try {
    const resposta = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    });

    const resultado = await resposta.json();
    if (resultado.success) {
      alert(modoEdicao ? "Polo atualizado!" : "Polo cadastrado com sucesso!");
      location.reload();
    } else {
      alert("Erro: " + resultado.error);
    }
  } catch (err) {
    console.error("Erro:", err);
  }

  modal.style.display = "none";
});

// abrir modal em modo editar
document.querySelectorAll(".editar").forEach((btn) => {
  btn.addEventListener("click", (e) => {
    const card = e.target.closest(".card-polo");

    modoEdicao = true;
    poloEditandoId = card.dataset.code;

    formPolo.handle.value = card.dataset.handle;
    formPolo.nome.value = card.dataset.nome;
    formPolo.descricao.value = card.dataset.descricao;
    formPolo.inicio.value = card.dataset.inicio;
    formPolo.fim.value = card.dataset.fim;
    formPolo.endereco.value = card.dataset.endereco;
    formPolo.latitude.value = card.dataset.latitude;
    formPolo.longitude.value = card.dataset.longitude;
    formPolo.urlimagem.value = card.dataset.urlimagem;
    formPolo.ismultilocal.checked = card.dataset.ismultilocal === "True";

    alterarTituloModal("Editar Polo");
    modal.style.display = "block";
  });
});
