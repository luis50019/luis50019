<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Luis Angel Diaz Dia - GitHub Profile</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background-color: #0d1117;
            color: #c9d1d9;
            line-height: 1.6;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .container {
            display: flex;
            flex-direction: column;
            gap: 30px;
        }
        
        .header {
            text-align: center;
            padding: 20px 0;
            position: relative;
        }
        
        .octocat-img {
            width: 200px;
            height: 200px;
            margin-bottom: 20px;
        }
        
        .typing-text {
            font-size: 32px;
            color: #6FDA44;
            margin-bottom: 20px;
            font-weight: bold;
        }
        
        .coding-gif {
            position: absolute;
            right: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 150px;
            border-radius: 10px;
        }
        
        .about {
            background-color: #161b22;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        .about h2 {
            color: #6FDA44;
            margin-bottom: 15px;
            border-bottom: 2px solid #6FDA44;
            padding-bottom: 8px;
        }
        
        .about p {
            margin-bottom: 15px;
        }
        
        .about a {
            color: #6FDA44;
            text-decoration: none;
            font-weight: bold;
        }
        
        .about a:hover {
            text-decoration: underline;
        }
        
        .stack {
            background-color: #161b22;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        .stack h1 {
            text-align: center;
            color: #6FDA44;
            margin-bottom: 30px;
            font-size: 28px;
        }
        
        .stack h3 {
            color: #6FDA44;
            margin: 20px 0 15px;
            text-align: center;
            font-size: 22px;
        }
        
        .badges-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 15px;
            margin-bottom: 25px;
        }
        
        .badge {
            display: flex;
            align-items: center;
            justify-content: center;
            background: #21262d;
            padding: 10px 15px;
            border-radius: 6px;
            min-width: 120px;
            transition: transform 0.2s;
        }
        
        .badge:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        .badge img {
            max-height: 30px;
            margin-right: 8px;
        }
        
        .badge span {
            font-size: 14px;
            color: #c9d1d9;
        }
        
        .snake-container {
            margin-top: 40px;
            text-align: center;
        }
        
        @media (max-width: 768px) {
            .coding-gif {
                position: static;
                transform: none;
                margin: 20px auto;
                display: block;
            }
            
            .typing-text {
                font-size: 24px;
            }
            
            .badge {
                min-width: 100px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://raw.githubusercontent.com/AhmedFathyDev/AhmedFathyDev/main/GitHub.png" alt="GitHub Octocat Drinking a Cup of Coffee" class="octocat-img">
            <div class="typing-text">Hola Yo soy Luis Angel Diaz Diaz</div>
            <img alt="Night Coding" src="https://raw.githubusercontent.com/AVS1508/AVS1508/master/assets/Night-Coding.gif" class="coding-gif"/>
        </div>
        
        <div class="about">
            <h2>Sobre mí</h2>
            <p>🎓 Soy estudiante de Licenciatura en Informática y tengo 21 años. Me apasiona la programación y desarrollo proyectos en mis tiempos libres.</p>
            <p>👩‍💻 Me gusta aprender cosas nuevas.</p>
            <p>💻 Estudio por mi cuenta por las noches.</p>
            <p>🤝 Me gusta trabajar en equipo.</p>
            <p>👨‍💻 Todos mis proyectos disponibles en <a href="https://github.com/luis50019" target="_blank">Github</a></p>
        </div>
        
        <div class="stack">
            <h1>Stack</h1>
            
            <h3>Lenguajes</h3>
            <div class="badges-container">
                <div class="badge">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg" alt="Java">
                    <span>Java</span>
                </div>
                <div class="badge">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" alt="JavaScript">
                    <span>JavaScript</span>
                </div>
                <div class="badge">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" alt="HTML5">
                    <span>HTML5</span>
                </div>
                <div class="badge">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" alt="CSS3">
                    <span>CSS3</span>
                </div>
            </div>
            
            <h3>Frameworks</h3>
            <div class="badges-container">
                <div class="badge">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/spring/spring-original.svg" alt="Spring">
                    <span>Spring</span>
                </div>
                <div class="badge">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tailwindcss/tailwindcss-plain.svg" alt="Tailwind">
                    <span>Tailwind</span>
                </div>
                <div class="badge">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg" alt="Node.js">
                    <span>Node.js</span>
                </div>
                <div class="badge">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/npm/npm-original-wordmark.svg" alt="NPM">
                    <span>NPM</span>
                </div>
                <div class="badge">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg" alt="React">
                    <span>React</span>
                </div>
                <div class="badge">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bootstrap/bootstrap-original.svg" alt="Bootstrap">
                    <span>Bootstrap</span>
                </div>
                <div class="badge">
                    <img src="https://www.chartjs.org/img/chartjs-logo.svg" alt="Chart.js" style="filter: invert(1);">
                    <span>Chart.js</span>
                </div>
            </div>
            
            <h3>Bases de Datos</h3>
            <div class="badges-container">
                <div class="badge">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" alt="PostgreSQL">
                    <span>PostgreSQL</span>
                </div>
                <div class="badge">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/firebase/firebase-plain.svg" alt="Firebase">
                    <span>Firebase</span>
                </div>
            </div>
            
            <h3>Herramientas</h3>
            <div class="badges-container">
                <div class="badge">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" alt="GitHub">
                    <span>GitHub</span>
                </div>
                <div class="badge">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/intellij/intellij-original.svg" alt="IntelliJ">
                    <span>IntelliJ</span>
                </div>
                <div class="badge">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg" alt="VS Code">
                    <span>VS Code</span>
                </div>
            </div>
        </div>
        
        <div class="snake-container">
            <img src="https://raw.githubusercontent.com/luis50019/luis50019/main/resources/img/github-contribution-grid-snake.svg" alt="GitHub Contribution Snake" />
        </div>
    </div>
</body>
</html>
