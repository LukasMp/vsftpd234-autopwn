# vsftpd234-autopwn
Autopwn exploit for vsFPTd 2.3.4 developed in Python 3. 
Developed by LukasMp

This exploit gives the user a reverse shell. It exploits the vulnerability of logging in with a user that includes the characters ":)" as part of its name, thus activating port 6200 that will provide a session as root


# Considerations to take into account:

- Modify the IP address of the *rhost* variable to that of the victim machine
- Modify (if necessary) the port that the FTP service runs from the *rport* variable
- The exploit works against the FTP service of version *vsftpd 2.3.4*
