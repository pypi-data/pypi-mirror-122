# -*- coding: utf-8 -*-

output = open('./mock-output.txt', 'r').read()

branch = 'main'
changeSetList = []
changeSetDict = {}
propertyName = ""
propertyData = ""
needPropertData = False
itemsDict = {}
isItemDict = False
changeSetDict["branch"] = branch

splits = [item for item in output.split("-" * 79 + '\n\n') if item]

import re
pattern = re.compile(r"""(?P<propertyName>(?=^)\w[\s\w,]+)(?(1):)(?:\s|\n)?(?P<propertyData>[\W\w\s]+)""", re.MULTILINE)

for changeset in splits:
    changeset_items = changeset.split("\n\n\n\n")

    changeset_items_formated = list()

    for _item in changeset_items:
        if any(_item.startswith(keyword) for keyword in ['Changeset', 'User', 'Date']):
            _item = _item.split('\n\n')
            changeset_items_formated.extend(_item)
        else:
            _item = _item.replace('\n\n', '\n')
            changeset_items_formated.append(_item)

    changeSetDict = {}
    itemsDict = {}

    for changeset_item in changeset_items_formated:
        for item in pattern.finditer(changeset_item):
            propertyName, propertyData = item.groups()
            propertyName = propertyName.lstrip().rstrip().replace(' ', '_').lower()
            propertyData = propertyData.lstrip().rstrip()

            changeSetDict[propertyName] = propertyData

            if propertyName == 'items':
                for i in propertyData.split('\n'):
                    i = i.lstrip().rstrip()
                    action, filename = i.split(' ', maxsplit=1)
                    action = action.lstrip().rstrip()
                    filename = filename.lstrip().rstrip()
                    itemsDict[action] = filename
                changeSetDict['items'] = itemsDict
    changeSetList.append(changeSetDict)


changesets_list = changeSetList

arr = changesets_list

length = len(arr)

commits = []

for changeSet in arr:
    changesetId = changeSet.get('changeset')
    if changesetId is None:
        print(changeSet)
        break
