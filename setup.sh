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
	$ECHO "-c <RELEASE>  \tCMSSW release to install (e.g. CMSSW_11_1_0_pre6)"
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
		echo "WARNING::Unknown SLC version. Defaulting to slc7."
		SLC_VERSION="slc7"
	fi
else
	echo "WARNING::Unknown SLC version. Defaulting to slc7."
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
	*)
		$ECHO "Unknown architecture for release $WHICH_CMSSW"
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
	git cms-init $ACCESS_CMSSW

	git clone ${ACCESS_GITHUB}chrispap95/particleGun particleGun
  mkdir particleGun/myGeneration
	if [[ $WHICH_CMSSW == *"CMSSW_11_"* ]]; then
    git clone ${ACCESS_GITHUB}${FORK}/reco-ntuples RecoNtuples -b topic_chrispap
  else
    git clone ${ACCESS_GITHUB}${FORK}/HGCalAnalysis hgcalAnalysis -b rechitDetID
  fi

	# use as little of genproductions as possible
	git clone --depth 1 --no-checkout ${ACCESS_GITHUB}cms-sw/genproductions Configuration/GenProduction
	# setup sparse checkout
	cd Configuration/GenProduction
	git config core.sparsecheckout true
	{
		echo '/python/Guns'
	} > .git/info/sparse-checkout
	git read-tree -mu HEAD
	cd $CMSSW_BASE/src

	scram b -j 8
	cd particleGun
fi
