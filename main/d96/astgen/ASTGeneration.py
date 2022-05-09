from D96Visitor import D96Visitor
from D96Parser import D96Parser
from AST import *
from functools import reduce

F_LOG = True

def log(*arg):
    if F_LOG: print('>>>>>', *arg)

def log1(*arg):
    if F_LOG: print('>>>>>>>>>>', *arg)

def log2(*arg):
    if F_LOG: print('>>>>>>>>>>>>>>>', *arg)

def flatten(lst):
    if not isinstance(lst, list):
        return [lst]
    if len(lst) == 0:
        return []
    if len(lst) == 1:
        return flatten(lst[0])
    head, tail = lst[0], lst[1:]
    return flatten(head) + flatten(tail)

class ASTGeneration(D96Visitor):

    def visitProgram(self, ctx: D96Parser.ProgramContext):
        res = []
        for i in ctx.classDecl():
            res.append(self.visit(i))
        return Program(res)

    def visitClassDecl(self, ctx: D96Parser.ClassDeclContext):
        memDecls = []
        ID = ctx.ID(0).getText()
        parentID = Id(ctx.ID(1).getText()) if ctx.ID(1) else None
        for i in ctx.getChildren():
            if i in ctx.funcDecl() + ctx.constructorFunc() + ctx.destructorFunc() + ctx.attributeDeclStmt():
                if i in ctx.funcDecl():
                    methodDecls = self.visit(i)
                    # print(str(methodDecls))
                    if methodDecls.name.name == 'main' and ID == 'Program' and len(methodDecls.param) == 0 :
                        methodDecls.kind = Static()
                    memDecls.append(methodDecls)
                elif i in ctx.constructorFunc():
                    memDecls += [self.visit(i)]
                elif i in ctx.destructorFunc():
                    memDecls += [self.visit(i)]
                elif i in ctx.attributeDeclStmt():
                    memDecls += [self.visit(i)]
        return ClassDecl(Id(ID), flatten(memDecls), parentID)


    def visitConstructorFunc(self, ctx:D96Parser.ConstructorFuncContext):
        return MethodDecl(
            Instance(),
            Id('Constructor'),
            self.visit(ctx.listDeclArgs()) if ctx.listDeclArgs() else [],
            self.visit(ctx.blockStmt())
        )

    def visitDestructorFunc(self, ctx:D96Parser.DestructorFuncContext):
        return MethodDecl(
            Instance(),
            Id('Destructor'),
            [],
            self.visit(ctx.blockStmt())
        )

    def visitBlockStmt(self, ctx:D96Parser.BlockStmtContext):
        stmts = []
        for i in range(len(ctx.stmt())):
            stmts.append(self.visit(ctx.stmt(i)))
        return Block(flatten(stmts))

    def visitStmt(self,ctx: D96Parser.StmtContext):
        return self.visitChildren(ctx)

    def visitAssignStmt(self, ctx:D96Parser.AssignStmtContext):
         rhs = self.visit(ctx.exp()[-1])
         return [ Assign(self.visit(ctx.exp(i)), rhs)
                  for i in range(len(ctx.exp())-1)
                ]

    def visitReturnStmt(self, ctx:D96Parser.ReturnStmtContext):
        return Return(self.visit(ctx.exp())) if ctx.exp() else Return()

    def visitContinueStmt(self, ctx:D96Parser.ContinueStmtContext):
        return Continue()

    def visitBreakStmt(self,ctx:D96Parser.BreakStmtContext):
        return Break()

    def visitIfElseStmt(self, ctx: D96Parser.IfElseStmtContext):
        return self.visit(ctx.ifBodyStmt())

    def visitElseIfBody(self, ctx:D96Parser.ElseIfBodyContext):
        return self.visit(ctx.exp()), self.visit(ctx.blockStmt())

    def visitIfBodyStmt(self, ctx: D96Parser.IfBodyStmtContext):
        expIf = self.visit(ctx.exp())
        thenStmt = self.visit(ctx.blockStmt())
        if ctx.elseIfBody():
            res = ''
            for i in reversed(ctx.elseIfBody()):
                exp, elseThenStmt = self.visit(i)
                if res == '' and ctx.elseBody():
                    res = self.visit(ctx.elseBody())
                res = If(exp,elseThenStmt,res)
            return If(expIf,thenStmt,res)
        else:
            elseStmt = self.visit(ctx.elseBody()) if ctx.elseBody() else []
            return If(expIf,thenStmt,elseStmt)

    def visitElseBody(self,ctx:D96Parser.ElseBodyContext):
            return self.visit(ctx.blockStmt())

    def visitForEachStmt(self, ctx:D96Parser.ForEachStmtContext):
        id, _= self.visit(ctx.mixedId())
        loopStmt = self.visit(ctx.blockStmt())
        exp1 = self.visit(ctx.exp(0))
        exp2 = self.visit(ctx.exp(1))
        exp3 = None if len(ctx.exp()) != 3 else self.visit(ctx.exp(2))
        return For(id, exp1, exp2,loopStmt, exp3)

    def visitAttributeDeclStmt(self, ctx:D96Parser.AttributeDeclStmtContext):
        stmts = []
        if ctx.VAR():
            if ctx.declareWithoutAssign():
                listIds, isStaticList, typeVar = self.visit(ctx.declareWithoutAssign())
                # log(listIds)
                # log(isStaticList)
                # log(str(type(typeVar)) == "<class 'AST.ClassType'>")
                initVal = NullLiteral() if str(type(typeVar)) == "<class 'AST.ClassType'>" else None
                for i in range(len(listIds)):
                    stmts.append(
                        AttributeDecl(
                            Static() if isStaticList[i] else Instance(),
                            VarDecl(listIds[i], typeVar,initVal)
                        )
                    )
            else:
                resArray = self.visit(ctx.declareWithAssign())
                mixedIds, listExps, isStaticList, typeVar = resArray[:-1:3], resArray[-3::-3], resArray[2:-1:3], resArray[-1]
                # log(mixedIds)
                # log(listExps)
                # log(isStaticList)
                # log(typeVar)
                for i in range(len(mixedIds)):
                    stmts.append(
                        AttributeDecl(
                            Static() if isStaticList[i] else Instance(),
                            VarDecl(mixedIds[i], typeVar, listExps[i])
                        )
                    )
            return stmts
        else: #ctx.VAL()
            if ctx.declareWithoutAssign():
                listIds, isStaticList, typeVar = self.visit(ctx.declareWithoutAssign())
                # log(listIds)
                # log(isStaticList)
                # log(typeVar)
                initVal = NullLiteral() if str(type(typeVar)) == "<class 'AST.ClassType'>" else None
                for i in range(len(listIds)):
                    stmts.append(
                        AttributeDecl(
                            Static() if isStaticList[i] else Instance(),
                            ConstDecl(listIds[i], typeVar,initVal),
                        )
                    )
            else:
                resArray = self.visit(ctx.declareWithAssign())
                mixedIds, listExps, isStaticList, typeVar = resArray[:-1:3], resArray[-3::-3], resArray[2:-1:3], resArray[-1]
                # log(mixedIds)
                # log(listExps)
                # log(isStaticList)
                # log(typeVar)
                for i in range(len(mixedIds)):
                    stmts.append(
                        AttributeDecl(
                            Static() if isStaticList[i] else Instance(),
                            ConstDecl(mixedIds[i], typeVar, listExps[i])
                        )
                    )
            return stmts

    def visitFuncDecl(self, ctx:D96Parser.FuncDeclContext):
        name, isStatic = self.visit(ctx.mixedId())
        kind = Static() if isStatic else Instance()
        param = self.visit(ctx.listDeclArgs()) if ctx.listDeclArgs() else []
        body = self.visit(ctx.blockStmt())
        return MethodDecl(kind,name,param,body)

    def visitValDecl(self, ctx:D96Parser.ValDeclContext):
        res = []
        if ctx.declareWithoutAssign():
            mixedIds, _, typeVar = self.visit(ctx.declareWithoutAssign())
            initVal = NullLiteral() if str(type(typeVar)) == "<class 'AST.ClassType'>" else None
            for mixedId in mixedIds:
                res.append(ConstDecl(mixedId,typeVar,initVal))

        else:
            resArray = self.visit(ctx.declareWithAssign())
            mixedIds, listExps, _, typeVar = resArray[:-1:3], resArray[-3::-3], resArray[2:-1:3],resArray[-1]
            for i in range(len(mixedIds)):
                res.append(ConstDecl(mixedIds[i],typeVar ,listExps[i]))
        return res

    def visitVarDecl(self, ctx:D96Parser.VarDeclContext):
        if ctx.declareWithoutAssign():
            mixedIds, _, typeVar = self.visit(ctx.declareWithoutAssign())
            initVal = NullLiteral() if str(type(typeVar)) == "<class 'AST.ClassType'>" else None
            return [VarDecl(id,typeVar,initVal) for id in mixedIds]
        else:
            resArray = self.visit(ctx.declareWithAssign())
            mixedIds, listExps, _, typeVar = resArray[:-1:3], resArray[-3::-3], resArray[2:-1:3],resArray[-1]
            # log(resArray)
            # log(mixedIds)
            # log(listExps)
            # log(isStaticList)
            return [VarDecl(mixedIds[i],typeVar,listExps[i]) for i in range(len(mixedIds))]

    def visitDeclareWithoutAssign(self,ctx:D96Parser.DeclareWithoutAssignContext):
        listMixedIds, isStaticList = self.visit(ctx.listMixedIds())
        varType = self.visit(ctx.varType())
        return listMixedIds ,isStaticList ,varType

    def visitDeclareWithAssign(self, ctx: D96Parser.DeclareWithAssignContext):
        idVar, isStatic = self.visit(ctx.mixedId())
        exp = self.visit(ctx.exp())
        if ctx.EQUAL():
            varTypeRecursive = self.visit(ctx.varType())
            return [idVar, exp, isStatic, varTypeRecursive]
        return [idVar, exp, isStatic] + self.visit(ctx.declareWithAssign())

    def visitExp(self,ctx: D96Parser.ExpContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.exp1(0))
        return BinaryOp(
            ctx.getChild(1).getText(),
            self.visit(ctx.exp1(0)),
            self.visit(ctx.exp1(1))
        )
    def visitExp1(self,ctx: D96Parser.Exp1Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.exp2())
        return BinaryOp(
            ctx.getChild(1).getText(),
            self.visit(ctx.exp1()),
            self.visit(ctx.exp2())
        )

    def visitExp2(self,ctx: D96Parser.Exp2Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.exp3())
        return BinaryOp(
            ctx.getChild(1).getText(),
            self.visit(ctx.exp2()),
            self.visit(ctx.exp3())
        )

    def visitExp3(self,ctx: D96Parser.Exp3Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.exp4())
        return BinaryOp(
            ctx.getChild(1).getText(),
            self.visit(ctx.exp3()),
            self.visit(ctx.exp4())
        )

    def visitExp4(self,ctx: D96Parser.Exp4Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.exp5())
        return BinaryOp(
            ctx.getChild(1).getText(),
            self.visit(ctx.exp4()),
            self.visit(ctx.exp5())
        )

    def visitExp5(self,ctx: D96Parser.Exp5Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.exp6())
        return UnaryOp(ctx.getChild(0).getText(), self.visit(ctx.exp5()))

    def visitExp6(self,ctx: D96Parser.Exp6Context):
        if ctx.operands():
            return self.visit(ctx.operands())
        exp6 = self.visit(ctx.exp6())
        listExps = self.visit(ctx.postfixArrayExp())
        return ArrayCell(exp6, listExps)

    def visitOperands(self, ctx: D96Parser.OperandsContext):
        if ctx.operands1():
            return self.visit(ctx.operands1())
        # For Instance class
        operands = self.visit(ctx.operands())
        idAttr = Id(ctx.ID().getText())
        if ctx.LB() and ctx.RB(): #If methodInvocation
            listExps = self.visit(ctx.listExps()) if ctx.listExps() else []
            return CallExpr(operands,idAttr,listExps)
        else: #If FieldAccess
            return FieldAccess(operands,idAttr)

    def visitOperands1(self, ctx: D96Parser.Operands1Context):
        if ctx.operands2():
            return self.visit(ctx.operands2())
        # For Static class
        operands = self.visit(ctx.operands1())
        idAttr = Id(ctx.DOLLAR_ID().getText())
        if ctx.LB() and ctx.RB():  # If methodInvocation
            listExps = self.visit(ctx.listExps()) if ctx.listExps() else []
            return CallExpr(operands, idAttr, listExps)
        else:  # If FieldAccess
            return FieldAccess(operands, idAttr)

    def visitOperands2(self,ctx:D96Parser.Operands2Context):
        if ctx.operands3():
            return self.visit(ctx.operands3())
        expId = Id(ctx.ID().getText())
        listExps = self.visit(ctx.listExps()) if ctx.listExps() else []
        return NewExpr(expId,listExps)

    def visitOperands3(self, ctx: D96Parser.Operands4Context):
        if ctx.operands4():
            return self.visit(ctx.operands4())
        return ArrayCell(self.visit(ctx.getChild(0)),self.visit(ctx.getChild(1)))


    def visitOperands4(self, ctx: D96Parser.Operands4Context):
        if ctx.mixedId():
            name, _ = self.visit(ctx.mixedId())
            return name
        return self.visit(ctx.getChild(0))

    def visitOperands5(self, ctx: D96Parser.Operands5Context):
        if ctx.getChildCount() == 3:
            return self.visit(ctx.getChild(1))
        return self.visit(ctx.getChild(0))

    def visitOperands6(self, ctx: D96Parser.Operands6Context):
        return self.visit(ctx.getChild(0))

    def visitPostfixArrayExp(self, ctx:D96Parser.PostfixArrayExpContext):
        return [self.visit(i) for i in ctx.exp()]

    def visitMethodInvocationStmt(self, ctx:D96Parser.MethodInvocationStmtContext):
        listExps = self.visit(ctx.listExps()) if ctx.listExps() else []
        if ctx.DOT():  # Instance class
            obj = self.visit(ctx.operands())
            res = CallStmt(obj, Id(ctx.ID().getText()), listExps)
            return res
        elif ctx.ATTR_ACCESS_OP():
            obj = self.visit(ctx.operands())
            className = Id(str(ctx.DOLLAR_ID().getText()))
            res = CallStmt(obj, className, listExps)
            return res

    def visitListDeclArgs(self,ctx:D96Parser.ListDeclArgsContext):
        res = []
        for i in range(len(ctx.varType())):
            varType = self.visit(ctx.varType(i))
            listIds = self.visit(ctx.listIds(i))
            for idDecl in listIds:
                res.append(VarDecl(idDecl,varType))
        return res

    def visitListExps(self, ctx: D96Parser.ListExpsContext):
        return flatten([self.visit(i) for i in ctx.exp()])

    def visitListIds(self, ctx: D96Parser.ListIdsContext):
        return [Id(i.getText()) for i in ctx.ID()]

    def visitMixedId(self, ctx:D96Parser.MixedIdContext):
        if ctx.ID():
            name = Id(ctx.ID().getText())
            isStatic = 0
        else:
            isStatic = 1
            ##Seem reasonalable????
            name = Id(str(ctx.DOLLAR_ID().getText()))
        return name, isStatic

    def visitListMixedIds(self, ctx:D96Parser.ListMixedIdsContext):
        listIds = []
        isInstanceList = []
        for i in ctx.mixedId():
            name ,isStatic = self.visit(i)
            listIds.append(name)
            isInstanceList.append(isStatic)
        return listIds, isInstanceList

    ############VARTYPE AND LITERAL##################
    def visitVarType(self, ctx: D96Parser.VarTypeContext):
        # log(ctx.getChild(0))
        if ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.BOOLEAN():
            return BoolType()
        elif ctx.STRING():
            return StringType()
        elif ctx.arrayType():
            return self.visit(ctx.arrayType())
        elif ctx.ID():
            return ClassType(Id(ctx.ID().getText()))
        else:
            return VoidType()

    def visitArrayType(self, ctx:D96Parser.ArrayTypeContext):
        arrayType = self.visit(ctx.varType())
        size = self.visit(ctx.intLit()).value
        return ArrayType(size,arrayType)

    def visitLiteral(self, ctx:D96Parser.LiteralContext):
        if ctx.intLit():
            return self.visit(ctx.intLit())
        if ctx.FLOATLIT():
            valueStr = ctx.FLOATLIT().getText()
            if valueStr[0] == '.':
                valueStr = '0' + valueStr
            return FloatLiteral(float(valueStr))
        if ctx.STRINGLIT():
            return StringLiteral(ctx.STRINGLIT().getText())
        if ctx.booleanLit():
            return self.visit(ctx.booleanLit())
        if ctx.indexedArray():
            return self.visit(ctx.indexedArray())
        if ctx.multiDimensionArray():
            return self.visit(ctx.multiDimensionArray())
        if ctx.SELF():
            return SelfLiteral()
        if ctx.NULL():
            return NullLiteral()

    def visitIntLit(self, ctx:D96Parser.IntLitContext):
        if ctx.INT_DEC():
            value = int(ctx.INT_DEC().getText())
        elif ctx.INT_OCT():
            value = int(ctx.INT_OCT().getText(), base=8)
        elif ctx.INT_HEX():
            value = int(ctx.INT_HEX().getText(), base=16)
        else:
            value = int(ctx.INT_BIN().getText(), base=2)
        return IntLiteral(value)

    def visitBooleanLit(self, ctx:D96Parser.BooleanLitContext):
        return BooleanLiteral(bool(1) if ctx.TRUE() else bool(0))

    def visitIndexedArray(self, ctx:D96Parser.IndexedArrayContext):
        listExps = self.visit(ctx.listExps())
        # log1(ArrayLiteral(listExps))
        return ArrayLiteral(listExps)

    def visitMultiDimensionArray(self, ctx:D96Parser.MultiDimensionArrayContext):
        listExps = []
        for i in ctx.indexedArray():
            listExps.append(self.visit(i))
        # log1(ArrayLiteral(listExps))
        return ArrayLiteral(listExps)