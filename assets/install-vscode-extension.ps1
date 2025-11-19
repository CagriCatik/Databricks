# Install-VSCodeExtension.ps1

param (
    [string]$ExtensionId
)

# Function to check if VS Code is installed and the `code` command is available
function Check-VSCodeInstallation {
    if (-not (Get-Command "code" -ErrorAction SilentlyContinue)) {
        Write-Host "VS Code is not installed or 'code' command is not added to PATH."
        Write-Host "Please ensure VS Code is installed and 'code' command is available in the terminal."
        return $false
    }
    return $true
}

# Function to install a VS Code extension given its unique ID
function Install-VSCodeExtension {
    param (
        [string]$ExtensionId
    )

    if (Check-VSCodeInstallation) {
        Write-Host "Installing VS Code extension: $ExtensionId"
        Start-Process -NoNewWindow -FilePath "code" -ArgumentList "--install-extension $ExtensionId"
        Write-Host "Extension $ExtensionId installation command executed. Check VS Code for confirmation."
    } else {
        Write-Host "VS Code installation check failed. Please ensure VS Code is installed and 'code' command is in PATH."
    }
}

# Main Execution
if (-not $ExtensionId) {
    Write-Host "Please provide an Extension ID as a parameter. Example: './Install-VSCodeExtension.ps1 -ExtensionId ms-python.python'"
    exit
}

Install-VSCodeExtension -ExtensionId $ExtensionId
