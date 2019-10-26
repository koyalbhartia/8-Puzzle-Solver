#
#  Copyright 2019 Koyal Bhartia
#  @file    8-puzzle solver.py
#  @author  Koyal Bhartia
#  @date    26/02/2019
#  @version 1.0
#
#  @brief This is the code to solve the 8-puzzle
#
# @Description This code has functions which returns all the possible paths that can be
# traversed given any goal matrix. Given any input matrix it gives the path to the goal matrix
#

import argparse
import numpy as np
import os, sys
import math
from collections import Counter

# @brief Comapares each element of any 2 3*3 matrices
#
#  @param The matrices A and b
#
#  @return Flag indicating if the matrices A and B are equal or not
def compare(A,B):
    for row in range(3):
        for col in range(3):
            if(A[row,col]!=B[row,col]):
                return 0
    return 1

# @brief Checks if the new node created is present in the nodes created earlier
#
#  @param The 3D matrix of all nodes and the new node generated
#
#  @return Flag indicating if the nodes are equal or not
'''
def checkrepeated(Nodes,new_mat):
    for position in range(Nodes.shape[2]):
        if(compare(Nodes[:,:,position],new_mat)):
            return 1
    return 0
'''
# @brief Generates all the possible nodes that can be traveresed along with its directions in
# nodeInfo
#
#  @param The desired goal node and the format of the nodeinfo
#
#  @return The updated 3D node matrix and the complete NodeInfo table
def createAllNodes(Nodes,NodesInfo):

    def countDistinct(arr):
        return len(Counter(arr).keys())

    # @brief Returns the position of the 0 in any given matrix
    #
    #  @param The matrix
    #
    #  @return The 0 positions

    def zero_position(matrix):
        for i in range(0,len(matrix)):
            for j in range(0,len(matrix)):
                if(matrix[i,j]==0):
                    zx=i
                    zy=j
        return zx , zy

    # @brief Swipes the 0 with its adjacent cells (if possible) and keeps updating the node matrix and nodeinfo
    #
    #  @param The matrix in which the 0 has to be swiped, the current parent and child status and the position of the "0" in the matrix
    #
    #  @return The current child position

    def Swipe(matrix,parent,child,row,col):
        checkrepeat=0
        if row is not 0: #top
            new_mat = matrix.copy()
            new_mat[row,col]=matrix[row-1,col]
            new_mat[row-1,col]=0
            #checkrepeat=checkrepeated(Nodes,new_mat)
            #if(checkrepeat==0):
            Nodes[:,:,child]=new_mat
            print(Nodes[:,:,child],"top")
            NodesInfo[child,:,:]=[parent, child, 0, 2] # 2-> top
            child+=1

        if row is not 2: #down
            new_mat = matrix.copy()
            new_mat[row,col]=matrix[row+1,col]
            new_mat[row+1,col]=0
            #checkrepeat=checkrepeated(Nodes,new_mat)
            #if(checkrepeat==0):
            Nodes[:,:,child]=new_mat
            print(Nodes[:,:,child],"dowm")
            NodesInfo[child,:,:]=[parent, child, 0, 8] #8-> down
            child+=1

        if col is not 0: #left
            new_mat = matrix.copy()
            new_mat[row,col]=matrix[row,col-1]
            new_mat[row,col-1]=0
            #checkrepeat=checkrepeated(Nodes,new_mat)
            #if(checkrepeat==0):
            Nodes[:,:,child]=new_mat
            print(Nodes[:,:,child],"left")
            NodesInfo[child,:,:]=[parent, child, 0, 4] #4 -> left
            child+=1

        if col is not 2: #right
            new_mat = matrix.copy()
            new_mat[row,col]=matrix[row,col+1]
            new_mat[row,col+1]=0
            #checkrepeat=checkrepeated(Nodes,new_mat)
            #if(checkrepeat==0):
            Nodes[:,:,child]=new_mat
            print(Nodes[:,:,child],"right")
            NodesInfo[child,:,:]=[parent, child, 0, 6] #6 -> right
            child+=1

        return child


    parent=0
    child=1

    while(child<Total-4):
        print("Child No",child)
        New_Parent=Nodes[:,:,parent]
        print("New_Parent",New_Parent)
        zx, zy = zero_position(New_Parent)
        child=Swipe(New_Parent,parent, child,zx, zy)
        parent+=1

    return Nodes, NodesInfo

