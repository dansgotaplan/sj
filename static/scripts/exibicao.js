const btnAdicionar = document.getElementById("adicionar");
const modal = document.getElementById("modal");
const fechar = document.querySelector(".fechar");
const cancelar = document.getElementById("cancelar");
const formExibicao = document.getElementById("exibicaoForm");

// Abrir modal
btnAdicionar.addEventListener("click", () => {
  modal.style.display = "block";
  formExibicao.onsubmit = null; // garante submit padrão para POST
});

// Fechar modal
fechar.addEventListener("click", () => modal.style.display = "none");
cancelar.addEventListener("click", () => modal.style.display = "none");
window.addEventListener("click", (e) => {
  if (e.target === modal) modal.style.display = "none";
});

// Adicionar exibição (POST)
formExibicao.addEventListener("submit", async (e) => {
  if (formExibicao.onsubmit) return; // se estiver em modo editar, ignora
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
      else alert(await res.text());
    } catch (err) {
      console.error(err);
      alert("Erro de rede ao excluir exibição.");
    }
  });
});

// Botão de editar
document.querySelectorAll(".editar").forEach(btn => {
  btn.addEventListener("click", async () => {
    const id = btn.getAttribute("data-id");
    try {
      const res = await fetch(`/exibicao/${id}`);
      if (!res.ok) throw new Error("Erro ao buscar exibição");
      const exibicao = await res.json();

      formExibicao.ordem.value = exibicao.ordem;
      formExibicao.fk.value = exibicao.fk;
      formExibicao.dia.value = exibicao.dia;
      formExibicao.horario.value = exibicao.horario;
      formExibicao.endereco.value = exibicao.endereco;
      formExibicao.latitude.value = exibicao.latitude;
      formExibicao.longitude.value = exibicao.longitude;

      modal.style.display = "block";

      // Submit para PUT
      formExibicao.onsubmit = async (e) => {
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
          const res = await fetch(`/exibicao/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados)
          });
          const json = await res.json();
          if (json.success) location.reload();
          else alert("Erro: " + json.error);
        } catch (err) {
          console.error(err);
          alert("Erro ao editar exibição.");
        }

        formExibicao.reset();
        modal.style.display = "none";
        formExibicao.onsubmit = null; // volta para POST padrão
      };
    } catch (err) {
      console.error(err);
      alert("Erro ao carregar exibição.");
    }
  });
});
