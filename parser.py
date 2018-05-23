
"""
GRAMMER

Stmt_list       ->      Stmt Stmt_list | .
Stmt            ->      id assign Expr | print Expr .
Expr            ->      ATerm ATerm_tail.
ATerm_tail       ->      OrOp ATerm ATerm_tail | .
ATerm            ->      BTerm BTerm_tail.
BTerm_tail      ->      AndOp BTerm BTerm_tail |.
BTerm           ->      Factor  | Notop Factor .
Factor          ->      (Expr) | id |number | .    
OrOp            ->      or  .
AndOp           ->      and .
Notop           ->      not .




"""


import plex

class ParseError(Exception): 
    pass

class RunError(Exception):
    pass

class MyParser:
    
    def __init__(self):
        self.st = {}
    
    
    def create_scanner(self,fp):
        
        space = plex.Rep1(plex.Any(' \n\t'))
        digit = plex.Range('09')
        true =  plex.NoCase(plex.Str('TRUE','t','1'))
        false = plex.NoCase(plex.Str('FALSE','f','0'))
        andop = plex.Str("and")
        orop  = plex.Str("or")
        notop = plex.Str("not")
        opereitor = plex.Any('=()')
        keyword = plex.Str('print')
        letter = plex.Range('azAZ')
        name = letter+ plex.Rep(letter|digit)
        single_coment = plex.Str('//') + plex.Rep(plex.AnyBut('\n'))

        lexicon = plex.Lexicon([
            (keyword,plex.TEXT),
            (orop,'OR'),
            (andop,'AND'),
            (notop,'NOT'),
            (true,'TRUE'),
            (false,'FALSE'),
            (name,'IDENTIFIR'),
            (space,plex.IGNORE),
            (opereitor,plex.TEXT),
            (single_coment,plex.IGNORE)
            ])
        # create and store the scanner object    
        self.scanner = plex.Scanner(lexicon,fp)
        # get initial lookahead
        self.la,self.val = self.next_token()
        
    def stmtList(self):
        print('Stmt_list :', self.la )
        if self.la == 'IDENTIFIR' or self.la == 'print':
            self.stmt()
            self.stmtList()
        elif self.la is None:
            return
        else:
            raise ParseError("Perimeno IDENTIFIR || print")
    
    def stmt(self):
        print('Stmt :',self.la)
        if self.la == 'IDENTIFIR':
            self.match('IDENTIFIR')
            self.match('=')
            self.expr()
        elif self.la == 'print':
            self.match('print')
            self.expr()
        else:
            raise ParseError("PERIMENO IDENTIFIR || =")
    
    def expr(self):
        print('Expr :',self.la)
        if  self.la == '(' or self.la == 'IDENTIFIR' or self.la == 'TRUE' or self.la == 'FALSE' or self.la == 'NOT'  :
            self.ATerm()
            self.ATermTail()
        elif self.la in ('IDENTIFIR','print',')'):
            return
        else:
            raise ParseError("PERIMENO ( || IDENTIFIR || TRUE || FALSE <++>")
    
    def ATermTail(self):
        print('ATermTail :',self.la)
        if self.la == 'OR':
            self.ATerm()
            self.ATermTail()
        elif self.la in ('IDENTIFIR','print',None,')'):
            return
        else:
            raise ParseError("PERIMENO OR")
    
    def ATerm(self):
        print('ATerm :',self.la)
        if self.la == '(' or self.la == 'IDENTIFIR' or self.la == 'TRUE' or self.la == 'FALSE' or self.la == 'NOT':
            self.BTerm()
            self.BTermTail()
        elif self.la in ('OR','IDENTIFIR','print',')'):
            return
        else:
            raise ParseError("PERIMENO ( || IDENTIFIR || TRUE || FALSE")
    
    
    def BTermTail(self):
        print('BTermTail :',self.la)
        if self.la == 'AND':
            self.andop()
            self.BTerm()
            self.BTermTail()    
        elif self.la in ('OR','IDENTIFIR','print',None,')'):
            return
        else:
            raise ParseError("PERIMENO AND")
    
    
    def BTerm(self):
        print('BTerm :',self.la)
        if self.la == 'NOT':
            self.notop()
            self.factor()
        elif self.la == '(' or self.la == 'IDENTIFIR' or self.la == 'TRUE' or self.la == 'FALSE':
            self.factor()
        else:
            raise ParseError("PERIMENO  not")
            
    
  
    
    def factor(self):
        print('Factor :',self.la)
        if self.la == '(':
            self.match('(')
            self.expr()
            self.match(')')
        elif self.la == 'IDENTIFIR':
            self.match('IDENTIFIR')
        elif self.la ==  'TRUE':
            self.match('TRUE')
        elif self.la == 'FALSE':
            self.match('FALSE')
        elif self.la in ('NOT','AND','OR',')','print'):
            return
        else:
            raise ParseError('Perimeno ( || IDENTIFIR || TRUE || FALSE ')
    
    def orop(self):
        print('Orop :',self.la)
        if self.la == 'OR':
            self.match('OR')
        else:
            raise ParseError("PERIMENO or")
    
    def andop(self):
        print('AndOp :',self.la)
        if self.la == 'AND':
            self.match('AND')
        else:
            raise ParseError("PERIMENO and ")
    
    def notop(self):
        print('NotOp :',self.la)
        if self.la == 'NOT':
            self.match('NOT')
        else:
            raise ParseError("PERIMENO  not ")
    
    def match(self,token):
        if self.la == token:
            #print('Match', self.la,' ' ,self.val)
            self.la,self.val = self.next_token()
        else:
            raise ParseError(self.la,token)
    
    
    def next_token(self):
        return self.scanner.read()
    
    def parse(self,fp):
        self.create_scanner(fp)
        self.stmtList()
        # while True:
        #     token,text = self.next_token()
        #     if token is None:break
        #     print(token,text)
   
parser = MyParser()
with open('test.txt') as fp:
    try:
        parser.parse(fp)
       
    except ParseError as perr:
        print(perr)





