const INTERVALO_ATUALIZACAO_MS = 5000;
let intervaloAgendamentosId = null;

function mostrarFeedback(mensagem, tipo = "success") {
    const feedback = document.getElementById("feedback");
    if (!feedback) return;

    feedback.textContent = mensagem;
    feedback.className = `feedback ${tipo}`;
    feedback.style.display = "block";
}

function limparFeedback() {
    const feedback = document.getElementById("feedback");
    if (!feedback) return;

    feedback.style.display = "none";
    feedback.textContent = "";
}

async function carregarDisponibilidade() {
    const data = document.getElementById("dataSelecionada").value;
    if (!salaSelecionada || !data) return;

    const horarios = await apiFetch(
        `/salas/${salaSelecionada.id_sala}/disponibilidade?data=${data}`
    );

    const tbody = document.querySelector("#tabelaHorarios tbody");
    if (!tbody) return;

    tbody.innerHTML = "";

    horarios.forEach(h => {
        // O endpoint atual retorna apenas blocos livres (sem campo "disponivel").
        // Mantemos compatibilidade caso o backend passe a enviar esse campo depois.
        const disponivel = typeof h.disponivel === "boolean" ? h.disponivel : true;

        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${h.hora_inicio}</td>
            <td>${h.hora_fim}</td>
            <td>${disponivel ? "Livre" : "Ocupado"}</td>
        `;
        tbody.appendChild(tr);
    });
}

document.getElementById("formAgendamento").onsubmit = async (e) => {
    e.preventDefault();

    try {
        limparFeedback();

        if (!salaSelecionada) {
            throw new Error("Selecione uma sala antes de confirmar o agendamento.");
        }

        const data = document.getElementById("dataSelecionada").value;
        if (!data) {
            throw new Error("Selecione uma data para o agendamento.");
        }

        await apiFetch("/agendamentos/", {
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

        await listarAgendamentos();
        await carregarDisponibilidade();

        mostrarFeedback("Agendamento criado com sucesso.", "success");
    } catch (erro) {
        mostrarFeedback(erro.message || "Falha ao criar agendamento.", "error");
    }
};

async function listarAgendamentos() {
    const lista = await apiFetch("/agendamentos/");
    const listaOrdenada = [...lista].sort((a, b) => b.id_agendamento - a.id_agendamento);

    const tbody = document.querySelector("#tabelaAgendamentos tbody");
    tbody.innerHTML = "";

    listaOrdenada.forEach(a => {
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

    if (!confirm("Deseja realmente cancelar este agendamento?")) {
        return;
    }

    try {
        await apiFetch(`/agendamentos/${id_agendamento}/cancelar`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                motivo: "Cancelado pelo usuário"
            })
        });

        await listarAgendamentos();
        await carregarDisponibilidade();

        mostrarFeedback("Agendamento cancelado com sucesso.", "success");
    } catch (erro) {
        mostrarFeedback(erro.message || "Falha ao cancelar agendamento.", "error");
    }
}

function iniciarAtualizacaoAutomaticaAgendamentos() {
    if (intervaloAgendamentosId) return;

    intervaloAgendamentosId = setInterval(async () => {
        try {
            await listarAgendamentos();
        } catch (_) {
            // Evita quebrar o loop de atualização automática em caso de falha pontual.
        }
    }, INTERVALO_ATUALIZACAO_MS);
}
