function rpmbuildpkg { 
    shortrpm \
		--define "_topdir ${PWD}/" \
		--define "_sourcedir %{_topdir}/" \
		--define "_specdir %{_topdir}/" \
		--define "_builddir %{_topdir}/BUILD/" \
		--define "_buildrootdir %{_topdir}/BUILDROOT/" \
		--define "_rpmdir %{_topdir}/" \
		--define "_srcrpmdir %{_topdir}/" \
		"$@"
}

function rpmpkg { 
    rpm \
		--define "_topdir ${PWD}/" \
		--define "_sourcedir %{_topdir}/" \
		--define "_specdir %{_topdir}/" \
		--define "_builddir %{_topdir}/BUILD/" \
		--define "_buildrootdir %{_topdir}/BUILDROOT/" \
		--define "_rpmdir %{_topdir}/" \
		--define "_srcrpmdir %{_topdir}/" \
		"$@"
}

function sourcespkg {
set -x
	PACKAGE="$1"

	if [ '.' = "$PACKAGE" ]
	then
		spectool -g *.spec
		sha512sum --tag $(spectool --sources *.spec |cut -d\  -f2 | xargs -I% basename %) > sources
	elif [ -d "$PACKAGE" ]
	then
		pushd "$PACKAGE"
		spectool -g "$PACKAGE".spec
		sha512sum --tag $(spectool --sources *.spec |cut -d\  -f2 | xargs -I% basename %) > sources
		popd
	elif [ -f "$PACKAGE" ] && echo "$PACKAGE" | grep -qP '\.spec$'
	then
		pushd "$(basename "$PACKAGE")"
		spectool -g "$PACKAGE"
		sha512sum --tag $(spectool --sources "$PACKAGE" |cut -d\  -f2 | xargs -I% basename %) > sources
		popd
	fi
set +x
}
