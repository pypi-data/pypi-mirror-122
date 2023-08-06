#by james zhuji hailiang expreimental high school 2021-10-5

import matplotlib.pyplot as plt
import math

def draw_circle(pos,r=10,text=""):
    #ax=plt.axis("off")
    plt.scatter(x=pos[0],y=pos[1],s=r*r*3.14,marker="o",c="#3399FF")
    plt.text(pos[0],pos[1],s=text,horizontalalignment="center",verticalalignment="center")
def draw_line(pos1,pos2):
    #ax=plt.axis("off")
    plt.plot([pos1[0],pos2[0]],[pos1[1],pos2[1]],c="#6699FF")

last_pos=[]
def draw_level(dts):
    global last_pos
    if len(dts)==0:
        return
    sub_dts=[]
    if len(last_pos)!=0:
        k=0
        for i in range(len(dts)):
            if i%2==0:
                if last_pos[k*2][2]!="":
                    draw_line((dts[i][0],dts[i][1]),(last_pos[k*2][0],last_pos[k*2][1]))
                if last_pos[k*2+1][2]!="":
                    draw_line((dts[i][0],dts[i][1]),(last_pos[k*2+1][0],last_pos[k*2+1][1]))
                k+=1
    last_pos=[]
    for i in range(len(dts)):
        if i%2==1:
            sub_dts.append((dts[i][0],dts[i][1]+1,dts[i][2]))
        else:
            if dts[i][2]!="":
                draw_circle((dts[i][0],dts[i][1]),text=dts[i][2])
            last_pos.append((dts[i][0],dts[i][1],dts[i][2]))
    draw_level(sub_dts)

data=[]
def root_mid1(tr,tree):
    global data
    lt=tr*2+1
    rt=tr*2+2
    if lt<len(tree):
        root_mid1(lt,tree)
    data.append(tree[tr])
    if rt<len(tree):
        root_mid1(rt,tree)


def max_lev(node,linktree):
    lv1=1
    lv2=1
    if linktree[node][1]==-1:
        lv1=0
    else:
        lv1+=max_lev(linktree[node][1],linktree)
    if linktree[node][2]==-1:
        lv2=0
    else:
        lv2+=max_lev(linktree[node][2],linktree)
    return max(lv1,lv2)
def root_mid2(node,tree,level):
    global data
    if tree[node][1]!=-1:
        root_mid2(tree[node][1],tree,level-1)
    elif level>1:
        tree.append(["",-1,-1])
        tree[node][1]=len(tree)-1
        root_mid2(tree[node][1],tree,level-1)
    elif level>0:
        data.append("")
    data.append(tree[node][0])
    if tree[node][2]!=-1:
        root_mid2(tree[node][2],tree,level-1)
    elif level>1:
        tree.append(["",-1,-1])
        tree[node][2]=len(tree)-1
        root_mid2(tree[node][2],tree,level-1)
    elif level>0 :
        data.append("")
        
        
def draw_full_tree(fulltree=["A","B","C","D","",'F','G']):
    lv=int(math.log2(len(fulltree)))+1
    max_n=2**lv-1
    fulltree=fulltree+[""]*(max_n-len(fulltree))
    global data,last_pos
    last_pos=[]
    data=[]
    root_mid1(0,fulltree)
    dts=[]
    for d in range(len(data)):
        dts.append((d,0,data[d]))
    draw_level(dts)
    plt.axis("off")
    plt.show()

def draw_link_tree(linktree=[['A',1,2],['B',3,-1],['C',4,5],['D',-1,-1],['F',-1,-1],['G',-1,-1]]):
    max_lv=max_lev(0,linktree)
    global data,last_pos
    last_pos=[]
    data=[]
    root_mid2(0,linktree,max_lv)
    dts=[]
    for d in range(len(data)):
        dts.append((d,0,data[d]))
    draw_level(dts)
    plt.axis("off")
    plt.show()

res=[]
def root_mid3(treelist,father=-1):
    global res
    res.append([treelist[0],-1,-1])
    father=len(res)-1
    if not treelist[1] is None:
        res[father][1]=len(res)
        root_mid3(treelist[1],father)
    if not treelist[2] is None:
        res[father][2]=len(res)
        root_mid3(treelist[2],father)
    
    
def draw_list_tree(listtree=['A',['B',['C',None,None],None],['D',['F',None,None],None]]):
    global res
    res=[]
    root_mid3(listtree)
    draw_link_tree(linktree=res)
    
    
