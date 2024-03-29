
"""
 * @author nhphung
"""
from ast import Global
from AST import * 
from Visitor import *
from StaticError import *
import sys
from functools import reduce

sys.path.append('../utils')

def lookup(name,lst,func):
    for x in lst:
        ## print('Looking up:', name, func(x))
        if name == func(x):
            # print('Accept')
            return x
    return None

def flatten(lst):
    if not isinstance(lst, list):
        return [lst]
    if len(lst) == 0:
        return []
    if len(lst) == 1:
        return flatten(lst[0])
    head, tail = lst[0], lst[1:]
    return flatten(head) + flatten(tail)

class Scope:
    debug = False
    # debug = True
    @staticmethod
    def start(section):
        print("================   " + section + "   ================") if Scope.debug else None
        pass

    @staticmethod
    def end():
        print("=====================================================") if Scope.debug else None
        pass

    @staticmethod
    def isExisten(listSymbols, symbol):
        return len([x for x in listSymbols if str(x.name) == str(symbol.name)]) > 0

    @staticmethod
    def merge(currentScope, comingScope):
        return reduce(lambda lst, sym: lst if Scope.isExisten(lst, sym) else lst+[sym], currentScope, comingScope)

    @staticmethod
    def log(scope): 
        [print(x) for x in scope] if Scope.debug else None


class TypeUtils:
    @staticmethod
    def isNaNType(expType):
        return type(expType) not in [IntType, FloatType]

    @staticmethod
    def isMatchType(var,types):
        lhs, rhs = var
        return type(lhs) in types and type(rhs) in types

    @staticmethod
    def isOpForIntFloat(operator):
        return str(operator).lower() in ['+', '-', '*', '/', '%', '>', '<', '>=', '<=']

    @staticmethod
    def isOpForIntBoolean(operator):
        return str(operator).lower() in ['==','!=']

    @staticmethod
    def isOpForBoolean(operator):
        return str(operator).lower() in ['&&','||']

    @staticmethod
    def isOpForString(operator):
        return str(operator).lower() in ['==.','+.']

    @staticmethod
    def mergeNumberType(lType, rType):
        return FloatType() if FloatType in [type(x) for x in [lType, rType]] else IntType()


class MType:
    def __init__(self,partype,rettype):
        self.partype = partype
        self.rettype = rettype

    def __str__(self):
        return 'MType([' + ','.join([str(i) for i in self.partype]) + '],' + str(self.rettype) + ')'


class Checker:
    # utils = Utils()

    @staticmethod
    def checkRedeclared(currentScope, listNewSymbols):
        # Return merged scope
        newScope = currentScope.copy()
        for x in listNewSymbols:
            f = lookup(Symbol.cmp(x), newScope, Symbol.cmp)
            if f is not None:
                raise Redeclared(x.kind, x.name)
            newScope.append(x)
        return newScope

    @staticmethod
    def checkUndeclared(visibleScope, name, kind, notGlobal=False):
        scope = visibleScope if not notGlobal else [x for x in visibleScope if not x.isGlobal]
        res = lookup(str(name), scope, lambda x: x.name)
        ## print('Check Undelcared with', kind)
        if res is None:
            raise Undeclared(kind, name)
        return res
    
    @staticmethod
    def checkUndeclaredWithType(visibleScope, name, kind, notGlobal=False):
        scope = visibleScope if not notGlobal else [x for x in visibleScope if not x.isGlobal]
        res = lookup((str(name),kind), scope, lambda x: x.toTuple())
        if res is None:
            raise Undeclared(kind, name)
        return res


    @staticmethod
    def matchType(patternType, paramType):
        # Handle Array Type
        if ArrayType in [type(x) for x in [patternType, paramType]]:
            if type(patternType) != type(paramType): return False
            return Checker.matchArrayType(patternType, paramType)

        # Handle Primitive Types
        # Type Coercion happens right here
        ## print('Comparing',type(patternType),type(paramType))
        if type(patternType) is ClassType and type(paramType) is NullLiteral: return True

        if type(patternType) == type(paramType): return True
        if type(patternType) is FloatType and type(paramType) is IntType: return True
        return False

    @staticmethod
    def matchArrayType(a, b):
        while type(a) is ArrayType and type(b) is ArrayType:
            if type(a.eleType) != type(b.eleType) or a.size != b.size:
                return False
            a = a.eleType
            b = b.eleType

        if type(a) != type(b): return False
        else: return True

    @staticmethod
    def checkParamType(pattern, params):
        if len(pattern) != len(params): return False
        return all([Checker.matchType(a, b) for a, b in zip(pattern, params)])

    @staticmethod
    def isSameTypeArray(lst):
        for i in lst:
            for j in lst:
                if type(i) != type(j): return False
        return True

