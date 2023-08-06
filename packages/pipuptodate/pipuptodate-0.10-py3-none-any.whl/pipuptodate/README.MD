# Updates all packages with pip in an environment - no dependencies 

### Tested against Windows 10 / Anaconda / Python 3.9.16

## pip install pipuptodate

```python


# How does it work
# 1) it creates a backup of the env if backupwholeenv is True
# 2) it downloads the wheels of all current installed packages if backuppackages is True
# 3) it does a dry run to get the highest compatible version and to resolve conflicts:
#    install --dry-run --progress-bar off --upgrade --upgrade-strategy eager --ignore-installed
# 4) it downloads the results from the dry run to download_folder
# 5) it installs the downloaded files

# How to use it 

from pipuptodate import update_pip_packages, restore_old_packages
update_pip_packages(
    download_folder="c:\\myupdatefolder21",  # all backups and the wheels of the new packages are stored here. Don't delete this folder. If anything goes wrong, you can restore the backup
    backuppackages=True,  # downloads all wheels from installed packages with the right version number
    backupwholeenv=True,  # makes a copy of all files in the env
)

# If something went wrong, you can install the previous versions:
restore_old_packages(
    requirementstxt="c:\\myupdatefolder21\backup\requirementsbackup.txt",  # created when you executed: update_pip_packages(...backuppackages=True)
    folder="c:\\myupdatefolder21\backup",  # the downloaded wheels


```