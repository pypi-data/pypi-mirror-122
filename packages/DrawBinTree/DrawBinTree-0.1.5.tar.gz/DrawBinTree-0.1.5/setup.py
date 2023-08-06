from setuptools import setup,find_packages

setup(

    name='DrawBinTree',
    version='0.1.5',
    keywords=('pip','binary','tree'),
    description="draw binary tree by matplotlib",
    long_description='''draw binary tree by matplotlib with three methods:\n
			draw_full_tree(["A","B","C","D","",'F'])\n
			draw_link_tree([['A',1,2],['B',3,-1],['C',4,5],['D',-1,-1],['F',-1,-1],['G',-1,-1]])\n
			draw_list_tree(listtree=['A',['B',['C',None,None],None],['D',['F',None,None],None]])
			''',
    licence='MIT Licence',

    url='https://github.com/jim0575/desktop-tutorial',
    author='james',
    author_email="jim0575@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[]
    )
