const btnAdicionar = document.getElementById("adicionar");
const modal = document.getElementById("modal");
const fechar = document.querySelector(".fechar");
const cancelar = document.getElementById("cancelar");
const formEvento = document.getElementById("atracaoForm");

btnAdicionar.addEventListener("click", () => {
  modal.style.display = "block";
});

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


formEvento.addEventListener("submit", (e) => {
  e.preventDefault();


  const dados = {
    handle: formEvento.handle.value,
    nome: formEvento.nome.value,
  };

  console.log("Evento cadastrado:", dados);

  formEvento.reset();
  modal.style.display = "none";
});