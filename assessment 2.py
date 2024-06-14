import unittest

"""
To run the app, just hit run, options will be written in the command line
"""


class Tree:

    __doc__ = 'Tree Class'

    #Initialises a Tree object
    def __init__(self, root, left = None, right = None):
        self._root = root
        self._left = left
        self._right = right


    def evaluate_tree(self):
        """
        Evaluates the tree using a postorder traversal of the tree
        """

        if self:
            if self._left is None and self._right is None:
                return float(self._root)
            if self._root == '*':
                return float(self._left.evaluate_tree()) * float(self._right.evaluate_tree())
            elif self._root == '-':
                return float(self._left.evaluate_tree()) - float(self._right.evaluate_tree())
            elif self._root == '+':
                return float(self._left.evaluate_tree()) + float(self._right.evaluate_tree())
            else:
                #To handle division by 0
                if float(self._right.evaluate_tree()) == 0:
                    raise ValueError("Division by zero is not allowed.")
                return float(self._left.evaluate_tree()) / float(self._right.evaluate_tree())
        else:
            return None


    def preorder_trav(self, preorder=[]):
        """
        Returns a list of the preorder travel of the Tree
        """

        if self:
            preorder.append(self._root)
            if self._left:
                self._left.preorder_trav(preorder)
            if self._right:
                self._right.preorder_trav(preorder)
        return preorder
    

    def postorder_trav(self, postorder=[]):
        """
        Returns a list of the postorder travel of the Tree
        """

        if self:
            if self._left:
                self._left.postorder_trav(postorder)
            if self._right:
                self._right.postorder_trav(postorder)
            postorder.append(self._root)
        return postorder
    

    def bfs_trav(self, level=0, bfs = []):
        """
        Returns a list of the breadth first travel of the Tree
        """

        if level == 0:
            bfs.append(self._root)
        if self._left:
            bfs.append(self._left._root)
        if self._right:
            bfs.append(self._right._root)  
        if self._left:
            self._left.bfs_trav(level + 1)
        if self._right:
            self._right.bfs_trav(level + 1)
        return bfs
    

    def _visualize_tree(self, node, level = 0):
        """
        Returns a visual representation using an inorder traversal
        """

        if node is None:
            return ""
        else:
            left_str = self._visualize_tree(node._left, level + 1)
            #creates line with the current node's value indented by its level
            current_str = " " * (level * 4) + node._root + "\n"
            right_str = self._visualize_tree(node._right, level + 1)
            return left_str + current_str + right_str
            

    def __str__(self):
        return self._visualize_tree(self)




class List_to_Tree:

    __doc__ = 'List to Tree class'

    #initialises object
    def __init__(self, exp):
        self._exp = exp
        self._nlist = self.convert_list()
        self._tree = self.convert_to_tree()

    def convert_list(self):
        """
        Converts the mathematical expression string into a nested list and validates it at the same time
        works by creating the current expression in current_list then saving it to stack then repeating 
        """

        current_list = []
        stack = [] # 
        count_bra = 0 #Keeps track of open and close brackets

        for i in self._exp:
            if len(current_list) > 3:
                raise ValueError('More operands than expected')
            if i == '(':
                current_list.append([])
                stack.append(current_list)
                current_list = current_list[-1]
                count_bra += 1
            elif i == ')':
                if len(current_list) < 3:
                    raise ValueError('Less operands than expected')
                if count_bra == 0:
                    raise ValueError('Mising opening brackets or excess closing brackets')
                else:
                    current_list = stack.pop()
                    count_bra -= 1 
            elif i != ' ':
                current_list.append(i)

        if count_bra != 0:
            raise ValueError('Missing closing brackets')
        if len(current_list) != 1:
            raise ValueError('Missing outer brackets')
        else:
            return current_list


    def convert_to_tree(self, nested_list = None):
        """ 
        Returns a tree object based off of the nested list
        """

        #Makes method use self._nlist on first round to allow for recursion to work
        nested_list = nested_list or self._nlist

        #Checks if nested list
        if len(nested_list) == 1 and isinstance(nested_list[0], list):
            nested_list = nested_list[0]

        #Checks if number
        if len(nested_list) == 1:
            return Tree(nested_list[0])
        
        #Checks if expression and creates a new tree with operator as root
        elif len(nested_list) == 3:
            left_tree = self.convert_to_tree(nested_list[0])
            right_tree = self.convert_to_tree(nested_list[2])
            return Tree(nested_list[1], left_tree, right_tree)
        

    def tree(self):
        """
        Method allows to access the private attribute tree
        """
        
        return self._tree


    def __str__(self):
        """
        Returns nested list
        """
        
        return str(self._nlist)