# @brief Searches if the input node is present in the list of all possible nodes created earlier
#
#  @param The node list, the input node and the flag as an indiactor of found node
#
#  @return The position where the node is found and the Flag indiacting a successful or an unsuccessful find
def search(Nodes, Input,Found):
    print(Nodes.shape[2],"Nodes.shape[2]")
    for position in range(Nodes.shape[2]):
        current =Nodes[:,:,position]
        if(compare(current,Input)):
            Found=True
            break;
    print(Found,"search pos")
    return position, Found

# @brief Generates the node path from the input node to get to the goal node
#
#  @param The desired goal node, the nodeInfo indiacting all the parent child relationships and the position where the node is found
#
#  @return The path that the node takes to reach the goal node

def NodePath(Nodes,NodesInfo,node_position):
    node_path=[]
    node_path.append(node_position)
    while(node_position!=0):
        print(node_position,"node_position")
        node_position=int(NodesInfo[node_position,0,0])
        node_path.append(node_position)
    nodePathMat=np.zeros((3,3,len(node_path)))
    for i in range(len(node_path)):
        nodePathMat[:,:,i]=Nodes[:,:,node_path[i]]
    return nodePathMat

# @brief Prints the List of nodes, the node info table and the node path to the goal node in 3 different text files
#
#  @param The updated matrices of the all possible nodes, the nodeinfo matrix and the node path from input to the goal
#
#  @return The 3 output text files

def TextOutput(Nodes,NodesInfo,nodePathMat):

    def NodesTransform(Nodes):
        NodesTf=np.zeros((Nodes.shape[2],1,9))
        for i in range(Nodes.shape[2]):
            counter=0
            for col in range(3):
                for row in range(3):
                    NodesTf[i,0,counter]=Nodes[row,col,i].copy()
                    counter+=1
        return NodesTf

    Nodes=NodesTransform(Nodes)
    with open('Nodes.txt', 'w') as file:
        for data in Nodes:
            np.savetxt(file, data, fmt='%-2.0f')

    with open('NodesInfo.txt', 'w') as file:
        for data in NodesInfo:
            np.savetxt(file, data, fmt='%-2.0f')

    with open('NodePath.txt', 'w') as file:
        if(len(nodePathMat)==0):
            data=[]
            file.write("The above combination does not exist")
            np.savetxt(file, data)
        else:
            NodePath=NodesTransform(nodePathMat)
            for data in NodePath:
                np.savetxt(file, data, fmt='%-2.0f')


if __name__ == '__main__':
    #Total no of possible nodes: 9!/2=181441
    Total=181441
    #The desired goal
    Goal=np.mat([[1,2,3],[4,5,6],[7,8,0]])
    #Backup Input if user enters wrong matrix
    Input=np.mat([[1,2,3],[4,5,6],[7,0,8]])
    #Initializing node, nodeinfo matrix
    Nodes=np.zeros((3,3,Total))
    NodesInfo=np.zeros((Total,1,4))
    Nodes[:,:,0]=Goal
    NodesInfo[0,:,:]=[0,0,0,0]
    #Indiactes if the iput node is found
    Found=False
    NodePathMat=[]
    flag=0

    while(flag!=1):
        input("Please enter the nos between 0-8 rowise to start the 8-puzzle after pressing enter")
        try:
            Input=np.zeros((3,3))
            for i in range(3):
                for j in range(3):
                    Input[i][j]=int(input('Element [%d][%d]=' %(i,j)))
                    if (Input[i][j]>8):
                        raise ValueError
            flag=1
            print(flag,"flag")
        except ValueError:
            print("No valid..! Please enter integer less than 8 ...")

    print("Input matrix",Input)
    Nodes, NodesInfo=createAllNodes(Nodes,NodesInfo)
    position,Found=search(Nodes,Input,Found)
    if Found:
        NodePathMat=NodePath(Nodes,NodesInfo,position)
    TextOutput(Nodes,NodesInfo,NodePathMat)
