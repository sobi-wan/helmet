import ftplib
import os

chunk_counter = 0
def upload(ftp, file):
	chunk_counter = 0
	ext = os.path.splitext(file)[1]
	fname = os.path.basename(file)
	if ext in (".txt", ".htm", ".html"):
		ftp.storlines("STOR " + fname, open(file))
	else:
		ftp.storbinary("STOR " + fname, open(file, "rb"), 1024)
	print "Upload of '", fname, "' complete."

def ftp_open(server_address, credentials):
	ftp = ftplib.FTP(server_address)
	user = credentials[0]
	pw = credentials[1]
	ftp.login(user, pw)
	return ftp

def upload_cb(param):
	print "upload chunk ok:", len(param)

#ftp = ftp_open("joshs-mbp", ("joshwest", "endorphine6"))
#ftp.cwd("hummingboard/")
#upload(ftp, "josh.py")
#ftp.quit()
