#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.08.1
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		k3b
Summary:	K3b - CD Kreator
Name:		ka6-%{kaname}
Version:	25.08.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	7a7a2c2a28bb7f0f7c2331b5a5d807bb
Patch0:		musepack.patch
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	cmake >= 3.20
BuildRequires:	ffmpeg-devel
BuildRequires:	flac-c++-devel
BuildRequires:	ka6-libkcddb-devel
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-karchive-devel
BuildRequires:	kf6-kcmutils-devel
BuildRequires:	kf6-kconfig-devel
BuildRequires:	kf6-kcoreaddons-devel
BuildRequires:	kf6-kdoctools-devel
BuildRequires:	kf6-kfilemetadata-devel
BuildRequires:	kf6-ki18n-devel
BuildRequires:	kf6-kiconthemes-devel
BuildRequires:	kf6-kio-devel
BuildRequires:	kf6-kjobwidgets-devel
BuildRequires:	kf6-knewstuff-devel
BuildRequires:	kf6-knotifications-devel
BuildRequires:	kf6-knotifyconfig-devel
BuildRequires:	kf6-kservice-devel
BuildRequires:	kf6-kwidgetsaddons-devel
BuildRequires:	kf6-kxmlgui-devel
BuildRequires:	kf6-solid-devel
BuildRequires:	lame-libs-devel
BuildRequires:	libdvdread-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libmad-devel
BuildRequires:	libmpcdec-devel
#BuildRequires:	libmusicbrainz-devel
BuildRequires:	libogg-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libvorbis-devel
BuildRequires:	musepack-devel
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	taglib-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-data = %{version}-%{release}
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The CD Kreator features:
 - the most userfriendly interface ever ;-)
 - writing audio-CDs
 - writing ISO-CDs
 - writing existing iso-images to CD
 - CD copy (data, audio, mixed mode)
 - blanking of CD-RWs
 - CD ripping to WAV
 - dvd ripping with the transcode tools
 - DivX/XviD encoding
 - K3b checks if the user inserted an empty disk
 - Retrieving CD info and toc
 - Support for ATAPI drives without SCSI-emulation for reading
 - integrated full featured audio player

%description -l pl.UTF-8
Kreator CD oferuje:
 - najbardziej przyjazny interfejs użytkownika
 - zapisywanie Audio-CD
 - zapisywanie ISO-CD
 - zapisywanie istniejących obrazów ISO na CD
 - kopiowanie płyt (dane, audio, tryb mieszany)
 - czyszczenie płyt CD-RW
 - "rippowanie" CD do WAWów
 - "rippowanie" DVD z użyciem transkodujących narzędzi
 - kodowanie DivX/XviD
 - K3b sprawdza czy użytkownik włożył pustą płytę
 - odczytywanie informacje o płycie CD i spisu treści
 - wspiera napędy ATAPI bez emulacji SCSI do odczytu
 - zintegrowany odtwarzacz audio

%package data
Summary:	Data files for %{kaname}
Summary(pl.UTF-8):	Dane dla %{kaname}
Group:		X11/Applications
Requires(post,postun):	desktop-file-utils
Obsoletes:	ka5-%{kaname}-data < %{version}
BuildArch:	noarch

%description data
Data files for %{kaname}.

%description data -l pl.UTF-8
Dane dla %{kaname}.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}
%patch -P0 -p1

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6 \
	-DK3B_ENABLE_MUSICBRAINZ=OFF
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post data
%update_desktop_database_post

%postun data
%update_desktop_database_postun

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/k3b
%ghost %{_libdir}/libk3bdevice.so.8
%attr(755,root,root) %{_libdir}/libk3bdevice.so.*.*
%ghost %{_libdir}/libk3blib.so.8
%attr(755,root,root) %{_libdir}/libk3blib.so.*.*
%dir %{_libdir}/qt6/plugins/k3b_plugins
%attr(755,root,root) %{_libdir}/qt6/plugins/k3b_plugins/k3baudiometainforenamerplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/k3b_plugins/k3baudioprojectcddbplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/k3b_plugins/k3bexternalencoder.so
%attr(755,root,root) %{_libdir}/qt6/plugins/k3b_plugins/k3bffmpegdecoder.so
%attr(755,root,root) %{_libdir}/qt6/plugins/k3b_plugins/k3bflacdecoder.so
%attr(755,root,root) %{_libdir}/qt6/plugins/k3b_plugins/k3blameencoder.so
%attr(755,root,root) %{_libdir}/qt6/plugins/k3b_plugins/k3blibsndfiledecoder.so
%attr(755,root,root) %{_libdir}/qt6/plugins/k3b_plugins/k3bmaddecoder.so
%attr(755,root,root) %{_libdir}/qt6/plugins/k3b_plugins/k3bmpcdecoder.so
%attr(755,root,root) %{_libdir}/qt6/plugins/k3b_plugins/k3boggvorbisdecoder.so
%attr(755,root,root) %{_libdir}/qt6/plugins/k3b_plugins/k3boggvorbisencoder.so
%attr(755,root,root) %{_libdir}/qt6/plugins/k3b_plugins/k3bsoxencoder.so
%attr(755,root,root) %{_libdir}/qt6/plugins/k3b_plugins/k3bwavedecoder.so
%dir %{_libdir}/qt6/plugins/k3b_plugins/kcms
%attr(755,root,root) %{_libdir}/qt6/plugins/k3b_plugins/kcms/kcm_k3bexternalencoder.so
%attr(755,root,root) %{_libdir}/qt6/plugins/k3b_plugins/kcms/kcm_k3blameencoder.so
%attr(755,root,root) %{_libdir}/qt6/plugins/k3b_plugins/kcms/kcm_k3boggvorbisencoder.so
%attr(755,root,root) %{_libdir}/qt6/plugins/k3b_plugins/kcms/kcm_k3bsoxencoder.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kio/videodvd.so
%attr(755,root,root) %{_prefix}/libexec/kf6/kauth/k3bhelper

