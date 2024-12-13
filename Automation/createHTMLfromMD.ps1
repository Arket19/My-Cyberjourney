# Obtener la ruta del directorio donde se encuentra el script de PowerShell
$directorio = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Construir la ruta completa al archivo Python
$archivoPython = Join-Path -Path $directorio -ChildPath 'createHTMLfromMD.py'

# Verificar si el archivo Python existe
if (Test-Path $archivoPython) {
    # Ejecutar el script Python usando Python
    python $archivoPython
} else {
    Write-Host "No se encontró el archivo Python en la carpeta."
}
