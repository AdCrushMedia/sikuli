import os
import sys
import json
import time
import getopt
import shutil
import ctypes
import zipfile
import hashlib 
import paramiko 
import functools
import subprocess

from collections import defaultdict

_NEW_ = "*new*"
_UPD_ = "*upd*"
_DEL_ = "*del*"

_ZIP_ = '.zip'
_JSON_ = '.json'
_PKGVER_ = 'version'+ _JSON_
_CHANGES_ = 'changes'+ _JSON_
_FILE_MAP_ = 'filemap'+ _JSON_
_SETTINGS_ = 'settings'+ _JSON_

__home = os.getcwd()
__temp_path = os.path.join(__home, 'temp')

__pkgver_path = os.path.join(__home, _PKGVER_)
__settings_path = os.path.join(__home, _SETTINGS_)

class AllowAnythingPolicy(paramiko.MissingHostKeyPolicy):
  def missing_host_key(self, client, hostname, key):
    return

def sftp_transcb(filepath, trans, spinner, bytes_so_far, bytes_total):
  sys.stdout.write('> sftp %s: %r %s (%d/%d)                         \r' % 
  	(trans, os.path.basename(filepath), spinner.next(), bytes_so_far, bytes_total))
  sys.stdout.flush()

def sftp_rexists(sftp, path):
	try:
		sftp.stat(path)
		return True
	except IOError, e:
		if e.errno == 2:
			return False
		return True

def sftp_upload(sftp, local_path, remote_path):
	spinner = spinning_cursor()
	cb = functools.partial(sftp_transcb, remote_path, 'put', spinner)
	remote_stat = sftp.put(local_path, remote_path, callback=cb, confirm=True)
	sys.stdout.write("\n")

	local_stat = os.stat(local_path)

	if remote_stat.st_size == local_stat.st_size:
		print '> transfer complete! remote file last modified: %s\n' % (
			time.ctime(remote_stat.st_mtime))
		
		return True

	else:
		print '> An error occured during the transfer..'
		return False

def sftp_download(sftp, remote_path, local_path):
	spinner = spinning_cursor()
	cb = functools.partial(sftp_transcb, remote_path, 'get', spinner)

	try:
		sftp.get(remote_path, local_path, callback=cb)
		sys.stdout.write("\n")
		return True

	except Exception, e:
		print "\n> An error occured during donwload"
		return False
	

def ask(question):
	# raw_input returns the empty string for "enter"
	yes = set(['yes','y', 'ye', ''])
	no = set(['no','n'])

	sys.stdout.write(question + ' [Y/n] ')

	while True:
		choice = raw_input().lower()
		if choice in yes:
			return True
		elif choice in no:
			return False
		else:
			sys.stdout.write('Please respond with [Y/n] ')

def Mbox(title, text, style=1):
  return ctypes.windll.user32.MessageBoxA(0, text, title, style)
  ##  Styles:
	##  0 : OK
	##  1 : OK | Cancel
	##  2 : Abort | Retry | Ignore
	##  3 : Yes | No | Cancel
	##  4 : Yes | No
	##  5 : Retry | No 
	##  6 : Cancel | Try Again | Continue

def spinning_cursor():
	while True:
		for cursor in '|/-\\':
			yield cursor

def checksum(fname):
	hash_md5 = hashlib.md5()
	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()

def get_hasver(sftp, rmt_ver_path):
	if not sftp_rexists(sftp, rmt_ver_path):
		return False
	else:
		return True

def rmvfile(filepath):
	if os.path.isfile(filepath):
		os.remove(filepath)