%files data -f %{kaname}.lang
%defattr(644,root,root,755)
%{_desktopdir}/org.kde.k3b.desktop
%{_datadir}/dbus-1/system-services/org.kde.k3b.service
%{_datadir}/dbus-1/system.d/org.kde.k3b.conf
%{_iconsdir}/hicolor/128x128/apps/k3b.png
%{_iconsdir}/hicolor/128x128/mimetypes/application-x-k3b.png
%{_iconsdir}/hicolor/16x16/apps/k3b.png
%{_iconsdir}/hicolor/22x22/apps/k3b.png
%{_iconsdir}/hicolor/32x32/apps/k3b.png
%{_iconsdir}/hicolor/32x32/mimetypes/application-x-k3b.png
%{_iconsdir}/hicolor/48x48/apps/k3b.png
%{_iconsdir}/hicolor/48x48/mimetypes/application-x-k3b.png
%{_iconsdir}/hicolor/64x64/apps/k3b.png
%{_iconsdir}/hicolor/64x64/mimetypes/application-x-k3b.png
%{_iconsdir}/hicolor/scalable/apps/k3b.svgz
%{_iconsdir}/hicolor/scalable/mimetypes/application-x-k3b.svgz
%{_datadir}/k3b
%{_datadir}/kio/servicemenus/k3b_create_audio_cd.desktop
%{_datadir}/kio/servicemenus/k3b_create_data_project.desktop
%{_datadir}/kio/servicemenus/k3b_create_video_cd.desktop
%{_datadir}/kio/servicemenus/k3b_write_bin_image.desktop
%{_datadir}/kio/servicemenus/k3b_write_iso_image.desktop
%{_datadir}/knotifications6/k3b.notifyrc
%{_datadir}/knsrcfiles/k3btheme.knsrc
%{_datadir}/konqsidebartng/virtual_folders/services/videodvd.desktop
%{_datadir}/metainfo/org.kde.k3b.appdata.xml
%{_datadir}/mime/packages/x-k3b.xml
%{_datadir}/polkit-1/actions/org.kde.k3b.policy
%{_datadir}/qlogging-categories6/k3b.categories
%{_datadir}/solid/actions/k3b_audiocd_rip.desktop
%{_datadir}/solid/actions/k3b_copy_disc.desktop
%{_datadir}/solid/actions/k3b_create_audio_cd_from_blank_medium.desktop
%{_datadir}/solid/actions/k3b_create_data_project_from_blank_medium.desktop
%{_datadir}/solid/actions/k3b_videodvd_rip.desktop

