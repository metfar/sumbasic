#!/bin/bash

#cd ~/sum/sumbasic/sumbasic-0.2.32

BUILD="examples/build/linux/nuitka";
DIST="examples/dist";
ARCH="examples/dist/happy_birthday";

PACKAGES=(
    sumcore sumfsa sumio sumdata sumplot sumr
    sumpy sumui sumtui sumgui sumide sumbasic
    sumbash sumterminal sumx sumdiff sumdoc
    sumkeyboard rich numpy pandas matplotlib
);
ARGS=();
for package in "${PACKAGES[@]}"; do
	echo "Package $package $(python -c "import $package; print('$package',$package.__version__);" 2>/dev/null) ";
    ARGS+=("--include-package=$package")
done;

ccache --show-stats

test -f "$BUILD/_sum_linux_main.py" || {
    echo "ERROR: falta el launcher generado por sumbuild";
    exit 1;
};

test -f "$BUILD/happy_birthday.bas" || {
    echo "ERROR: falta el BASIC empaquetado";
    exit 1;
};



python3 -m nuitka \
    --onefile \
    --low-memory \
    --jobs=1 \
    --assume-yes-for-downloads \
    --output-dir="$DIST" \
    --output-filename=happy_birthday \
    "${ARGS[@]}" \
    --include-package-data=rich \
    --include-package-data=numpy \
    --include-package-data=pandas \
    --include-package-data=matplotlib \
	--noinclude-numba-mode=nofollow \
	--nofollow-import-to=torch \
	--nofollow-import-to=onnxruntime \
	--nofollow-import-to=nvidia \
	--nofollow-import-to=cv2 \
    --enable-plugin=no-qt \
	--report=build-report.xml \
    "--include-data-files=$BUILD/happy_birthday.bas=happy_birthday.bas" \
    "$BUILD/_sum_linux_main.py"
e=$?;

if [ $e -lt 1 ]; then
	err=0; 
	file $ARCH ; e=$? ; err=$((err+e));
	ldd $ARCH  ; e=$? ; err=$((err+e));

	if [ $err -lt 1 ]; then
		echo "Everything is okay. Running $ARCH." ;
		$ARCH ;
		exit $? ;
	else
		echo "Errors $err, something goes wrong"
		exit 2;
	fi ;
else
    echo "Compilation failed. Error $e";
    echo "## Kernel OOM diagnostics";
    journalctl -k -b --since "10 minutes ago" --no-pager | grep -Ei 'oom|out of memory|killed process|cc1' ;
	echo "-------------------------";
	exit $e;
fi ;

