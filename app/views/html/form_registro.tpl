<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registro - BoletimOSS</title>
    <link rel="stylesheet" href="../../static/css/login.css"> <link href="https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600&display=swap" rel="stylesheet">

</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <h1>BoletimOSS</h1>
            <p>Sistema de Gestão Acadêmica</p>
        </div>
        
        <div class="login-card">
            <h2>Registrar</h2>
            <form action="/registro" method="post">
                <div class="form-group">
                    <label for="matricula">Matrícula</label>
                    <input type="text" id="matricula" name="matricula" required>
                </div>
                <div class="form-group">
                    <label for="nome">Nome Completo</label>
                    <input type="text" id="nome" name="nome" required>
                </div>
                <div class="form-group">
                    <label for="curso">Curso</label>
                    <input type="text" id="curso" name="curso" required>
                </div>
                <div class="form-group">
                    <label for="password">Senha</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit" class="login-btn">Registrar</button>
            </form>
            <p>Já tem conta? <a href="./login">Faça Login</a></p>
        </div>
        
        <div class="login-footer">
            <p>© 2025 BoletimOSS. Todos os direitos reservados.</p>
        </div>
    </div>
% include('app/views/html/alerta.tpl')

</body>
</html>