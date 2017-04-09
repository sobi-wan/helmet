SUMMARY = "My test music"
DESCRIPTION = "Test Music"
HOMEPAGE = ""
LICENSE = "CLOSED"
RDEPENDS_${PN} += " python bash "

SRC_URI = "file://${BP}.tar.gz"

inherit bin_package

## The following code will package up the helmet-rootfs-1.0.0/ structure before
## the tar is fetched and extracted into the working dir
do_createtar () {
#!/usr/bin/bash
    echo "****** MY STUFF *******"
    cd ${FILE_DIRNAME}
    tar -cvzf files/helmet-rootfs-1.0.0.tar.gz helmet-rootfs-1.0.0/
}
addtask createtar before do_fetch
do_createtar[nostamp] = "1"
