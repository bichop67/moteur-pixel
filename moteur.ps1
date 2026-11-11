# MOTEUR PIXEL : installer, envoyer et recevoir (un seul script, à lancer depuis le dossier du dépôt)
#   powershell -ExecutionPolicy Bypass -File moteur.ps1 installe   sur un NOUVEL ordinateur, juste après « git clone »
#   powershell -ExecutionPolicy Bypass -File moteur.ps1 envoie     envoyer le travail de cet ordinateur vers GitHub
#   powershell -ExecutionPolicy Bypass -File moteur.ps1 recois     prendre le travail fait sur un autre ordinateur
# Les skills Claude (video-pixel, film-pixel) voyagent dans le dossier « skills » du dépôt ; ils sont copiés vers
# %USERPROFILE%\.claude\skills, avec le chemin du moteur de CET ordinateur écrit dedans.
param([Parameter(Position = 0)][string]$Action = "aide", [Parameter(Position = 1)][string]$Message = "")

$ErrorActionPreference = "Stop"
$Depot = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillsDepot = Join-Path $Depot "skills"
$SkillsClaude = Join-Path $env:USERPROFILE ".claude\skills"
$Skills = @("video-pixel", "film-pixel")
$Origine = "C:\Users\abdellah\Desktop\VIDEO YOUTUBE"        # le chemin écrit dans les skills du dépôt
$Utf8 = New-Object System.Text.UTF8Encoding($false)

function Copie-Skills([string]$De, [string]$Vers, [string]$Cherche, [string]$Remplace) {
    foreach ($s in $Skills) {
        $src = Join-Path $De $s
        if (-not (Test-Path $src)) { continue }
        Get-ChildItem $src -Recurse -File | ForEach-Object {
            $dst = Join-Path (Join-Path $Vers $s) $_.FullName.Substring($src.Length + 1)
            New-Item -ItemType Directory -Force (Split-Path -Parent $dst) | Out-Null
            if ($_.Extension -in ".md", ".txt" -and $Cherche -ne $Remplace) {
                $t = [IO.File]::ReadAllText($_.FullName, $Utf8)
                [IO.File]::WriteAllText($dst, $t.Replace($Cherche, $Remplace), $Utf8)
            }
            else { Copy-Item $_.FullName $dst -Force }
        }
        Write-Host "  skill $s -> $Vers"
    }
}

switch ($Action) {
    "installe" {
        Write-Host "1. Python"
        $v = (& python --version) 2>&1
        Write-Host "  $v"
        if ("$v" -notmatch "Python 3\.(1[0-9])") { Write-Host "  ! Installer Python 3.10 ou plus récent (python.org), en cochant « Add to PATH », puis relancer." ; exit 1 }
        Write-Host "2. Bibliothèques (pip)"
        & python -m pip install -r (Join-Path $Depot "requirements.txt")
        if ($LASTEXITCODE -ne 0) { Write-Host "  ! pip a échoué : lire le message ci-dessus." ; exit 1 }
        Write-Host "3. Skills Claude"
        Copie-Skills $SkillsDepot $SkillsClaude $Origine $Depot
        Write-Host "4. Polices Windows utilisées par le moteur"
        foreach ($f in "tahomabd.ttf", "tahoma.ttf", "verdanab.ttf", "seguibl.ttf", "arialbd.ttf", "segoeprb.ttf") {
            if (-not (Test-Path (Join-Path $env:WINDIR "Fonts\$f"))) { Write-Host "  ! police absente : $f (le moteur a besoin d'un Windows avec ses polices d'origine)" }
        }
        Write-Host "5. Essai du moteur (une image, sans voix)"
        Push-Location (Join-Path $Depot "_MOTEUR_PIXEL")
        $env:PYTHONIOENCODING = "utf-8"
        $essai = Join-Path $env:TEMP "essai_moteur_pixel.png"
        & python scenario.py scenarios\islam_13_telephone.txt still 3.0 $essai
        Pop-Location
        if (Test-Path $essai) { Write-Host "OK : le moteur marche ici. Image d'essai : $essai" }
        else { Write-Host "! Le moteur n'a pas produit d'image : lire le message ci-dessus." ; exit 1 }
        Write-Host "À la première transcription de voix, faster-whisper télécharge son modèle (≈ 1,5 Go, une seule fois)."
    }
    "envoie" {
        Copie-Skills $SkillsClaude $SkillsDepot $Depot $Origine
        Push-Location $Depot
        & git add -A
        & git status --short | Select-Object -First 40
        if (-not $Message) { $Message = "Travail du " + (Get-Date -Format "dd/MM/yyyy HH:mm") + " (" + $env:COMPUTERNAME + ")" }
        & git commit -m $Message
        & git push
        Pop-Location
    }
    "recois" {
        Push-Location $Depot
        & git pull --ff-only
        $ok = $LASTEXITCODE -eq 0
        Pop-Location
        if (-not $ok) { Write-Host "! git pull a refusé : du travail non envoyé existe ici. Lancer d'abord « envoie », ou demander à Claude." ; exit 1 }
        Copie-Skills $SkillsDepot $SkillsClaude $Origine $Depot
    }
    default {
        Write-Host "moteur.ps1 installe | envoie [`"message`"] | recois   (voir README.md)"
    }
}
