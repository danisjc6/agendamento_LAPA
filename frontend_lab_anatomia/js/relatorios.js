document.addEventListener("DOMContentLoaded", function () {

  fetch("http://127.0.0.1:8000/relatorios/agendamentos")
    .then(response => response.json())
    .then(dados => {

      const tbody = document.getElementById("tabela-relatorios");
      tbody.innerHTML = "";

      dados.forEach(item => {

        const linha = document.createElement("tr");

        linha.innerHTML = `
          <td>${formatarData(item.data)}</td>
          <td>${formatarHora(item.hora_inicio)}</td>
          <td>${formatarHora(item.hora_fim)}</td>
          <td>${item.nome_sala}</td>
          <td>${item.nome_usuario}</td>
          <td>${item.status}</td>
        `;

        tbody.appendChild(linha);
      });
    })
    .catch(error => console.error("Erro:", error));

});

function formatarHora(segundos) {
  const horas = Math.floor(segundos / 3600);
  const minutos = Math.floor((segundos % 3600) / 60);
  return `${String(horas).padStart(2, '0')}:${String(minutos).padStart(2, '0')}`;
}

function formatarData(dataISO) {
  const [ano, mes, dia] = dataISO.split("-");
  return `${dia}/${mes}/${ano}`;
}

function exportarCSV() {
  window.open("http://127.0.0.1:8000/relatorios/agendamentos/csv", "_blank");
}