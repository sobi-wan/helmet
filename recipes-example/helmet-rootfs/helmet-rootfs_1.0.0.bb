SUMMARY = "My test music"
DESCRIPTION = "Test Music"
HOMEPAGE = ""
LICENSE = "CLOSED"
RDEPENDS_${PN} += " python bash "

SRC_URI = "file://${BP}.tar.gz"

inherit bin_package

