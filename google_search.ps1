param(
    [Parameter(Mandatory=$true)]
    [string]$Query,
    
    [Parameter(Mandatory=$true)]
    [string]$ApiKey,
    
    [Parameter(Mandatory=$true)]
    [string]$SearchEngineId
)

$url = "https://www.googleapis.com/customsearch/v1?q=$Query&key=$ApiKey&cx=$SearchEngineId"

try {
    $response = Invoke-RestMethod -Uri $url
    $response.items | Select-Object title, link | Export-Csv "results.csv" -NoTypeInformation
    Write-Host "Ergebnisse gespeichert in results.csv"
}
catch {
    Write-Host "Fehler: $_"
}