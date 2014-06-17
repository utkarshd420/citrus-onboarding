import imaplib, email

#log in and select the inbox
def email_rec(bank_obj):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('citruspay.bankrelations@gmail.com', 'ASDFGHJKLqwertyuiop')
    mail.select('inbox')

    #get uids of all messages
    result, data = mail.uid('search', None, 'X-GM-RAW',r'has:attachment from:' + str(bank_obj.bank.email))
    uids = data[0].split()

    #read the lastest message
    result, data = mail.uid('fetch', uids[-1], '(RFC822)')
    m = email.message_from_string(data[0][1].strip())
    if m.get_content_maintype() == 'multipart': #multipart messages only
        for part in m.walk():
            #find the attachment part
            if part.get_content_maintype() == 'multipart': continue
            if part.get('Content-Disposition') is None: continue

            #save the attachment in the program directory
            filename = 'received file/'+part.get_filename()
            fp = open(filename, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()
            return part.get_filename()

