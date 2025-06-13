document.addEventListener("DOMContentLoaded", () => {
    const botao = document.getElementById("botao_cabecalho");
    const header = document.querySelector("header");
    const main = document.querySelector("main")

    let da_pra_ver = false;

    botao.addEventListener("click", () => {
        da_pra_ver = !da_pra_ver;
        header.style.display = da_pra_ver ? "flex" : "none";
        main.style.height = da_pra_ver ? "90vh" : "97vh";
        botao.textContent = da_pra_ver ? "⬆️" : "⬇️";
    });
});