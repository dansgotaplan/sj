const btnAdicionar = document.getElementById("adicionar");
const modal = document.getElementById("modal");
const fechar = document.querySelector(".fechar");
const cancelar = document.getElementById("cancelar");
const formExibicao = document.getElementById("exibicaoForm");

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
  if (e.target === modal) modal.style.display = "none";
});

formExibicao.addEventListener("submit", async (e) => {
  e.preventDefault();

  const dados = {
    ordem: formExibicao.ordem.value,
    fk: formExibicao.fk.value,
    dia: formExibicao.dia.value,
    horario: formExibicao.horario.value,
    endereco: formExibicao.endereco.value,
    latitude: formExibicao.latitude.value,
    longitude: formExibicao.longitude.value
  };

  try {
    const res = await fetch("/exibicao", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados)
    });

    const json = await res.json();
    if (json.success) {
      location.reload(); // atualiza a página pra mostrar nova exibição
    } else {
      alert("Erro: " + json.error);
    }
  } catch (err) {
    console.error(err);
    alert("Erro ao cadastrar exibição.");
  }

  formExibicao.reset();
  modal.style.display = "none";
});
