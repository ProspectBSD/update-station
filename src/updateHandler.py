#!/usr/local/bin/python

from os import listdir, path
from subprocess import Popen, PIPE, STDOUT, call
ustation_db = '/var/db/update-station/'

pkglockfile = '%slock-pkgs' % ustation_db
pkglist = '/var/db/pkg-update-check/pkg-update-list'
fbsduf = '/var/db/freebsd-update-check/'
pkgupdatefile = ustation_db + 'pkg-to-upgrade'
fbtag = '%stag' % fbsduf
fblist = '%stag' % fbsduf
fbvcmd = "freebsd-version"
fblist = '%stag' % fbsduf
checkpkgupgrade = 'sudo operator fbsdpkgupdate check'
fetchpkgupgrade = 'sudo operator pkg upgrade -Fy'
isntallpkgupgrade = 'sudo operator pkg upgrade -y'
lockpkg = 'sudo operator pkg lock -y '
unlockallpkg = 'sudo operator pkg unlock -ay'
unlockpkg = 'sudo operator pkg unlock -y '

arch = Popen('uname -m', shell=True, stdin=PIPE, stdout=PIPE,
    stderr=STDOUT, close_fds=True).stdout.readlines()[0].rstrip()
release = Popen('uname -r', shell=True, stdin=PIPE, stdout=PIPE,
    stderr=STDOUT, close_fds=True).stdout.readlines()[0].rstrip()
if not path.isdir(ustation_db):
    Popen('sudo operator mkdir -p ' + ustation_db, shell=True, close_fds=True)
    Popen('sudo operator chmod -R 665 ' + ustation_db, shell=True, close_fds=True)
    Popen('sudo operator chown root:wheel ' + ustation_db, shell=True, close_fds=True)

fbsrcurl = "ftp://ftp.freebsd.org/pub/FreeBSD/releases/%s/%s/%s/src.txz" % (arch, arch, release)
fetchsrc = "sudo operator fetch %s" % fbsrcurl
extractsrc = "sudo operator tar Jxvf src.txz -C /"
fetchports = "sudo operator portsnap fetch"
extractports = "sudo operator portsnap extract"
updateports = "sudo operator portsnap update"
cleandesktop = "sudo operator sh /usr/local/lib/update-station/cleandesktop.sh"


def dowloadSrc():
    fetch = Popen('fetch %s' % fbsrcurl, shell=True, stdout=PIPE, close_fds=True)
    return fetch.stdout


def installSrc():
    extract = Popen(extractsrc, shell=True, stdout=PIPE, close_fds=True)
    return extract.stdout


def portsFetch():
    fetch = Popen(fetchports, shell=True, stdout=PIPE, close_fds=True)
    return fetch.stdout


def portsExtract():
    extract = Popen(extractports, shell=True, stdout=PIPE, close_fds=True)
    return extract.stdout


def portsUpdate():
    update = Popen(updateports, shell=True, stdout=PIPE, close_fds=True)
    return update.stdout


def IfPortsUpdated():
    fetch = Popen(fetchports, shell=True, stdout=PIPE, close_fds=True)
    if "No updates needed." in fetch.stdout.read():
        return False
    else:
        return True


def ifPortsIstall():
    if path.isdir('/usr/ports') is True:
        return True
    else:
        return False


def listOfInstal():
    ls = listdir(fbsduf)
    for line in ls:
        if 'install.' in line:
            uptag = open(fbsduf + line + '/INDEX-NEW', 'r')
            info = uptag.readlines()
            return info


def checkFreeBSDUpdate():
    check = 'sudo operator fbsdupdatecheck check'
    fbsdInstall = Popen(check, shell=True, stdin=PIPE, stdout=PIPE,
                        stderr=STDOUT, close_fds=True)
    if "updating to" in fbsdInstall.stdout.read():
        return True
    else:
        return False


def checkVersionUpdate():
    if path.exists(fbtag):
        uptag = open(fbtag, 'r')
        tag = uptag.readlines()[0].rstrip().split('|')
        upversion = tag[2] + "-p" + tag[3]
        fbv = Popen(fbvcmd, shell=True, stdin=PIPE, stdout=PIPE,
                    stderr=STDOUT, close_fds=True)
        fbsdversion = fbv.stdout.readlines()[0].rstrip()
        if fbsdversion == upversion:
            return False
        else:
            return True
    else:
        return True


def lookFbsdUpdate():
    if path.exists(fbtag):
        uptag = open(fbtag, 'r')
        tag = uptag.readlines()[0].rstrip().split('|')
        return "FreeBSD Update: " + tag[2] + "-p" + tag[3]
    else:
        return None


def updateText():
    udatetitle = lookFbsdUpdate()
    text = "Update Details:\n"
    text += "%s\n\n" % udatetitle
    text += "The following files will be update:\n"
    for line in listOfInstal():
        txtlist = line.split('|')
        text += "%s" % txtlist[0] + "\n"
    return text


def fetchFreeBSDUpdate():
    download = 'sudo operator fbsdupdatecheck fetch'
    fbsdDownload = Popen(download, shell=True, stdout=PIPE, close_fds=True)
    return fbsdDownload.stdout


def installFreeBSDUpdate():
    install = 'sudo operator fbsdupdatecheck install'
    fbsdInstall = Popen(install, shell=True, stdout=PIPE, close_fds=True)
    return fbsdInstall.stdout


def checkPkgUpdate():
    call(checkpkgupgrade, shell=True, stdout=PIPE, close_fds=True)


def runCheckUpdate():
    checkFreeBSDUpdate()
    checkPkgUpdate()


def CheckPkgUpdateFromFile():
    uptag = open(pkglist, 'r')
    if "UPGRADED:" in uptag.read():
        return True
    else:
        return False

def pkgUpdateList():
    uppkg = open(pkglist, 'r')
    pkgList = []
    for line in uppkg.readlines():
        if "->" in line:
            pkgList.append(line.rstrip()[1:])
    return pkgList


def lockPkg(lockPkg):
    for line in lockPkg:
        call(lockpkg + line.rstrip(), shell=True)
    return True


def unlockPkg():
    # unlock all pkg
    call(unlockpkg, shell=True)
    return True


def fetchPkgUpdate():
    fetch = Popen(fetchpkgupgrade, shell=True, stdout=PIPE, close_fds=True)
    return fetch.stdout


def installPkgUpdate():
    install = Popen(isntallpkgupgrade, shell=True, stdout=PIPE, close_fds=True)
    return install.stdout


def checkForUpdate():
    if checkVersionUpdate() is True or CheckPkgUpdateFromFile() is True:
        print True
        return True
    else:
        print False
        return False


def cleanDesktop():
    call(cleandesktop, shell=True)
    return