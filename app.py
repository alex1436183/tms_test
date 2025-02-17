from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Information</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            color: #333;
            margin: 20px;
            line-height: 1.6;
            transition: background-color 0.3s, color 0.3s;
        }

        h1 {
            color: #555;
            text-align: center;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
        }

        .content {
            margin-top: 20px;
            padding: 20px;
            background: #fff;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .content:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }

        .ip-address {
            font-weight: bold;
            color: #007BFF;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
        }

        .images {
            margin-top: 30px;
            display: flex;
            justify-content: center;
            gap: 20px;
        }

        .images img {
            width: 150px;
            height: 150px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .images img:hover {
            transform: scale(1.1);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }

        .footer {
            margin-top: 30px;
            text-align: center;
            font-size: 0.9em;
            color: #777;
        }

        .footer a {
            color: #007BFF;
            text-decoration: none;
            transition: color 0.3s;
        }

        .footer a:hover {
            color: #0056b3;
        }
    </style>
</head>
<body>
    <h1>Information</h1>
    <div class="content">
        <p>Levchenko Alexey Viktorovich</p>
        <p>Group: DOS24-onl</p>
        <p>Topic: webserver</p>
        <p>IP Address: <span class="ip-address">192.168.1.210:8080</span></p>
    </div>

    <div class="images">
        <!-- Используем url_for для правильного пути к картинке -->
        <img src="{{ url_for('static', filename='images/1.jpg') }}" alt="Example Image 1">
        <img src="{{ url_for('static', filename='images/1.jpg') }}" alt="Example Image 2">
        <img src="{{ url_for('static', filename='images/1.jpg') }}" alt="Example Image 3">
    </div>

    <div class="footer">
        <p>Created by <a href="https://example.com" target="_blank">Levchenko Alexey</a></p>
    </div>
</body>
</html>'''
    return render_template_string(html_content)

if __name__ == '__main__':
    # Указываем host='0.0.0.0', чтобы приложение слушало все интерфейсы
    app.run(debug=True, host='0.0.0.0', port=8080)
