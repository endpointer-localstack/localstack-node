import endpointer.email as ep_email

################################################ regular functions

def send_email(sender_name, receiver_email, subject, body):

    my_sender_email = 'youremail'
    my_sender_email_password = 'youremailpassword'
    my_smtp_server = 'yoursmtpserver'
    my_smtp_port = 465

    ep_email.send_plain_email(

        sender_name,
        my_sender_email,
        my_sender_email_password,
        receiver_email,
        subject,
        body,
        my_smtp_server,
        my_smtp_port
        
    )

################################################ input checking functions
################################################ response functions
################################################ db functions
