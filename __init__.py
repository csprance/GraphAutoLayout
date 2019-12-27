# -*- coding: utf-8 -*-

# This code is part of Graph Auto-Layout plugin for Substance Designer
# Copyright (C) 2018 Alex Zotikov (twitter.com/z_fighting)
# Updated to work with Designer 2019 by Chris Sprance (twitter.com/csprance)
# Published under GPLv2 license


# Can't believe you are reading the tool description. I appreciate your curiosity.
# The core of the tool is grandalf library. It provides Sugiyama algorithm for layout of directed acyclic graph.
# Everything else is a wrapper for Substance Designer nodes and some UX dancing.

import os
import sys
sys.path.append(os.path.dirname(__file__))

import sd
import sdplugins
from sd.api import sdproperty
try:
    # 2018.2 API
    from sd.api.sdvalue import float2
except:
    # 2018.3 API
    from sd.api.sdbasetypes import float2

from grandalf.graphs import Vertex, Edge, Graph
from grandalf.layouts import SugiyamaLayout

from PySide2 import QtCore, QtWidgets, QtGui

import settings

# Actual standard node size is 96x96, but there is some padding in algorithm, so I use magic numbers for now
NODE_HEIGHT = 76
NODE_WIDTH = 76

# Get the application and UI manager object.
ctx = sd.getContext()
app = ctx.getSDApplication()
uiMgr = app.getQtForPythonUIMgr()

class AutoNodeLayout(object):
    def run(self):
        selected_nodes = uiMgr.getCurrentGraphSelection()
        hierarchy = NodesHierarchy(ctx, selected_nodes)
        vertexes = [Vertex(data) for data in range(len(hierarchy.nodes))]
        nodesConnections = hierarchy.getEdges()
        edges = [Edge(vertexes[vertex], vertexes[w]) for (vertex, w) in nodesConnections]
        graph = SubstanceGraph(vertexes, edges)

        for vertex in vertexes:
            vertex.view = VertexView(hierarchy.nodes[vertex.data])
        # For each separate graph
        for subGraph in range(len(graph.C)):
            center = graph.getSubgraphCenter(subGraph)

            sug = SugiyamaLayout(graph.C[subGraph])
            # Vertexes without input edges
            roots = list(filter(lambda x: len(x.e_in()) == 0, graph.C[subGraph].sV))
            sug.init_all(roots=roots)
            sug.draw()

            newCenter = graph.getSubgraphCenter(subGraph)
            if len(selected_nodes) == 1:
                # Offset everything to save the selected node initial position
                rootPosition = hierarchy.nodes[roots[0].data].getPosition()
                # Have to compensate the final root node offset
                offset = float2(rootPosition[1] - roots[0].view.xy[0], -rootPosition[0] - roots[0].view.xy[1])
            else:
                offset = float2(center[0] - newCenter[0], center[1] - newCenter[1])

            for i, vertex in enumerate(graph.C[subGraph].sV):
                vertex.view.node.setPosition(float2(-vertex.view.xy[1] - offset[1], vertex.view.xy[0] + offset[0]))


class VertexView(object):

    def __init__(self, node):
        self.node = node
        self.w, self.h = (settings.VERTICAL_GAP + 1) * NODE_HEIGHT, (settings.HORIZONTAL_GAP + 1) * NODE_WIDTH
        position = self.node.getPosition()
        self.xy = float2(position[1], -position[0])


class NodesHierarchy(object):

    def __init__(self, aContext, nodes):
        super(NodesHierarchy, self).__init__()
        nodesCount = len(nodes)
        self.nodes = []
        if nodesCount == 0:
            self.nodes = uiMgr.getCurrentGraph().getNodes()
        elif nodesCount == 1:
            node = nodes[0]
            self.nodes = [node]
            self.nodes.extend(self.getAllInputNodes(node))
        else:
            self.nodes = nodes

    def getEdges(self):
        edges = []
        for i, node in enumerate(self.nodes):
            for connectedNode in self.getConnectedNodes(node, sdproperty.SDPropertyCategory.Input):
                identifier = connectedNode.getIdentifier()
                for j, other_node in enumerate(self.nodes):
                    if other_node.getIdentifier() == identifier:
                        edges.append((i, j))
        return edges

    def getAllInputNodes(self, node):
        returnNodes = []
        currentNodes = [node]
        while True:
            nextNodes = []
            for currentNode in currentNodes:
                inputNodes = self.getConnectedNodes(currentNode, sdproperty.SDPropertyCategory.Input)
                if inputNodes:
                    for inputNode in inputNodes:
                        identifier = inputNode.getIdentifier()
                        for node in returnNodes + nextNodes:
                            if node.getIdentifier() == identifier:
                                break
                        else:
                            nextNodes.append(inputNode)
            returnNodes.extend(nextNodes)
            if not nextNodes:
                break
            currentNodes = nextNodes
        return returnNodes

    def getConnectedNodes(self, node, connectionType):
        connectedNodes = []
        outputProperties = node.getProperties(connectionType)
        for property in outputProperties:
            if property.isConnectable():
                connections = node.getPropertyConnections(property)
                for connection in connections:
                    try:
                        connectedNode = connection.getTargetNode()
                    except:
                        connectedNode = connection.getInputPropertyNode()
                    connectedNodes.append(connectedNode)
        return connectedNodes


class SubstanceGraph(Graph):

    def __init_(self):
        super(SubstanceGraph, self).__init__()

    # Extension to the Graph class
    def getSubgraphCenter(self, subGraphIndex):
        positions = [v.view.xy for v in self.C[subGraphIndex].sV]
        center = (sum(x[0] for x in positions) / len(positions), sum(x[1] for x in positions) / len(positions))
        return center


def initializeSDPlugin():
    # Get Designer's main window.
    mainWindow = uiMgr.getMainWindow()
    # Create our toolbar.
    toolbar = QtWidgets.QToolBar()
    action = toolbar.addAction("Auto-Layout")
    action.setToolTip('Auto layout any selected nodes.')
    action.setIcon(QtGui.QIcon(os.path.abspath(os.path.join(os.path.dirname(__file__), 'extra', 'arrange_auto.png'))))
    action.setShortcut(settings.SHORTCUT)
    action.triggered.connect(AutoNodeLayout.run)

    # Add our toolbar to Designer's window.
    mainWindow.addToolBar(QtCore.Qt.TopToolBarArea, toolbar)
