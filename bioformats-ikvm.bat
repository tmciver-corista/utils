
set projectdir=z:\Documents\workspace\BioFormatsTest

set jarfiles= ^
%projectdir%\build\bioformats-test.jar ^
%projectdir%\lib\bio-formats.jar ^
%projectdir%\lib\loci_plugins.jar ^
%projectdir%\lib\loci-common.jar ^
%projectdir%\lib\ij.jar ^
%projectdir%\lib\scifio.jar ^
%projectdir%\lib\slf4j-log4j12-1.6.1.jar ^
%projectdir%\lib\slf4j-api-1.6.1.jar ^
%projectdir%\lib\log4j-core.jar ^
%projectdir%\lib\log4j-1.2.15.jar ^
%projectdir%\lib\kryo-2.21.jar ^
%projectdir%\lib\ome-xml.jar ^
z:\Documents\bioformats-test-deps\metakit.jar ^
z:\Documents\bioformats-test-deps\mdbtools-java.jar

set jarfiles2= ^
%projectdir%\build\bioformats-test.jar ^
z:\Documents\bioformats-test-deps\loci_tools.jar ^
%projectdir%\lib\ij.jar

ikvmc -target:library -out:bioformats-small.dll -debug %jarfiles2%