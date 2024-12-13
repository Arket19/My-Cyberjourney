import os
import zipfile
import shutil
import markdown

# Crear el contenido HTML
def generate_html(md_content, title):

    html_template = f"""
<!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset=\"UTF-8\">
            <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
            <title>{title} - My Cyberjourney</title>
            <link rel=\"stylesheet\" href=\"https://www.w3schools.com/w3css/4/w3.css\">
            <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
            <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
            <link href=\"{title}.css\" rel=\"stylesheet\">
            <link href=\"https://fonts.googleapis.com/css2?family=Alumni+Sans+Pinstripe:ital@0;1&display=swap\" rel=\"stylesheet\">
            <link href=\"https://fonts.googleapis.com/css2?family=Roboto+Serif:ital,opsz,wght@0,8..144,100..900;1,8..144,100..900&display=swap\" rel=\"stylesheet\">
        </head>
        <body>
            <!-- Menú -->
            <nav class=\"w3-bar\">
                <div class=\"logo\">
                    <p>My Cyberjourney</p>
                </div>
                <div class=\"w3-bar-item w3-right w3-hide-large w3-hover-opacity\" onclick=\"w3_open()\">
                    <i class=\"fa fa-bars w3-xlarge\"></i>
                </div>
                <div class=\"w3-hide-small\">
                    <ul class=\"elementos-menu\">
                        <li class=\"w3-bar-item\"><a href=\"index.html\">Home</a></li>
                        <li class=\"w3-bar-item\"><a href=\"curriculum/curriculum.html\">Resume (CV)</a></li>
                        <li class=\"w3-bar-item\"><a href=\"writeups/writeups.html\">Writeups</a></li>
                        <li class=\"w3-bar-item\"><a href=\"learning/learning.html\">Learning Journey</a></li>
                    </ul>
                </div>
            </nav> 
            <div class=\"content\">
                {md_content}
            </div>
        </body>
    </html>
"""
    return html_template

def process_zip_files():
    # Guardar las rutas de las carpetas y el archivo de errores
    root_dir = os.path.dirname(os.path.abspath(__file__))  
    files_dir = os.path.join(root_dir, 'files') 
    writeups_dir = os.path.join(root_dir, '..', 'writeups') 
    
    error_file = os.path.join(root_dir, 'error.txt')
    if os.path.exists(error_file):
        os.remove(error_file)

    errors = ""

    # Verificar que 'files' existe
    if not os.path.exists(files_dir):
        errors = "Folder 'files' doesn't exist.\n"
        with open(error_file, 'w', encoding='utf-8') as error_log:
            error_log.write(errors)
        return

    # Crear 'writeups' si no existe
    os.makedirs(writeups_dir, exist_ok=True)

    # Localizar los archivos zip en 'files'
    zip_files = [f for f in os.listdir(files_dir) if f.endswith('.zip')]

    if not zip_files:
        errors = "No .zip files were found in 'files'\n"
        with open(error_file, 'w', encoding='utf-8') as error_log:
            error_log.write(errors)
        return

    # Procesar cada archivo zip encontrado en la carpeta
    for zip_file in zip_files:
        zip_file_path = os.path.join(files_dir, zip_file)
        folder_name = os.path.splitext(zip_file)[0]

        # Crear carpeta temporal para extraer el contenido del ZIP
        extracted_folder = os.path.join(files_dir, folder_name)
        os.makedirs(extracted_folder, exist_ok=True)

        try:
            # Extraer el contenido del archivo ZIP
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extracted_folder)

            # Localizar los archivos .md en el contenido extraído
            md_files = [f for f in os.listdir(extracted_folder) if f.endswith('.md')]

            # Si hay más de un archivo .md, registrar un error y continuar
            if len(md_files) != 1:
                errors += f"There are more than one .md files in '{zip_file}'.\n"
                continue

            md_file = md_files[0]
            md_file_path = os.path.join(extracted_folder, md_file)

            # Crear la carpeta del writeup
            writeup_folder = os.path.join(writeups_dir, folder_name.capitalize())

            # Si la carpeta ya existe, registrar un error y detener el programa
            if os.path.exists(writeup_folder):
                errors += f"The folder '{writeup_folder}' already exists.\n"
                break

            os.makedirs(writeup_folder, exist_ok=True)

            # Leer el archivo Markdown
            with open(md_file_path, 'r', encoding='utf-8') as file:
                md_content = file.read()

            # Convertir de Markdown a HTML
            html_content = markdown.markdown(md_content)
            title = folder_name.capitalize()
            html_output = os.path.join(writeup_folder, f'{title}.html')
            css_output = os.path.join(writeup_folder, f'{title}.css')

            # Crear el archivo .html
            with open(html_output, 'w', encoding='utf-8') as html_file:
                html_file.write(generate_html(html_content, title))

            # Crear el archivo .css
            css_content =  """
        /* General */
body {
    font-family: 'Roboto Serif', serif;
    background-color: #222222; /* Fondo negro */
    color: white; /* Texto claro */
    margin: 0;
    padding: 0;
}

/* Barra de navegación */
nav {
    background-color: #333; 
    color: white;
    padding: 5px 10px; 
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 5rem;
    position: fixed; 
    top: 0; 
    left: 0; 
    width: 100%;
    z-index: 1000; 
}

nav .logo a {
    font-size: 1.8rem;
    font-weight: bold;
    text-decoration: none;
    color: white;
}

nav ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-wrap: wrap;
}

nav ul li {
    margin: 0 10px;
}

nav ul li a {
    text-decoration: none;
    color: white;
    transition: color 0.3s;
}


.content {
    padding-top: 3rem;
    width: 45%;
    margin-left: auto;
    margin-right: auto;
    background-color: #222222;
}

.title{
    color: white;
}
h1 {
    padding-top: 4rem;
    color: #d4a200d3;
}

h2,
h3 {
    color: #00bcd4;
}

ul {
    padding-left: 20px;
}

li {
    margin-bottom: 10px;
}

a {
    color: rgb(0, 128, 128);
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

pre {
    background-color: #1e1e1e;
    color: #dcdcdc;
    padding: 10px;
    border-radius: 5px;
    overflow-x: auto;
    margin-bottom: 20px;
}

code {
    background-color: #1c1c1c;
    color: #a03939;
    padding: 2px 4px;
    border-radius: 3px;
}

img {
    display: block;
    max-width: 100%;
    margin: 20px auto;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
}

p {
    margin-bottom: 15px;
}
        
        """
            with open(css_output, 'w', encoding='utf-8') as css_file:
                css_file.write(css_content)

            # Mover las imágenes a la carpeta del writeup
            for item in os.listdir(extracted_folder):
                if item.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(extracted_folder, item)
                    shutil.move(img_path, os.path.join(writeup_folder, item))

        finally:
            # Eliminar la carpeta temporal en todos los casos
            shutil.rmtree(extracted_folder)

    # Si hubo errores, escribirlos en error.txt
    if errors:
        with open(error_file, 'w', encoding='utf-8') as error_log:
            error_log.write(errors)

# Ejecutar el proceso
if __name__ == "__main__":
    process_zip_files()