def rmvdir_contents(dirpath):
	for the_file in os.listdir(dirpath):
		file_path = os.path.join(dirpath, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print "> READ ONLY folder cant be deleted"
			print "> %S" % file_path

def reset():
	rmvfile(__pkgver_path)

	with open(__settings_path) as settings_file:
		settings = json.load(settings_file)
		watch_folder = settings['watch_folder']
		
		rmvdir_contents(watch_folder)
		rmvdir_contents(__temp_path)

def extract(zipath, dest):
	filename = os.path.basename(zipath)
	print "> Extracting package '%s'" % filename

	with zipfile.ZipFile(zipath, "r") as z:
		try:
			z.extractall(dest)
			z.close()
			return True

		except:
			print "> Error on zip extract. \n>'%s'" % filename
			return False

def check_integrity(watch_folder):

	print '# Checking for file integrity'
	
	fmap = defaultdict(dict)
	spinner = spinning_cursor()

	filemap_path = os.path.join(watch_folder, _FILE_MAP_)
	with open(filemap_path) as fmout:
		fmap = json.load(fmout)

		for path, csum in fmap['map'].items():
			target = os.path.join(watch_folder, path)
			if os.path.isfile(target):
				localcsum = checksum(target)
				same = localcsum == csum

				if same:
					sys.stdout.write('> %s %s\r' % (csum, spinner.next()))
					sys.stdout.flush()
					time.sleep(0.002)
				else:
					print "> Bad checksum: %s %s" % (csum, path)

  	print "\n> done.."

def checkploy(tempver_path, watch_folder):
	changes = defaultdict(dict)
	fmap = defaultdict(dict)

	changes_path = os.path.join(tempver_path, _CHANGES_)

	with open(changes_path) as fileout:
		changes = json.load(fileout)
		csum = changes['checksum']

	filemap_path = os.path.join(tempver_path, _FILE_MAP_)
	with open(filemap_path) as fmout:
		fmap = json.load(fmout)

	pkgzip_path = os.path.join(tempver_path, csum + _ZIP_)

	extr_dest = os.path.join(tempver_path, csum)
	if not os.path.exists(extr_dest):
		os.makedirs(extr_dest)

	if extract(pkgzip_path, extr_dest):
		print '> Checking for file integrity at temp level'

		for path, csum in fmap['map'].items():
			target = os.path.join(extr_dest, path)
			if os.path.isfile(target):
				localcsum = checksum(target)
				same = localcsum == csum

				if same:
					sys.stdout.write('> %s\r' % csum)
					sys.stdout.flush()
				else:
					print "> Bad checksum: local: %s >> %s %s" % (csum, localcsum, path)
					return False

		print '> checksum passed.. '
		rmvdir_contents(extr_dest)
		os.rmdir(extr_dest)

	print "\n# Deploying version package"

	if not extract(pkgzip_path, watch_folder):
		return False

	for path, tag in changes['pkg'].items():
		if tag == _DEL_:
			abspath = os.path.join(watch_folder, path)
			rmvfile(abspath)

	return True

def deploy_pkg(pkgpath, watch_folder, version):
	filename = os.path.basename(pkgpath)
	fn, fe = os.path.splitext(filename)

	extr_dest = os.path.join(__temp_path, fn)
	if not os.path.exists(extr_dest):
		os.makedirs(extr_dest)

	if not extract(pkgpath, extr_dest):
		return False

	if not checkploy(extr_dest, watch_folder):
		return False
	
	else:
		pkgver = defaultdict(dict)
		pkgver['version'] = version
		with open(__pkgver_path, 'w') as pvout:
			json.dump(pkgver, pvout)

		print "> Package deployed. Current version: %d\n" % version

	return True
	

def analyze(watch_folder, ver):
	changes = defaultdict(dict)
	changes_path = os.path.join(watch_folder, _CHANGES_)

	with open(changes_path) as fileout:
		changes = json.load(fileout)

		if ver != changes['version']:
			print '> package version not the same [%d.zip]' % ver
			return False

		zipname = changes['checksum']+ _ZIP_
		pkgzip = os.path.join(watch_folder, zipname)

		if not os.path.isfile(pkgzip):
			print "> package %s not found in '%s.zip'" % (changes['checksum'], ver)
			return False

		extract(pkgzip, watch_folder, zipname)
		rmvfile(pkgzip)

		print '> root folder: %s' % watch_folder
		for path, tag in changes['pkg'].items():
			print "> %s %s" % (tag, path)
			if tag == _DEL_:
				abspath = os.path.join(watch_folder, path)
				rmvfile(abspath)

	rmvfile(changes_path)

def run_cmd(exe, arg):
	print "> running defined command.."
	if os.path.isfile(exe):
		p = subprocess.Popen([exe, arg])
	else:
		print "> Cant find defined 'exe_to_run' path"
		print '> Please check your settings'
	
# --- main

def main_puller():
	_pkgver = defaultdict(dict)

	if not os.path.isfile(__settings_path):
		print '> Cant find required file \'%s\'' %(_SETTINGS_)
		sys.exit()

	# -- load settings variables 

	with open(__settings_path) as settings_file:
		_settings = json.load(settings_file)
		_address = _settings['ftp']['address']
		_username = _settings['ftp']['username']
		_password = _settings['ftp']['password']

		_keep_pkg = _settings['keep_pkg']
		_ftp_home = _settings['ftp_home']
		_app_title = _settings['app_title']
		_watch_folder = _settings['watch_folder']

		_exe_to_run = _settings['exe_to_run']
		_exe_argument = _settings['exe_argument']

	if not os.path.exists(_watch_folder):
		print "> Defined watch folder not found!"
		print "> %s" % _watch_folder
		print "\n> Please check your settings"
		
		errmsg = "> Defined watch folder not found!\n> %s\n> Please check your settings" % _watch_folder
		Mbox( "Settings Problem", str(errmsg), 0)

		sys.exit()

	if not os.path.exists(__temp_path):
		os.makedirs(__temp_path)

	if not os.path.isfile(__pkgver_path):
		print "> Cant find '%s'. Assumed first pull setting version to 0" % _PKGVER_
		_pkgver['version'] = 0

	else:
		with open(__pkgver_path) as pkgver_file:
			_pkgver = json.load(pkgver_file)

	print "# Current version: %d" % _pkgver['version']

	user_ok = False
	box_title = "Package Update for '%s'" % _app_title
	box_msg = "An update has been detected. Click 'OK' to download or 'Cancel' to ingore."

	print '# Connecting to server \'%s\'' % _address

	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(AllowAnythingPolicy())
	client.connect(_address, username=_username, password=_password)
	_sftp = client.open_sftp()

	print '# Checking for updates..'
	version = _pkgver['version']

	while True:
		version += 1
		verzip = str(version)+ _ZIP_
		remote_verpkg = os.path.join(_ftp_home, verzip)

		if not get_hasver(_sftp, remote_verpkg):
			print '> No updates detected..'
			break
		
		else:

			if not user_ok:
				if Mbox( str(box_title), box_msg) == 1:
					user_ok = True
				else:
					sys.exit()

			pkgver_zip = os.path.join(__temp_path, verzip)

			if not sftp_download(_sftp, remote_verpkg, pkgver_zip):
				sys.exit()
			
			if not deploy_pkg(pkgver_zip, _watch_folder, version):
				sys.exit()


	_sftp.close()
	client.close()

	run_cmd(_exe_to_run, _exe_argument)

def print_help():
	print 'puller.py [-h]'

def main(argv):
	try:
		opts,args = getopt.getopt(argv,"hxp", ['help', 'reset', 'pull'])
	except getopt.GetoptError:
		print_help()

	for opt, arg in opts:
		if opt == '-h':
			print_help()
			sys.exit()

		elif opt in ("-x", "--reset"):
			reset() # for debugging only
			sys.exit()

		elif opt in ("-p", "--pull"):
			print ''

	main_puller()

if __name__ == "__main__":
	main(sys.argv[1:])