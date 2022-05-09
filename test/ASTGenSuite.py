import unittest
from TestUtils import TestAST
from AST import *



class ASTGenSuite(unittest.TestCase):


    def test_0(self):
        input = """
        Class Program {}
        """
        expect = "Program([ClassDecl(Id(Program),[])])"
        self.assertTrue(TestAST.test(input, expect, 0))

    def test_1(self):
        input = "Class abcClass:kE29Doew {}"
        expect = "Program([ClassDecl(Id(abcClass),Id(kE29Doew),[])])"
        self.assertTrue(TestAST.test(input, expect, 1))

    def test_2(self):
        input = "Class abcClass {} Class OfgKa3 {} Class _123 {}"
        expect = "Program([ClassDecl(Id(abcClass),[]),ClassDecl(Id(OfgKa3),[]),ClassDecl(Id(_123),[])])"
        self.assertTrue(TestAST.test(input, expect, 2))

    def test_3(self):
        input = """
        Class abcClass {
            Var attrB:Int;
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),[AttributeDecl(Instance,VarDecl(Id(attrB),IntType))])])'
        self.assertTrue(TestAST.test(input, expect, 3))

    def test_4(self):
        """Simple program: int main() {} """
        input = """
        Class abcClass {
            Var attrB:Int;
            Var haveAbs:Boolean;
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),[AttributeDecl(Instance,VarDecl(Id(attrB),IntType)),AttributeDecl(Instance,VarDecl(Id(haveAbs),BoolType))])])'
        self.assertTrue(TestAST.test(input, expect, 4))

    def test_5(self):
        input = """
        Class Stock {
            Var abcClassStock:Array[Int,5];
        }
        """
        expect = 'Program([ClassDecl(Id(Stock),[AttributeDecl(Instance,VarDecl(Id(abcClassStock),ArrayType(5,IntType)))])])'
        self.assertTrue(TestAST.test(input, expect, 5))

    def test_6(self):
        input = """
        Class abcClass {
            Var numOfWheels:Int=2;
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),[AttributeDecl(Instance,VarDecl(Id(numOfWheels),IntType,IntLit(2)))])])'
        self.assertTrue(TestAST.test(input, expect, 6))

    def test_7(self):
        input = """
        Class someClass {
            Var numOfWheels:Int=2+2;
        }
        """
        expect = 'Program([ClassDecl(Id(someClass),[AttributeDecl(Instance,VarDecl(Id(numOfWheels),IntType,BinaryOp(+,IntLit(2),IntLit(2))))])])'
        self.assertTrue(TestAST.test(input, expect, 7))

    def test_8(self):
        input = """
        Class A {
            Var a:Int=1+1*2;
        }
        """
        expect = 'Program([ClassDecl(Id(A),[AttributeDecl(Instance,VarDecl(Id(a),IntType,BinaryOp(+,IntLit(1),BinaryOp(*,IntLit(1),IntLit(2)))))])])'
        self.assertTrue(TestAST.test(input, expect, 8))

    def test_9(self):
        input = """
        Class abcClass {
            Var Name:Int= 1 + .2e1 +3;
        }
        """
        expect = '''Program([ClassDecl(Id(abcClass),[AttributeDecl(Instance,VarDecl(Id(Name),IntType,BinaryOp(+,BinaryOp(+,IntLit(1),FloatLit(2.0)),IntLit(3))))])])'''
        self.assertTrue(TestAST.test(input, expect, 9))

    def test_10(self):
        input = """
        Class someClass {
            Var attrB:Int = !abcClassSpeed + (3* -4);
        }
        """
        expect = '''Program([ClassDecl(Id(someClass),[AttributeDecl(Instance,VarDecl(Id(attrB),IntType,BinaryOp(+,UnaryOp(!,Id(abcClassSpeed)),BinaryOp(*,IntLit(3),UnaryOp(-,IntLit(4))))))])])'''
        self.assertTrue(TestAST.test(input, expect, 10))

    def test_11(self):
        input = """
        Class abcClass {
            Val over150cc : Boolean=False;
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),[AttributeDecl(Instance,ConstDecl(Id(over150cc),BoolType,BooleanLit(False)))])])'
        self.assertTrue(TestAST.test(input, expect, 11))

    def test_12(self):
        input = """
        Class someClass {
            Val brand:String=specs[1][1];
        }
        """
        expect = 'Program([ClassDecl(Id(someClass),[AttributeDecl(Instance,ConstDecl(Id(brand),StringType,ArrayCell(Id(specs),[IntLit(1),IntLit(1)])))])])'
        self.assertTrue(TestAST.test(input, expect, 12))

    def test_13(self):
        """Simple program: int main() {} """
        input = """
        Class abcClass {
            Var newWheel:Int = New Wheel();
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),[AttributeDecl(Instance,VarDecl(Id(newWheel),IntType,NewExpr(Id(Wheel),[])))])])'
        self.assertTrue(TestAST.test(input, expect, 13))

    def test_14(self):
        """Simple program: int main() {} """
        input = """
        Class someClass {
            Val name:ss;
        }
        """
        expect = '''Program([ClassDecl(Id(someClass),[AttributeDecl(Instance,ConstDecl(Id(name),ClassType(Id(ss)),NullLiteral()))])])'''
        self.assertTrue(TestAST.test(input, expect, 14))

    def test_15(self):
        """Simple program: int main() {} """
        input = """
        Class _123 {
            Val section_1:Int = New Section("Section" + "1",Null);
        }
        """
        expect = 'Program([ClassDecl(Id(_123),[AttributeDecl(Instance,ConstDecl(Id(section_1),IntType,NewExpr(Id(Section),[BinaryOp(+,StringLit(Section),StringLit(1)),NullLiteral()])))])])'
        self.assertTrue(TestAST.test(input, expect, 15))

    def test_16(self):
        """Simple program: int main() {} """
        input = """
        Class abcClass {
            Var $attrB:Float=100;
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),[AttributeDecl(Static,VarDecl(Id($attrB),FloatType,IntLit(100)))])])'
        self.assertTrue(TestAST.test(input, expect, 16))

    def test_17(self):
        input = """
        Class abcClass {
            run(){}
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),[MethodDecl(Id(run),Instance,[],Block([]))])])'
        self.assertTrue(TestAST.test(input, expect, 17))

    def test_18(self):
        input = """
        Class abcClass {
            run(min_speed,max_speed:Int;avg_speed:Float){}
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),[MethodDecl(Id(run),Instance,[param(Id(min_speed),IntType),param(Id(max_speed),IntType),param(Id(avg_speed),FloatType)],Block([]))])])'
        self.assertTrue(TestAST.test(input, expect, 18))

    def test_19(self):
        input = """
        Class abcClass {
            run(speed:Int;fast:Boolean;des:String){}
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),[MethodDecl(Id(run),Instance,[param(Id(speed),IntType),param(Id(fast),BoolType),param(Id(des),StringType)],Block([]))])])'
        self.assertTrue(TestAST.test(input, expect, 19))

    def test_20(self):
        input = """
        Class abcClass {
            run(){
                Var speed:Int;
            }
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),[MethodDecl(Id(run),Instance,[],Block([VarDecl(Id(speed),IntType)]))])])'
        self.assertTrue(TestAST.test(input, expect, 20))

    def test_21(self):
        input = """
        Class abcClass {
            fillGas(){
                Var Amount:Float = 10;
            }
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),[MethodDecl(Id(fillGas),Instance,[],Block([VarDecl(Id(Amount),FloatType,IntLit(10))]))])])'
        self.assertTrue(TestAST.test(input, expect, 21))

    def test_22(self):
        input = """
        Class abcClass {
            run(){
                Var attrB:Int = 100;
                Var attrA:Float = 30;
                Val customized:Boolean = False;
            }
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),[MethodDecl(Id(run),Instance,[],Block([VarDecl(Id(attrB),IntType,IntLit(100)),VarDecl(Id(attrA),FloatType,IntLit(30)),ConstDecl(Id(customized),BoolType,BooleanLit(False))]))])])'
        self.assertTrue(TestAST.test(input, expect, 22))

    def test_23(self):
        input = """
        Class abcClass {
            Var $count:Int = 1;
            stop(){
                Var status:Int = 0;
            }
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),[AttributeDecl(Static,VarDecl(Id($count),IntType,IntLit(1))),MethodDecl(Id(stop),Instance,[],Block([VarDecl(Id(status),IntType,IntLit(0))]))])])'
        self.assertTrue(TestAST.test(input, expect, 23))

    def test_24(self):
        input = """
        Class abcClass {
            someClassry(a,b,c,d,e:Int){
                Var people:Int = 3+3/2;
            }
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),[MethodDecl(Id(someClassry),Instance,[param(Id(a),IntType),param(Id(b),IntType),param(Id(c),IntType),param(Id(d),IntType),param(Id(e),IntType)],Block([VarDecl(Id(people),IntType,BinaryOp(+,IntLit(3),BinaryOp(/,IntLit(3),IntLit(2))))]))])])'
        self.assertTrue(TestAST.test(input, expect, 24))

    def test_25(self):
        input = """
        Class someClass {
            $updateCount(){
                Var count:Int = count;
                count=1;
            }
        }
        """
        expect = 'Program([ClassDecl(Id(someClass),[MethodDecl(Id($updateCount),Static,[],Block([VarDecl(Id(count),IntType,Id(count)),AssignStmt(Id(count),IntLit(1))]))])])'
        self.assertTrue(TestAST.test(input, expect, 25))

    def test_26(self):
        input = """
        Class abcClass {
            $updateStock(){
                stock[1][3]= stock[1][3] + 1;
            }
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),[MethodDecl(Id($updateStock),Static,[],Block([AssignStmt(ArrayCell(Id(stock),[IntLit(1),IntLit(3)]),BinaryOp(+,ArrayCell(Id(stock),[IntLit(1),IntLit(3)]),IntLit(1)))]))])])'
        self.assertTrue(TestAST.test(input, expect, 26))

    def test_27(self):
        input = """
        Class abcClass {
            spank(){
                vicepresident_adshfj[1][-1+5+cal.dot]="hoho";
            }
        }
        """
        expect ='''Program([ClassDecl(Id(abcClass),[MethodDecl(Id(spank),Instance,[],Block([AssignStmt(ArrayCell(Id(vicepresident_adshfj),[IntLit(1),BinaryOp(+,BinaryOp(+,UnaryOp(-,IntLit(1)),IntLit(5)),FieldAccess(Id(cal),Id(dot)))]),StringLit(hoho))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 27))

    def test_28(self):
        input = """
        Class abcClass {
            changeName(){
                Self.name1.name2="ei29So";
            }
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),[MethodDecl(Id(changeName),Instance,[],Block([AssignStmt(FieldAccess(FieldAccess(Self(),Id(name1)),Id(name2)),StringLit(ei29So))]))])])'
        self.assertTrue(TestAST.test(input, expect, 28))

    def test_29(self):
        input = """
        Class abcClass {
            changeName(){
                Self.name1.name2[1]=Self.name3.getName(1,"first");
            }
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),[MethodDecl(Id(changeName),Instance,[],Block([AssignStmt(ArrayCell(FieldAccess(FieldAccess(Self(),Id(name1)),Id(name2)),[IntLit(1)]),CallExpr(FieldAccess(Self(),Id(name3)),Id(getName),[IntLit(1),StringLit(first)]))]))])])'
        self.assertTrue(TestAST.test(input, expect, 29))

    def test_30(self):
        input = """
        Class abcClass {
            foo(){
                Var speed:Speed = Self.s.getSpeed(10,20+30) + 20;
            }
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),[MethodDecl(Id(foo),Instance,[],Block([VarDecl(Id(speed),ClassType(Id(Speed)),BinaryOp(+,CallExpr(FieldAccess(Self(),Id(s)),Id(getSpeed),[IntLit(10),BinaryOp(+,IntLit(20),IntLit(30))]),IntLit(20)))]))])])'
        self.assertTrue(TestAST.test(input, expect, 30))

    def test_31(self):
        input = """
        Class someClass {
            foo(){
                Var someClassStock:Array[Array[Int,5],5];
            }
        }
        """
        expect = 'Program([ClassDecl(Id(someClass),[MethodDecl(Id(foo),Instance,[],Block([VarDecl(Id(someClassStock),ArrayType(5,ArrayType(5,IntType)))]))])])'
        self.assertTrue(TestAST.test(input, expect, 31))

    def test_32(self):
        input = """
        Class someClass {
            foo(){
                {}
            }
        }
        """
        expect = '''Program([ClassDecl(Id(someClass),[MethodDecl(Id(foo),Instance,[],Block([Block([])]))])])'''
        self.assertTrue(TestAST.test(input, expect, 32))

    def test_33(self):
        input = """
        Class someClass:kE29Doew{
            createsomeClass(){
                someClass = New someClass("huyndai").model.init();
            }
        }
        """
        expect = 'Program([ClassDecl(Id(someClass),Id(kE29Doew),[MethodDecl(Id(createsomeClass),Instance,[],Block([AssignStmt(Id(someClass),CallExpr(FieldAccess(NewExpr(Id(someClass),[StringLit(huyndai)]),Id(model)),Id(init),[]))]))])])'
        self.assertTrue(TestAST.test(input, expect, 33))

    def test_34(self):
        input = """
        Class abcClass:kE29Doew{
            createabcClass(){
                abcClass = New abcClass("reype").b;
            }
        }
        """
        expect = '''Program([ClassDecl(Id(abcClass),Id(kE29Doew),[MethodDecl(Id(createabcClass),Instance,[],Block([AssignStmt(Id(abcClass),FieldAccess(NewExpr(Id(abcClass),[StringLit(reype)]),Id(b)))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 34))

    def test_35(self):
        input = """
        Class abcClass:kE29Doew{
            foo(){
                speed = (10+20)*3;
            }
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),Id(kE29Doew),[MethodDecl(Id(foo),Instance,[],Block([AssignStmt(Id(speed),BinaryOp(*,BinaryOp(+,IntLit(10),IntLit(20)),IntLit(3)))]))])])'
        self.assertTrue(TestAST.test(input, expect, 35))

    def test_36(self):
        input = """
        Class someClass:kE29Doew{
            recur(){
                Return Self.recur();
            }
            Constructor (speed,brand:Name){}
            Destructor (){}
        }
        """
        expect = 'Program([ClassDecl(Id(someClass),Id(kE29Doew),[MethodDecl(Id(recur),Instance,[],Block([Return(CallExpr(Self(),Id(recur),[]))])),MethodDecl(Id(Constructor),Instance,[param(Id(speed),ClassType(Id(Name))),param(Id(brand),ClassType(Id(Name)))],Block([])),MethodDecl(Id(Destructor),Instance,[],Block([]))])])'
        self.assertTrue(TestAST.test(input, expect, 36))

    def test_37(self):
        input = """
        Class abcClass:kE29Doew{
            Var speed,$good:Int;
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),Id(kE29Doew),[AttributeDecl(Instance,VarDecl(Id(speed),IntType)),AttributeDecl(Static,VarDecl(Id($good),IntType))])])'
        self.assertTrue(TestAST.test(input, expect, 37))

    def test_38(self):
        input = """
        Class abcClass:kE29Doew{
            Var maxPing,$attrB:Int = 0,100;
            Val $count,boo:Boolean = True, Null;
        }
        """
        expect = '''Program([ClassDecl(Id(abcClass),Id(kE29Doew),[AttributeDecl(Instance,VarDecl(Id(maxPing),IntType,IntLit(0))),AttributeDecl(Static,VarDecl(Id($attrB),IntType,IntLit(100))),AttributeDecl(Static,ConstDecl(Id($count),BoolType,BooleanLit(True))),AttributeDecl(Instance,ConstDecl(Id(boo),BoolType,NullLiteral()))])])'''
        self.assertTrue(TestAST.test(input, expect, 38))

    def test_39(self):
        input = """
        Class abcClass:kE29Doew{
            Var speed1, speed2, speed3:Int;
            Foo(){
                Var speed1, speed2, speed3:Int;
            }
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),Id(kE29Doew),[AttributeDecl(Instance,VarDecl(Id(speed1),IntType)),AttributeDecl(Instance,VarDecl(Id(speed2),IntType)),AttributeDecl(Instance,VarDecl(Id(speed3),IntType)),MethodDecl(Id(Foo),Instance,[],Block([VarDecl(Id(speed1),IntType),VarDecl(Id(speed2),IntType),VarDecl(Id(speed3),IntType)]))])])'
        self.assertTrue(TestAST.test(input, expect, 39))

    def test_40(self):
        input = """
        Class someClass:kE29Doew{
            Foo(){
                Val speed1, speed1, speed1:Int = 10,20,30;
                Var d:Boolean = True;
            }
        }
        """
        expect = 'Program([ClassDecl(Id(someClass),Id(kE29Doew),[MethodDecl(Id(Foo),Instance,[],Block([ConstDecl(Id(speed1),IntType,IntLit(10)),ConstDecl(Id(speed1),IntType,IntLit(20)),ConstDecl(Id(speed1),IntType,IntLit(30)),VarDecl(Id(d),BoolType,BooleanLit(True))]))])])'
        self.assertTrue(TestAST.test(input, expect, 40))

    def test_41(self):
        input = """
        Class abcClass:kE29Doew{
            Var $stock:Array[Int,3] = Array(1,1,1);
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),Id(kE29Doew),[AttributeDecl(Static,VarDecl(Id($stock),ArrayType(3,IntType),[IntLit(1),IntLit(1),IntLit(1)]))])])'
        self.assertTrue(TestAST.test(input, expect, 41))

    def test_42(self):
        input = """
        Class abcClass:kE29Doew{
            Var $someClass:Array[Array[Int,1],3] = Array(Array(1),Array(1),Array(1));
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),Id(kE29Doew),[AttributeDecl(Static,VarDecl(Id($someClass),ArrayType(3,ArrayType(1,IntType)),[[IntLit(1)],[IntLit(1)],[IntLit(1)]]))])])'
        self.assertTrue(TestAST.test(input, expect, 42))

    def test_43(self):
        input = """
        Class abcClass:kE29Doew{
            Var $3:Int;
            $foo(i:Array [Boolean ,0105]){
                d=0105;
                e.z(Self,Null,Array(1)).d=0b01010;
                g[k][w[x]]=0123;
            }
        }
        """
        expect = '''Program([ClassDecl(Id(abcClass),Id(kE29Doew),[AttributeDecl(Static,VarDecl(Id($3),IntType)),MethodDecl(Id($foo),Static,[param(Id(i),ArrayType(69,BoolType))],Block([AssignStmt(Id(d),IntLit(69)),AssignStmt(FieldAccess(CallExpr(Id(e),Id(z),[Self(),NullLiteral(),[IntLit(1)]]),Id(d)),IntLit(10)),AssignStmt(ArrayCell(Id(g),[Id(k),ArrayCell(Id(w),[Id(x)])]),IntLit(83))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 43))

    def test_44(self):
        input = """
        Class abcClass:kE29Doew{
            Var $0,s,$s1,sb,$2s,cs:Int = 50,40,30,20,10,0;
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),Id(kE29Doew),[AttributeDecl(Static,VarDecl(Id($0),IntType,IntLit(50))),AttributeDecl(Instance,VarDecl(Id(s),IntType,IntLit(40))),AttributeDecl(Static,VarDecl(Id($s1),IntType,IntLit(30))),AttributeDecl(Instance,VarDecl(Id(sb),IntType,IntLit(20))),AttributeDecl(Static,VarDecl(Id($2s),IntType,IntLit(10))),AttributeDecl(Instance,VarDecl(Id(cs),IntType,IntLit(0)))])])'
        self.assertTrue(TestAST.test(input, expect, 44))

    def test_45(self):
        input = """
        Class abcClass:kE29Doew{
            Run(){
                If(3){}
                Else{
                    obj.Donesk();
                }
            }
        }
        """
        expect = '''Program([ClassDecl(Id(abcClass),Id(kE29Doew),[MethodDecl(Id(Run),Instance,[],Block([If(IntLit(3),Block([]),Block([Call(Id(obj),Id(Donesk),[])]))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 45))

    def test_46(self):
        input = """
        Class abcClass:kE29Doew{
            Run(){
                If(10){}
                If(20){}Else{}
                If(30){}Elseif(40){}Else{stop=1;}
            }
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),Id(kE29Doew),[MethodDecl(Id(Run),Instance,[],Block([If(IntLit(10),Block([])),If(IntLit(20),Block([]),Block([])),If(IntLit(30),Block([]),If(IntLit(40),Block([]),Block([AssignStmt(Id(stop),IntLit(1))])))]))])])'
        self.assertTrue(TestAST.test(input, expect, 46))

    def test_47(self):
        input = """
        Class abcClass:kE29Doew{
            Run(){
                If(3){}Elseif(4){}Elseif(5){}Else{a=1;}
            }
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),Id(kE29Doew),[MethodDecl(Id(Run),Instance,[],Block([If(IntLit(3),Block([]),If(IntLit(4),Block([]),If(IntLit(5),Block([]),Block([AssignStmt(Id(a),IntLit(1))]))))]))])])'
        self.assertTrue(TestAST.test(input, expect, 47))

    def test_48(self):
        input = """
        Class abcClass:kE29Doew{
            Foo(){
                abcClass.foo(1+20,30*4-50.50);
                If(10)
                    {}
                Elseif(20)
                    {}
                Elseif(30)
                    {}
            }
        }
        """
        expect = 'Program([ClassDecl(Id(abcClass),Id(kE29Doew),[MethodDecl(Id(Foo),Instance,[],Block([Call(Id(abcClass),Id(foo),[BinaryOp(+,IntLit(1),IntLit(20)),BinaryOp(-,BinaryOp(*,IntLit(30),IntLit(4)),FloatLit(50.5))]),If(IntLit(10),Block([]),If(IntLit(20),Block([]),If(IntLit(30),Block([]))))]))])])'
        self.assertTrue(TestAST.test(input, expect, 48))

    def test_49(self):
        input = """
        Class abcClass:kE29Doew
        {
            Foo()
            {
                If(30){}
                Elseif(40)
                    {{}}
                Elseif(50)
                    {Return Self;}
            }
        }
        """
        expect = '''Program([ClassDecl(Id(abcClass),Id(kE29Doew),[MethodDecl(Id(Foo),Instance,[],Block([If(IntLit(30),Block([]),If(IntLit(40),Block([Block([])]),If(IntLit(50),Block([Return(Self())]))))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 49))

    def test_50(self):
        line = '''
        Class abcClass {
            $countabcClass() {
                If ((1+1) ){
                    Var x,y:Boolean = False, True;
                }
            }
        }
        '''
        expect = '''Program([ClassDecl(Id(abcClass),[MethodDecl(Id($countabcClass),Static,[],Block([If(BinaryOp(+,IntLit(1),IntLit(1)),Block([VarDecl(Id(x),BoolType,BooleanLit(False)),VarDecl(Id(y),BoolType,BooleanLit(True))]))]))])])'''
        self.assertTrue(TestAST.test(line, expect, 50))

    def test_51(self):
        line = '''
        Class DataOfSquare {
            Val c: Array[Int,5] = New ArrayList();
            Val color: Int;
            Val square: SquarePanel;
            DataOfSquare(col: Int){
                C.add(Color.darkGray);
                C.add(Color.BLUE);
                C.add(Color.white);
                color=col;
                square = New SquarePanel(C.get(color));
            }
            lightMeUp(c:Int){
                square.ChangeColor(C.get(c));
            }
        }
        '''
        expect='''Program([ClassDecl(Id(DataOfSquare),[AttributeDecl(Instance,ConstDecl(Id(c),ArrayType(5,IntType),NewExpr(Id(ArrayList),[]))),AttributeDecl(Instance,ConstDecl(Id(color),IntType,None)),AttributeDecl(Instance,ConstDecl(Id(square),ClassType(Id(SquarePanel)),NullLiteral())),MethodDecl(Id(DataOfSquare),Instance,[param(Id(col),IntType)],Block([Call(Id(C),Id(add),[FieldAccess(Id(Color),Id(darkGray))]),Call(Id(C),Id(add),[FieldAccess(Id(Color),Id(BLUE))]),Call(Id(C),Id(add),[FieldAccess(Id(Color),Id(white))]),AssignStmt(Id(color),Id(col)),AssignStmt(Id(square),NewExpr(Id(SquarePanel),[CallExpr(Id(C),Id(get),[Id(color)])]))])),MethodDecl(Id(lightMeUp),Instance,[param(Id(c),IntType)],Block([Call(Id(square),Id(ChangeColor),[CallExpr(Id(C),Id(get),[Id(c)])])]))])])'''
        self.assertTrue(TestAST.test(line, expect, 51))

    def test_52(self):
        line = '''
        Class Game: JFrame
            {
              Val Height:Int = 30;
              Val Width:Int = 30;
              Val Scale:Float = 10;
              main(args: GFrame) {
                Val $gameBoard:SnakeBoard = New SnakeDataModel();
                Val view: View = New View(gameBoard);
                object.add(view);
                Val $controller:Controller = New Controller(gameBoard);
                object.addKeyListener(controller);
                object.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                a.setVisible(true);
                this.setSize(Width * Scale + Scale / 2, Height * Scale + Scale / 2);
                a = controller.start;
              }
            }
        '''
        expect = '''Program([ClassDecl(Id(Game),Id(JFrame),[AttributeDecl(Instance,ConstDecl(Id(Height),IntType,IntLit(30))),AttributeDecl(Instance,ConstDecl(Id(Width),IntType,IntLit(30))),AttributeDecl(Instance,ConstDecl(Id(Scale),FloatType,IntLit(10))),MethodDecl(Id(main),Instance,[param(Id(args),ClassType(Id(GFrame)))],Block([ConstDecl(Id($gameBoard),ClassType(Id(SnakeBoard)),NewExpr(Id(SnakeDataModel),[])),ConstDecl(Id(view),ClassType(Id(View)),NewExpr(Id(View),[Id(gameBoard)])),Call(Id(object),Id(add),[Id(view)]),ConstDecl(Id($controller),ClassType(Id(Controller)),NewExpr(Id(Controller),[Id(gameBoard)])),Call(Id(object),Id(addKeyListener),[Id(controller)]),Call(Id(object),Id(setDefaultCloseOperation),[FieldAccess(Id(JFrame),Id(EXIT_ON_CLOSE))]),Call(Id(a),Id(setVisible),[Id(true)]),Call(Id(this),Id(setSize),[BinaryOp(+,BinaryOp(*,Id(Width),Id(Scale)),BinaryOp(/,Id(Scale),IntLit(2))),BinaryOp(+,BinaryOp(*,Id(Height),Id(Scale)),BinaryOp(/,Id(Scale),IntLit(2)))]),AssignStmt(Id(a),FieldAccess(Id(controller),Id(start)))]))])])'''
        self.assertTrue(TestAST.test(line, expect, 52))

    def test_53(self):
        line = '''
        Class SquarePanel:JPanel{
            Val $serialVersionUID:Int = 1;
            SquarePanel(d:Color){
                Self::$d.det(d);
            }
            ChangeColor(d:Color){
                this.setBackground(d);
                this.repaint();
            }
        }
        '''
        expect = '''Program([ClassDecl(Id(SquarePanel),Id(JPanel),[AttributeDecl(Static,ConstDecl(Id($serialVersionUID),IntType,IntLit(1))),MethodDecl(Id(SquarePanel),Instance,[param(Id(d),ClassType(Id(Color)))],Block([Call(FieldAccess(Self(),Id($d)),Id(det),[Id(d)])])),MethodDecl(Id(ChangeColor),Instance,[param(Id(d),ClassType(Id(Color)))],Block([Call(Id(this),Id(setBackground),[Id(d)]),Call(Id(this),Id(repaint),[])]))])])'''
        self.assertTrue(TestAST.test(line, expect, 53))

    def test_54(self):
        line = '''
        Class Rectangle{
        foo(){
        }
        }
        '''
        expect = '''Program([ClassDecl(Id(Rectangle),[MethodDecl(Id(foo),Instance,[],Block([]))])])'''
        self.assertTrue(TestAST.test(line, expect, 54))

    def test_55(self):
        line = '''
        Class initUI{
            add(board: Board){
                this.board = board;
                this.setResizable(width,height);
                this.pack();
                this.setTitle("Snake");
                this.setLocationRelativeTo(null);
                this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            }
        }
        '''
        expect = '''Program([ClassDecl(Id(initUI),[MethodDecl(Id(add),Instance,[param(Id(board),ClassType(Id(Board)))],Block([AssignStmt(FieldAccess(Id(this),Id(board)),Id(board)),Call(Id(this),Id(setResizable),[Id(width),Id(height)]),Call(Id(this),Id(pack),[]),Call(Id(this),Id(setTitle),[StringLit(Snake)]),Call(Id(this),Id(setLocationRelativeTo),[Id(null)]),Call(Id(this),Id(setDefaultCloseOperation),[FieldAccess(Id(JFrame),Id(EXIT_ON_CLOSE))])]))])])'''
        self.assertTrue(TestAST.test(line, expect, 55))

    def test_56(self):
        line = '''
        Class SquarePanel:JPanel{
            ChangeColor(d:Color){
                Self::$panel.setBackground(d);
                Self::$panel.repaint();
                Foreach(a In 1 .. 1000 By a-2){
                    Self::$panel = d;
                }
            }
        }
        '''
        expect = '''Program([ClassDecl(Id(SquarePanel),Id(JPanel),[MethodDecl(Id(ChangeColor),Instance,[param(Id(d),ClassType(Id(Color)))],Block([Call(FieldAccess(Self(),Id($panel)),Id(setBackground),[Id(d)]),Call(FieldAccess(Self(),Id($panel)),Id(repaint),[]),For(Id(a),IntLit(1),IntLit(1000),BinaryOp(-,Id(a),IntLit(2)),Block([AssignStmt(FieldAccess(Self(),Id($panel)),Id(d))])])]))])])'''
        self.assertTrue(TestAST.test(line, expect, 56))

    def test_57(self):
        input = """
        Class Rectangle : Line {}
        """
        expect = '''Program([ClassDecl(Id(Rectangle),Id(Line),[])])'''
        self.assertTrue(TestAST.test(input, expect, 57))

    def test_58(self):
        input = """
        Class That {
        }
        Class That : This {
        }
        Class Those : That {
        }
        """
        expect ='''Program([ClassDecl(Id(That),[]),ClassDecl(Id(That),Id(This),[]),ClassDecl(Id(Those),Id(That),[])])'''
        self.assertTrue(TestAST.test(input, expect, 58))

    def test_59(self):
        input = """
        Class Square {
            Val dots : Array[Float, 4];
            Var $dots : Array[Float, 4] = Array(1.2, 3.4, 5.6, 7.8);
        }
        """
        expect = '''Program([ClassDecl(Id(Square),[AttributeDecl(Instance,ConstDecl(Id(dots),ArrayType(4,FloatType),None)),AttributeDecl(Static,VarDecl(Id($dots),ArrayType(4,FloatType),[FloatLit(1.2),FloatLit(3.4),FloatLit(5.6),FloatLit(7.8)]))])])'''
        self.assertTrue(TestAST.test(input, expect, 59))

    def test_60(self):
        input = """
        Class Rectangle {
            Val $numOfRectangle: Int = 0;

            $getNumOfRectangle() {

            }
        }
        """
        expect = '''Program([ClassDecl(Id(Rectangle),[AttributeDecl(Static,ConstDecl(Id($numOfRectangle),IntType,IntLit(0))),MethodDecl(Id($getNumOfRectangle),Static,[],Block([]))])])'''
        self.assertTrue(TestAST.test(input, expect, 60))

    def test_61(self):
        input = """
        Class Rectangle {
            $getNumOfRectangle(size : Float; dotNum, lineNum : Int; type : Rectangle) {
            }
        }
        """
        expect = '''Program([ClassDecl(Id(Rectangle),[MethodDecl(Id($getNumOfRectangle),Static,[param(Id(size),FloatType),param(Id(dotNum),IntType),param(Id(lineNum),IntType),param(Id(type),ClassType(Id(Rectangle)))],Block([]))])])'''
        self.assertTrue(TestAST.test(input, expect, 61))

    def test_62(self):
        input = """
        Class Rectangle {
            $getNumOfRectangle(size : Float; dotNum, lineNum : Int; type : Rectangle) {
            }
            getArea() {
            }
        }
        """
        expect = '''Program([ClassDecl(Id(Rectangle),[MethodDecl(Id($getNumOfRectangle),Static,[param(Id(size),FloatType),param(Id(dotNum),IntType),param(Id(lineNum),IntType),param(Id(type),ClassType(Id(Rectangle)))],Block([])),MethodDecl(Id(getArea),Instance,[],Block([]))])])'''
        self.assertTrue(TestAST.test(input, expect, 62))


    def test_63(self):
        input = """
        Class Single {
            dubbed() {
                If(a){
                    anc = 5;
                }
            }
        }
        """
        expect = '''Program([ClassDecl(Id(Single),[MethodDecl(Id(dubbed),Instance,[],Block([If(Id(a),Block([AssignStmt(Id(anc),IntLit(5))]))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 63))

    def test_64(self):
        input = """
        Class Rectangle {
            loop(){
                Foreach (i In 1 .. 100) {
                    age = 1;
                }
            }
        }
        """
        expect = '''Program([ClassDecl(Id(Rectangle),[MethodDecl(Id(loop),Instance,[],Block([For(Id(i),IntLit(1),IntLit(100),Block([AssignStmt(Id(age),IntLit(1))])])]))])])'''
        self.assertTrue(TestAST.test(input, expect, 64))


    def test_65(self):
        input = """
        Class Rectangle {
            getArea(){
                Return;
            }
        }
        """
        expect ='''Program([ClassDecl(Id(Rectangle),[MethodDecl(Id(getArea),Instance,[],Block([Return()]))])])'''
        self.assertTrue(TestAST.test(input, expect, 65))

    def test_66(self):
        input = """
        Class A {
            Var a : Int = 1 + 1 * 2;
        }
        """
        expect = '''Program([ClassDecl(Id(A),[AttributeDecl(Instance,VarDecl(Id(a),IntType,BinaryOp(+,IntLit(1),BinaryOp(*,IntLit(1),IntLit(2)))))])])'''
        self.assertTrue(TestAST.test(input, expect, 66))

    def test_67(self):
        input = """
        Class A {
            foo(){
                Single.name.first = "Davis";
            }
        }
        """
        expect = '''Program([ClassDecl(Id(A),[MethodDecl(Id(foo),Instance,[],Block([AssignStmt(FieldAccess(FieldAccess(Id(Single),Id(name)),Id(first)),StringLit(Davis))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 67))

    def test_68(self):
        input = """
        Class Program {
            main(){
                Return New A().anc();
            }
        }
        """
        expect = '''Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([Return(CallExpr(NewExpr(Id(A),[]),Id(anc),[]))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 68))

    def test_69(self):
        input = """
        Class Program {
            main(){
            }
        }
        Class NotAProgram {
            main(a:Int;b:Args){
            }
        }
        """
        expect = '''Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([]))]),ClassDecl(Id(NotAProgram),[MethodDecl(Id(main),Instance,[param(Id(a),IntType),param(Id(b),ClassType(Id(Args)))],Block([]))])])'''
        self.assertTrue(TestAST.test(input, expect, 69))


    def test_70(self):
        input = """
        Class Program {
            main(){
            }
        }
        Class NotAProgram {
            main(a:Int;b:Args){
                $getTotal(a:Int; b:Int){
                    Return a+b;
                }
            }
        }
        """
        expect = '''Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([]))]),ClassDecl(Id(NotAProgram),[MethodDecl(Id(main),Instance,[param(Id(a),IntType),param(Id(b),ClassType(Id(Args)))],Block([MethodDecl(Id($getTotal),Static,[param(Id(a),IntType),param(Id(b),IntType)],Block([Return(BinaryOp(+,Id(a),Id(b)))]))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 70))


    def test_71(self):
        input = """
            Class Program {
                main(){
                }
            }
            Class __this_nor_t_prgram {
                main(a:Int;b:Args){
                    $getTotal(a:Int; b:Int){
                        Return this::$getTotal();
                    }
                }
            }
            """
        expect = '''Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([]))]),ClassDecl(Id(__this_nor_t_prgram),[MethodDecl(Id(main),Instance,[param(Id(a),IntType),param(Id(b),ClassType(Id(Args)))],Block([MethodDecl(Id($getTotal),Static,[param(Id(a),IntType),param(Id(b),IntType)],Block([Return(CallExpr(Id(this),Id($getTotal),[]))]))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 71))

    def test_72(self):
        input = """
        Class SuperfastCar:VinFast{
            superFastMode(){
                Val speed2,speed3:Int = 10,30;
                Var d:SomeClass;
            }
        }
        """
        expect = '''Program([ClassDecl(Id(SuperfastCar),Id(VinFast),[MethodDecl(Id(superFastMode),Instance,[],Block([ConstDecl(Id(speed2),IntType,IntLit(10)),ConstDecl(Id(speed3),IntType,IntLit(30)),VarDecl(Id(d),ClassType(Id(SomeClass)),NullLiteral())]))])])'''
        self.assertTrue(TestAST.test(input, expect, 72))


    def test_73(self):
        input = """
        Class abcClass {
            Val array:Array[Array[Int,5],5] = New Wheel();
        }
        """
        expect = '''Program([ClassDecl(Id(abcClass),[AttributeDecl(Instance,ConstDecl(Id(array),ArrayType(5,ArrayType(5,IntType)),NewExpr(Id(Wheel),[])))])])'''
        self.assertTrue(TestAST.test(input, expect, 73))


    def test_74(self):
        input = """
        Class abcClass {
            foo(){
                Var speed: someZurg = Self::$s.get(10,20+30) + 20;
            }
            main(){
                object.dot.project = 123;
            }
        }
        """
        expect ='''Program([ClassDecl(Id(abcClass),[MethodDecl(Id(foo),Instance,[],Block([VarDecl(Id(speed),ClassType(Id(someZurg)),BinaryOp(+,CallExpr(FieldAccess(Self(),Id($s)),Id(get),[IntLit(10),BinaryOp(+,IntLit(20),IntLit(30))]),IntLit(20)))])),MethodDecl(Id(main),Instance,[],Block([AssignStmt(FieldAccess(FieldAccess(Id(object),Id(dot)),Id(project)),IntLit(123))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 74))


    def test_75(self):
        input = """
        Class someClass {
            fang(){
                Var mainStankOfTheWeek:object = workd::$obejct(a+6.4243e91,b);
            }
        }
        """
        expect = '''Program([ClassDecl(Id(someClass),[MethodDecl(Id(fang),Instance,[],Block([VarDecl(Id(mainStankOfTheWeek),ClassType(Id(object)),CallExpr(Id(workd),Id($obejct),[BinaryOp(+,Id(a),FloatLit(6.4243e+91)),Id(b)]))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 75))

    def test_76(self):
        input = """
        Class Send:Exception {
            main(){
                oos.writeObject(collection);
                oos.flush();
                logger.info("please speak a word");
            }
            printLog(){
                e.printStackTrace();
                back.backup(bakFileName, collection);
                logger.error("something happens");
            }
        }
        """
        expect = '''Program([ClassDecl(Id(Send),Id(Exception),[MethodDecl(Id(main),Instance,[],Block([Call(Id(oos),Id(writeObject),[Id(collection)]),Call(Id(oos),Id(flush),[]),Call(Id(logger),Id(info),[StringLit(please speak a word)])])),MethodDecl(Id(printLog),Instance,[],Block([Call(Id(e),Id(printStackTrace),[]),Call(Id(back),Id(backup),[Id(bakFileName),Id(collection)]),Call(Id(logger),Id(error),[StringLit(something happens)])]))])])'''
        self.assertTrue(TestAST.test(input, expect, 76))

    def test_77(self):
        input = """
        Class SysUserController {
            Var userService: SysUserService;
            userList(request: QueryRequest) {
                page = New Page(request.getPageNum(), request.getPageSize());
                sysUser = userService.selectByPage(page);
                Return sysUser;
            }
            checkUserName(){
                Return this.userService.findByName(username) == Null;
            }
        }
        """
        expect = '''Program([ClassDecl(Id(SysUserController),[AttributeDecl(Instance,VarDecl(Id(userService),ClassType(Id(SysUserService)),NullLiteral())),MethodDecl(Id(userList),Instance,[param(Id(request),ClassType(Id(QueryRequest)))],Block([AssignStmt(Id(page),NewExpr(Id(Page),[CallExpr(Id(request),Id(getPageNum),[]),CallExpr(Id(request),Id(getPageSize),[])])),AssignStmt(Id(sysUser),CallExpr(Id(userService),Id(selectByPage),[Id(page)])),Return(Id(sysUser))])),MethodDecl(Id(checkUserName),Instance,[],Block([Return(BinaryOp(==,CallExpr(FieldAccess(Id(this),Id(userService)),Id(findByName),[Id(username)]),NullLiteral()))]))])])'''

        self.assertTrue(TestAST.test(input, expect, 77))


    def test_78(self):
        input = """
        Class Program{
            main() {
                Val sc:Scanner = New Scanner(System.in);
                System.out.println("Enter the number n to find nth Catalan number (n <= 50)");
                Var n:Int = sc.nextInt();
                System.out.println();
                sc.close();
            }
        }
        """
        expect = '''Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([ConstDecl(Id(sc),ClassType(Id(Scanner)),NewExpr(Id(Scanner),[FieldAccess(Id(System),Id(in))])),Call(FieldAccess(Id(System),Id(out)),Id(println),[StringLit(Enter the number n to find nth Catalan number (n <= 50))]),VarDecl(Id(n),IntType,CallExpr(Id(sc),Id(nextInt),[])),Call(FieldAccess(Id(System),Id(out)),Id(println),[]),Call(Id(sc),Id(close),[])]))])])'''
        self.assertTrue(TestAST.test(input, expect, 78))


    def test_79(self):
        input = """
        Class Program{
            findNthCatalan(n:Int) {
                Var catalanArray:Long = New long();
                catalanArray[0] = 1;
                catalanArray[1] = 1;
                Foreach (i In 2 .. n By 1) {
                    catalanArray[i] = 0;
                    Foreach (j In 1 .. n By 1) {
                        catalanArray[i] = catalanArray[j] * catalanArray[i - j - 1];
                    }
                }
                Return catalanArray[n];
            }
        }
        """
        expect = '''Program([ClassDecl(Id(Program),[MethodDecl(Id(findNthCatalan),Instance,[param(Id(n),IntType)],Block([VarDecl(Id(catalanArray),ClassType(Id(Long)),NewExpr(Id(long),[])),AssignStmt(ArrayCell(Id(catalanArray),[IntLit(0)]),IntLit(1)),AssignStmt(ArrayCell(Id(catalanArray),[IntLit(1)]),IntLit(1)),For(Id(i),IntLit(2),Id(n),IntLit(1),Block([AssignStmt(ArrayCell(Id(catalanArray),[Id(i)]),IntLit(0)),For(Id(j),IntLit(1),Id(n),IntLit(1),Block([AssignStmt(ArrayCell(Id(catalanArray),[Id(i)]),BinaryOp(*,ArrayCell(Id(catalanArray),[Id(j)]),ArrayCell(Id(catalanArray),[BinaryOp(-,BinaryOp(-,Id(i),Id(j)),IntLit(1))])))])])])]),Return(ArrayCell(Id(catalanArray),[Id(n)]))]))])])'''
        self.assertTrue(TestAST.test(input, expect,79 ))


    def test_80(self):
        input = """
        Class Fibonacci {
            Var map: Map = New HashMap();
            main() {
                Var sc:Scanner = New Scanner(Scanner.in);
                Val n:Int = sc.nextInt();
                System.out.println(obj.fibMemo(n));
                System.out.println(this.fibBotUp(n));
                System.out.println(this.fibOptimized(n));
                sc.close();
            }
        }
        """
        expect = '''Program([ClassDecl(Id(Fibonacci),[AttributeDecl(Instance,VarDecl(Id(map),ClassType(Id(Map)),NewExpr(Id(HashMap),[]))),MethodDecl(Id(main),Instance,[],Block([VarDecl(Id(sc),ClassType(Id(Scanner)),NewExpr(Id(Scanner),[FieldAccess(Id(Scanner),Id(in))])),ConstDecl(Id(n),IntType,CallExpr(Id(sc),Id(nextInt),[])),Call(FieldAccess(Id(System),Id(out)),Id(println),[CallExpr(Id(obj),Id(fibMemo),[Id(n)])]),Call(FieldAccess(Id(System),Id(out)),Id(println),[CallExpr(Id(this),Id(fibBotUp),[Id(n)])]),Call(FieldAccess(Id(System),Id(out)),Id(println),[CallExpr(Id(this),Id(fibOptimized),[Id(n)])]),Call(Id(sc),Id(close),[])]))])])'''
        self.assertTrue(TestAST.test(input, expect, 80))

    def test_81(self):
        input = """
        Class Fibonacci {
            Var map: Map = New HashMap();
            main() {
                Var sc:Scanner = New Scanner(Scanner.in);
                Val n:Int = sc.nextFloat();
                System.out.println(obj.fibMemo(n));
                Foreach( i In 1 .. 100 By 1){
                    If( i == 1 ){
                        System.out.println(obj.fibMemo(n));
                    }Else{
                        System.out.println(obj.fibMemo(n));
                    }
                }
            }
        }
        """
        expect = '''Program([ClassDecl(Id(Fibonacci),[AttributeDecl(Instance,VarDecl(Id(map),ClassType(Id(Map)),NewExpr(Id(HashMap),[]))),MethodDecl(Id(main),Instance,[],Block([VarDecl(Id(sc),ClassType(Id(Scanner)),NewExpr(Id(Scanner),[FieldAccess(Id(Scanner),Id(in))])),ConstDecl(Id(n),IntType,CallExpr(Id(sc),Id(nextFloat),[])),Call(FieldAccess(Id(System),Id(out)),Id(println),[CallExpr(Id(obj),Id(fibMemo),[Id(n)])]),For(Id(i),IntLit(1),IntLit(100),IntLit(1),Block([If(BinaryOp(==,Id(i),IntLit(1)),Block([Call(FieldAccess(Id(System),Id(out)),Id(println),[CallExpr(Id(obj),Id(fibMemo),[Id(n)])])]),Block([Call(FieldAccess(Id(System),Id(out)),Id(println),[CallExpr(Id(obj),Id(fibMemo),[Id(n)])])]))])])]))])])'''
        self.assertTrue(TestAST.test(input, expect, 81))

    def test_82(self):
        input = """
        Class someClass {
            mainRussia(a:Int){
            }
            main(){
                Var mainObjectOfTheWeek: Week = workd::$obejct(a+6.4243e91,b);
                Var sc:Scanner = New Scanner(Scanner.in);
            }
        }
        """
        expect = '''Program([ClassDecl(Id(someClass),[MethodDecl(Id(mainRussia),Instance,[param(Id(a),IntType)],Block([])),MethodDecl(Id(main),Instance,[],Block([VarDecl(Id(mainObjectOfTheWeek),ClassType(Id(Week)),CallExpr(Id(workd),Id($obejct),[BinaryOp(+,Id(a),FloatLit(6.4243e+91)),Id(b)])),VarDecl(Id(sc),ClassType(Id(Scanner)),NewExpr(Id(Scanner),[FieldAccess(Id(Scanner),Id(in))]))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 82))

    def test_83(self):
        input = """
        Class abcClass {
            main(){
                registerLister(registry, KubernetesInformer: KubernetesInformer) {
                        listerBean = BeanDefinitionBuilder.rootBeanDefinition(Lister.class).getBeanDefinition();
                        listerBean.setInstanceSupplier(api.lister(kubernetesInformer.apiTypeClass()));
                        listerType = ResolvableType.forClassWithGenerics(Lister.class, kubernetesInformer.apiTypeClass());
                        listerBean.setTargetType(listerType);
                        registry.registerBeanDefinition(listerType.toString(), listerBean);
                  }
            }
        }
        """
        expect = '''Program([ClassDecl(Id(abcClass),[MethodDecl(Id(main),Instance,[],Block([MethodDecl(Id(registerLister),Instance,[param(Id(registry),ClassType(Id(KubernetesInformer))),param(Id(KubernetesInformer),ClassType(Id(KubernetesInformer)))],Block([AssignStmt(Id(listerBean),CallExpr(CallExpr(Id(BeanDefinitionBuilder),Id(rootBeanDefinition),[FieldAccess(Id(Lister),Id(class))]),Id(getBeanDefinition),[])),Call(Id(listerBean),Id(setInstanceSupplier),[CallExpr(Id(api),Id(lister),[CallExpr(Id(kubernetesInformer),Id(apiTypeClass),[])])]),AssignStmt(Id(listerType),CallExpr(Id(ResolvableType),Id(forClassWithGenerics),[FieldAccess(Id(Lister),Id(class)),CallExpr(Id(kubernetesInformer),Id(apiTypeClass),[])])),Call(Id(listerBean),Id(setTargetType),[Id(listerType)]),Call(Id(registry),Id(registerBeanDefinition),[CallExpr(Id(listerType),Id(toString),[]),Id(listerBean)])]))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 83))



    def test_84(self):
        input = """
        Class Program{
        defaultApiClient(){
              Var apiClient: ApiClient = ClientBuilder.defaultClient();
              LOGGER.warn(
                  "Could not create a Kubernetes ApiClient from either a cluster or standard environment. "
                      +. "Will return one that always connects to localhost:8080" );
              Return New ClientBuilder().build();
            }
          }
        }
        """
        expect = '''Program([ClassDecl(Id(Program),[MethodDecl(Id(defaultApiClient),Instance,[],Block([VarDecl(Id(apiClient),ClassType(Id(ApiClient)),CallExpr(Id(ClientBuilder),Id(defaultClient),[])),Call(Id(LOGGER),Id(warn),[BinaryOp(+.,StringLit(Could not create a Kubernetes ApiClient from either a cluster or standard environment. ),StringLit(Will return one that always connects to localhost:8080))]),Return(CallExpr(NewExpr(Id(ClientBuilder),[]),Id(build),[]))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 84))


    def test_85(self):
        input = """
        Class Program{
            main(){
                Var r:Random = ThreadLocalRandom.current();
                Var size,maxElement :Int = 100,100000;
                Var integers : Array[Int,5] = IntStream.generate()
                                .limit(size)
                                .sorted()
                                .boxed()
                                .toArray(new);
                Var shouldBeFound: Int = integers[r.nextInt(size - 1)];
                Var search: ExponentialSearch = New ExponentialSearch();
                Var atIndex: Int = search.find(integers, shouldBeFound);
            }
        }
        """
        expect = '''Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(r),ClassType(Id(Random)),CallExpr(Id(ThreadLocalRandom),Id(current),[])),VarDecl(Id(size),IntType,IntLit(100)),VarDecl(Id(maxElement),IntType,IntLit(100000)),VarDecl(Id(integers),ArrayType(5,IntType),CallExpr(CallExpr(CallExpr(CallExpr(CallExpr(Id(IntStream),Id(generate),[]),Id(limit),[Id(size)]),Id(sorted),[]),Id(boxed),[]),Id(toArray),[Id(new)])),VarDecl(Id(shouldBeFound),IntType,ArrayCell(Id(integers),[CallExpr(Id(r),Id(nextInt),[BinaryOp(-,Id(size),IntLit(1))])])),VarDecl(Id(search),ClassType(Id(ExponentialSearch)),NewExpr(Id(ExponentialSearch),[])),VarDecl(Id(atIndex),IntType,CallExpr(Id(search),Id(find),[Id(integers),Id(shouldBeFound)]))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 85))


    def test_86(self):
        input = """
        Class Program{
          main() {
            Var task: ABCParent = New SimpleTask();
            task.executeWithError(error);
          }
        }
        """
        expect = '''Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(task),ClassType(Id(ABCParent)),NewExpr(Id(SimpleTask),[])),Call(Id(task),Id(executeWithError),[Id(error)])]))])])'''
        self.assertTrue(TestAST.test(input, expect, 86))

    def test_87(self):
        input = """
         Class Task {
            executeWith(callback:Callback) {
                Self::$execute();
                Optional.ofNullable(callback).ifPresent(Callback::$call);
              }
            execute() {
                LOGGER.info("Perform some important activity and after call the callback method.");
            }
        }
        """
        expect = '''Program([ClassDecl(Id(Task),[MethodDecl(Id(executeWith),Instance,[param(Id(callback),ClassType(Id(Callback)))],Block([Call(Self(),Id($execute),[]),Call(CallExpr(Id(Optional),Id(ofNullable),[Id(callback)]),Id(ifPresent),[FieldAccess(Id(Callback),Id($call))])])),MethodDecl(Id(execute),Instance,[],Block([Call(Id(LOGGER),Id(info),[StringLit(Perform some important activity and after call the callback method.)])]))])])'''
        self.assertTrue(TestAST.test(input, expect, 87))

    def test_88(self):
        input = """
         Class Beast {
          OrcBeast(orcBeast : OrcBeast) {
            Self::$super(orcBeast);
            this.weapon = orcBeast.weapon;
          }
            copy() {
                Return New OrcBeast(this);
              }
          toString() {
            Return ("Orcish wolf attacks with " +. weapon);
          }
        }
        """
        expect = '''Program([ClassDecl(Id(Beast),[MethodDecl(Id(OrcBeast),Instance,[param(Id(orcBeast),ClassType(Id(OrcBeast)))],Block([Call(Self(),Id($super),[Id(orcBeast)]),AssignStmt(FieldAccess(Id(this),Id(weapon)),FieldAccess(Id(orcBeast),Id(weapon)))])),MethodDecl(Id(copy),Instance,[],Block([Return(NewExpr(Id(OrcBeast),[Id(this)]))])),MethodDecl(Id(toString),Instance,[],Block([Return(BinaryOp(+.,StringLit(Orcish wolf attacks with ),Id(weapon)))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 88))

    def test_89(self):
        input = """
        Class Program{
            main() {
                Var factory: HeroFactoryImpl = New HeroFactoryImpl(
                    New ElfMage("cooking"),
                    New ElfWarlord("cleaning"),
                    New ElfBeast("protecting")
                );
            }
        }
        """
        expect = '''Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(factory),ClassType(Id(HeroFactoryImpl)),NewExpr(Id(HeroFactoryImpl),[NewExpr(Id(ElfMage),[StringLit(cooking)]),NewExpr(Id(ElfWarlord),[StringLit(cleaning)]),NewExpr(Id(ElfBeast),[StringLit(protecting)])]))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 89))

    def test_90(self):
        input = """
        Class Program{
            main(){
                factory = New HeroFactoryImpl(
                    New OrcMage("axe"),
                    New OrcWarlord("sword"),
                    New OrcBeast("laser")
                );
                Var mage: Mage = factory.createMage();
                warlord = factory.createWarlord();
                beast = factory.createBeast();
                LOGGER.info(mage.toString());
                LOGGER.info(warlord.toString());
                LOGGER.info(beast.toString());
            }
        }
        """
        expect = '''Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([AssignStmt(Id(factory),NewExpr(Id(HeroFactoryImpl),[NewExpr(Id(OrcMage),[StringLit(axe)]),NewExpr(Id(OrcWarlord),[StringLit(sword)]),NewExpr(Id(OrcBeast),[StringLit(laser)])])),VarDecl(Id(mage),ClassType(Id(Mage)),CallExpr(Id(factory),Id(createMage),[])),AssignStmt(Id(warlord),CallExpr(Id(factory),Id(createWarlord),[])),AssignStmt(Id(beast),CallExpr(Id(factory),Id(createBeast),[])),Call(Id(LOGGER),Id(info),[CallExpr(Id(mage),Id(toString),[])]),Call(Id(LOGGER),Id(info),[CallExpr(Id(warlord),Id(toString),[])]),Call(Id(LOGGER),Id(info),[CallExpr(Id(beast),Id(toString),[])])]))])])'''
        self.assertTrue(TestAST.test(input, expect, 90))

    def test_91(self):
        input = """
        Class Prgram{
            main(){
              stop(){
                reactor.stop();
                dispatcher.stop();
                Foreach ( channel In 1 .. 100 ) {
                  channel.getJavaChannel().close();
                }
              }
          }
        }
        """
        expect = '''Program([ClassDecl(Id(Prgram),[MethodDecl(Id(main),Instance,[],Block([MethodDecl(Id(stop),Instance,[],Block([Call(Id(reactor),Id(stop),[]),Call(Id(dispatcher),Id(stop),[]),For(Id(channel),IntLit(1),IntLit(100),Block([Call(CallExpr(Id(channel),Id(getJavaChannel),[]),Id(close),[])])])]))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 91))

    def test_92(self):
        input = """
        Class Reactor{
            main(){
                tcpChannel(port:Int;handler:ChannelHandler){
                    Var channel: Channel = New NioServerSocketChannel(port, handler);
                    channel.bind();
                    channels.add(channel);
                    Return channel;
              }
            }  
        }
        """
        expect = '''Program([ClassDecl(Id(Reactor),[MethodDecl(Id(main),Instance,[],Block([MethodDecl(Id(tcpChannel),Instance,[param(Id(port),IntType),param(Id(handler),ClassType(Id(ChannelHandler)))],Block([VarDecl(Id(channel),ClassType(Id(Channel)),NewExpr(Id(NioServerSocketChannel),[Id(port),Id(handler)])),Call(Id(channel),Id(bind),[]),Call(Id(channels),Id(add),[Id(channel)]),Return(Id(channel))]))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 92))

    def test_93(self):
        input = """
        Class Reactor{
            udpChannel(port: Int;handler:ChannelHandler){
                Var channel:CHannel = New NioDatagramChannel(port, handler);
                channel.bind();
                channels.add(channel);
                Return channel;
          }
        }
        """
        expect = '''Program([ClassDecl(Id(Reactor),[MethodDecl(Id(udpChannel),Instance,[param(Id(port),IntType),param(Id(handler),ClassType(Id(ChannelHandler)))],Block([VarDecl(Id(channel),ClassType(Id(CHannel)),NewExpr(Id(NioDatagramChannel),[Id(port),Id(handler)])),Call(Id(channel),Id(bind),[]),Call(Id(channels),Id(add),[Id(channel)]),Return(Id(channel))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 93))

    def test_94(self):
        input = """
        Class Program{
            main(){
                 getModelsAfter2000(cars: Array[Car,5]) {
                    Return cars.stream().filter(car.getYear() > 2000)
                        .sorted(Comparator.comparing(Car::$getYear))
                        .map(Car::$getModel).collect(Collectors.toList());
                  }
            }
        }
        """
        expect = '''Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([MethodDecl(Id(getModelsAfter2000),Instance,[param(Id(cars),ArrayType(5,ClassType(Id(Car))))],Block([Return(CallExpr(CallExpr(CallExpr(CallExpr(CallExpr(Id(cars),Id(stream),[]),Id(filter),[BinaryOp(>,CallExpr(Id(car),Id(getYear),[]),IntLit(2000))]),Id(sorted),[CallExpr(Id(Comparator),Id(comparing),[FieldAccess(Id(Car),Id($getYear))])]),Id(map),[FieldAccess(Id(Car),Id($getModel))]),Id(collect),[CallExpr(Id(Collectors),Id(toList),[])]))]))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 94))

    def test_95(self):
        input = """
        Class Program{
            getSedanCarsOwnedSortedByDate(person:Person) {
                Return persons.stream().map(Person::$getCars).flatMap(List::$stream)
                    .filter(Category.SEDAN.equals(car.getCategory()))
                    .sorted(Comparator.comparing(Car::$getYear)).collect(Collectors.toList());
              }
        }
        """
        expect = '''Program([ClassDecl(Id(Program),[MethodDecl(Id(getSedanCarsOwnedSortedByDate),Instance,[param(Id(person),ClassType(Id(Person)))],Block([Return(CallExpr(CallExpr(CallExpr(CallExpr(CallExpr(CallExpr(Id(persons),Id(stream),[]),Id(map),[FieldAccess(Id(Person),Id($getCars))]),Id(flatMap),[FieldAccess(Id(List),Id($stream))]),Id(filter),[CallExpr(FieldAccess(Id(Category),Id(SEDAN)),Id(equals),[CallExpr(Id(car),Id(getCategory),[])])]),Id(sorted),[CallExpr(Id(Comparator),Id(comparing),[FieldAccess(Id(Car),Id($getYear))])]),Id(collect),[CallExpr(Id(Collectors),Id(toList),[])]))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 95))

    def test_96(self):
        input = """
        Class Program{
              main() {
                Var cars:Car = CarFactory.createCars();
                modelsImperative = ImperativeProgramming.getModelsAfter2000(cars);
                LOGGER.info(modelsImperative.toString());
            
                modelsFunctional = FunctionalProgramming.getModelsAfter2000(cars);
                LOGGER.info(modelsFunctional.toString());
            
                groupingByCategoryImperative = ImperativeProgramming.getGroupingOfCarsByCategory(cars);
                LOGGER.info(groupingByCategoryImperative.toString());
            
                groupingByCategoryFunctional = FunctionalProgramming.getGroupingOfCarsByCategory(cars);
                LOGGER.info(groupingByCategoryFunctional.toString());
                
                john = New Person(cars);
                
                sedansOwnedImperative = ImperativeProgramming.getSedanCarsOwnedSortedByDate(List.of(john));
                LOGGER.info(sedansOwnedImperative.toString());
            
                sedansOwnedFunctional = FunctionalProgramming.getSedanCarsOwnedSortedByDate(List.of(john));
                LOGGER.info(sedansOwnedFunctional.toString());
              }
        }
        """
        expect = '''Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(cars),ClassType(Id(Car)),CallExpr(Id(CarFactory),Id(createCars),[])),AssignStmt(Id(modelsImperative),CallExpr(Id(ImperativeProgramming),Id(getModelsAfter2000),[Id(cars)])),Call(Id(LOGGER),Id(info),[CallExpr(Id(modelsImperative),Id(toString),[])]),AssignStmt(Id(modelsFunctional),CallExpr(Id(FunctionalProgramming),Id(getModelsAfter2000),[Id(cars)])),Call(Id(LOGGER),Id(info),[CallExpr(Id(modelsFunctional),Id(toString),[])]),AssignStmt(Id(groupingByCategoryImperative),CallExpr(Id(ImperativeProgramming),Id(getGroupingOfCarsByCategory),[Id(cars)])),Call(Id(LOGGER),Id(info),[CallExpr(Id(groupingByCategoryImperative),Id(toString),[])]),AssignStmt(Id(groupingByCategoryFunctional),CallExpr(Id(FunctionalProgramming),Id(getGroupingOfCarsByCategory),[Id(cars)])),Call(Id(LOGGER),Id(info),[CallExpr(Id(groupingByCategoryFunctional),Id(toString),[])]),AssignStmt(Id(john),NewExpr(Id(Person),[Id(cars)])),AssignStmt(Id(sedansOwnedImperative),CallExpr(Id(ImperativeProgramming),Id(getSedanCarsOwnedSortedByDate),[CallExpr(Id(List),Id(of),[Id(john)])])),Call(Id(LOGGER),Id(info),[CallExpr(Id(sedansOwnedImperative),Id(toString),[])]),AssignStmt(Id(sedansOwnedFunctional),CallExpr(Id(FunctionalProgramming),Id(getSedanCarsOwnedSortedByDate),[CallExpr(Id(List),Id(of),[Id(john)])])),Call(Id(LOGGER),Id(info),[CallExpr(Id(sedansOwnedFunctional),Id(toString),[])])]))])])'''
        self.assertTrue(TestAST.test(input, expect, 96))

    def test_97(self):
        input = """
        Class Program{
                filteringSimpleProbableThreats() {
                    LOGGER.info("### Filtering ProbabilisticThreatAwareSystem by probability ###");
                
                    trojanArcBomb = New SimpleProbableThreat("Trojan-ArcBomb", 1, ThreatType.TROJAN, 0.99);
                    rootkit = New SimpleProbableThreat("Rootkit-Kernel", 2, ThreatType.ROOTKIT, 0.8);
                    probableThreats = List.of(trojanArcBomb, rootkit);
                
                    probabilisticThreatAwareSystem = New SimpleProbabilisticThreatAwareSystem("Sys-1", probableThreats);
                
                    LOGGER.info("Filtering ProbabilisticThreatAwareSystem. Initial : " +. probabilisticThreatAwareSystem);
                }
        }
        """
        expect = '''Program([ClassDecl(Id(Program),[MethodDecl(Id(filteringSimpleProbableThreats),Instance,[],Block([Call(Id(LOGGER),Id(info),[StringLit(### Filtering ProbabilisticThreatAwareSystem by probability ###)]),AssignStmt(Id(trojanArcBomb),NewExpr(Id(SimpleProbableThreat),[StringLit(Trojan-ArcBomb),IntLit(1),FieldAccess(Id(ThreatType),Id(TROJAN)),FloatLit(0.99)])),AssignStmt(Id(rootkit),NewExpr(Id(SimpleProbableThreat),[StringLit(Rootkit-Kernel),IntLit(2),FieldAccess(Id(ThreatType),Id(ROOTKIT)),FloatLit(0.8)])),AssignStmt(Id(probableThreats),CallExpr(Id(List),Id(of),[Id(trojanArcBomb),Id(rootkit)])),AssignStmt(Id(probabilisticThreatAwareSystem),NewExpr(Id(SimpleProbabilisticThreatAwareSystem),[StringLit(Sys-1),Id(probableThreats)])),Call(Id(LOGGER),Id(info),[BinaryOp(+.,StringLit(Filtering ProbabilisticThreatAwareSystem. Initial : ),Id(probabilisticThreatAwareSystem))])]))])])'''
        self.assertTrue(TestAST.test(input, expect, 97))

    def test_98(self):
        input = """
        Class Program{
            main() {
                holderThreadSafe = New HolderThreadSafe();
                another = holderThreadSafe.getHeavy();
                LOGGER.info("another", another);
                java8Holder = New Java8Holder();
                next = java8Holder.getHeavy();
                LOGGER.info("next", next);
              }
        }
        """
        expect = '''Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([AssignStmt(Id(holderThreadSafe),NewExpr(Id(HolderThreadSafe),[])),AssignStmt(Id(another),CallExpr(Id(holderThreadSafe),Id(getHeavy),[])),Call(Id(LOGGER),Id(info),[StringLit(another),Id(another)]),AssignStmt(Id(java8Holder),NewExpr(Id(Java8Holder),[])),AssignStmt(Id(next),CallExpr(Id(java8Holder),Id(getHeavy),[])),Call(Id(LOGGER),Id(info),[StringLit(next),Id(next)])]))])])'''
        self.assertTrue(TestAST.test(input, expect, 98))

    def test_99(self):
        input = """
        Class Program{
            createAndCacheHeavy() {
              heavyInstance = New Heavy();
              get() {
                Return heavyInstance;
              }
          }
        }
        """
        expect = '''Program([ClassDecl(Id(Program),[MethodDecl(Id(createAndCacheHeavy),Instance,[],Block([AssignStmt(Id(heavyInstance),NewExpr(Id(Heavy),[])),MethodDecl(Id(get),Instance,[],Block([Return(Id(heavyInstance))]))]))])])'''
        self.assertTrue(TestAST.test(input, expect, 99))
