function rpmpkg {
	rpmbuild \
--define "_topdir ${PWD}/" \
--define "_sourcedir %{_topdir}/" \
--define "_specdir %{_topdir}/" \
--define "_builddir %{_topdir}/" \
--define "_buildrootdir %{_topdir}/" \
--define "_rpmdir %{_topdir}/" \
--define "_srcrpmdir %{_topdir}/" "$@"

}
