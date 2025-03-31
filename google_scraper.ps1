param(
    [string]$SearchTerm,
    [string]$OutputFile = "results.csv"
)

$Results = @()

$Response = Invoke-RestMethod -Uri "https://www.googleapis.com/customsearch/v1?q=$SearchTerm&key=YOUR_API_KEY&cx=YOUR_CX"

foreach ($Item in $Response.items) {
    $Results += [PSCustomObject]@{
        Title = $Item.title
        Link  = $Item.link
        Snippet = $Item.snippet
    }
}

$Results | Export-Csv -Path $OutputFile -NoTypeInformation
Write-Host "Ergebnisse gespeichert in $OutputFile"