#!/bin/bash

while getopts v:r: option
do
case "${option}"
in
v) VERSION=${OPTARG};;
r) RELEASE=${OPTARG};;
esac
done

DUT='10.111.111.1'
mkdir -p rpmbuild/SOURCES
mkdir -p rpmbuild/RPM
tar -cvf rpmbuild/SOURCES/PbrMon-${VERSION}-${RELEASE}.tar source/*

cd /workspaces/pbrmon/rpmbuild/SPECS

rpmbuild -ba PbrMon.spec

cd /workspaces/pbrmon

rm manifest.txt

echo "format: 1" >> manifest.txt
echo "primaryRPM: PbrMon-${VERSION}-${RELEASE}.noarch.rpm" >> manifest.txt
echo -n "PbrMon-${VERSION}-${RELEASE}.noarch.rpm: " >> manifest.txt
echo $(sha1sum rpmbuild/RPM/noarch/PbrMon-${VERSION}-${RELEASE}.noarch.rpm | awk '{print $1}') >> manifest.txt

scp -i ~/.ssh/builder /workspaces/pbrmon/rpmbuild/RPM/noarch/PbrMon-${VERSION}-${RELEASE}.noarch.rpm builder@${DUT}:/mnt/flash/ext-eos/
scp -i ~/.ssh/builder manifest.txt builder@${DUT}:/mnt/flash/ext-eos/

ssh -i ~/.ssh/builder builder@${DUT} swix create /mnt/flash/ext-eos/swix/PbrMon-${VERSION}-${RELEASE}.swix /mnt/flash/ext-eos/PbrMon-${VERSION}-${RELEASE}.noarch.rpm

scp -i ~/.ssh/builder builder@${DUT}:/mnt/flash/ext-eos/swix/PbrMon-${VERSION}-${RELEASE}.swix /workspaces/pbrmon/