class Symbol:
    def __init__(self, name, mtype, value=None, kind=Class(), isGlobal=False, memberKind=None, isConstant = False):
        self.name = name
        self.mtype = mtype
        self.value = value
        self.kind = kind
        self.isGlobal = isGlobal
        self.child = None
        self.memberKind = memberKind
        self.isConstant = isConstant

    def __str__(self):
        return 'Symbol(' + self.name + ',' + str(self.mtype) + ',' + str(self.kind) + ',' + str(self.value) + ')'


    def setGlobal(self):
        self.isGlobal = True
        return self
    
    def setParam(self):
        self.kind = Parameter()
        return self

    def getKind(self):
        return self.kind if type(self.mtype) is MType else Identifier()

    def toTuple(self):
        return (str(self.name), type(self.getKind()))

    def toTupleString(self):
        return (str(self.name), str(self.mtype))
    
    # compare function between 2 instances
    @staticmethod
    def cmp(symbol):
        return str(symbol.name)

    @staticmethod
    def fromVarDecl(decl,value=None):
        return Symbol(decl.variable.name, decl.varType, kind=Variable(),value=value)

    @staticmethod
    def fromConstDecl(decl,value=None):
        return Symbol(decl.constant.name, decl.constType, kind=Constant(),value=value,isConstant=True)

    @staticmethod
    def fromMethodDecl(decl):
        paramType = [x.varType for x in decl.param]
        return Symbol(decl.name.name, MType(paramType, VoidType()), kind=Method())

    @staticmethod
    def fromAttributeDecl(decl):
        kind = Attribute()
        if type(decl.decl) is VarDecl:
            # name = decl.decl.variable.name[1:] if type(decl.kind) == Static else decl.decl.variable.name 
            return Symbol(decl.decl.variable.name, decl.decl.varType, kind=kind, memberKind=decl.kind)
        else:
            # name = decl.decl.constant.name[1:] if type(decl.kind) == Static else decl.decl.constant.name 
            return Symbol(decl.decl.constant.name, decl.decl.constType, kind=kind, memberKind=decl.kind, isConstant=True)

    @staticmethod
    def fromDecl(decl):
        return Symbol.fromAttributeDecl(decl) if type(decl) is AttributeDecl else Symbol.fromMethodDecl(decl)

    @staticmethod
    def fromClassDecl(decl):
        return Symbol(decl.classname.name,ClassType(decl.classname),kind=Class())

class GlobalStack:
    stack = []

    def isEmpty():
        return GlobalStack.stack.isEmpty()
    def pop():
        return GlobalStack.stack.pop()

    def push(symbols):
        ## print('new symbol pushed to stack')
        GlobalStack.stack.append(symbols)

    def log():
        ## print('Stack trace:')
        [print(x) for x in GlobalStack.stack]
        ## print('End stack trace:')

