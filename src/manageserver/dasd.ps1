# just some fake data here
$exportObject = @(
    [PSCustomObject]@{
        'Server' = 'Server1.com'
        'Cube' = 'Cube1'
        'Connection Details' = 'Connection changed!'
    },
    [PSCustomObject]@{
        'Server' = 'Server2.com'
        'Cube' = 'Cube2'
        'Connection Details' = 'Connection Unchanged!'
    },
        [PSCustomObject]@{
        'Server' = 'Server3.com'
        'Cube' = 'Cube3'
        'Connection Details' = 'Connection changed!'
    }
)

function ConvertTo-HTMLTable ($obj) {
    # Accepts a System.Data.DataTable object or an array of PSObjects and converts to styled HTML table

    # add type needed to replace HTML special characters into entities
    Add-Type -AssemblyName System.Web

    $sb = New-Object -TypeName System.Text.StringBuilder
    [void]$sb.AppendLine('<table>')
    if ($null -ne $obj) {
        if (([object]$obj).GetType().FullName -eq 'System.Data.DataTable'){
            # it is a DataTable; convert to array of PSObjects
            $obj = $obj | Select-Object * -ExcludeProperty ItemArray, Table, RowError, RowState, HasErrors
        }
        $headers = $obj[0].PSObject.Properties | Select -ExpandProperty Name
        [void]$sb.AppendLine('<thead><tr>')
        foreach ($column in $headers) {
            [void]$sb.AppendLine(('<th>{0}</th>' -f [System.Web.HttpUtility]::HtmlEncode($column)))
        }
        [void]$sb.AppendLine('</tr></thead><tbody>')
        $row = 0
        $obj | ForEach-Object {
            # add inline style for zebra color rows
            if ($row++ -band 1) {
                $tr = '<tr style="background-color: {0};">' -f $oddRowBackColor
            } 
            else {
                $tr = '<tr>'
            }
            [void]$sb.AppendLine($tr)
            foreach ($column in $headers) {
                [string]$val = $($_.$column)
                if ([string]::IsNullOrWhiteSpace($val)) { 
                    $td = '<td>&nbsp;</td>' 
                } 
                else { 
                    $td = '<td>{0}</td>' -f [System.Web.HttpUtility]::HtmlEncode($val)
                }
                [void]$sb.Append($td)
            }
            [void]$sb.AppendLine('</tr>')
        }

        [void]$sb.AppendLine('</tbody>')
    }
    [void]$sb.AppendLine('</table>')

    return $sb.ToString()
}


$headerBackColor = '#4F81BD'  # backgroundcolor for column headers
$oddRowBackColor = '#DCE6F1'  # background color for odd rows

$style = @"
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <title>Report</title>
    <meta name="generator" content="PowerShell" />
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <style type="text/css">
    body {
        font-family: Verdana, Arial, Geneva, Helvetica, sans-serif;
        font-size: 12px;
        color: black;
    }
    table, td, th {
        border-color: black;
        border-style: solid;
        font-family: Verdana, Arial, Geneva, Helvetica, sans-serif;
        font-size: 11px;
    }
    table {
        border-width: 0 0 1px 1px;
        border-spacing: 0;
        border-collapse: collapse;
    }

    td, th {
        margin: 0;
        padding: 4px;
        border-width: 1px 1px 0 0;
        text-align: left;
    }
    th {
        color: white;
        background-color: $headerBackColor;
        font-weight: bold;
    }
    </style>
"@

$body = '{0}</head><body>{1}</body></html>' -f $style, (ConvertTo-HTMLTable $exportObject)
$smtpPort = 587
$smtpServer = "smtp.office365.com" 
$receiverEmail = "raghavendra.ga9@outlook.com",
"Raghavendra.Gandanahalli_EXT@medikind.com",
"kothakota.deepika_ext@mediakind.com"
$senderEmail = "raghavendra.ga9@outlook.com"
$password = "Rathna@123"
$SecurePassword = ConvertTo-SecureString -string $password -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential -argumentlist $senderEmail, $SecurePassword
Send-MailMessage -From $senderEmail -To $receiverEmail -Subject $subj -Body $body -BodyAsHtml -SmtpServer $smtpServer -Port $smtpPort -UseSsl -Credential (Get-Credential -Credential $Cred)