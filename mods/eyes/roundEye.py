

from Element import Element


def draw(x, y):
    path = Element("path")
    path.add_attribute("d", f"M{x*24+5.5*24} {y*24+24}a12 12 90 0112 12v96a12 12 90 01-12 12h-96a12 12 90 01-12-12v-96a12 12 90 0112-12h96m0-24h-108q-24 0-24 24v120q0 24 24 24h120q24 0 24-24v-120q0-24-24-24zm-84 54v60a6 6 90 006 6h60a6 6 90 006-6v-60a6 6 90 00-6-6h-60a6 6 90 00-6 6")
    path.add_attribute("fill", "black")
    path.add_attribute("fill-rule", "evenodd")

    return path
