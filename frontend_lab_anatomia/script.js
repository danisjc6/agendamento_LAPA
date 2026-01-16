const dados = {
  usuarios: [],
  salas: [],
  pecas: []
};

/* ================= PERSISTÊNCIA ================= */

function salvarLocal() {
  localStorage.setItem("dados_anatomia", JSON.stringify(dados));
}

function carregarLocal() {
  const salvo = localStorage.getItem("dados_anatomia");
  if (salvo) {
    const obj = JSON.parse(salvo);
    dados.usuarios = obj.usuarios || [];
    dados.salas = obj.salas || [];
    dados.pecas = obj.pecas || [];
  }
}

/* ================= INTERFACE ================= */

function mostrar(secao) {
  document.querySelectorAll("section")
    .forEach(s => s.style.display = "none");

  document.getElementById(secao).style.display = "block";
}

function salvar(tipo) {
  const inputs = document.querySelectorAll(`#${tipo} input`);
  const valores = [];

  inputs.forEach(i => valores.push(i.value));

  dados[tipo].push(valores);

  salvarLocal();
  atualizarTabela(tipo);

  inputs.forEach(i => i.value = "");
}

function atualizarTabela(tipo) {
  const tbody = document.getElementById(`tabela_${tipo}`);
  tbody.innerHTML = "";

  dados[tipo].forEach((linha, index) => {
    const tr = document.createElement("tr");

    linha.forEach(valor => {
      const td = document.createElement("td");
      td.textContent = valor;
      tr.appendChild(td);
    });

    const tdAcoes = document.createElement("td");
    tdAcoes.innerHTML = `
      <button onclick="editar('${tipo}', ${index})">Editar</button>
      <button onclick="excluir('${tipo}', ${index})">Excluir</button>
    `;
    tr.appendChild(tdAcoes);

    tbody.appendChild(tr);
  });
}

function excluir(tipo, index) {
  dados[tipo].splice(index, 1);
  salvarLocal();
  atualizarTabela(tipo);
}

function editar(tipo, index) {
  const inputs = document.querySelectorAll(`#${tipo} input`);
  const valores = dados[tipo][index];

  inputs.forEach((i, pos) => i.value = valores[pos]);

  excluir(tipo, index);
}

/* ================= INICIALIZAÇÃO ================= */

window.onload = () => {
  carregarLocal();
  atualizarTabela("usuarios");
  atualizarTabela("salas");
  atualizarTabela("pecas");
};
