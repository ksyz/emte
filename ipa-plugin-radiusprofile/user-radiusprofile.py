import re
from ipalib.plugins.user import user, user_add, user_mod
from ipalib.parameters import ( Str, Int )
from ipalib import _
from ipapython.ipautil import ipa_generate_password, CheckedIPAddress

"""
    CheckedIPAddress
    def __init__(self, addr, match_local=False, parse_netmask=True,
                 allow_network=False, allow_loopback=False,
                 allow_broadcast=False, allow_multicast=False):
"""
def validate_ipaddr(ugettext, ipaddr):
	try:
		CheckedIPAddress(ipaddr, 
			parse_netmask=False,
			allow_loopback=True,
			allow_broadcast=True,
			allow_multicast=True)
	except Exception, e:
		return unicode(e)
	return None


def validate_ipnet(ugettext, ipaddr):
	m = re.match(r'^(?:\+=\s+)(?P<addr>.*)$', ipaddr)
	if m is not None:
		if m.group('addr'):
			ipaddr = m.group('addr')

	# for some reason, +addr pass as valid in built-in CheckedIPAddress
	m = re.match(r'^[0-9].*', ipaddr)
	if m is None:
		return _("Invalid IP network address: <%s>" % ipaddr)

	try:
		CheckedIPAddress(ipaddr, 
			allow_network=True,
			allow_loopback=True,
			allow_broadcast=True,
			allow_multicast=True)
	except Exception, e:
		return unicode(e)
	return None


def framed_route_normalizer(ugettext, value):
	value = re.sub(r'^\+=\s+', '', value)
	return unicode(value)


user.takes_params += (
	Str('radiusreplyitem*',
		cli_name = 'radius_reply_item',
		label = _('Radius reply item'),
	),
	Str('radiusframedipaddress?', validate_ipaddr,
		cli_name = 'radius_ip_addr',
		label = _('Radius Framed IP Address'),
	),
	Str('radiusframedroute*', validate_ipnet,
		cli_name = 'radius_route',
		label = _('Radius Framed route'),
		# normalizer = framed_route_normalizer,
	),
	Int('radiusclass?',
		cli_name = 'radius_class',
		label = _('Radius Class'),
		minvalue = 0,
	),
)

def useradd_precallback(self, ldap, dn, entry_attrs, attrs_list, *keys, **options):
	entry_attrs['objectclass'].append('radiusprofile')
	self.log.debug('Adding radiusprofile objectClass')
	return dn


def usermod_precallback(self, ldap, dn, entry_attrs, attrs_list, *keys, **options):
	if 'objectclass' not in entry_attrs.keys():
		old_entry = ldap.get_entry(dn, ['objectclass'])
		entry_attrs['objectclass'] = old_entry['objectclass']
	if 'radiusprofile' not in entry_attrs['objectclass']:
		entry_attrs['objectclass'].append('radiusprofile')
		self.log.info('Appending radiusprofile objectClass')
	return dn

# radiusframedroute
# if there si only 1:
# - no prefix.
# if there is more than 1:
# prefix each with +=
def user_framed_route_callback(self, ldap, dn, entry_attrs, attrs_list, *keys, **options):
	if 'radiusframedroute' not in entry_attrs.keys():
		return dn

	self.log.info("Fix radiusframedroute")
	routes = entry_attrs['radiusframedroute']
	_routes = []

	if type(routes) not in (tuple, list):
		_routes = [unicode(re.sub(r'^\+=\s+', '', routes))]
	else:
		m = re.compile(r'^(?:\+=\s+)?(?P<addr>.*)$')
		for route in routes:
			res = m.match(route)
			if res is not None:
				if routes.__len__ > 1:
					_routes.append(unicode('+= ' + res.group('addr')))
				else:
					_routes.append(unicode(res.groups('addr')))
			
	entry_attrs['radiusframedroute'] = _routes
	return dn



user_mod.register_pre_callback(usermod_precallback)
user_add.register_pre_callback(useradd_precallback)

user_mod.register_pre_callback(user_framed_route_callback)
user_add.register_pre_callback(user_framed_route_callback)

for item in ('radiusreplyitem', 'radiusframedipaddress', 'radiusframedroute', 'radiusclass'):
	user.default_attributes.append(item)

