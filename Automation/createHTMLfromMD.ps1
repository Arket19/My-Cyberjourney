$directorio = Split-Path -Parent $MyInvocation.MyCommand.Definition
$archivoPython = Join-Path -Path $directorio -ChildPath 'createHTMLfromMD.py'

if (Test-Path $archivoPython) {
    python $archivoPython
}