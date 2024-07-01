# pdf parser

from typing import Iterator, NoReturn
import re
from enum import Enum

class PDFStructure(Enum):
    Default= 'default' # default
    Header= 'header' # header
    Body= 'body' # body
    CRT= 'crt' # cross-reference table
    Trailer= 'trainer' # trailer
    EOF= 'eof' # eof
    

class PDFParser():
    """PDF Parser Class
    """
    def __init__(
            self,
            content:Iterator[bytes]
        ) -> NoReturn:
        self.content = content

        self.current_struct = PDFStructure.Default

        # pdf header
        self.header = []
        self.pdf_version = ''

        self.tmp_obj_id = -1
        self.tmp_obj_a = -1

        # pdf body
        self.body = []
        self.obj_list = {}

        # pdf CRT
        self.crt = []

        # pdf trailer
        self.trailer = []

    def parser(self) -> NoReturn:
        """对PDF原始文件进行解析

        Returns:
            NoReturn: _description_
        """
        self.split_struture()

        # 对body中的obj进行解析
        self.get_obj_list()

        # 根据trailer对文件进行解析，分为，file struct和 document struct


    def split_struture(self) -> NoReturn:
        """对PDF原始文件进行切分，分为header,body,crt,trailer部分

        Returns:
            NoReturn: _description_
        """
        for content_line in self.content:
            content_line_str = str(content_line)
            # get current struct
            if self.current_struct == PDFStructure.Default:
                # find header
                bool_find = self.find_header(content_line=content_line_str)
                if bool_find == True:
                    self.current_struct = PDFStructure.Header
                    self.header.append(content_line)
            elif self.current_struct == PDFStructure.Header:
                # find body
                bool_find = self.find_body_obj_start(content_line=content_line_str)
                if bool_find == True:
                    self.current_struct = PDFStructure.Body
                    self.body.append(content_line)
                else:
                    self.header.append(content_line)
            elif self.current_struct == PDFStructure.Body:
                # find crt
                bool_find = self.find_crt(content_line=content_line_str)

                if bool_find == True:
                    self.current_struct = PDFStructure.CRT
                    self.crt.append(content_line)
                else:
                    self.body.append(content_line)
                
            elif self.current_struct == PDFStructure.CRT:
                # find trailer
                bool_find = self.find_trailer(content_line=content_line_str)
                if bool_find == True:
                    self.current_struct = PDFStructure.Trailer
                    self.trailer.append(content_line)
                else:
                    self.crt.append(content_line)
            elif self.current_struct == PDFStructure.Trailer:
                # find eof
                bool_find = self.find_eof(content_line=content_line_str)
                if bool_find == True:
                    self.trailer.append(content_line)
                    self.current_struct = PDFStructure.EOF
                else:
                    self.trailer.append(content_line)
            elif self.current_struct == PDFStructure.EOF:
                break

    def get_obj_list(self) -> NoReturn:
        # 是否在obj中标识符
        bool_in_obj = False
        self.obj_list = {}

        tmp_obj_list = {
            'obj_content_line': [],
        }
        # 遍历body中的行
        for content_line in self.body:
            content_line_str = str(content_line)
            if not bool_in_obj:
                bool_find = self.find_body_obj_start(content_line=content_line_str)
                if bool_find:
                    tmp_obj_list['obj_content_line'].append(content_line)
                    bool_in_obj = True
            else:
                bool_find = self.find_body_obj_end(content_line=content_line_str)
                if bool_find:
                    tmp_obj_list['obj_content_line'].append(content_line)
                    self.obj_list[self.tmp_obj_id] = tmp_obj_list
                    tmp_obj_list = {
                        'obj_content_line': [],
                    }
                    bool_in_obj = False



    def find_header(self, content_line:str) -> bool:
        """找到PDF原始内容中的header部分

        Args:
            content_line (str): PDF原始内容中的一行数据

        Returns:
            bool: _description_
        """
        pattern = r'%PDF-([\d\.]+)'
        match = re.search(pattern, content_line)
        
        if match:
            self.pdf_version = match.group(1)
            return True
        else:
            return False
        
    def find_body_obj_start(self, content_line:str) -> bool:
        """找到PDF原始内容中obj块中的开始部分

        Args:
            content_line (str): PDF原始内容中的一行数据

        Returns:
            bool: _description_
        """
        pattern = r'(\d+)\s+(\d+)\s+obj'
        match = re.search(pattern=pattern, string=content_line)
        if match :
            self.tmp_obj_id = match.group(1)
            self.tmp_obj_a = match.group(2)
            return True
        return bool(match)

    def find_body_obj_end(self, content_line:str) -> bool:
        """找到PDF原始内容中obj块中的结束部分

        Args:
            content_line (str): PDF原始内容中的一行数据

        Returns:
            bool: _description_
        """
        pattern = r'endobj'
        match = re.search(pattern=pattern, string=content_line)

        return bool(match)

    def find_crt(self, content_line:str) -> bool:
        """找到PDF原始内容中crt块

        Args:
            content_line (str): PDF原始内容中的一行数据

        Returns:
            bool: _description_
        """
        pattern = r'xref'
        match = re.search(pattern=pattern, string=content_line)

        return bool(match)

    def find_trailer(self, content_line:str) -> bool:
        """找到PDF原始内容中trailer块

        Args:
            content_line (str): PDF原始内容中的一行数据

        Returns:
            bool: _description_
        """
        pattern = r'trailer'
        match = re.search(pattern=pattern, string=content_line)
        return bool(match)

    def find_eof(self, content_line:str) -> bool:
        """找到PDF原始内容中EOF结束标识

        Args:
            content_line (str): PDF原始内容中的一行数据

        Returns:
            bool: _description_
        """
        pattern = r'%%EOF'
        match = re.search(pattern=pattern, string=content_line)
        return bool(match)

