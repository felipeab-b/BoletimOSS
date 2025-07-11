% if mostrar_alerta:
<style>
    .alert {
        display: none;
        background-color: #fdecea;
        color: #611a15;
        border: 1px solid #f5c6cb;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        min-width: 250px;
        font-family: 'Segoe UI', sans-serif;
    }
    .alert.show {
        display: block;
    }
    .close-btn {
        float: right;
        font-weight: bold;
        cursor: pointer;
    }
</style>

<div id="meu-alerta" class="alert">
    <span class="close-btn" onclick="fecharAlerta()">&times;</span>
    {{mensagem}}
</div>

<script>
    function mostrarAlerta() {
        var alerta = document.getElementById("meu-alerta");
        alerta.classList.add("show");

        setTimeout(function () {
            alerta.classList.remove("show");
        }, 4000);
    }

    function fecharAlerta() {
        document.getElementById("meu-alerta").classList.remove("show");
    }

    window.onload = mostrarAlerta;
</script>
% end