%files devel
%defattr(644,root,root,755)
%{_includedir}/k3b_export.h
%{_includedir}/k3bactivepipe.h
%{_includedir}/k3baudiocdtrackdrag.h
%{_includedir}/k3baudiocdtrackreader.h
%{_includedir}/k3baudiocdtracksource.h
%{_includedir}/k3baudiocuefilewritingjob.h
%{_includedir}/k3baudiodatasource.h
%{_includedir}/k3baudiodatasourceiterator.h
%{_includedir}/k3baudiodecoder.h
%{_includedir}/k3baudiodoc.h
%{_includedir}/k3baudiodocreader.h
%{_includedir}/k3baudioencoder.h
%{_includedir}/k3baudiofile.h
%{_includedir}/k3baudiofileanalyzerjob.h
%{_includedir}/k3baudiofilereader.h
%{_includedir}/k3baudiojob.h
%{_includedir}/k3baudiotrack.h
%{_includedir}/k3baudiotrackreader.h
%{_includedir}/k3baudiozerodata.h
%{_includedir}/k3baudiozerodatareader.h
%{_includedir}/k3bbinimagewritingjob.h
%{_includedir}/k3bblankingjob.h
%{_includedir}/k3bbootitem.h
%{_includedir}/k3bbusywidget.h
%{_includedir}/k3bcdcopyjob.h
%{_includedir}/k3bcddb.h
%{_includedir}/k3bcdparanoialib.h
%{_includedir}/k3bcdrdaowriter.h
%{_includedir}/k3bcdrecordwriter.h
%{_includedir}/k3bcdrskinwriter.h
%{_includedir}/k3bcdtext.h
%{_includedir}/k3bcdtextvalidator.h
%{_includedir}/k3bchecksumpipe.h
%{_includedir}/k3bclonejob.h
%{_includedir}/k3bcore.h
%{_includedir}/k3bcuefileparser.h
%{_includedir}/k3bdatadoc.h
%{_includedir}/k3bdataitem.h
%{_includedir}/k3bdatajob.h
%{_includedir}/k3bdefaultexternalprograms.h
%{_includedir}/k3bdevice.h
%{_includedir}/k3bdevice_export.h
%{_includedir}/k3bdevicecombobox.h
%{_includedir}/k3bdeviceglobals.h
%{_includedir}/k3bdevicehandler.h
%{_includedir}/k3bdevicemanager.h
%{_includedir}/k3bdeviceselectiondialog.h
%{_includedir}/k3bdevicetypes.h
%{_includedir}/k3bdiritem.h
%{_includedir}/k3bdirsizejob.h
%{_includedir}/k3bdiskinfo.h
%{_includedir}/k3bdoc.h
%{_includedir}/k3bdvdcopyjob.h
%{_includedir}/k3bdvdformattingjob.h
%{_includedir}/k3bexceptions.h
%{_includedir}/k3bexternalbinmanager.h
%{_includedir}/k3bfileitem.h
%{_includedir}/k3bfilesplitter.h
%{_includedir}/k3bfilesysteminfo.h
%{_includedir}/k3bglobals.h
%{_includedir}/k3bglobalsettings.h
%{_includedir}/k3bgrowisofswriter.h
%{_includedir}/k3bimagefilereader.h
%{_includedir}/k3binffilewriter.h
%{_includedir}/k3bintmapcombobox.h
%{_includedir}/k3bintvalidator.h
%{_includedir}/k3biso9660.h
%{_includedir}/k3biso9660backend.h
%{_includedir}/k3biso9660imagewritingjob.h
%{_includedir}/k3bisooptions.h
%{_includedir}/k3bjob.h
%{_includedir}/k3bjobhandler.h
%{_includedir}/k3bmd5job.h
%{_includedir}/k3bmediacache.h
%{_includedir}/k3bmedium.h
%{_includedir}/k3bmetawriter.h
%{_includedir}/k3bmixeddoc.h
%{_includedir}/k3bmixedjob.h
%{_includedir}/k3bmovixdoc.h
%{_includedir}/k3bmovixfileitem.h
%{_includedir}/k3bmovixjob.h
%{_includedir}/k3bmsf.h
%{_includedir}/k3bmsfedit.h
%{_includedir}/k3bmultichoicedialog.h
%{_includedir}/k3bplugin.h
%{_includedir}/k3bpluginconfigwidget.h
%{_includedir}/k3bpluginmanager.h
%{_includedir}/k3bprocess.h
%{_includedir}/k3bprojectplugin.h
%{_includedir}/k3brawaudiodatareader.h
%{_includedir}/k3brawaudiodatasource.h
%{_includedir}/k3bsignalwaiter.h
%{_includedir}/k3bsimplejobhandler.h
%{_includedir}/k3bstdguiitems.h
%{_includedir}/k3bthreadjob.h
%{_includedir}/k3bthreadwidget.h
%{_includedir}/k3bthroughputestimator.h
%{_includedir}/k3btoc.h
%{_includedir}/k3btocfilewriter.h
%{_includedir}/k3btrack.h
%{_includedir}/k3bvalidators.h
%{_includedir}/k3bvcddoc.h
%{_includedir}/k3bvcdjob.h
%{_includedir}/k3bvcdoptions.h
%{_includedir}/k3bverificationjob.h
%{_includedir}/k3bversion.h
%{_includedir}/k3bvideodvd.h
%{_includedir}/k3bvideodvdaudiostream.h
%{_includedir}/k3bvideodvddoc.h
%{_includedir}/k3bvideodvdjob.h
%{_includedir}/k3bvideodvdptt.h
%{_includedir}/k3bvideodvdsubpicturestream.h
%{_includedir}/k3bvideodvdtime.h
%{_includedir}/k3bvideodvdtitle.h
%{_includedir}/k3bvideodvdtitledetectclippingjob.h
%{_includedir}/k3bvideodvdtitletranscodingjob.h
%{_includedir}/k3bvideodvdvideostream.h
%{_includedir}/k3bwavefilewriter.h
%{_libdir}/libk3bdevice.so
%{_libdir}/libk3blib.so
