window.addEventListener("DOMContentLoaded", () => {
    const pagina = document.body.dataset.page;

    switch (pagina) {
        case "agendamentos":
            carregarSalas();
            listarAgendamentos();
            iniciarAtualizacaoAutomaticaAgendamentos();
            break;

        case "usuarios":
            atualizarTabela("usuarios");
            break;
    }
});

