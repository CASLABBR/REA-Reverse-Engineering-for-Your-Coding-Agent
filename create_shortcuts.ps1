$WshShell = New-Object -comObject WScript.Shell
$Desktop = [Environment]::GetFolderPath('Desktop')

$repos = @(
    @{Name='REA'; Path='D:\repos\rea'},
    @{Name='Ruflo'; Path='D:\repos\ruflo'},
    @{Name='Aweosome-Video-Agent'; Path='D:\repos\Aweosome-Video-Agent'}
)

foreach ($repo in $repos) {
    $Shortcut = $WshShell.CreateShortcut("$Desktop\$($repo.Name).lnk")
    $Shortcut.TargetPath = $repo.Path
    $Shortcut.WorkingDirectory = $repo.Path
    $Shortcut.Save()
    Write-Host "Criado: $($repo.Name).lnk"
}