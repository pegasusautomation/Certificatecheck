$logFileDir = '.'
$job = $null
$currLogFile = $null

while ($true)
{

  # Check for new content of interest from the background job.
  if ($job -and ($result = Receive-Job $job)) {
    # Send an email here, e.g.:
    # Send-MailMessage -SmtpServer exchange.example.com -From alerts@example.com -To jdoe@example.com -Subject 'Error' -Body $result
    # Send the email
        # Send mail if the server is in off state
        # Office 365 credentials
        $username = "raghavendra.ga9@outlook.com"
        $password = Get-Content 'C:\manageserver\mysecurestring.txt' | ConvertTo-SecureString
        $credential = new-object -typename System.Management.Automation.PSCredential `
            -argumentlist $username, $password 

        # Sender and recipient email addresses
        $sender = "raghavendra.ga9@outlook.com"
        $recipient = "raghavendra.ga9@outlook.com"

        # SMTP server and port for Office 365
        $smtpServer = "smtp.office365.com"
        $smtpPort = 587

        # Email subject and body
        $subject = "SERVER NOT ACTIVE ALERT"
        $body = $result

        # Create the email message
        $mailParams = @{
            From       = $sender
            To         = $recipient
            Subject    = $subject
            Body       = $body
            SmtpServer = $smtpServer
            Port       = $smtpPort
            Credential = $credential
            UseSsl     = $true
        }
        Send-MailMessage @mailParams
  }

  # See if a new log file has appeared.
  # For simplicity, go by creation date.
  # If a new file only appears once a day, you could keep track
  # of the current calendar date and only look when it changes.
  $newLogFile = (Get-ChildItem -File "$logFile/*_*_*.txt" | 
                  Sort-Object -Descending CreationTime | 
                    Select-Object -First 1).FullName
  
  if ($newLogFile -ne $currLogFile) {

    # If there's a current job for the previous log file, terminate it now.
    if ($job) { Remove-Job $job -Force }

    # Create a job for the new log file.
    $currLogFile = $newLogFile
    $job = Start-Job {
       # Wait indefinitely for content to be added to the file,
       # and output lines matching the string of interest.
       Get-Content -LiteralPath $using:currLogFile -Wait 
    #    |
    #      Where-Object { $_ -match "ERROR" }
    }

  }

  # Sleep a little.
  Start-Sleep -Seconds 1
}
