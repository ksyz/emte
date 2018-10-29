1. Extend schema attributes

	```bash
    ldapmodify -ZZ -x -D "cn=Directory Manager" -W -H ldap://localhost -f /usr/share/freeipa-plugin-radiusprofile/Attributes.ldif
    ```

2. Extend schema objectClasses

	```bash
    ldapmodify -ZZ -x -D "cn=Directory Manager" -W -H ldap://localhost -f /usr/share/freeipa-plugin-radiusprofile/Classes.ldif
    ```

3. Modify permissions Server/RBAC/Permmissions:
	- Permission: System: Modify Users, radiusprofile attributes
	- Permission: System: Read User Standard Attributes, radiusprofile attributes
