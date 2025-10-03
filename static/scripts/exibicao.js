const btnAdicionar = document.getElementById("adicionar");
const modal = document.getElementById("modal");
const fechar = document.querySelector(".fechar");
const cancelar = document.getElementById("cancelar");
const formExibicao = document.getElementById("exibicaoForm");

// Abrir modal
btnAdicionar.addEventListener("click", () => {
  modal.style.display = "block";
});

// Fechar modal
fechar.addEventListener("click", () => {
  modal.style.display = "none";
});
cancelar.addEventListener("click", () => {
  modal.style.display = "none";
});
window.addEventListener("click", (e) => {
  if (e.target === modal) modal.style.display = "none";
});

// Adicionar exibição
formExibicao.addEventListener("submit", async (e) => {
  e.preventDefault();

  const dados = {
    ordem: formExibicao.ordem.value,
    fk: formExibicao.fk.value,
    dia: formExibicao.dia.value,
    horario: formExibicao.horario.value,
    endereco: formExibicao.endereco.value,
    latitude: parseFloat(formExibicao.latitude.value),
    longitude: parseFloat(formExibicao.longitude.value)
  };

  try {
    const res = await fetch("/exibicao", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados)
    });
    const json = await res.json();
    if (json.success) location.reload();
    else alert("Erro: " + json.error);
  } catch (err) {
    console.error(err);
    alert("Erro ao cadastrar exibição.");
  }

  formExibicao.reset();
  modal.style.display = "none";
});

// Botão de excluir
document.querySelectorAll(".excluir").forEach(btn => {
  btn.addEventListener("click", async () => {
    const id = btn.getAttribute("data-id");
    if (!confirm("Deseja realmente excluir esta exibição?")) return;

    try {
      const res = await fetch(`/exibicao/excluir/${id}`, { method: "GET" });
      if (res.ok) location.reload();
      else {
        const text = await res.text();
        alert("Erro ao excluir: " + text);
      }
    } catch (err) {
      console.error(err);
      alert("Erro de rede ao excluir exibição.");
    }
  });
});
