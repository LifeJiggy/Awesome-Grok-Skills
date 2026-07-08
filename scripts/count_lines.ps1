Get-ChildItem -Path 'C:\Users\ADMIN\Python_Project\JavaScript\GROK\Awesome-Grok-Skills\agents' -Directory | ForEach-Object {
    $dir = $_.FullName
    $name = $_.Name
    Get-ChildItem -Path $dir -File | ForEach-Object {
        $lines = (Get-Content $_.FullName | Measure-Object -Line).Lines
        "$name|$($_.Name)|$lines"
    }
}
