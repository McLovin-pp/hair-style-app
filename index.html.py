<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Подбор Причёски</title>
    <style>
        body { font-family: sans-serif; background: #121212; color: white; text-align: center; padding: 20px; }
        .card { background: #1e1e1e; padding: 20px; border-radius: 16px; margin-top: 20px; }
        input[type="file"] { display: none; }
        .btn { background: #6200ee; color: white; padding: 12px 24px; border: none; border-radius: 8px; font-size: 16px; margin: 10px; cursor: pointer; }
        img { max-width: 100%; border-radius: 12px; margin-top: 15px; }
    </style>
</head>
<body>

    <h2>💈 Новый Стиль</h2>
    <p>Загрузи фото и выбери причёску</p>

    <div class="card">
        <label class="btn">
            📷 Выбрать фото
            <input type="file" id="photoInput" accept="image/*" onchange="previewImage(event)">
        </label>
        <br>
        <img id="preview" style="display:none;">

        <h3>Выбери причёску:</h3>
        <button class="btn" onclick="sendRequest('short fade haircut, realistic, 8k')">Короткая (Fade)</button>
        <button class="btn" onclick="sendRequest('curly hair afro style, realistic')">Кудрявые</button>
        <button class="btn" onclick="sendRequest('long blonde hair style, realistic')">Длинные светлые</button>
    </div>

    <div id="resultContainer" class="card" style="display:none;">
        <h3>Результат:</h3>
        <img id="resultImage">
    </div>

    <script>
        let selectedFile = null;

        function previewImage(event) {
            selectedFile = event.target.files[0];
            const reader = new FileReader();
            reader.onload = function(){
                const img = document.getElementById('preview');
                img.src = reader.result;
                img.style.display = 'block';
            };
            reader.readAsDataURL(selectedFile);
        }

        async function sendRequest(promptText) {
            if (!selectedFile) {
                alert("Сначала выбери фото!");
                return;
            }

            const formData = new FormData();
            formData.append("file", selectedFile);
            formData.append("prompt", promptText);

            alert("Генерируем причёску... Это займет около 10-15 секунд.");

            // Замени этот URL на адрес твоего бесплатного сервера Render
            const SERVER_URL = "https://твой-сервер.onrender.com/generate-hairstyle";

            try {
                const response = await fetch(SERVER_URL, {
                    method: "POST",
                    body: formData
                });
                const data = await response.json();
                
                // Отображаем результат
                document.getElementById('resultImage').src = data.result_url;
                document.getElementById('resultContainer').style.display = 'block';
            } catch (err) {
                alert("Ошибка при генерации. Проверь подключение к серверу.");
            }
        }
    </script>
</body>
</html>