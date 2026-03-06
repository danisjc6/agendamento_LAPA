let salaSelecionada = null;
let linhaSalaSelecionada = null;

async function carregarSalas() {
    const salas = await apiFetch("/salas");

    const tbody = document.querySelector("#tabelaSalas tbody");
    tbody.innerHTML = "";

    salas.forEach(sala => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${sala.id_sala}</td>
            <td>${sala.nome_sala}</td>
            <td>${sala.tipo}</td>
            <td>${sala.capacidade}</td>
        `;

        tr.onclick = () => {
            salaSelecionada = sala;

            if (linhaSalaSelecionada) {
                linhaSalaSelecionada.classList.remove("sala-selecionada");
            }

            tr.classList.add("sala-selecionada");
            linhaSalaSelecionada = tr;

            const tabelaHorarios = document.querySelector("#tabelaHorarios tbody");
            if (tabelaHorarios) {
                carregarDisponibilidade();
            }
        };

        tbody.appendChild(tr);
    });
}
