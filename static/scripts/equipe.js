const btnAdicionar = document.getElementById("adicionar");
const modal = document.getElementById("modal");
const fechar = document.querySelector(".fechar");
const cancelar = document.getElementById("cancelar");
const formEquipe = document.getElementById("equipeForm");

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

// Se você quiser enviar via Flask normalmente, não use preventDefault
formEquipe.addEventListener("submit", (e) => {
  // e.preventDefault(); // comente para enviar normal

  const dados = {
    nome: formEquipe.nome.value,
    turma: formEquipe.turma.value,
    email: formEquipe.email.value,
    funcao: formEquipe.funcao.value,
    ano: formEquipe.ano.value,
    urlimagem: formEquipe.urlimagem.value,
  };

  console.log("Equipe cadastrada:", dados);
  // formEquipe.reset();
  // modal.style.display = "none";
});
