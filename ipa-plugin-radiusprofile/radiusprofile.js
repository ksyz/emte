define(
	[ 'freeipa/phases', 'freeipa/user'],
	function (phases, user_mod) {

	// helper function
	function get_item(array, attr, value) {
		for (var i=0,l=array.length; i<l; i++) {
			if (array[i][attr] === value) return array[i];
		}

		return null;
	}

	var emp_plugin = {};

	emp_plugin.add_emp_radius_profile = function() {
		var facet = get_item(user_mod.entity_spec.facets, '$type', 'details');
		facet.sections.push({
			name: 'radiusprofile',
			label: 'Radius Profile',
			fields: [{
					name: 'radiusframedipaddress',
					label: 'Radius Framed IP Address',
				},
				{
					name: 'radiusframedroute',
					label: 'Radius Framed Routes',
					'$type': 'multivalued',
				},
				{
					name: 'radiusreplyitem',
					label: 'Radius Reply Items',
					'$type': 'multivalued',
					size: 128,
				},
				{
					name: 'radiusclass',
					label: 'Radius Class',
					size: 2,
				},
			],
		});

		return true;
	};


	phases.on('customization', emp_plugin.add_emp_radius_profile);
	return emp_plugin;
}); 

