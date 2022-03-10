# AST相关

ast的使用：https://jckling.github.io/2021/07/14/Other/Python%20ast%20%E6%A8%A1%E5%9D%97%E4%BD%BF%E7%94%A8/

![image-20220307150343187](AST相关文档.assets/image-20220307150343187-6636624.png)



反向解析ast库 astor



class ast.NodeVisitor 和 class ast.NodeTransformer。。这两个的区别就是visit是修改原来的node,transformer可以替换一个新的node.

https://www.escapelife.site/posts/40a2fc93.html



当我们去编译一个节点树的时候，编译器需要为支持它们的提供一个`lineno`和`col_offset`来表示它们的位置。而`Python`又是一个非常注意代码缩进的语言，所以使用`fix_missing_locations`来自动补齐缩进功能。
