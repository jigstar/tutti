"""Module for one-way sync between two datasets."""
from typing import List, Dict, Tuple

from ldapsync.ldap import LDAPAttributeType
from ldapsync.ldapoperations import LDAPOperation, AddOperation, DeleteOperation, ModifyDNOperation, ModifyOperation


def remap(entries: Dict[str, Dict[str, List[LDAPAttributeType]]],
          on: str) -> Dict[LDAPAttributeType, Tuple[str, Dict]]:
    """Remap LDAP dataset into one which maps on the given attribute.

    Args:
        entries: LDAP dataset.
        on: Attribute that will be used as key for the new mapping.

    Raises:
        KeyError: If the mapping attribute is not present in an entry.
        ValueError: If another issue arose with the mapping attribute value.

    Returns:
        A dictionary which maps from the value of the given attribute onto a
        2-tuple with Distinguished Name and attributes dictionary.
    """
    d = {}
    for dn, attributes in entries.items():
        key_values = attributes[on]
        if len(key_values) != 1:
            raise ValueError('Mapping attribute does not have exactly 1 value.')
        key = key_values[0]
        if key in d:
            raise ValueError('Mapping attribute value is not unique.')
        d[key] = dn, attributes
    return d


def sync(change_to: Dict[str, Dict[str, List[LDAPAttributeType]]],
         to_change: Dict[str, Dict[str, List[LDAPAttributeType]]],
         on: str = "qDBLinkID") -> List[LDAPOperation]:
    """Get operations to perform to change the second dataset into the first.

    The datasets are dictionaries of LDAP entries. The dictionary key is the
    Distinguished Name of an entry, the value is a dictionary of entry
    attributes to list of values.

    Args:
        change_to: The dataset which has the new data.
        to_change: The dataset that is old and needs to be modified.
        on: Attribute that will be used to match entries from both datasets.

    Returns:
        A list of add, delete, modify operations. Order matters.
    """
    ops = []

    change_to = remap(change_to, on)
    to_change = remap(to_change, on)

    # Get add/delete operations
    to_add = change_to.keys() - to_change.keys()
    ops.extend([AddOperation(*change_to[k]) for k in to_add])

    to_delete = to_change.keys() - change_to.keys()
    ops.extend([DeleteOperation(to_change[k][0]) for k in to_delete])

    # Check for value/DN changes
    in_both = change_to.keys() - to_add
    for k in in_both:
        new_dn, new_attrs = change_to[k]
        cur_dn, cur_attrs = to_change[k]

        # DN
        # Modify DN needs to be performed before attribute modify!
        # Otherwise the LDAP server will probably throw an error.
        if new_dn.lower() != cur_dn.lower():
            ops.append(ModifyDNOperation(cur_dn, new_dn))

        # Attribute deletions
        attr_delete = cur_attrs.keys() - new_attrs.keys()
        for attr in attr_delete:
            ops.append(ModifyOperation(new_dn, attr, []))

        # Attribute changes and additions
        for key, new_values in new_attrs.items():
            cur_values = cur_attrs.get(key, [])
            if sorted(new_values) != sorted(cur_values):
                ops.append(ModifyOperation(new_dn, key, new_values))
    return ops
