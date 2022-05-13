import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):
    
    def test_simple(self):
        input = """
        Class Program{
            main(){}
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_1(self):
        input = """
        Class Normal{

        }
        Class Normal{

        }
        Class Program{
            main(){

            }
        }
        """
        expect = "Redeclared Class: Normal"
        self.assertTrue(TestChecker.test(input,expect,401))

    def test_2(self):
        input = """
        Class Normal{
            Var a,b,c:Int;
            function(a:Int;b:Float){
                Val a:Int = 0;
            }
        }
        Class Program{
            main(){

            }  
        }
        """
        expect = "Redeclared Constant: a"
        self.assertTrue(TestChecker.test(input,expect,402))

    def test_3(self):
        input = """
        Class Normal{
            Var a:Int;
            function(){
                Var b,c: Int;
                b = a;
            }
            another_function(a:Int;b:Float){
                Var c: Float;
                b = a + c + 1.01;
            }
        }
        Class Program{
            main(){

            }  
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,403))

    def test_4(self):
        input = """
        Class Program{
            main(){
                Var a,c:Int;
                Var b:Float = 1;
                b = 1 + 2 + c + a;
            }  
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,404))

    def test_5(self):
        input = """
        Class Normal{
            Var a:Int;
            function(){
                Var b,c:Int;
                b = a;
            }
            another_function(a:Int;b:Float){
                Var c: Float;
                Var a:Int;
                b = a + c + 1.01;
            }
        }
        Class Program{
            main(){

            }  
        }
        """
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,405))

    def test_6(self):
        input = """
        Class Normal{
            another_function(a:Int;b,a:Float){
                Var c: Float;
                Var a:Int;
                b = a + c + 1.01;
            }
        }
        Class Program{
            main(){

            }  
        }
        """
        expect = "Redeclared Parameter: a"
        self.assertTrue(TestChecker.test(input,expect,406))

    def test_7(self):
        input = """
        Class Normal{
            another_function(a:Int;b:Float){
            }
        }
        Class Program{
            main(){
                Var b:Boolean = 1.72;
            }  
        }
        """
        expect = "Type Mismatch In Statement: VarDecl(Id(b),BoolType,FloatLit(1.72))"
        self.assertTrue(TestChecker.test(input,expect,407))

    def test_8(self):
        input = """
        Class Normal{
            Var a: Bool = 1;
            another_function(a:Int;b:Float){
                b = a + c + 1.01;
                a = 1.1;
            }
        }
        Class Program{
            main(){

            }  
        }
        """
        expect = "Type Mismatch In Statement: VarDecl(Id(a),ClassType(Id(Bool)),IntLit(1))"
        self.assertTrue(TestChecker.test(input,expect,408))

    def test_9(self):
        input = """
        Class Normal{
            another_function(a:Int;b:Float){
            }
        }
        Class Program{
            main(){
                Val b:Boolean = 1.72;
            }  
        }
        """
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(b),BoolType,FloatLit(1.72))"
        self.assertTrue(TestChecker.test(input,expect,409))

    def test_10(self):
        input = """
        Class Normal{
            Val b: Boolean = 1.72;
            another_function(a:Int;b:Float){
            }
        }
        Class Program{
            main(){
                Var a:Float;
            }  
        }
        """
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(b),BoolType,FloatLit(1.72))"
        self.assertTrue(TestChecker.test(input,expect,410))
    
    def test_11(self):
        input = """
        Class Normal{
            Val a:Int =1;
            another_function(a:Int){
                Var a:Float = 1;
            }
        }
        Class Program{
            main(){
            }  
        }
        """
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,411))

    def test_12(self):
        input = """
        Class Normal{
            another_function(){
                Var a:Float;
            }
            another_function(){
                Var a:Float;
            }
        }
        Class Program{
            main(){
            }  
        }
        """
        expect = "Redeclared Method: another_function"
        self.assertTrue(TestChecker.test(input,expect,412))

    def test_13(self):
        input = """
        Class Program{
            main(){
            }  
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,413))

    def test_14(self):
        input = """
        Class Program{
            main(a:Int){
            }
        }
        """
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input,expect,414))

    def test_15(self):
        input = """
        Class normal{
            Var a: Int = 5.0;
        }
        Class Program{
            main(){
                Var b: Boolean = 1 == 2;
            }
        }
        """
        expect = "Type Mismatch In Statement: VarDecl(Id(a),IntType,FloatLit(5.0))"
        self.assertTrue(TestChecker.test(input,expect,415))
    
    def test_16(self):
        input = """
        Class normal{
        }
        Class Program{
            main(){
                Var b: String = 1 +. "as";
            }
        }
        """
        expect = "Type Mismatch In Expression: BinaryOp(+.,IntLit(1),StringLit(as))"
        self.assertTrue(TestChecker.test(input,expect,416))

    def test_17(self):
        input = """
        Class normal{
        }
        Class Program{
            main(){
                Var a: Int = 0;
                Foreach(a In 1 .. 9 By 3){
                    Continue;
                }
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,417))


    def test_18(self):
        input = """
        Class normal{
        }
        Class Program{
            main(){
                Break;
                Var a: Int = 0;
                Foreach(a In 1 .. 9 By 3){
                }
            }
        }
        """
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,418))

    def test_19(self):
        input = """
        Class normal{
        }
        Class Program{
            main(){
                Var a,b: Int = 0,1;
                Var c : Boolean; 
                If(1){
                    c = (1 + 3) == 1;
                }Else{
                    c = (1 + 3) == 2;
                }
            }
        }
        """
        expect = "Type Mismatch In Statement: If(IntLit(1),Block([AssignStmt(Id(c),BinaryOp(==,BinaryOp(+,IntLit(1),IntLit(3)),IntLit(1)))]),Block([AssignStmt(Id(c),BinaryOp(==,BinaryOp(+,IntLit(1),IntLit(3)),IntLit(2)))]))"
        self.assertTrue(TestChecker.test(input,expect,419))

    def test_20(self):
        input = """
        Class normal{
            sub(a,b:Int){
                a = a+b;
            }
        }
        Class Program{
            main(){
                Var a: Int = 0;
                Var b : Boolean;
                Var c : normal;
                c.sub(1,2);
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,420))

    def test_21(self):
        input = """
        Class normal{
            Val a,b: Float = 3,4;
            Val c,d: Int = 4 ,5;
            sub(a,b:Int){
                Return a-b;
            }
        }
        Class Program{
            main(){
                Var a: Int = 1;
                Var b: normal;
                a = b.sub(1,1);
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,421))

    def test_22(self):
        input = """
        Class normal{
            sub(a,b:Int){
                Return a-b;
            }
        }
        Class Program{
            main(){
                Var a : normal;
                a.sub(1,1);
            }
        }
        """
        expect = "Type Mismatch In Statement: Call(Id(a),Id(sub),[IntLit(1),IntLit(1)])"
        self.assertTrue(TestChecker.test(input,expect,422))

    def test_23(self):
        input = """
        Class normal{
            sub(a,b:Int){
                Return a-b;
            }
        }
        Class Program{
            main(){
                Var a: Float;
                Var b: normal;
                a = 1.0 + b.sub(1,1);
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,423))

    def test_24(self):
        input = """
        Class normal{
            Val a,b: Float = 3,4;
            Val c,d: Int = 4 ,5;
            sub(a,b:Float){
                Return a-b;
            }
        }
        Class Program{
            main(){
                Var a: Float;
                Var b: normal;
                a = 1.0 + b.sub(1,1);
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,424))

    def test_25(self):
        input = """
        Class normal{
            Val a,b: Float = 3,4;
            Val c,d: Int = 4 ,5;
            sub(a,b:Float){
                Return a-b;
            }
        }
        Class Program{
            main(){
                Var a: Float;
                Var b: normal;
                a = 1.0 + b.sub1(1,1);
            }
        }
        """
        expect = "Undeclared Method: sub1"
        self.assertTrue(TestChecker.test(input,expect,425))

    def test_26(self):
        input = """
        Class normal{
            Val a,b: Float = 3,4;
            Val c,d: Int = 4 ,5;
            sub(a,b:Float){
                Return a-b;
            }
        }
        Class Program{
            main(){
                Var a: Float;
                a = 1.0 + normal1.sub1(1,1);
            }
        }
        """
        expect = "Undeclared Identifier: normal1"
        self.assertTrue(TestChecker.test(input,expect,426))

    def test_27(self):
        input = """
        Class normal{
            Val a,b: Float = 3,4;
            Val c,d: Int = 4 ,5;
            sub(a,b:Float){
                a = a-b;
            }
        }
        Class Program{
            main(){
                Var a: Float;
                Var b: normal;
                b.sub1(1,1);
            }
        }
        """
        expect = "Undeclared Method: sub1"
        self.assertTrue(TestChecker.test(input,expect,427))

    def test_28(self):
        input = """
        Class normal{
            Val a,b: Float = 3,4;
            Val c,d: Int = 4 ,5;
            sub(a,b:Float){
                Return a-b;
            }
        }
        Class Program{
            main(){
                Var a: Float;
                a = 1.0 + normal1.sub1(1,1);
            }
        }
        """
        expect = "Undeclared Identifier: normal1"
        self.assertTrue(TestChecker.test(input,expect,428))

    def test_29(self):
        input = """
        Class normal{
            Val a,b: Int = 3,4;
            Val $c,d: Int = 4,5;
        }
        Class Program{
            main(){
                Var a: Boolean;
                Var res: Float;
                res = 1.0 + normal.a;
            }
        }
        """
        expect = "Illegal Member Access: FieldAccess(Id(normal),Id(a))"
        self.assertTrue(TestChecker.test(input,expect,429))

    def test_30(self):
        input = """
        Class normal{
            Var a,$b: Int = 3,4;
            Val c,d: Int = 4,5;
            main(){
                a= a+$b+c;
            }
        }
        Class Program{
            main(){
                Var res: Float;
                res = 1.0 + normal::$b;
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,430))

    def test_31(self):
        input = """
        Class normal{
            Var a,b,$b: Int = 3,4,5;
            Val c,d: Int = 4,5;
            main(){
                a= a+$b+c;
            }
        }
        Class Program{
            main(){
                Var res: Float;
                Var o : normal = New normal();
                res = normal::$b;
                res = 1.0 + o.b;
            }
        }
        """
        expect = "Illegal Member Access: FieldAccess(Id(o),Id(b))"
        self.assertTrue(TestChecker.test(input,expect,431))

    def test_32(self):
        input = """
        Class Program{
            main(){
                Var a: Array[Int,5] = Array(1,2,3,4,5);                
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,432))

    def test_33(self):
        input = """
        Class Program{
            main(){
                Var a: Array[Int,5] = Array(1,2,True,4,5);                
            }
        }
        """
        expect = "Illegal Array Literal: [IntLit(1),IntLit(2),BooleanLit(True),IntLit(4),IntLit(5)]"
        self.assertTrue(TestChecker.test(input,expect,433))

    def test_34(self):
        input = """
        Class Program{
            main(){
                Var a: Array[Int,5] = Array(1,2,3,4,5);
                a[1][2][3.0] = 2;                
            }
        }
        """
        expect = "Type Mismatch In Expression: ArrayCell(Id(a),[IntLit(1),IntLit(2),FloatLit(3.0)])"
        self.assertTrue(TestChecker.test(input,expect,434))

    def test_35(self):
        input = """
        Class Program{
            main(){
                Var a: Array[Int,5] = Array(1,2,3,4,5);
                a[1] = 2.0;                
            }
        }
        """
        expect = "Type Mismatch In Statement: AssignStmt(ArrayCell(Id(a),[IntLit(1)]),FloatLit(2.0))"
        self.assertTrue(TestChecker.test(input,expect,435))

    def test_36(self):
        input = """
        Class A{

        }
        Class Program{
            main(){
                Var a: A;
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,436))

    def test_37(self):
        input = """
        Class A{
            Constructor(a,b:Int){
                Return a+b;
            }
        }
        Class Program{
            main(){
                Var a: A = New A(1,2);
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,437))

    def test_38(self):
        input = """
        Class A{
            Constructor(a,b:Int){
                Return a+b;
            }
        }
        Class Program{
            main(){
                Var a: A = New A(1,2);
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,438))

    def test_39(self):
        input = """
        Class Program{
            main(){
                Var a: Array[Int,1] = Array(1);
                Var b: Array[Int,2] = Array(1,2);
                a = b;
            }
        }
        """
        expect = "Type Mismatch In Statement: AssignStmt(Id(a),Id(b))"
        self.assertTrue(TestChecker.test(input,expect,439))

    def test_40(self):
        input = """
        Class Program{
            main(){
                Var a: Array[Int,1] = Array(1);
                Var b: Array[Int,2] = Array(1,2);
                a[0][1] = b;
            }
        }
        """
        expect = "Type Mismatch In Expression: ArrayCell(Id(a),[IntLit(0),IntLit(1)])"
        self.assertTrue(TestChecker.test(input,expect,440))

    def test_41(self):
        input = """
        Class Program{
            main(){
                Var a: Array[Int,1] = Array(1);
                Var b: Int;
                a[0] = b;
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,441))
    
    def test_42(self):
        input = """
        Class Program{
            main(){
                Var a: Int ;
                Val b: Int = a;
                a = b;
            }
        }
        """
        expect = "Illegal Constant Expression: Id(a)"
        self.assertTrue(TestChecker.test(input,expect,442))

    def test_43(self):
        input = """
        Class Program{
            main(){
                Val a,b: Int = 1,2;
                Var c: Float = b;
                c = a + b;
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,443))

    def test_44(self):
        input = """
        Class Program{
            main(){
                Val a,b: Int = 1,2;
                Var c: Float = b;
                c = a + b;
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,444))

    def test_45(self):
        input = """
        Class Program{
            main(){
                Val a: Array[Array[Int,2],1] = Array(Array(2),Array(3));
                Var c: Array[Int,5] = Array(1,2,3,4,5);
                a[1] = c;
            }
        }
        """
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(a),ArrayType(1,ArrayType(2,IntType)),[[IntLit(2)],[IntLit(3)]])"
        self.assertTrue(TestChecker.test(input,expect,445))

    def test_46(self):
        input = """
        Class Program{
            main(){
                Val a: Array[Array[Int,2],1] = Array(Array(1,2));
                Var c: Array[Int,2] = Array(1,2);
                a[0] = c;
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,446))


    def test_47(self):
        input = """
        Class Program{
            main(){
                Val a: Array[Array[Int,2],2] = Array(Array(1,2),Array(2,3));
                Var c: Array[Int,5] = Array(1,2,3,4,5);
                a[1][2] = c[1];
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,447))

    def test_48(self):
        input = """
        Class Program{
            main(){
                Val a: Array[Array[Int,2],1] = Array(Array(2),Array(3));
                Var c: Array[Int,5] = Array(Array(1,2),Array(1));
                a[1] = c;
            }
        }
        """
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(a),ArrayType(1,ArrayType(2,IntType)),[[IntLit(2)],[IntLit(3)]])"
        self.assertTrue(TestChecker.test(input,expect,448))

    def test_49(self):
        input = """
        Class Program{
            main(){
                Val a: Array[Array[Int,2],2] = Array(Array(1,2),Array(1.2,True));
                Var c: Array[Int,5] = Array(1,2,3,4,5);
                a[1] = c;
            }
        }
        """
        expect = "Illegal Array Literal: [FloatLit(1.2),BooleanLit(True)]"
        self.assertTrue(TestChecker.test(input,expect,449))

    def test_50(self): 
        input = """
            Class Person{
                Var name: String;
                Var phone: String;
                Constructor(newName: String; newphone : String){
                    Self.name = newName;
                    Self.phone = newphone;
                }
            }
            Class Program{
                main(){
                    Var a : Person = New Person("Name","928103495");
                }
            }
            """
        expect = "[]"
        self.assertTrue(TestChecker.test(input, expect, 450)) 

    def test_51(self):
        input = """
        Class Program{
            main(){}
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,451))
    
    def test_52(self):
        input = """
        Class Normal{

        }
        Class Normal{

        }
        Class Program{
            main(){

            }
        }
        """
        expect = "Redeclared Class: Normal"
        self.assertTrue(TestChecker.test(input,expect,452))

    def test_53(self):
        input = """
        Class Normal{
            Var a,b,c:Int;
            function(a:Int;b:Float){
                Val a:Int = 0;
            }
        }
        Class Program{
            main(){

            }  
        }
        """
        expect = "Redeclared Constant: a"
        self.assertTrue(TestChecker.test(input,expect,453))

    def test_54(self):
        input = """
        Class Normal{
            Var a:Int;
            function(){
                Var b,c: Int;
                b = a;
            }
            another_function(a:Int;b:Float){
                Var c: Float;
                b = a + c + 1.01;
            }
        }
        Class Program{
            main(){

            }  
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,454))

    def test_55(self):
        input = """
        Class Program{
            main(){
                Var a,c:Int;
                Var b:Float = 1;
                b = 1 + 2 + c + a;
            }  
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,455))

    def test_56(self):
        input = """
        Class Normal{
            Var a:Int;
            function(){
                Var b,c:Int;
                b = a;
            }
            another_function(a:Int;b:Float){
                Var c: Float;
                Var a:Int;
                b = a + c + 1.01;
            }
        }
        Class Program{
            main(){

            }  
        }
        """
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,456))

    def test_57(self):
        input = """
        Class Normal{
            another_function(a:Int;b,a:Float){
                Var c: Float;
                Var a:Int;
                b = a + c + 1.01;
            }
        }
        Class Program{
            main(){

            }  
        }
        """
        expect = "Redeclared Parameter: a"
        self.assertTrue(TestChecker.test(input,expect,457))

    def test_58(self):
        input = """
        Class Normal{
            another_function(a:Int;b:Float){
            }
        }
        Class Program{
            main(){
                Var b:Boolean = 1.72;
            }  
        }
        """
        expect = "Type Mismatch In Statement: VarDecl(Id(b),BoolType,FloatLit(1.72))"
        self.assertTrue(TestChecker.test(input,expect,458))

    def test_59(self):
        input = """
        Class Normal{
            Var a: Bool = 1;
            another_function(a:Int;b:Float){
                b = a + c + 1.01;
                a = 1.1;
            }
        }
        Class Program{
            main(){

            }  
        }
        """
        expect = "Type Mismatch In Statement: VarDecl(Id(a),ClassType(Id(Bool)),IntLit(1))"
        self.assertTrue(TestChecker.test(input,expect,459))

    def test_60(self):
        input = """
        Class Normal{
            another_function(a:Int;b:Float){
            }
        }
        Class Program{
            main(){
                Val b:Boolean = 1.72;
            }  
        }
        """
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(b),BoolType,FloatLit(1.72))"
        self.assertTrue(TestChecker.test(input,expect,460))

    def test_61(self):
        input = """
        Class Normal{
            Val b: Boolean = 1.72;
            another_function(a:Int;b:Float){
            }
        }
        Class Program{
            main(){
                Var a:Float;
            }  
        }
        """
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(b),BoolType,FloatLit(1.72))"
        self.assertTrue(TestChecker.test(input,expect,461))
    
    def test_62(self):
        input = """
        Class Normal{
            Val a:Int =1;
            another_function(a:Int){
                Var a:Float = 1;
            }
        }
        Class Program{
            main(){
            }  
        }
        """
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,462))

    def test_63(self):
        input = """
        Class Normal{
            another_function(){
                Var a:Float;
            }
            another_function(){
                Var a:Float;
            }
        }
        Class Program{
            main(){
            }  
        }
        """
        expect = "Redeclared Method: another_function"
        self.assertTrue(TestChecker.test(input,expect,463))

    def test_64(self):
        input = """
        Class Program{
            main(){
            }  
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,464))

    def test_65(self):
        input = """
        Class Program{
            main(a:Int){
            }
        }
        """
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input,expect,465))

    def test_66(self):
        input = """
        Class normal{
            Var a: Int = 5.0;
        }
        Class Program{
            main(){
                Var b: Boolean = 1 == 2;
            }
        }
        """
        expect = "Type Mismatch In Statement: VarDecl(Id(a),IntType,FloatLit(5.0))"
        self.assertTrue(TestChecker.test(input,expect,466))
    
    def test_67(self):
        input = """
        Class normal{
        }
        Class Program{
            main(){
                Var b: String = 1 +. "as";
            }
        }
        """
        expect = "Type Mismatch In Expression: BinaryOp(+.,IntLit(1),StringLit(as))"
        self.assertTrue(TestChecker.test(input,expect,467))

    def test_68(self):
        input = """
        Class normal{
        }
        Class Program{
            main(){
                Var a: Int = 0;
                Foreach(a In 1 .. 9 By 3){
                    Continue;
                }
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,468))


    def test_69(self):
        input = """
        Class normal{
        }
        Class Program{
            main(){
                Break;
                Var a: Int = 0;
                Foreach(a In 1 .. 9 By 3){
                }
            }
        }
        """
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,469))

    def test_70(self):
        input = """
        Class normal{
        }
        Class Program{
            main(){
                Var a,b: Int = 0,1;
                Var c : Boolean; 
                If(1){
                    c = (1 + 3) == 1;
                }Else{
                    c = (1 + 3) == 2;
                }
            }
        }
        """
        expect = "Type Mismatch In Statement: If(IntLit(1),Block([AssignStmt(Id(c),BinaryOp(==,BinaryOp(+,IntLit(1),IntLit(3)),IntLit(1)))]),Block([AssignStmt(Id(c),BinaryOp(==,BinaryOp(+,IntLit(1),IntLit(3)),IntLit(2)))]))"
        self.assertTrue(TestChecker.test(input,expect,470))

    def test_71(self):
        input = """
        Class normal{
            sub(a,b:Int){
                a = a+b;
            }
        }
        Class Program{
            main(){
                Var a: Int = 0;
                Var b : normal;
                b.sub(1,2);
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,471))

    def test_72(self):
        input = """
        Class normal{
            Val a,b: Float = 3,4;
            Val c,d: Int = 4 ,5;
            sub(a,b:Int){
                Return a- b ;
            }
        }
        Class Program{
            main(){
                Var a: Int = 1;
                Var b : normal;
                a = b.sub(1,1);
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,472))

    def test_73(self):
        input = """
        Class normal{
            sub(a,b:Int){
                Return a-b;
            }
        }
        Class Program{
            main(){
                Var b : normal;
                b.sub(1,1);
            }
        }
        """
        expect = "Type Mismatch In Statement: Call(Id(b),Id(sub),[IntLit(1),IntLit(1)])"
        self.assertTrue(TestChecker.test(input,expect,473))

    def test_74(self):
        input = """
        Class normal{
            sub(a,b:Int){
                Return a-b;
            }
        }
        Class Program{
            main(){
                Var a: Float;
                Var b : normal;
                a = 1.0 + b.sub(1,1);
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,474))

    def test_75(self):
        input = """
        Class normal{
            Val a,b: Float = 3,4;
            Val c,d: Int = 4 ,5;
            sub(a,b:Float){
                Return a-b;
            }
        }
        Class Program{
            main(){
                Var a: Float;
                Var b : normal;
                a = 1.0 + b.sub(1,1);
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,475))

    def test_76(self):
        input = """
        Class normal{
            Val a,b: Float = 3,4;
            Val c,d: Int = 4 ,5;
            sub(a,b:Float){
                Return a-b;
            }
        }
        Class Program{
            main(){
                Var a: Float;
                Var b : normal;
                a = 1.0 + b.sub1(1,1);
            }
        }
        """
        expect = "Undeclared Method: sub1"
        self.assertTrue(TestChecker.test(input,expect,476))

    def test_77(self):
        input = """
        Class normal{
            Val a,b: Float = 3,4;
            Val c,d: Int = 4 ,5;
            sub(a,b:Float){
                Return a-b;
            }
        }
        Class Program{
            main(){
                Var a: Float;
                Var b : normal;
                a = 1.0 + normal1.sub1(1,1);
            }
        }
        """
        expect = "Undeclared Identifier: normal1"
        self.assertTrue(TestChecker.test(input,expect,477))

    def test_78(self):
        input = """
        Class normal{
            Val a,b: Float = 3,4;
            Val c,d: Int = 4 ,5;
            sub(a,b:Float){
                a = a-b;
            }
        }
        Class Program{
            main(){
                Var a: Float;
                Var b : normal;
                b.sub1(1,1);
            }
        }
        """
        expect = "Undeclared Method: sub1"
        self.assertTrue(TestChecker.test(input,expect,478))

    def test_79(self):
        input = """
        Class normal{
            Val a,b: Float = 3,4;
            Val c,d: Int = 4 ,5;
            sub(a,b:Float){
                Return a-b;
            }
        }
        Class Program{
            main(){
                Var a: Float;
                a = 1.0 + normal1.sub1(1,1);
            }
        }
        """
        expect = "Undeclared Identifier: normal1"
        self.assertTrue(TestChecker.test(input,expect,479))

    def test_80(self):
        input = """
        Class normal{
            Val a,b: Int = 3,4;
            Val $c,d: Int = 4,5;
        }
        Class Program{
            main(){
                Var a: Boolean;
                Var res: Float;
                res = 1.0 + normal.a;
            }
        }
        """
        expect = "Illegal Member Access: FieldAccess(Id(normal),Id(a))"
        self.assertTrue(TestChecker.test(input,expect,480))

    def test_81(self):
        input = """
        Class normal{
            Var a,$b: Int = 3,4;
            Val c,d: Int = 4,5;
            main(){
                a= a+$b+c;
            }
        }
        Class Program{
            main(){
                Var res: Float;
                res = 1.0 + normal::$b;
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,481))

    def test_82(self):
        input = """
        Class normal{
            Var a,b,$b: Int = 3,4,5;
            Val c,d: Int = 4,5;
            main(){
                a= a+$b+c;
            }
        }
        Class Program{
            main(){
                Var res: Float;
                Var o : normal = New normal();
                res = normal::$b;
                res = 1.0 + o.b;
            }
        }
        """
        expect = "Illegal Member Access: FieldAccess(Id(o),Id(b))"
        self.assertTrue(TestChecker.test(input,expect,482))

    def test_83(self):
        input = """
        Class Program{
            main(){
                Var a: Array[Int,5] = Array(1,2,3,4,5);                
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,483))

    def test_84(self):
        input = """
        Class Program{
            main(){
                Var a: Array[Int,5] = Array(1,2,True,4,5);                
            }
        }
        """
        expect = "Illegal Array Literal: [IntLit(1),IntLit(2),BooleanLit(True),IntLit(4),IntLit(5)]"
        self.assertTrue(TestChecker.test(input,expect,484))

    def test_85(self):
        input = """
        Class Program{
            main(){
                Var a: Array[Int,5] = Array(1,2,3,4,5);
                a[1][2][3.0] = 2;                
            }
        }
        """
        expect = "Type Mismatch In Expression: ArrayCell(Id(a),[IntLit(1),IntLit(2),FloatLit(3.0)])"
        self.assertTrue(TestChecker.test(input,expect,485))

    def test_86(self):
        input = """
        Class Program{
            main(){
                Var a: Array[Int,5] = Array(1,2,3,4,5);
                a[1] = 2.0;                
            }
        }
        """
        expect = "Type Mismatch In Statement: AssignStmt(ArrayCell(Id(a),[IntLit(1)]),FloatLit(2.0))"
        self.assertTrue(TestChecker.test(input,expect,486))

    def test_87(self):
        input = """
        Class A{

        }
        Class Program{
            main(){
                Var a: A;
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,487))

    def test_88(self):
        input = """
        Class A{
            Constructor(a,b:Int){
                Return a+b;
            }
        }
        Class Program{
            main(){
                Var a: A = New A(1,2);
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,488))

    def test_89(self):
        input = """
        Class A{
            Constructor(a,b:Int){
                Return a+b;
            }
        }
        Class Program{
            main(){
                Var a: A = New A(1,2);
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,489))

    def test_90(self):
        input = """
        Class Program{
            main(){
                Var a: Array[Int,1] = Array(1);
                Var b: Array[Int,2] = Array(1,2);
                a = b;
            }
        }
        """
        expect = "Type Mismatch In Statement: AssignStmt(Id(a),Id(b))"
        self.assertTrue(TestChecker.test(input,expect,490))

    def test_91(self):
        input = """
        Class Program{
            main(){
                Var a: Array[Int,1] = Array(1);
                Var b: Array[Int,2] = Array(1,2);
                a[0][1] = b;
            }
        }
        """
        expect = "Type Mismatch In Expression: ArrayCell(Id(a),[IntLit(0),IntLit(1)])"
        self.assertTrue(TestChecker.test(input,expect,491))

    def test_92(self):
        input = """
        Class Program{
            main(){
                Var a: Array[Int,1] = Array(1);
                Var b: Int;
                a[0] = b;
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,492))
    
    def test_93(self):
        input = """
        Class Program{
            main(){
                Var a: Int ;
                Val b: Int = a;
                a = b;
            }
        }
        """
        expect = "Illegal Constant Expression: Id(a)"
        self.assertTrue(TestChecker.test(input,expect,493))

    def test_94(self):
        input = """
        Class Program{
            main(){
                Val a,b: Int = 1,2;
                Var c: Float = b;
                c = a + b;
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,494))

    def test_95(self):
        input = """
        Class Program{
            main(){
                Val a,b: Int = 1,2;
                Var c: Float = b;
                c = a + b;
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,495))

    def test_96(self):
        input = """
        Class Program{
            main(){
                Val a: Array[Array[Int,2],1] = Array(Array(2),Array(3));
                Var c: Array[Int,5] = Array(1,2,3,4,5);
                a[1] = c;
            }
        }
        """
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(a),ArrayType(1,ArrayType(2,IntType)),[[IntLit(2)],[IntLit(3)]])"
        self.assertTrue(TestChecker.test(input,expect,496))

    def test_97(self):
        input = """
        Class Program{
            main(){
                Val a: Array[Array[Int,2],1] = Array(Array(1,2));
                Var c: Array[Int,2] = Array(1,2);
                a[0] = c;
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,497))


    def test_98(self):
        input = """
        Class Program{
            main(){
                Val a: Array[Array[Int,2],2] = Array(Array(1,2),Array(2,3));
                Var c: Array[Int,5] = Array(1,2,3,4,5);
                a[1][2] = c[1];
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,498))

    def test_99(self):
        input = """
        Class Program{
            main(){
                Val a: Array[Array[Int,2],1] = Array(Array(2),Array(3));
                Var c: Array[Int,5] = Array(Array(1,2),Array(1));
                a[1] = c;
            }
        }
        """
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(a),ArrayType(1,ArrayType(2,IntType)),[[IntLit(2)],[IntLit(3)]])"
        self.assertTrue(TestChecker.test(input,expect,499))

    def test_100(self):
        input = """
        Class Program{
            main(){
                Val a: Array[Array[Int,2],2] = Array(Array(1,2),Array(1.2,True));
                Var c: Array[Int,5] = Array(1,2,3,4,5);
                a[1] = c;
            }
        }
        """
        expect = "Illegal Array Literal: [FloatLit(1.2),BooleanLit(True)]"
        self.assertTrue(TestChecker.test(input,expect,500))