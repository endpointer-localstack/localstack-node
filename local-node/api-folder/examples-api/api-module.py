import endpointer.email as ep_email

################################################ regular functions

def send_email(sender_name, receiver_email, subject, body):

    my_sender_email = 'yoursenderemailaccount'
    my_email_server_user = 'yoursenderemailserveruser'
    my_email_server_password = 'yoursenderemailserveruserpassword'
    my_smtp_server = 'yoursenderemailserver'
    my_smtp_port = 587

    ep_email.send_plain_email(

        sender_name,
        my_sender_email,
        my_email_server_user,
        my_email_server_password,
        receiver_email,
        subject,
        body,
        my_smtp_server,
        my_smtp_port
        
    )

################################################ input checking functions
################################################ response functions
################################################ db functions
