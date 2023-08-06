class string(str):
    def rep(self,substring):
        self = string(self.replace(substring,''))
        return self
    def isempty(self):
        return self.strip() == ''
    def ad(self, value):
        self = string(self + getattr(self, 'delim', "")  + value)
        return self
    def delim(self, value):
        self.delim = value
    def pre(self, value):
        self = string(value + getattr(self, 'delim', "")  + self)
        return self
    def pres(self, *args):
        for arg in args:
            self = self.pre(arg)
        return self
    def empty(self):
        return self is None or self.strip() == '' or self.strip().lower() == 'nan'
    def format(self, numstyle='06'):
        return format(int(self),numstyle)
    def splitsies(self,*args,joiner=":"):
        output_list = []
        for splitter_itr, splitter in enumerate(args):
            if splitter_itr == 0:
                output_list = self.split(splitter)
            else:
                temp_list = string(joiner.join(output_list)).splitsies(splitter,joiner=joiner)
                output_list = []
                for temp_item in temp_list:
                    for temp_split_item in temp_item.split(joiner):
                        output_list.append(temp_split_item)

        return output_list