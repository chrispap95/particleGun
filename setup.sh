#!/bin/bash -e

# Created based on template from Kevin Pedro's script for SVJ analysis

case `uname` in
	Linux) ECHO="echo -e" ;;
	*) ECHO="echo" ;;
esac

ACCESS=https

usage() {
	$ECHO "setup.sh [options]"
	$ECHO
	$ECHO "Options:"
	$ECHO "-c <RELEASE>  \tCMSSW release to install (e.g. CMSSW_11_3_1_patch1)"
	$ECHO "-f [fork]     \tclone from specified fork (default = chrispap95)"
	$ECHO "-b [branch]   \tclone specified branch (default = master)"
	$ECHO "-s            \tuse protocol to clone (default = ${ACCESS}, alternative = ssh)"
	$ECHO "-h            \tprint this message and exit"
	exit $1
}

CUR_DIR=`pwd`
WHICH_CMSSW=""
FORK=chrispap95
BRANCH=topic_chrispap
#check arguments
while getopts "c:f:b:s:h" opt; do
	case "$opt" in
	c) WHICH_CMSSW=$OPTARG
	;;
	f) FORK=$OPTARG
	;;
	b) BRANCH=$OPTARG
	;;
	s) ACCESS=$OPTARG
	;;
	h) usage 0
	;;
	esac
done

if [ -z "$WHICH_CMSSW" ]; then
	usage 1
fi

if [ "$ACCESS" = "ssh" ]; then
	export ACCESS_GITHUB=git@github.com:
	export ACCESS_CMSSW=--ssh
elif [ "$ACCESS" = "https" ]; then
	export ACCESS_GITHUB=https://github.com/
	export ACCESS_CMSSW=--https
else
	usage 1
fi

# OS check
if [[ `uname -r` == *"el6"* ]]; then
	SLC_VERSION="slc6"
	$ECHO "Unsupported architecture $SLC_VERSION. Please switch to slc7."
	exit 1
elif [[ `uname -r` == *"el7"* ]]; then
	SLC_VERSION="slc7"
	$ECHO "Detected $SLC_VERSION architecture."
elif [[ -f "/etc/redhat-release" ]]; then
	VERSION_TMP=`awk -F'[ .]' '{print $4}' "/etc/redhat-release"`
	POSSIBLE_VERSIONS=( 6 7 )
	if [[ "${POSSIBLE_VERSIONS[@]} " =~ " ${VERSION_TMP}" ]]; then
		SLC_VERSION="slc${VERSION_TMP}"
		if [[ "$SLC_VERSION" == "slc6" ]]; then
			$ECHO "Unsupported architecture $SLC_VERSION. Please switch to slc7."
			exit 1
		else
			$ECHO "Detected $SLC_VERSION architecture."
		fi
	else
		$ECHO "WARNING::Unknown SLC version. Defaulting to slc7."
		SLC_VERSION="slc7"
	fi
else
	$ECHO "WARNING::Unknown SLC version. Defaulting to slc7."
	SLC_VERSION="slc7"
fi

# -------------------------------------------------------------------------------------
# CMSSW release area
# -------------------------------------------------------------------------------------
if [ -n "$WHICH_CMSSW" ]; then
	case $WHICH_CMSSW in
	CMSSW_10_6_*)
		export SCRAM_ARCH=${SLC_VERSION}_amd64_gcc820
	;;
	CMSSW_11_1_*)
		export SCRAM_ARCH=${SLC_VERSION}_amd64_gcc820
	;;
	CMSSW_11_2_*)
		export SCRAM_ARCH=${SLC_VERSION}_amd64_gcc900
	;;
	CMSSW_11_3_*)
		export SCRAM_ARCH=${SLC_VERSION}_amd64_gcc900
	;;
	CMSSW_11_4_*)
		export SCRAM_ARCH=${SLC_VERSION}_amd64_gcc900
	;;
	CMSSW_12_*)
		export SCRAM_ARCH=${SLC_VERSION}_amd64_gcc900
	;;
	*)
		$ECHO "Unknown architecture for release $WHICH_CMSSW."
		$ECHO "Make sure it is at least CMSSW_10_6_X."
		exit 1
	;;
	esac
	scramv1 project CMSSW $WHICH_CMSSW
	cd $WHICH_CMSSW
	CUR_DIR=`pwd`
	eval `scramv1 runtime -sh`
	$ECHO "setup $CMSSW_VERSION"
fi

# -------------------------------------------------------------------------------------
# CMSSW compilation
# -------------------------------------------------------------------------------------

if [ -n "$WHICH_CMSSW" ]; then
	# reinitialize environment
	eval `scramv1 runtime -sh`
	cd src
	#git cms-init $ACCESS_CMSSW

	# CMSSW_10_X_Y needs the HGCalAnalysis ntuplizer
	# CMSSW_11_2_0_pre3 and below work with reco-ntuples ntuplizer
	# CMSSW_11_2_0_pre4 and above work with a patched reco-ntuples ntuplizer
	# See https://github.com/cms-sw/cmssw/pull/31013 for more details
	if [[ "$WHICH_CMSSW" == *"CMSSW_11_"[0-1]* || "$WHICH_CMSSW" == *"CMSSW_11_2_0_pre"[123]  ]]; then
		git clone ${ACCESS_GITHUB}${FORK}/reco-ntuples RecoNtuples -b topic_chrispap_old
		git clone ${ACCESS_GITHUB}chrispap95/particleGun
		mkdir particleGun/myGeneration
	elif [[ "$WHICH_CMSSW" == *"CMSSW_11_"[2-9]* || "$WHICH_CMSSW" == *"CMSSW_12_"* ]]; then
		git clone ${ACCESS_GITHUB}${FORK}/reco-ntuples RecoNtuples -b topic_chrispap
		git clone ${ACCESS_GITHUB}chrispap95/particleGun
		mkdir particleGun/myGeneration
	elif [[ "$WHICH_CMSSW" == *"CMSSW_10_6"* ]]; then
		git clone ${ACCESS_GITHUB}${FORK}/HGCalAnalysis HGCalAnalysis -b rechitDetID
		git clone ${ACCESS_GITHUB}chrispap95/particleGun -b CMSSW_10_6_3_patch1-2026D41
		mkdir particleGun/myGeneration
	else
		$ECHO "Unknown CMSSW configuration: $WHICH_CMSSW"
		$ECHO "Cannot find an appropriate ntuplizer. You need to set up ntuples step manually."
	fi

	mkdir -pv Configuration/GenProduction/python

	scram b -j 8
	cd particleGun
fi
