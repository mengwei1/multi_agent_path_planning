from xml.dom.minidom import parse
import xml.dom.minidom
from LucadPoint import Point
from LucadPath import Path


def parse_lucad_(file_name):
    DOMTree = xml.dom.minidom.parse(file_name)
    database = DOMTree.documentElement
    points = database.getElementsByTagName("_NodePointManager_Table")
    paths = database.getElementsByTagName("_PathPointManager_Table")

    result_points = dict()
    result_edges = dict()

    for point in points:
        name = point.getElementsByTagName("NodeID")[0].childNodes[0].data
        x = point.getElementsByTagName("Node_x")[0].childNodes[0].data
        y = point.getElementsByTagName("Node_y")[0].childNodes[0].data
        result_points.update({name: Point(name, x, y)})

    for path in paths:
        name = path.getElementsByTagName("PathID")[0].childNodes[0].data
        start = path.getElementsByTagName("StartNode")[0].childNodes[0].data
        end = path.getElementsByTagName("EndNode")[0].childNodes[0].data
        param = path.getElementsByTagName("StringParam")[0].childNodes[0].data
        length = str(param).split(" ")[1]
        if start in result_edges.keys():
            result_edges[start].append(Path(name, start, end, length))
        else:
            result_edges.update({start: [Path(name, start, end, length)]})

    for edge in result_edges.keys():
        print('node %s has path to' % edge)
        for path in result_edges[edge]:
            if path.start != edge:
                print('path start does not equal edge vertex!')
                exit()
            print('\t%s with cost %s' % (path.end, path.length))
    return result_points, result_edges


def parse_lucad(file_name):
    DOMTree = xml.dom.minidom.parse(file_name)
    database = DOMTree.documentElement
    points = database.getElementsByTagName("point")
    paths = database.getElementsByTagName("path")

    result_points = dict()
    result_edges = dict()

    for point in points:
        name = point.getAttribute('name')
        x = point.getAttribute('xPosition')
        y = point.getAttribute('yPosition')
        result_points.update({name: Point(name, x, y)})

    for path in paths:
        name = path.getAttribute('name')
        try:
            if int(name) > 10000:
                continue
        except ValueError as e:
            pass
        start = path.getAttribute('sourcePoint')
        end = path.getAttribute('destinationPoint')
        length = path.getAttribute('routingCost')
        if start in result_edges.keys():
            result_edges[start].append(Path(name, start, end, length))
        else:
            result_edges.update({start: [Path(name, start, end, length)]})

    for edge in result_edges.keys():
        print('node %s has path to' % edge)
        for path in result_edges[edge]:
            if path.start != edge:
                print('path start does not equal edge vertex!')
                exit()
            print('\t%s with cost %s' % (path.end, path.length))
    return result_points, result_edges


if __name__ == '__main__':
    parse_lucad("huahai.xml")