#aar = "((((5+2)*(2-1))/((2+9)+((7-2)-1)))*8)"

class Test_list_class(unittest.TestCase):
    
    def test_convesion_working(self):
        self.assertEqual(List_to_Tree("((1-2)+(3*4))").convert_list(), [[['1', '-', '2'], '+', ['3', '*', '4']]])

    def test_excess_operands(self):
        with self.assertRaises(ValueError) as cm:
            List_to_Tree('(4*3*2)')
        self.assertEqual(str(cm.exception), 'More operands than expected')

    def test_missing_operands(self):
        with self.assertRaises(ValueError) as cm:
            List_to_Tree('(4*(2))')
        self.assertEqual(str(cm.exception), 'Less operands than expected')

    def test_missing_outer_brackets(self):
        with self.assertRaises(ValueError) as cm:
            List_to_Tree('(2*4)*(3+2)')
        self.assertEqual(str(cm.exception), 'Missing outer brackets')

    def test_missing_closing_brackets(self):
        with self.assertRaises(ValueError) as cm:
            List_to_Tree('((2+3)*(4*5)')
        self.assertEqual(str(cm.exception), 'Missing closing brackets')

    def test_missing_opening_brackets(self):
        with self.assertRaises(ValueError) as cm:
            List_to_Tree('(2+5)*(4/(2+2)))')
        self.assertEqual(str(cm.exception), 'Mising opening brackets or excess closing brackets')


    def test_simple_list_to_tree(self):
        tree = List_to_Tree(['4']).convert_to_tree()
        self.assertEqual(tree._root, '4')
        self.assertIsNone(tree._left)
        self.assertIsNone(tree._right)

    def test_nested_list_to_tree(self):
        tree = List_to_Tree([['4', '*', '3']]).convert_to_tree()
        self.assertEqual(tree._root, '*')
        self.assertEqual(tree._left._root, '4')
        self.assertEqual(tree._right._root, '3')


class Test_tree_class(unittest.TestCase):

    def setUp(self):
        self.tree = List_to_Tree('((1-2)+(3*4))').tree()

    def test_evaluate_tree(self):
        self.assertEqual(self.tree.evaluate_tree(), 11.0)

    def test_preorder_trav(self):
        self.assertEqual(self.tree.preorder_trav(), ['+','-','1','2','*','3','4'])

    def test_postorder_trav(self):
        self.assertEqual(self.tree.postorder_trav(), ['1','2','-','3','4','*','+'])

    def test_bfs_trav(self):
        self.assertEqual(self.tree.bfs_trav(), ['+','-','*','1','2','3','4'])

    def test_division_by_zero(self):
        with self.assertRaises(ValueError) as cm:
            Tree('/', Tree('1'), Tree('0')).evaluate_tree()
        self.assertEqual(str(cm.exception), "Division by zero is not allowed.")



if __name__ == '__main__':
    
    expression = None
    while expression != 'quit':
        expression = raw_input("\n Enter an expression, if you want to run the tests: 'tests' or to exit: 'quit': ")
        if expression.lower() == 'quit':
            break
        if expression.lower() == 'tests':
            unittest.main()
        try:
            binarytree = List_to_Tree(expression)
            print("\n[1] Evaluate \n[2] Preorder \n[3] Postorder \n[4] Breadth First \n[5] Visualize the Tree \n[6] Nested List\n[0] new expression\n")
            option = None
            while option != '0':


                option = raw_input('\n which of the following would you like know about this tree ')
                if option == '1':
                    print('\n The result of this expression is: ' + str(binarytree._tree.evaluate_tree()))
                elif option == '2':
                    print('\n This preorder traversal of this tree is: ' + str(binarytree._tree.preorder_trav()))
                elif option == '3':
                    print('\n This postorder traversal of this tree is: ' + str(binarytree._tree.postorder_trav()))
                elif option == '4':
                    print('\n This breadth first traversal of this tree is: ' + str(binarytree._tree.bfs_trav()))
                elif option == '5':
                    print('\n The visualisation of the tree is: \n')
                    print(binarytree.tree())
                elif option == '6':
                    print('\n' + 'The nested list the epxression was converted into is: ' + str(binarytree))

        except Exception as error:
            print("\nAn error occurred: {}".format(error))
