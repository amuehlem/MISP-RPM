#!/bin/sh
HOST_RPM_SCRIPTDIR=$(pwd)

BUILDDIR=localbuild
rm -Rf $BUILDDIR
mkdir -p $BUILDDIR
cp ../SOURCES/fake-tgz.tgz $BUILDDIR/
cp ../SPECS/lief.spec $BUILDDIR/
cp pkg.lief pkg
docker run --volume $HOST_RPM_SCRIPTDIR/$BUILDDIR:/home/builder/rpm --volume $HOST_RPM_SCRIPTDIR:/srv -ti rpmbuild/centos7

echo ""
echo "RPMs built:"
find $BUILDDIR -name '*.rpm'

echo ""
