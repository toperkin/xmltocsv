import xml.etree.ElementTree as ET


def convert(fileName):

    def clean(filename):
        with open(filename, 'r') as file:
            content = ' '.join(file.read().split())
        return content

    cls = []
    def add(key):
        if key not in cls:
            cls.append(key)

    def genColumns(root, prefix=''):
        for child in root:
            tag = child.tag
            if prefix:
                tag = f"{prefix}.{tag}"

            for key in child.attrib:
                add(f"{tag}.att_{key}")

            if child.text and child.text.strip():
                add(tag)

            genColumns(child, tag)
        return


    root = ET.fromstring(clean(fileName))
    genColumns(root)

    def cleanValue(v):
        return v.replace(",", "").replace("\"", "").replace("\'", "").strip()

    res = [cls]
    def genRows(root, prefix='', row=[], lastChild=False):
        nChildren = len(root)

        if nChildren == 0 and lastChild:
            r = ["" for k in cls]
            for a in row:
                r[cls.index(a["key"])] = a["value"]
            res.append(r)

        for idx, child in enumerate(root):
            tag = child.tag
            if prefix:
                tag = f"{prefix}.{tag}"

            for key in child.attrib:
                row.append({"key":f"{tag}.att_{key}", "value": cleanValue(child.attrib.get(key))})

            if child.text and child.text.strip():
                row.append({"key":tag, "value": cleanValue(child.text)})

            genRows(child, tag, [a for a in row], idx == nChildren - 1)

        return

    genRows(root)
    outName = fileName.replace(".xml", ".csv")
    with open(outName, "w") as f:
        for line in res:
            f.write(','.join(['' if k is None else k  for k in line]))
            f.write('\n')

# example usages
if __name__ == "__main__":
    convert("./data.xml")