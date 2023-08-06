import subprocess
import sys
import os
import shutil
from typing import Union

fo = os.path.join(os.path.abspath(os.path.dirname(sys.executable)))

cmdbase = os.path.normpath(os.path.join(fo, "Scripts", "pip.exe"))


def execute_subprocess(
    cmd: str,
    end_of_printline: str = "",
) -> list:
    popen = None

    def run_subprocess(cmd):
        nonlocal popen

        try:
            popen = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, universal_newlines=True
            )
            counter = -1
            for stdout_line in iter(popen.stdout.readline, ""):
                counter += 1
                try:
                    yield stdout_line
                except Exception as Fehler:
                    continue
            popen.stdout.close()
            return_code = popen.wait()
        except Exception as Fehler:
            print(Fehler)
            try:
                popen.stdout.close()
                return_code = popen.wait()
            except Exception as Fehler:
                yield ""

    proxyresults = []
    try:
        for proxyresult in run_subprocess(cmd):
            proxyresults.append(proxyresult)
            print(proxyresult, end=end_of_printline)
    except BaseException:
        try:
            popen.kill()
            popen = None
        except Exception as da:
            print(da)

    try:
        if popen is not None:
            popen.kill()
    except Exception as da:
        pass

    return proxyresults


class CTError(Exception):
    def __init__(self, errors):
        self.errors = errors


try:
    O_BINARY = os.O_BINARY
except:
    O_BINARY = 0
READ_FLAGS = os.O_RDONLY | O_BINARY
WRITE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | O_BINARY
BUFFER_SIZE = 32 * 1024


def copyfile(src: str, dst: str, copystat: bool = False) -> bool:
    copyok = False
    try:
        fin = os.open(src, READ_FLAGS)
        stat = os.fstat(fin)
        fout = os.open(dst, WRITE_FLAGS, stat.st_mode)
        for x in iter(lambda: os.read(fin, BUFFER_SIZE), b""):
            os.write(fout, x)
        print(dst, end="\r")

        copyok = True
    finally:
        try:
            os.close(fin)
        except Exception:
            pass
        try:
            os.close(fout)
        except Exception:
            pass
    if copystat:
        try:
            shutil.copystat(src, dst)
            return True
        except Exception:
            return False
    if copyok:
        return True
    return False


def movefile(src: str, dst: str, copystat: bool = False) -> bool:
    copyok = False
    try:
        fin = os.open(src, READ_FLAGS)
        stat = os.fstat(fin)
        fout = os.open(dst, WRITE_FLAGS, stat.st_mode)
        for x in iter(lambda: os.read(fin, BUFFER_SIZE), b""):
            os.write(fout, x)
        print(dst, end="\r")
        copyok = True
    finally:
        try:
            os.close(fin)
        except Exception:
            pass
        try:
            os.close(fout)
        except Exception:
            pass
    if copystat and copyok:
        try:
            shutil.copystat(src, dst)
        except Exception:
            return False
    if copyok:
        try:
            os.remove(src)
            return True

        except Exception:
            return False
    return False


def copytree(
    src: str, dst: str, ignore: Union[list, type(None)] = None, symlinks: bool = False
):
    if ignore is None:
        ignore = []
    names = os.listdir(src)

    if not os.path.exists(dst):
        os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignore:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, ignore, symlinks)
            else:
                copyfile(srcname, dstname)

        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        except CTError as err:
            errors.extend(err.errors)
    if errors:
        raise CTError(errors)


def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def restore_old_packages(
    requirementstxt,
    folder,
):
    updateinstallcmd = f"{cmdbase} install --no-index --find-links={folder} --upgrade -r {requirementstxt}"
    execute_subprocess(updateinstallcmd, end_of_printline="")


def update_pip_packages(
    download_folder,
    backuppackages=True,
    backupwholeenv=True,
):
    download_folder = os.path.normpath(download_folder)
    updatefolderbackup = os.path.join(download_folder, "backup")
    updatefolderbackupenv = os.path.join(download_folder, "backupenv")
    create_folder(updatefolderbackupenv)
    if backupwholeenv:
        copytree(fo, updatefolderbackupenv)

    create_folder(updatefolderbackup)
    newversion = os.path.join(download_folder, "updated")
    create_folder(newversion)
    savereq = os.path.join(download_folder, "backup", "requirementsbackup.txt")
    updatedreq = os.path.join(download_folder, "updated", "requirementsnov.txt")
    updatedreqsorted = os.path.join(
        download_folder, "updated", "requirementsnovsort.txt"
    )
    cmdfreeze = cmdbase + " freeze"
    results = execute_subprocess(
        cmdfreeze,
        end_of_printline="",
    )
    allresults = "".join(results)
    with open(savereq, mode="w", encoding="utf-8") as f:
        f.write(allresults)
    print("Installed packages: \n==================================")
    print(allresults)

    oldw = os.getcwd()
    os.chdir(updatefolderbackup)
    if backuppackages:
        for res in results:
            backuppa = (
                cmdbase
                + f" download --dest {updatefolderbackup} --progress-bar off --ignore-requires-python {res.strip()} "
            )
            execute_subprocess(
                backuppa,
                end_of_printline="",
            )
    os.chdir(oldw)

    allpanames = [x.split("==")[0] for x in results if "==" in x]
    allresultsup = "\n".join(allpanames).strip()
    with open(updatedreq, mode="w", encoding="utf-8") as f:
        f.write(allresultsup)

    print("Starting dryrun")
    dryrun = (
        cmdbase
        + f" install --dry-run --progress-bar off --upgrade --upgrade-strategy eager --ignore-installed -r {updatedreq}"
    )
    dryrunresult = execute_subprocess(
        dryrun,
        end_of_printline="",
    )

    packagestoinstall = "\n".join(
        [
            "-".join(q.split("-")[:-1]) + "==" + q.split("-")[-1]
            for q in dryrunresult[-1].split()[2:]
        ]
    )

    with open(updatedreqsorted, mode="w", encoding="utf-8") as f:
        f.write(packagestoinstall)
    print("Packages are being downloaded and installed")
    print(packagestoinstall)

    os.chdir(newversion)
    downloadupfilescmd = (
        cmdbase
        + f" download --dest {newversion} --progress-bar off --ignore-requires-python -r {updatedreqsorted} "
    )
    execute_subprocess(
        downloadupfilescmd,
        end_of_printline="",
    )

    os.chdir(oldw)

    updateinstallcmd = f"{cmdbase} install --no-index --find-links={newversion} --upgrade -r {updatedreqsorted}"
    execute_subprocess(
        updateinstallcmd,
        end_of_printline="",
    )

