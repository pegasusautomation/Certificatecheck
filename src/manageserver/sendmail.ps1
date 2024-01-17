$smtpPort = 587
$smtpServer = "smtp.office365.com" 
$receiverEmail = "raghavendra.ga9@outlook.com"
$senderEmail = "raghavendra.ga9@outlook.com"
$password = "Rathna@123"

# $Password = "lcapqfbfhhraqbqnxfzgs"
$SecurePassword = ConvertTo-SecureString -string $password -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential -argumentlist $senderEmail, $SecurePassword


#Read more: https://www.sharepointdiary.com/2020/08/send-email-powershell.html#ixzz8OCoINH5r


$subj = "SERVER NOT ACTIVE ALERT"
$Body = "hi $vms is not active"

# formatted data file
# $attachmentPath = " "

# Send the email
Send-MailMessage -From $senderEmail -To $receiverEmail -Subject $subj -Body $Body -BodyAsHtml -SmtpServer $smtpServer -Port $smtpPort -UseSsl -Credential (Get-Credential -Credential $Cred)