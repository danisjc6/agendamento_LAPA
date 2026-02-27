async function carregarDisponibilidade() {
    const data = document.getElementById("dataSelecionada").value;
    if (!salaSelecionada || !data) return;

    const horarios = await apiFetch(
        `/salas/${salaSelecionada.id_sala}/disponibilidade?data=${data}`
    );

    const tbody = document.querySelector("#tabelaHorarios tbody");
    tbody.innerHTML = "";

    horarios.forEach(h => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${h.hora_inicio}</td>
            <td>${h.hora_fim}</td>
            <td>${h.disponivel ? "Livre" : "Ocupado"}</td>
        `;
        tbody.appendChild(tr);
    });
}

document.getElementById("formAgendamento").onsubmit = async (e) => {
    e.preventDefault();

    const data = document.getElementById("dataSelecionada").value;

    const agendamento = await apiFetch("/agendamentos", {
        method: "POST",
        body: JSON.stringify({
            matricula: document.getElementById("matricula").value,
            id_sala: salaSelecionada.id_sala,
            data: data,
            hora_inicio: document.getElementById("horaInicio").value,
            hora_fim: document.getElementById("horaFim").value,
            finalidade: document.getElementById("finalidade").value
        })
    });

    await apiFetch("/reservas", {
        method: "POST",
        body: JSON.stringify({
            id_agendamento: a.id_agendamento,
            id_sala: salaSelecionada.id_sala
        })
    });

    alert("Agendamento criado!");
    listarAgendamentos();
};

async function listarAgendamentos() {
    const lista = await apiFetch("/agendamentos");

    const tbody = document.querySelector("#tabelaAgendamentos tbody");
    tbody.innerHTML = "";

    lista.forEach(a => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${a.id_agendamento}</td>
            <td>${a.data}</td>
            <td>${a.hora_inicio}</td>
            <td>${a.hora_fim}</td>
            <td>${a.status}</td>
            <td>
                <button class="btn btn-cancelar"
                    onclick="cancelarAgendamento(${a.id_agendamento})">
                    Cancelar
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function cancelarAgendamento(id_agendamento) {
    await apiFetch(`/agendamentos/${id_agendamento}/cancelar`, {
        method: "POST"
    });

    listarAgendamentos();
}
