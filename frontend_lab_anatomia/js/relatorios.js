const LABELS_VIEWS = {
  agendamentos_detalhados: "Agendamentos detalhados",
  salas_mais_utilizadas: "Salas mais utilizadas",
  agendamentos_ativos: "Agendamentos ativos",
  ocupacao_salas_por_data: "Ocupacao de salas por data",
  salas_livres: "Salas livres"
};

function formatarValor(chave, valor) {
  if (valor === null || valor === undefined) return "-";

  if (chave === "data" && typeof valor === "string") {
    const partes = valor.split("-");
    if (partes.length === 3) return `${partes[2]}/${partes[1]}/${partes[0]}`;
  }

  if ((chave === "hora_inicio" || chave === "hora_fim") && typeof valor === "string") {
    return valor.slice(0, 5);
  }

  return String(valor);
}

function montarCabecalho(colunas) {
  const thead = document.getElementById("cabecalho-relatorios");
  thead.innerHTML = "";

  const tr = document.createElement("tr");
  colunas.forEach((coluna) => {
    const th = document.createElement("th");
    th.textContent = coluna;
    tr.appendChild(th);
  });

  thead.appendChild(tr);
}

function montarLinhas(colunas, dados) {
  const tbody = document.getElementById("tabela-relatorios");
  tbody.innerHTML = "";

  if (!dados.length) {
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = Math.max(colunas.length, 1);
    td.textContent = "Nenhum registro encontrado para esta view.";
    tr.appendChild(td);
    tbody.appendChild(tr);
    return;
  }

  dados.forEach((item) => {
    const tr = document.createElement("tr");

    colunas.forEach((coluna) => {
      const td = document.createElement("td");
      td.textContent = formatarValor(coluna, item[coluna]);
      tr.appendChild(td);
    });

    tbody.appendChild(tr);
  });
}

async function carregarViews() {
  const views = await apiFetch("/relatorios/views");
  const selector = document.getElementById("viewSelector");
  selector.innerHTML = "";

  views.forEach((view) => {
    const option = document.createElement("option");
    option.value = view.id;
    option.textContent = LABELS_VIEWS[view.id] || view.id;
    selector.appendChild(option);
  });
}

async function carregarDadosDaView() {
  const selector = document.getElementById("viewSelector");
  const status = document.getElementById("status");
  const viewSelecionada = selector.value;

  if (!viewSelecionada) return;

  status.textContent = "Carregando...";

  try {
    const dados = await apiFetch(`/relatorios/views/${viewSelecionada}`);
    const colunas = dados.length ? Object.keys(dados[0]) : [];

    montarCabecalho(colunas);
    montarLinhas(colunas, dados);
    status.textContent = `${dados.length} registro(s) carregado(s).`;
  } catch (erro) {
    montarCabecalho([]);
    montarLinhas([], []);
    status.textContent = `Erro ao carregar dados: ${erro.message}`;
  }
}

function exportarCSV() {
  const viewSelecionada = document.getElementById("viewSelector").value;
  if (!viewSelecionada) return;
  window.open(`${API_URL}/relatorios/views/${viewSelecionada}/csv`, "_blank");
}

document.addEventListener("DOMContentLoaded", async () => {
  await carregarViews();
  await carregarDadosDaView();

  document.getElementById("viewSelector").addEventListener("change", carregarDadosDaView);
  document.getElementById("btnAtualizar").addEventListener("click", carregarDadosDaView);
  document.getElementById("btnExportar").addEventListener("click", exportarCSV);
});
