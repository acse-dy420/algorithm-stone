from manim_imports_ext import *
import io

# 红黑树的噩梦，可以结束了

class RedBlackTreePreface(AlgoScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def construct(self):
        # self.start_logo(subtitle="红黑树")
        self.wait(100)

class RedBlackTreeWhatIs(AlgoScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def compare_nodes(self, a, b):
        left = a.copy()
        right = b.copy()
        p = LEFT*3+UP*3
        self.play(ApplyMethod(left.move_to, p+LEFT*0.5), ApplyMethod(right.move_to, p+RIGHT*0.5))
        t = AlgoText("<").next_to(left)
        self.play(FadeIn(t))
        self.play(FadeOut(left), FadeOut(right))

    def hide_and_show(self, tree:AlgoRBTree, root):
        el = tree.get_edge(tree.root.id, tree.root.left.id)
        er = tree.get_edge(tree.root.id, tree.root.right.id)
        self.play(FadeOut(root, remover=False), FadeOut(el, remover=False), FadeOut(er, remover=False))
        self.show_message("左子树是二叉查找树")
        self.show_message("右子树也是二叉查找树")
        self.wait(2)
        self.play(FadeIn(root), FadeIn(el), FadeIn(er))
        self.wait()

    def construct(self):
        self.init_message("红黑树的性质")
        tree = AlgoRBTree(self)
        tree.ctx.insert_message = False
        tree.ctx.delete_message = False
        tree.ctx.animate = False

        self.add(tree)
        max_value = 100
        n = 8
        random.seed(3)
        arr = np.random.choice(max_value, size=n, replace=False)
        tree.shift(UP*2)
        for i in arr:
            tree.set(i, i)

        self.show_message("红黑树是自平衡二叉查找树")
        root = tree.get_node(tree.root.id)
        left = tree.get_node(tree.root.left.id)
        right = tree.get_node(tree.root.right.id)

        self.show_message("左孩子的值大于根节点")
        self.compare_nodes(left, root)

        self.show_message("右孩子的值小于根节点")
        self.compare_nodes(root, right)
        
        self.show_message("左右子树分别为二叉查找树")
        self.hide_and_show(tree, root)

        self.show_message("红黑树有5条性质")

        text_list = [
            "1 每个节点是红色或者黑色，包括叶子nil节点",
            "2 根节点是黑色",
            "3 叶子nil节点是黑色",
            "4 如果一个节点是红色，则其子节点都是黑色",
            "5 对于每一个节点，从该节点到叶子节点的所有路径上，黑色节点数量相同",
        ]
        panel = AlgoPropertyPanel(text_list)
        panel.to_edge(UR)
        self.play(ShowCreation(panel))

        self.snapshot()
        
        self.show_message("1 每个节点是红色或者黑色，包括叶子nil节点")
        panel.light(0)

        self.show_message("2 根节点是黑色")
        panel.light(1)

        self.show_message("3 叶子nil节点是黑色")
        panel.light(2)

        self.show_message("4 如果一个节点是红色，则其子节点都是黑色")
        panel.light(3)

        self.show_message("5 对于每一个节点，从该节点到叶子节点的所有路径上，黑色节点数量相同")
        panel.light(4)
        
        self.wait()

class RedBlackTreeRotate(AlgoScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def construct(self):
        self.init_message("红黑树的旋转")
        tree = AlgoRBTree(self)
        tree.ctx.insert_message = True
        tree.ctx.delete_message = False
        tree.ctx.animate = True
        self.add(tree)

        arr = [1,2,3]
        v = AlgoVector(self, arr)
        self.play(ShowCreation(v))
        self.play(v.to_edge, UP)

        self.show_message("插入和删除操作会破坏红黑树的5条性质")
        self.show_message("维护这5条性质是通过旋转来完成的")
        self.show_message("来看这3个节点的插入操作")
        self.snapshot()

        tree.shift(UP*2)
        for i in arr:
            tree.set(i, i)

        self.show_message("节点3插入后，需要左旋达到平衡")
        self.snapshot()

        self.show_message("如果节点换成是[3, 2, 1]")
        arr = [3, 2, 1]
        v2 = AlgoVector(self, arr)
        v2.to_edge(UP)
        self.play(Transform(v, v2))
        self.play(Uncreate(tree))
        self.remove(tree)
        self.snapshot()

        tree = AlgoRBTree(self)
        tree.ctx.insert_message = True
        tree.ctx.delete_message = False
        tree.ctx.animate = True
        self.add(tree)
        tree.shift(UP*2)
        for i in arr:
            tree.set(i, i)

        self.show_message("节点1插入后，需要右旋达到平衡")
        self.snapshot()

        self.wait()

# 3 case
class RedBlackTreeInsert(AlgoScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def rand(self, seed, animate_index):
        tree = AlgoRBTree(self)
        self.add(tree)
        tree.ctx.insert_message = False
        tree.ctx.delete_message = False
        tree.ctx.animate = False
        max_value = 100
        np.random.seed(seed)
        n = 8
        arr = np.random.choice(max_value, size=n, replace=False)
        print(arr)
        tree.shift(UP*2)
        index = 0
        for i in arr:
            if index >= animate_index:
                tree.ctx.insert_message = True
                tree.ctx.animate = True
            tree.set(i, i)
            index += 1

        self.play(FadeOut(tree))
    
    def construct(self):
        self.init_message("红黑树插入")
        # left case 
        self.rand(5, 6)

        # right case 1,2,3
        self.rand(3, 6)

        self.wait()

# 4 case
class RedBlackTreeDelete(AlgoScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def rand(self, seed, count, animate_index):
        print("--------------rand-------------", seed)
        tree = AlgoRBTree(self)
        self.add(tree)
        tree.ctx.insert_message = False
        tree.ctx.delete_message = False
        tree.ctx.animate = False
        max_value = 100
        np.random.seed(seed)
        n = count
        arr = np.random.choice(max_value, size=n, replace=False)
        print(arr)
        tree.shift(UP*2)
        index = 0

        for i in arr:
            tree.set(i, i)

        np.random.shuffle(arr)
        for i in arr:
            if index >= animate_index:
                tree.ctx.delete_message = True
                tree.ctx.animate = True
            tree.delete(i)
            index += 1

        self.play(FadeOut(tree))

    def construct(self):
        self.init_message("红黑树删除的4个case")
        # left case 1,2,3,4
        self.rand(560, 9, 3)

        # right case 1,2,3,4
        self.rand(18, 8, 2)
        
        self.wait()

def memory():
    import os
    import psutil
    pid = os.getpid()
    py = psutil.Process(pid)
    memoryUse = py.memory_info()[0]/2.**30  # memory use in GB...I think
    return memoryUse

class RedBlackTreeEnd(AlgoScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def rand(self, seed, count):
        tree = AlgoRBTree(self)
        self.add(tree)
        tree.ctx.insert_message = False
        tree.ctx.delete_message = False
        tree.ctx.animate = True
        tree.ctx.run_time = 0.1
        tree.ctx.wait_time = 0.1

        max_value = count*2
        np.random.seed(seed)
        n = count
        arr = np.random.choice(max_value, size=n, replace=False)
        print(arr)
        tree.shift(UP*2)
        index = 1
        for i in arr:
            print("insert:", memory(), index, i)
            tree.set(i, i)
            index += 1

        np.random.shuffle(arr)
        index = 1
        for i in arr:
            print("delete:", index, i)
            tree.delete(i)
            index += 1

        self.play(FadeOut(tree))

    def construct(self):
        self.init_message("红黑树大型树结构变化")

        self.show_message("在最后，让我们创建一个1000个节点的巨型树")
        self.show_message("便于我们更加直观的了解红黑树是如何运作的")
        self.rand(560, 100)
        self.show_message("完成红黑树，谢谢观看！")
        self.wait()
