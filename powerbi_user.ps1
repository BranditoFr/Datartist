#!/usr/bin/powershell -Command

$path = $args[0]
$user="xxxx@myges.fr"
$pwd= ConvertTo-SecureString "xxxx" -AsPlainText -Force

$cred = New-Object System.Management.Automation.PSCredential($user,$pwd)

Connect-PowerBIServiceAccount -Credential $cred

$csv = Import-Csv $path -Header "email"

$csv | ForEach { 
    Write-Output $_
    Add-PowerBIWorkspaceUser -Id 51060895-0cea-429c-936d-a954babfb88a -UserEmailAddress $_.email -AccessRight Viewer
}