class StaticChecker(BaseVisitor):

    global_envi = [
    # Symbol("getInt",MType([],IntType())),
    # Symbol("putIntLn",MType([IntType()],VoidType()))
    ]

    def __init__(self,ast):
        self.ast = ast

    def check(self):
        return self.visit(self.ast,StaticChecker.global_envi)

    def visitProgram(self,ast:Program, scope):

        ## Pop all element from GlobalStack
        while len(GlobalStack.stack) != 0 :
            GlobalStack.stack.pop()
        
        symbols= [Symbol.fromClassDecl(x) for x in ast.decl]
        scope = Checker.checkRedeclared(scope,symbols)
        for x in ast.decl:
            self.visit(x,scope)

        ## NO ENTRY POINT EXCEPTION
        flag = False
        for x in GlobalStack.stack:
            if x.name == 'Program':
                for y in x.child:
                    flag = True if (y.name == 'main' and len(y.mtype.partype) == 0)  else False

        if not flag: raise NoEntryPoint()

        return []
    
    ################ CLASS DECLARATION ###################
    def visitClassDecl(self,ast:ClassDecl, scope):
        
        Scope.start('ClassDecl')
        Scope.log(scope)

        if ast.parentname is not None:
            Checker.checkUndeclared(scope,ast.parentname.name,Class())
        
        symbols = [Symbol.fromDecl(x) for x in ast.memlist]

        ## Add nested symbol to scoped
        classSymbol = Symbol.fromClassDecl(ast)
        classSymbol.child = symbols
        GlobalStack.push(classSymbol)
        # GlobalStack.log()

        ## Check redeclared
        newScope = Checker.checkRedeclared([],symbols)
        scope = scope + newScope

        attributes = [self.visit(x,scope) for x in ast.memlist]
        
        Scope.end()

        return scope

    def visitMethodDecl(self,ast:MethodDecl, scope):
        # methodSymbol = Symbol.fromMethodDecl(ast)

        Scope.start('Method Decl')
        Scope.log(scope)
        #Get params symbol and recheck for redeclared
        listParams = [Symbol.fromVarDecl(x).setParam() for x in ast.param]
        listParams = Checker.checkRedeclared([],listParams)
        # Merge the parameters with scope before putting to block statement
        scope = Scope.merge(scope,listParams)
        returnTypes, localVars = self.visit(ast.body,(scope,0))
        
        ## Check redeclared after getting local vars from body
        Checker.checkRedeclared(listParams,localVars)

        returnTypes = [x for x in returnTypes if issubclass(type(x),Type)]
        retType = returnTypes[0] if len(returnTypes) != 0 else VoidType()
        
        #After get the new vars that appear in block statements, check with the params the redeclared with outside scope
        # listNewSymbols = listParams
        # newScope = Checker.checkRedeclared([],listNewSymbols)

        f = lookup(ast.name.name,scope, lambda x: x.name)
        f.mtype.rettype = retType

        listParams = [x.mtype for x in listParams ]
        ## print(ast.name.name,'returning:',Symbol(ast.name.name, MType(listParams,retType),kind=Method()))
        Scope.end()

        return  Symbol(ast.name.name, MType(listParams,retType),kind=Method())

    def visitAttributeDecl(self, ast:AttributeDecl, scope):
        #check type before assignment
        ## Khai typemismatch bi thieu AttributeDecl
        attrSymbol = self.visit(ast.decl, scope) 
        attrSymbol.kind = Attribute()
        attrSymbol.memberKind = ast.kind
        return attrSymbol

    def visitVarDecl(self, ast:VarDecl, scope):
        if type(scope[0]) is list:
            scope, _ = scope

        #check type before assignment
        varInitType = None
        if ast.varInit is not None:
            varInitType,_ = self.visit(ast.varInit,scope)
            ## print('Checking ')
            ### Only support primitive type only, will error when test with Array + Object
            ## print(ast.varType,varInitType)
            if not Checker.matchType(ast.varType,varInitType): 
                raise TypeMismatchInStatement(ast)
            
        if type(ast.varType) is ClassType:
            Checker.checkUndeclared(GlobalStack.stack,ast.varType.classname.name,Class())

        return Symbol.fromVarDecl(ast,value=varInitType)

    def visitConstDecl(self, ast:ConstDecl, scope):
        if type(scope[0]) is list:
            scope, _ = scope
        #check type before assignment
        if ast.value is None:
            raise IllegalConstantExpression(ast.value)
        # raise IllegalConstantExpression(ast.value)


        valueType, symbol = self.visit(ast.value,scope)
        if symbol is not None:
            if symbol.value is None: 
                raise IllegalConstantExpression(ast.value)

        ## print('Checking ')
        ### Only support primitive type only, will error when test with Array + Object
        ## print(ast.constType,valueType)
        if not Checker.matchType(ast.constType,valueType): 
            raise TypeMismatchInConstant(ast)

        return Symbol.fromConstDecl(ast,value=valueType)


    ################### STATEMENT PART #######################
    def visitBlock(self, ast:Block,scope):
        scope, inLoop = scope
        # print('Block in loop: ' + str(inLoop))

        #used to get objects returned from decls
        arr = []
        symbols = []

        for i in ast.inst:
            if i is None: continue
            res= self.visit(i, (scope,inLoop))
            if type(res) is Symbol:
                scope = Scope.merge(scope,[res])
                symbols.append(res)
            # elif issubclass(type(res),Type):
            arr.append(res)
        return flatten(arr),symbols

    def visitIf(self,ast:If,scope):
        scope, inLoop = scope
        expr, _ = self.visit(ast.expr, scope)
        thenStmt, _ = self.visit(ast.thenStmt, (scope, inLoop)) 
        
        # print(ast.elseStmt)
        elseStmt = None
        if ast.elseStmt is not None:
            elseStmt, _  = self.visit(ast.elseStmt, (scope, inLoop)) 
        
        if type(expr) is not BoolType:
            raise TypeMismatchInStatement(ast)
        
        return [thenStmt,elseStmt] 

    def visitAssign(self,ast:Assign,scope):
        scope, inLoop = scope

        Scope.start("Assign")
        Scope.log(scope)
        
        #Return symbol for lhs and rhs
        lhsType, symbol = self.visit(ast.lhs, scope)
        rhsType, _ = self.visit(ast.exp, scope)
        
        if symbol is not None:
            if symbol.isConstant: raise CannotAssignToConstant(ast)

        ## print("Comparing")
        ## print(type(lhsType))
        ## print(type(rhsType))
        if type(lhsType) is VoidType or not Checker.matchType(lhsType, rhsType):
            raise TypeMismatchInStatement(ast)
        Scope.end()

    def visitCallStmt(self,ast:CallStmt,scope):
        scope, inLoop = scope
        # Return None Type
        Scope.start("CallStmt")
        Scope.log(scope)

        objType, symbol = self.visit(ast.obj,scope)

        ## If obj is not an ID
        if symbol is None: raise TypeMismatchInStatement(ast)
        
        ##This is static field access
        if ast.method.name[0] == '$':
            if type(symbol.kind) is not Class:
                raise IllegalMemberAccess(ast)

            classSymbol = Checker.checkUndeclared(GlobalStack.stack, ast.obj.name, kind=Class())
        ## This is instance field access
        else:
            objInstance = symbol
            if type(symbol.kind) is Class:
                raise IllegalMemberAccess(ast)

            className = objInstance.mtype.classname.name
            classSymbol = Checker.checkUndeclared(GlobalStack.stack, className, kind=Class())

        if type(classSymbol.kind) is not Class: raise TypeMismatchInStatement(ast)

        methodSymbol = Checker.checkUndeclared(classSymbol.child, ast.method.name,kind=Method())
        if methodSymbol.mtype.rettype is None: raise Undeclared(Method(),ast.method.name)
        ## print('afsdfasdfasdf',methodSymbol.mtype)
        # ## If obj is an ID
        # if type(ast.obj) is not Id: raise TypeMismatchInStatement(ast)

        # ## Look up in the GlobalStack to find the correct nested array
        # obj = Checker.checkUndeclared(GlobalStack.stack,ast.obj.name,Class())
        
        # # print('kind',obj.kind)
        # # if type(obj.kind) is not Class: raise TypeMismatchInStatement(ast)

        # f = Checker.checkUndeclared(obj.child, ast.method.name, kind=Method())
        # # print('childList',[str(x) for x in childList])

        paramsRetType = [self.visit(x,scope)[0] for x in ast.param]
        
        ## print('Call method type: ',methodSymbol.mtype.rettype)
        if not all([Checker.matchType(a,b) for a,b in zip(methodSymbol.mtype.partype,paramsRetType)]) \
            or len(methodSymbol.mtype.partype) != len(paramsRetType) \
            or type(methodSymbol.mtype.rettype) is not VoidType :
            raise TypeMismatchInStatement(ast)
            
        Scope.end()
        return
    
    def visitFor(self,ast:For,scope):
        scope, inLoop = scope
        inLoop = 1
        
        scalar_var, scalarSymbol  = self.visit(ast.id,scope)
        type1, _ = self.visit(ast.expr1,scope)
        type2, _ = self.visit(ast.expr2,scope)
        if ast.expr3 is not None:
            self.visit(ast.expr3,scope)
        
        ## print(scalar_var,type1,type2)
        for x in [scalar_var,type1,type2]:
            if type(x) is not IntType:
                raise TypeMismatchInStatement(ast)

        newAssignAST = Assign(Id(scalarSymbol.name),ast.expr1)
        self.visit(newAssignAST,(scope,0))

        retTypes, _ = self.visit(ast.loop, (scope,inLoop))
        # print("For",retTypes)
        return retTypes
    
    def visitBreak(self,ast:Break,scope): 
        scope, inLoop = scope
        if not inLoop:
            raise MustInLoop(ast)
        return
    
    def visitContinue(self,ast:Continue,scope):
        scope, inLoop = scope
        if not inLoop:
            raise MustInLoop(ast)
        return 

    def visitReturn(self,ast:Return,scope):
        scope, inLoop = scope
        if ast.expr is not None:
            return  self.visit(ast.expr,scope)[0] ##Take the first element of expr return, which is returnType            
        return VoidType()

    def visitId(self, ast:Id, scope):
        Scope.start('Id')
        Scope.log(scope)
        
        symbol = Checker.checkUndeclared(scope, ast.name, Identifier())
        ## print(ast.name,'return type:',symbol)
        Scope.end()

        return symbol.mtype, symbol

    ############ EXPRESSION PART ##############
    
    def visitBinaryOp(self,ast:BinaryOp,scope):
        op = str(ast.op).lower()
        lType, _ = self.visit(ast.left, scope)
        rType, _ = self.visit(ast.right, scope)
        types = (lType,rType)

        #### Devide op by their operand's type
        if TypeUtils.isOpForIntFloat(op):
            if not TypeUtils.isMatchType(types,[IntType,FloatType]):
                raise TypeMismatchInExpression(ast)
            if op in ['+', '-', '*','/']: 
                return TypeUtils.mergeNumberType(lType, rType), None
            if op in ['%']: return IntType(), None
            #case '<' '>' '<=' '>='
            return BoolType() , None

        if TypeUtils.isOpForIntBoolean(op):
            if not TypeUtils.isMatchType(types, [IntType, BoolType]):
                raise TypeMismatchInExpression(ast)
            return BoolType(), None

        if TypeUtils.isOpForBoolean(op):
            ## print('receive boolean')
            if not ( BoolType is type(lType) and BoolType is type(rType) ):
                raise TypeMismatchInExpression(ast)
            return BoolType(), None

        if TypeUtils.isOpForString(op):
            if not ( StringType is type(lType) and StringType is type(rType) ):
                raise TypeMismatchInExpression(ast)
            if op == '+.': return StringType(), None
            if op == '==.': return BoolType(), None
                

    def visitUnaryOp(self,ast:UnaryOp,scope):
        op = str(ast.op).lower()
        body, _ = self.visit(ast.body,scope)

        #Check type
        if op == '-' and type(body) not in [IntType,FloatType]:
            raise TypeMismatchInExpression(ast)
        if op == '!' and type(body) is not BoolType:
            raise TypeMismatchInExpression(ast)
        
        return body, None

    def visitCallExpr(self,ast:CallExpr,scope):
        Scope.start("CallExpr")
        Scope.log(scope)

        objType, symbol = self.visit(ast.obj,scope)

        ## If obj is not an ID
        if symbol is None: raise TypeMismatchInExpression(ast)
        
        ##This is static field access
        if ast.method.name[0] == '$':
            if type(symbol.kind) is not Class:
                raise IllegalMemberAccess(ast)

            classSymbol = Checker.checkUndeclared(GlobalStack.stack, ast.obj.name, kind=Class())
        
        ## This is instance field access
        else:
            objInstance = symbol
            if type(symbol.kind) is Class:
                raise IllegalMemberAccess(ast)

            className = objInstance.mtype.classname.name
            classSymbol = Checker.checkUndeclared(GlobalStack.stack, className, kind=Class())


        if type(classSymbol.kind) is not Class: raise TypeMismatchInExpression(ast)

        methodSymbol = Checker.checkUndeclared(classSymbol.child, ast.method.name, kind=Method())
        if methodSymbol.mtype.rettype is None: raise Undeclared(Method(),ast.method.name)
        paramsRetType = [self.visit(x,scope)[0] for x in ast.param]

        # print('Call expr type: ',methodSymbol.mtype.rettype)
        if not all([Checker.matchType(a,b) for a,b in zip(methodSymbol.mtype.partype,paramsRetType)]) \
            or len(methodSymbol.mtype.partype) != len(paramsRetType):
            raise TypeMismatchInExpression(ast)
        
        Scope.end()
        return methodSymbol.mtype.rettype, None
    

    def visitNewExpr(self,ast:NewExpr,scope):
        Scope.start("NewExpr")
        Scope.log(scope)

        classSymbol = Checker.checkUndeclared(GlobalStack.stack, ast.classname.name, kind=Class())

        if type(classSymbol.mtype) is not ClassType:
            raise TypeMismatchInExpression(ast) 

        constructorSymbol = lookup('Constructor',classSymbol.child, Symbol.cmp)
        
        ## Here are the params and input expression that needs to be check
        listParamsType = constructorSymbol.mtype.partype if constructorSymbol is not None else []
        listExprsType = [self.visit(x,scope)[0] for x in ast.param]
        
        ## print('Param for constructor: ',listParamsType)
        ## print('Expression type input to constructor: ',listExprsType)
        if not all([Checker.matchType(a,b) for a,b in zip(listParamsType,listExprsType)]) \
            or len(listParamsType) != len(listExprsType):
            raise TypeMismatchInExpression(ast)

        Scope.end()
        return classSymbol.mtype, None

    def visitArrayCell(self,ast:ArrayCell,scope):
        Scope.start('ArrayCell')
        Scope.log(scope)
        retType, symbol = self.visit(ast.arr,scope)

        if type(symbol.mtype) is not ArrayType or symbol is None:
            raise TypeMismatchInExpression(ast)

        idxs_intTypes = [type(self.visit(x,scope)[0]) is not IntType for x in ast.idx]
        if any(idxs_intTypes):
            raise TypeMismatchInExpression(ast)
        
        numLoop = len(idxs_intTypes)
        while type(retType) is ArrayType and numLoop > 0 :
            retType = retType.eleType
            numLoop -=1

        if numLoop > 0:
            raise TypeMismatchInExpression(ast)

        Scope.end()
        ## print('ArrayCel return',retType)
        return retType ,None


    def visitFieldAccess(self,ast:FieldAccess,scope):
        # GlobalStack.log()
        Scope.start("FieldAccess")
        Scope.log(scope)

        selfVisitFlag = True if type(ast.obj) is SelfLiteral else False
        
        objType, symbol = self.visit(ast.obj,scope)

        ## If obj is not a symbol
        if symbol is None: raise TypeMismatchInExpression(ast)

        ##This is static field access
        if ast.fieldname.name[0] == '$':
            classSymbol = Checker.checkUndeclared(GlobalStack.stack, symbol.name, kind=Class())

        ## This is instance field access
        else:
            objInstance = symbol
            if type(symbol.mtype) is not ClassType:
                raise IllegalMemberAccess(ast)

            className = objInstance.mtype.classname.name
            classSymbol = Checker.checkUndeclared(GlobalStack.stack, className, kind=Class())
        
        ## print('kind',classSymbol.kind)
        if type(classSymbol.kind) is not Class: raise TypeMismatchInExpression(ast)

        attributeSymbol = Checker.checkUndeclared(classSymbol.child, ast.fieldname.name, kind=Attribute())
        # print('childList',[str(x) for x in childList])

        ## print('memberKind',attributeSymbol.memberKind,'kind',attributeSymbol.kind)
        if type(attributeSymbol.memberKind) is Instance \
            and type(attributeSymbol.kind) is Attribute \
            and not selfVisitFlag:
            
            raise IllegalMemberAccess(ast)

        ## print('FieldAccess return', attributeSymbol.mtype)
        Scope.end()
        return attributeSymbol.mtype, None
    
    ################ LITERAL PART ###################
    def visitArrayLiteral(self,ast, params):
        Scope.start('ArrayLiteral')
        Scope.log(params)
        lst = [self.visit(x,params)[0] for x in ast.value]
        if not Checker.isSameTypeArray(lst):
            raise IllegalArrayLiteral(ast)
        
        Scope.end()
        
        # return ArrayLiteral(lst), None
        return ArrayType(len(lst),lst[0]), None

    def visitIntLiteral(self, ast, params):
        return IntType(), None

    def visitFloatLiteral(self, ast, params):
        return FloatType(), None

    def visitBooleanLiteral(self, ast, params):
        return BoolType(), None

    def visitStringLiteral(self, ast, params):
        return StringType(), None

    def visitNullLiteral(self,ast,params):
        return NullLiteral(), None
    
    def visitSelfLiteral(self, ast, params):
        symbol = GlobalStack.stack[-1]
        return symbol.mtype, symbol

    def visitArrayType(self,ast,params):
        eleType, _ = self.visit(ast.eleType,params)
        return eleType, ast.size