$env_vars = Get-Content ../backend/.env
foreach ($env_var in $env_vars) {
    $parts = $env_var -split '='
    if ($parts.Length -eq 2) {
        $name = $parts[0].Trim()
        $value = $parts[1].Trim()
        [System.Environment]::SetEnvironmentVariable($name, $value, [System.EnvironmentVariableTarget]::Process)
        Write-Output "$name = $value"
    }
}