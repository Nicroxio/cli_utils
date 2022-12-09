# Maintainer: Nicroxio <Nic _at_ nicroxio dot co dot uk>
pkgname=shronk-cli-utils
pkgver=1.0.0
pkgrel=1
pkgdesc="A compilation of my own CLI Utils"
arch=("x86_64")
url="https://github.com/nicroxio/cli_utils"
license=('GPL3')
depends=("restic" "python-rich" "python" "python-click")
makedepends=("git")
source=("git+https://github.com/nicroxio/cli_utils.git")
sha256sums=("SKIP" "SKIP")

package() {
	cd $(pkgdir)/cli_utils
  cd cli_utils
	cp Backups.py /bin/backup
  cp Systemd_service.py /bin/mkservice
  }
