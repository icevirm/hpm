# hpm
Hive Package Manager

hpm is a Python script which takes command-line parameters, such as -i, -u, -l, etc. and the name of a package and applies an corresponding action to the package.

For example,
`hpm -i bash` will (re)install bash,
`hpm -l ALL` will list all installed packages,
`hpm -u glibc` will uninstall glibc (effectively making the system unusable)

All parameters are available with `hpm -h`.

Packages configuration is described in a form of yaml file in pkg_def/ directory which contains instructions for configuring, building and other actions required for package managegement.

