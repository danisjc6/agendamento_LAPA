document.getElementById("dataSelecionada")
    .addEventListener("change", carregarDisponibilidade);

window.onload = () => {
    carregarSalas();
    listarAgendamentos();
};
