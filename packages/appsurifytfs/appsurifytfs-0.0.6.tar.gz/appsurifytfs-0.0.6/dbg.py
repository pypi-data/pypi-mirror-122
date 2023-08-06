# -*- coding: utf-8 -*-

output = open('./mock-output.txt', 'r').read()


import re
pattern = re.compile(r"""(?P<propertyName>(?=^)\w[\s\w,]+)(?(1):)(?:\s|\n)?(?P<propertyData>[\W\w\s]+)""", re.MULTILINE)

def get_last_branch_changeSet(branch, numberOfChangets):
    changeSetList = []
    # changeSetDict = {}
    # propertyName = ""
    # propertyData = ""
    # needPropertData = False
    # itemsDict = {}
    # isItemDict = False
    # changeSetDict["branch"] = branch

    output_list = [item for item in output.split("-" * 79 + '\n\n') if item]

    for changeset_raw in output_list:
        changeSetDict = {}
        itemsDict = {}

        changeSetDict['branch'] = 'branch'
        changeSetDict['items'] = itemsDict

        changeset_info_items = changeset_raw.split("\n\n\n\n")
        changeset_items = list()

        for changeset_info_item in changeset_info_items:
            if any(changeset_info_item.startswith(keyword) for keyword in ['Changeset', 'User', 'Date']):
                changeset_info_item = changeset_info_item.split('\n\n')
                changeset_items.extend(changeset_info_item)
            else:
                changeset_info_item = changeset_info_item.replace('\n\n', '\n')
                changeset_items.append(changeset_info_item)

        for changeset_item in changeset_items:
            for item in pattern.finditer(changeset_item):
                propertyName, propertyData = item.groups()
                propertyName = propertyName.lstrip().rstrip().replace(' ', '_').lower()
                propertyData = propertyData.lstrip().rstrip()

                changeSetDict[propertyName] = propertyData

                if propertyName == 'items':
                    for i in propertyData.split('\n'):
                        i = i.lstrip().rstrip()
                        action = i[:i.find("$/")]
                        filename = i[i.find("$/"):]

                        action = action.lstrip().rstrip()
                        filename = filename.lstrip().rstrip()

                        if ',' in action:
                            actions = action.split(', ')
                            if all(s in actions for s in ('delete', 'source rename')):
                                action = 'delete'
                            elif all(s in actions for s in ('encoding', 'edit')):
                                action = 'edit'
                            elif all(s in actions for s in ('merge', 'edit')):
                                action = 'edit'
                            elif all(s in actions for s in ('rename', 'edit')):
                                action = 'rename'

                        itemsDict[action] = filename
                    changeSetDict['items'] = itemsDict

        changeSetList.append(changeSetDict)

    return changeSetList

for changeSet in get_last_branch_changeSet('branch', numberOfChangets=None):
    items = changeSet.get('items', {})
    for key in items:
        print(f'{key}\t{items[key]}')

print('Finish')
