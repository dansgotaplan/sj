const btnAdicionar = document.getElementById("adicionar");
const modal = document.getElementById("modal");
const fechar = document.querySelector(".fechar");
const cancelar = document.getElementById("cancelar");
const formEquipe = document.getElementById("equipeForm");
let editarCode = null;

// abrir modal para adicionar
btnAdicionar.addEventListener("click", () => {
  editarCode = null;
  formEquipe.reset();
  modal.style.display = "block";
});

// fechar modal
fechar.addEventListener("click", () => modal.style.display = "none");
cancelar.addEventListener("click", () => modal.style.display = "none");
window.addEventListener("click", (e) => { if(e.target === modal) modal.style.display = "none"; });

// abrir modal para editar
document.querySelectorAll(".editar").forEach(btn => {
  btn.addEventListener("click", () => {
    const code = btn.dataset.code;
    editarCode = code;

    // pegar dados do card
    const card = btn.closest("#card-equipe");
    formEquipe.nome.value = card.querySelector("strong").innerText;
    formEquipe.turma.value = card.querySelector("#card-turma").innerText.replace('Turma: ', '');
    formEquipe.email.value = card.querySelector("#card-email").innerText.replace('E-mail: ', '');
    formEquipe.funcao.value = card.querySelector("#card-funcao").innerText.replace('Função: ', '');
    formEquipe.ano.value = card.querySelector("#card-ano").innerText;
    formEquipe.urlimagem.value = card.querySelector("#card-imagem").src;

    modal.style.display = "block";
  });
});

// envio do form
formEquipe.addEventListener("submit", async (e) => {
  e.preventDefault();

  const dados = {
    nome: formEquipe.nome.value,
    turma: formEquipe.turma.value,
    email: formEquipe.email.value,
    funcao: formEquipe.funcao.value,
    ano: formEquipe.ano.value,
    urlimagem: formEquipe.urlimagem.value
  };

  try {
    const url = editarCode ? `/equipe/editar/${editarCode}` : "/equipe";
    const method = editarCode ? "PUT" : "POST";

    const resposta = await fetch(url, {
      method: method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados)
    });

    const resultado = await resposta.json();
    if(resultado.success){
      alert("Salvo com sucesso!");
      location.reload();
    } else {
      alert("Erro: " + resultado.error);
    }
  } catch(err){
    console.error(err);
  }

  formEquipe.reset();
  modal.style.display = "none";
});
