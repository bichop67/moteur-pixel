# Installation du moteur pixel sur un nouvel ordinateur, en UNE commande a coller dans PowerShell :
#   irm https://raw.githubusercontent.com/bichop67/moteur-pixel/main/demarre.ps1 | iex
# (ASCII seulement, sans accent : ce fichier est lu puis execute directement depuis GitHub.)
# Il installe Git et Python 3.10 s'ils manquent (winget), telecharge le depot sur le Bureau dans "VIDEO YOUTUBE",
# puis lance "moteur.ps1 installe" (bibliotheques, skills Claude, image d'essai).

$Depot = Join-Path ([Environment]::GetFolderPath('Desktop')) 'VIDEO YOUTUBE'

function Rafraichit-Chemin {
    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'User') + ';' + [Environment]::GetEnvironmentVariable('Path', 'Machine')
}
function Present([string]$cmd) { return [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }
function Python-Ok {
    if (-not (Present 'python')) { return $false }
    $v = ''
    try { $v = (& python --version 2>&1 | Out-String) } catch { return $false }
    return ($v -match 'Python 3\.1[0-2]\.')
}
function Echec([string]$msg) { Write-Host ''; Write-Host ('MOTEUR-PIXEL : ECHEC - ' + $msg) -ForegroundColor Red }

Write-Host '== Moteur pixel : installation ==' -ForegroundColor Cyan
Rafraichit-Chemin
$ok = $true

if (-not (Present 'git') -or -not (Python-Ok)) {
    if (-not (Present 'winget')) {
        Echec 'winget est absent : installer Git (git-scm.com) et Python 3.10 (python.org, cocher Add to PATH), puis relancer.'
        $ok = $false
    }
}
if ($ok -and -not (Present 'git')) {
    Write-Host '1. Git manque : installation (winget)...'
    winget install -e --id Git.Git --silent --accept-source-agreements --accept-package-agreements
    Rafraichit-Chemin
    if (-not (Present 'git')) { Echec 'Git ne s''est pas installe.'; $ok = $false }
} elseif ($ok) { Write-Host '1. Git : deja la.' }

if ($ok -and -not (Python-Ok)) {
    Write-Host '2. Python 3.10 a 3.12 manque : installation de Python 3.10 (winget)...'
    winget install -e --id Python.Python.3.10 --silent --accept-source-agreements --accept-package-agreements --override '/quiet InstallAllUsers=0 PrependPath=1 Include_launcher=0'
    Rafraichit-Chemin
    if (-not (Python-Ok)) { Echec 'Python 3.10 installe, mais "python" ne repond pas (ou une autre version passe devant) : fermer cette fenetre, en ouvrir une neuve et relancer la commande.'; $ok = $false }
} elseif ($ok) { Write-Host ('2. Python : ' + ((& python --version 2>&1 | Out-String).Trim())) }

if ($ok) {
    if (Test-Path (Join-Path $Depot '.git')) {
        Write-Host '3. Le depot est deja la : mise a jour...'
        git -C $Depot pull --ff-only
    } elseif (Test-Path $Depot) {
        Echec ('le dossier "' + $Depot + '" existe deja et n''est pas le depot : le renommer, puis relancer.')
        $ok = $false
    } else {
        Write-Host '3. Telechargement du depot (77 Mo)...'
        git clone https://github.com/bichop67/moteur-pixel.git $Depot
    }
    if ($ok -and -not (Test-Path (Join-Path $Depot 'moteur.ps1'))) { Echec 'le telechargement n''a pas abouti.'; $ok = $false }
}

if ($ok) {
    Write-Host '4. Installation (bibliotheques Python, skills Claude, image d''essai)...'
    powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $Depot 'moteur.ps1') installe
    if ($LASTEXITCODE -eq 0) {
        Write-Host ''
        Write-Host ('MOTEUR-PIXEL : TERMINE - le moteur est dans ' + $Depot) -ForegroundColor Green
    } else { Echec 'moteur.ps1 installe a signale une erreur (lire au-dessus).' }
}
