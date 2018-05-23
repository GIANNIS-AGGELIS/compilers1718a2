
"""
GRAMMER

Stmt_list       ->      Stmt Stmt_list | .
Stmt            ->      id assign Expr | print Expr .
Expr            ->      ATerm ATerm_tail.
ATerm_tail       ->      OrOp ATerm ATerm_tail | .
ATerm            ->      BTerm BTerm_tail.
BTerm_tail      ->      AndOp BTerm BTerm_tail |.
BTerm           ->      Factor  | Notop Factor .
Factor          ->      (Expr) | id |number  .    
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
        self.not_op = ' ' 
    
    
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
        #print('Stmt_list :', self.la )
        if self.la == 'IDENTIFIR' or self.la == 'print':
            self.stmt()
            self.stmtList()
        elif self.la is None:
            return
        else:
            raise ParseError("Perimeno IDENTIFIR || print")
    
    def stmt(self):
        #print('Stmt :',self.la)
        if self.la == 'IDENTIFIR':
            varname = self.val
            self.match('IDENTIFIR')
            self.match('=')
            self.st[varname] = self.expr()
        elif self.la == 'print':
            self.match('print')
            print(self.expr())
        else:
            raise ParseError("PERIMENO IDENTIFIR || =")
    
    def expr(self):
        #print('Expr :',self.la)
        if  self.la == '(' or self.la == 'IDENTIFIR' or self.la == 'TRUE' or self.la == 'FALSE' or self.la == 'NOT'  :
            e  = self.ATerm()
            AtT = self.ATermTail()
            if AtT is None:
                return e
            if AtT[0] == 'OR':
                if e == 'FALSE' and AtT[1] == 'FALSE':
                    return('FALSE')
                else:
                    return('TRUE')
        elif self.la in ('IDENTIFIR','print',')'):
            return
        else:
            raise ParseError("PERIMENO ( || IDENTIFIR || TRUE || FALSE <++>")
    
    def ATermTail(self):
        #print('ATermTail :',self.la)
        if self.la == 'OR':
            op = self.orop()
            AT  = self.ATerm()
            AtT = self.ATermTail()
            if AtT is None :
                return(op,AT)
            if AtT[0] == 'OR':
                if AT == 'FALSE' and AtT[1] == 'FALSE':
                    return(op,'FALSE')
                else:
                    return(op,'TRUE')
        elif self.la in ('IDENTIFIR','print',None,')'):
            return
        else:
            raise ParseError("PERIMENO OR")
    
    def ATerm(self):
        #print('ATerm :',self.la)
        if self.la == '(' or self.la == 'IDENTIFIR' or self.la == 'TRUE' or self.la == 'FALSE' or self.la == 'NOT':
            Bt  = self.BTerm()
            BtT = self.BTermTail()
            if BtT is None:
                return Bt
            if BtT[0] == 'AND':
                if Bt == 'TRUE' and BtT[1] == 'TRUE':
                    return('TRUE')
                else:
                    return('FALSE')
        elif self.la in ('OR','IDENTIFIR','print',')'):
            return
        else:
            raise ParseError("PERIMENO ( || IDENTIFIR || TRUE || FALSE")
    
    
    def BTermTail(self):
        #print('BTermTail :',self.la)
        if self.la == 'AND':
            op = self.andop()
            bt = self.BTerm()
            btT = self.BTermTail()  
            if btT is None:
                return op,bt
            if btT[0] == 'AND':
                if bt == 'TRUE' and btT[1] == 'TRUE':
                    return(op,'TRUE')
                else:
                    return(op,'FALSE')
        elif self.la in ('OR','IDENTIFIR','print',None,')'):
            return
        else:
            raise ParseError("PERIMENO AND")
    
    
    def BTerm(self):
        #print('BTerm :',self.la)
        if self.la == 'NOT':
            self.not_op = self.notop()
            f = self.factor()
            return f
        elif self.la == '(' or self.la == 'IDENTIFIR' or self.la == 'TRUE' or self.la == 'FALSE':
            f = self.factor()
            return f
        else:
            raise ParseError("PERIMENO  not")
            
    
  
    
    def factor(self):
        #print('Factor :',self.la)
        if self.la == '(':
            self.match('(')
            e = self.expr()
            self.match(')')
            return e
        elif self.la == 'IDENTIFIR':
            varname = self.val
            #print('123', self.val)
            self.match('IDENTIFIR')
            if varname in self.st:
                #print('st ',self.st[varname])
                return self.st[varname]
            raise RunError('inisialize variable ' + varname ) 
        elif self.la ==  'TRUE':
            self.match('TRUE')
            if self.not_op == 'NOT':
                return('FALSE')
            return('TRUE')
        elif self.la == 'FALSE':
            self.match('FALSE')
            if self.not_op == 'NOT':
                return('TRUE')
            return('FALSE')
        elif self.la in ('NOT','AND','OR',')','print'):
            return
        else:
            raise ParseError('Perimeno ( || IDENTIFIR || TRUE || FALSE ')
    
    def orop(self):
        #print('Orop :',self.la)
        if self.la == 'OR':
            self.match('OR')
            return('OR')
        else:
            raise ParseError("PERIMENO or")
    
    def andop(self):
        #print('AndOp :',self.la)
        if self.la == 'AND':
            self.match('AND')
            return('AND')
        else:
            raise ParseError("PERIMENO and ")
    
    def notop(self):
        #print('NotOp :',self.la)
        if self.la == 'NOT':
            self.match('NOT')
            return('NOT')
        else:
            raise ParseError("PERIMENO  not ")
    
    def match(self,token):
        if self.la == token:
            print('Match', self.la,' ' ,self.val)
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





