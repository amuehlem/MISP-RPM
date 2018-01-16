#!/bin/sh
HOST_RPM_SCRIPTDIR=$(pwd)

BUILDDIR=localbuild
rm -Rf $BUILDDIR
mkdir -p $BUILDDIR
cp ../SOURCES/{fake-tgz.tgz,misp.conf,misp-*.pp} $BUILDDIR/
cp ../SPECS/misp.spec $BUILDDIR/
cp pkg.misp pkg
docker run --volume $HOST_RPM_SCRIPTDIR/$BUILDDIR:/home/builder/rpm --volume $HOST_RPM_SCRIPTDIR:/srv -ti rpmbuild/centos7

echo ""
echo "RPMs built:"
find $BUILDDIR -name '*.rpm'

echo ""
