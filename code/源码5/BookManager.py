class Book:
    # 类属性：受保护，子类可访问，外部不可直接修改
    _book_counter = 0
    _book_list = []

    def __init__(self):
        self.name = ""
        self.author = ""
        self.isbn_number = ""
        self.book_type = ""

    def add_book(self):
        """父类统一处理计数和列表添加"""
        if not all([self.name, self.author, self.isbn_number, self.book_type]):
            raise ValueError("图书名称、作者、ISBN、类型不能为空！")
        # 校验ISBN避免重复添加
        for book in Book._book_list:
            if book["ISBN"] == self.isbn_number:
                raise ValueError(f"ISBN {self.isbn_number} 已存在，无法重复添加！")
        Book._book_counter += 1
        Book._book_list.append({
            "Name": self.name,
            "Type": self.book_type,
            "Author": self.author,
            "ISBN": self.isbn_number
        })
        print(f"添加成功")

    def get_book_list(self):
        """查询所有图书"""
        print(f"\n当前库存总数：{Book._book_counter} 本")
        if not Book._book_list:
            print("库存为空")
            return
        for idx, book in enumerate(Book._book_list, 1):
            # 添加序号方便查看
            print(f"{idx}. {book}")

    def _check_book_exist_by_name(self, name):
        """受保护方法：查询图书是否存在，返回索引（0开始），不存在返回-1"""
        if not Book._book_list:
            return -1
        for idx, book in enumerate(Book._book_list):
            if book["Name"] == name:
                return idx
        return -1

    def del_book(self, name):
        """删除图书（按书名）"""
        idx = self._check_book_exist_by_name(name)
        if idx != -1:
            deleted_book = Book._book_list.pop(idx)
            Book._book_counter -= 1
            print(f"成功删除：{deleted_book}")
        else:
            raise ValueError(f"删除失败：不存在书名为《{name}》的图书")

# 子类：纸质书（继承Book，复用核心方法，仅扩展类型）
class PaperBook(Book):
    def __init__(self, name="", author="", isbn_number=""):
        super().__init__()
        self.book_type = "纸质书"  # 固定类型
        self.name = name
        self.author = author
        self.isbn_number = isbn_number

# 子类：电子书（继承Book，复用核心方法，仅扩展类型）
class EBook(Book):
    def __init__(self, name="", author="", isbn_number=""):
        super().__init__()
        self.book_type = "电子书"
        self.name = name
        self.author = author
        self.isbn_number = isbn_number

# 测试代码
if __name__ == "__main__":
    book1 = PaperBook(name="Python编程", author="Tom", isbn_number="123456")
    book2 = EBook(name="Java核心技术", author="Jerry", isbn_number="789012")

    try:

        book1.add_book()
        book2.add_book()

        book1.get_book_list()

        book1.del_book("Python编程")
        book1.get_book_list()

        # 删除不存在的书
        book1.del_book("C++ Primer")
    except ValueError as e:
        print(f"\n错误提示：{e}")