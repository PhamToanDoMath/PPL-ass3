import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):
    
    # def test_simple(self):
    #     input = """
    #     Class Program{
    #         main(){}
    #     }
    #     """
    #     expect = "[]"
    #     self.assertTrue(TestChecker.test(input,expect,400))
    
    # def test_1(self):
    #     input = """
    #     Class Normal{

    #     }
    #     Class Normal{

    #     }
    #     Class Program{
    #         main(){

    #         }
    #     }
    #     """
    #     expect = "Redeclared Class: Normal"
    #     self.assertTrue(TestChecker.test(input,expect,401))

    # def test_2(self):
    #     input = """

    #     Class Normal{
    #         Var a,b,c:Int;
    #         function(a:Int;b:Float){
    #             Val a:Int;
    #         }
    #     }
    #     Class Program{
    #         main(){

    #         }  
    #     }
    #     """
    #     expect = "Redeclared Constant: a"
    #     self.assertTrue(TestChecker.test(input,expect,402))

    # def test_3(self):
    #     input = """
    #     Class Normal{
    #         Var a:Int;
    #         function(){
    #             Var b,c: Int;
    #             b = a;
    #         }
    #         another_function(a:Int;b:Float){
    #             Var c: Float;
    #             b = a + c + 1.01;
    #         }
    #     }
    #     Class Program{
    #         main(){

    #         }  
    #     }
    #     """
    #     expect = "[]"
    #     self.assertTrue(TestChecker.test(input,expect,403))

    # def test_4(self):
    #     input = """
    #     Class Program{
    #         main(){
    #             Var a,c:Int;
    #             Var b:Float = 1;
    #             b = 1 + 2 + c + a;
    #         }  
    #     }
    #     """
    #     expect = "[]"
    #     self.assertTrue(TestChecker.test(input,expect,404))

    # def test_5(self):
    #     input = """
    #     Class Normal{
    #         Var a:Int;
    #         function(){
    #             Var b,c:Int;
    #             b = a;
    #         }
    #         another_function(a:Int;b:Float){
    #             Var c: Float;
    #             Var a:Int;
    #             b = a + c + 1.01;
    #         }
    #     }
    #     Class Program{
    #         main(){

    #         }  
    #     }
    #     """
    #     expect = "Redeclared Variable: a"
    #     self.assertTrue(TestChecker.test(input,expect,405))

    # def test_6(self):
    #     input = """
    #     Class Normal{
    #         another_function(a:Int;b,a:Float){
    #             Var c: Float;
    #             Var a:Int;
    #             b = a + c + 1.01;
    #         }
    #     }
    #     Class Program{
    #         main(){

    #         }  
    #     }
    #     """
    #     expect = "Redeclared Parameter: a"
    #     self.assertTrue(TestChecker.test(input,expect,406))

    # def test_7(self):
    #     input = """
    #     Class Normal{
    #         another_function(a:Int;b:Float){
    #         }
    #     }
    #     Class Program{
    #         main(){
    #             Var b:Boolean = 1.72;
    #         }  
    #     }
    #     """
    #     expect = "Type Mismatch In Statement: VarDecl(Id(b),BoolType,FloatLit(1.72))"
    #     self.assertTrue(TestChecker.test(input,expect,407))

    # def test_8(self):
    #     input = """
    #     Class Normal{
    #         Var a: Bool = 1;
    #         another_function(a:Int;b:Float){
    #             b = a + c + 1.01;
    #             a = 1.1;
    #         }
    #     }
    #     Class Program{
    #         main(){

    #         }  
    #     }
    #     """
    #     expect = "Type Mismatch In Statement: VarDecl(Id(a),ClassType(Id(Bool)),IntLit(1))"
    #     self.assertTrue(TestChecker.test(input,expect,408))

    # def test_9(self):
    #     input = """
    #     Class Normal{
    #         another_function(a:Int;b:Float){
    #         }
    #     }
    #     Class Program{
    #         main(){
    #             Val b:Boolean = 1.72;
    #         }  
    #     }
    #     """
    #     expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(b),BoolType,FloatLit(1.72))"
    #     self.assertTrue(TestChecker.test(input,expect,409))

    # def test_10(self):
    #     input = """
    #     Class Normal{
    #         Val b: Boolean = 1.72;
    #         another_function(a:Int;b:Float){
    #         }
    #     }
    #     Class Program{
    #         main(){
    #             Var a:Float;
    #         }  
    #     }
    #     """
    #     expect = "Type Mismatch In Constant Declaration: AttributeDecl(ConstDecl(Id(b),BoolType,FloatLit(1.72)))"
    #     self.assertTrue(TestChecker.test(input,expect,410))
    
    # def test_11(self):
    #     input = """
    #     Class Normal{
    #         another_function(a:Int){
    #             Var a:Float;
    #         }
    #     }
    #     Class Program{
    #         main(){
    #         }  
    #     }
    #     """
    #     expect = "Redeclared Variable: a"
    #     self.assertTrue(TestChecker.test(input,expect,411))

    # def test_12(self):
    #     input = """
    #     Class Normal{
    #         another_function(){
    #             Var a:Float;
    #         }
    #         another_function(){
    #             Var a:Float;
    #         }
    #     }
    #     Class Program{
    #         main(){
    #         }  
    #     }
    #     """
    #     expect = "Redeclared Method: another_function"
    #     self.assertTrue(TestChecker.test(input,expect,412))

    # def test_13(self):
    #     input = """
    #     Class Program{
    #         main(){
    #         }  
    #     }
    #     """
    #     expect = "[]"
    #     self.assertTrue(TestChecker.test(input,expect,413))

    # def test_14(self):
    #     input = """
    #     Class Program{
    #         main(a:Int){
    #         }
    #     }
    #     """
    #     expect = "No Entry Point"
    #     self.assertTrue(TestChecker.test(input,expect,414))

    # def test_15(self):
    #     input = """
    #     Class normal{
    #         Var a: Int = -5.0;
    #     }
    #     Class Program{
    #         main(){
    #             Var b: Boolean = 1 == 2;
    #         }
    #     }
    #     """
    #     expect = "Type Mismatch In Statement: AttributeDecl(VarDecl(Id(a),IntType,FloatLit(5.0)))"
    #     self.assertTrue(TestChecker.test(input,expect,415))
    
    # def test_16(self):
    #     input = """
    #     Class normal{
    #     }
    #     Class Program{
    #         main(){
    #             Var b: String = 1 +. "as";
    #         }
    #     }
    #     """
    #     expect = "Type Mismatch In Expression: BinaryOp(+.,IntLit(1),StringLit(as))"
    #     self.assertTrue(TestChecker.test(input,expect,416))

    # def test_17(self):
    #     input = """
    #     Class normal{
    #     }
    #     Class Program{
    #         main(){
    #             Var a: Int = 0;
    #             Foreach(a In 1 .. 9 By 3){
    #                 Continue;
    #             }
    #         }
    #     }
    #     """
    #     expect = "[]"
    #     self.assertTrue(TestChecker.test(input,expect,417))


    # def test_18(self):
    #     input = """
    #     Class normal{
    #     }
    #     Class Program{
    #         main(){
    #             Break;
    #             Var a: Int = 0;
    #             Foreach(a In 1 .. 9 By 3){
    #             }
    #         }
    #     }
    #     """
    #     expect = "Break Not In Loop"
    #     self.assertTrue(TestChecker.test(input,expect,418))

    # def test_19(self):
    #     input = """
    #     Class normal{
    #     }
    #     Class Program{
    #         main(){
    #             Var a,b: Int = 0,1;
    #             Var c : Boolean; 
    #             If(1){
    #                 c = (1 + 3) == 1;
    #             }Else{
    #                 c = (1 + 3) == 2;
    #             }
    #         }
    #     }
    #     """
    #     expect = "Type Mismatch In Statement: If(IntLit(1),Block([AssignStmt(Id(c),BinaryOp(==,BinaryOp(+,IntLit(1),IntLit(3)),IntLit(1)))]),Block([AssignStmt(Id(c),BinaryOp(==,BinaryOp(+,IntLit(1),IntLit(3)),IntLit(2)))]))"
    #     self.assertTrue(TestChecker.test(input,expect,419))

    # def test_20(self):
    #     input = """
    #     Class normal{
    #         sub(a,b:Int){
    #             a = a+b;
    #         }
    #     }
    #     Class Program{
    #         main(){
    #             Var a: Int = 0;
    #             Var b : Boolean;
    #             normal.sub(1,2);
    #         }
    #     }
    #     """
    #     expect = "[]"
    #     self.assertTrue(TestChecker.test(input,expect,420))

    # def test_21(self):
    #     input = """
    #     Class normal{
    #         Val a,b: Float = 3,4;
    #         Val c,d: Int = 4 ,5;
    #         sub(a,b:Int){
    #             Return a- b ;
    #         }
    #     }
    #     Class Program{
    #         main(){
    #             Val a: Int = 1;
    #             a = normal.sub(1,1);
    #         }
    #     }
    #     """
    #     expect = "[]"
    #     self.assertTrue(TestChecker.test(input,expect,421))

    # def test_22(self):
    #     input = """
    #     Class normal{
    #         sub(a,b:Int){
    #             Return a-b;
    #         }
    #     }
    #     Class Program{
    #         main(){
    #             normal.sub(1,1);
    #         }
    #     }
    #     """
    #     expect = "Type Mismatch In Statement: Call(Id(normal),Id(sub),[IntLit(1),IntLit(1)])"
    #     self.assertTrue(TestChecker.test(input,expect,422))

    # def test_23(self):
    #     input = """
    #     Class normal{
    #         sub(a,b:Int){
    #             Return a-b;
    #         }
    #     }
    #     Class Program{
    #         main(){
    #             Var a: Float;
    #             a = 1.0 + normal.sub(1,1);
    #         }
    #     }
    #     """
    #     expect = "[]"
    #     self.assertTrue(TestChecker.test(input,expect,423))

    # def test_24(self):
    #     input = """
    #     Class normal{
    #         Val a,b: Float = 3,4;
    #         Val c,d: Int = 4 ,5;
    #         sub(a,b:Float){
    #             Return a-b;
    #         }
    #     }
    #     Class Program{
    #         main(){
    #             Var a: Float;
    #             a = 1.0 + normal.sub(1,1);
    #         }
    #     }
    #     """
    #     expect = "[]"
    #     self.assertTrue(TestChecker.test(input,expect,424))

    # def test_25(self):
    #     input = """
    #     Class normal{
    #         Val a,b: Float = 3,4;
    #         Val c,d: Int = 4 ,5;
    #         sub(a,b:Float){
    #             Return a-b;
    #         }
    #     }
    #     Class Program{
    #         main(){
    #             Var a: Float;
    #             a = 1.0 + normal.sub1(1,1);
    #         }
    #     }
    #     """
    #     expect = "Undeclared Method: sub1"
    #     self.assertTrue(TestChecker.test(input,expect,425))

    # def test_26(self):
    #     input = """
    #     Class normal{
    #         Val a,b: Float = 3,4;
    #         Val c,d: Int = 4 ,5;
    #         sub(a,b:Float){
    #             Return a-b;
    #         }
    #     }
    #     Class Program{
    #         main(){
    #             Var a: Float;
    #             a = 1.0 + normal1.sub1(1,1);
    #         }
    #     }
    #     """
    #     expect = "Undeclared Identifier: normal1"
    #     self.assertTrue(TestChecker.test(input,expect,426))

    # def test_27(self):
    #     input = """
    #     Class normal{
    #         Val a,b: Float = 3,4;
    #         Val c,d: Int = 4 ,5;
    #         sub(a,b:Float){
    #             a = a-b;
    #         }
    #     }
    #     Class Program{
    #         main(){
    #             Var a: Float;
    #             normal.sub1(1,1);
    #         }
    #     }
    #     """
    #     expect = "Undeclared Method: sub1"
    #     self.assertTrue(TestChecker.test(input,expect,427))

    # def test_28(self):
    #     input = """
    #     Class normal{
    #         Val a,b: Float = 3,4;
    #         Val c,d: Int = 4 ,5;
    #         sub(a,b:Float){
    #             Return a-b;
    #         }
    #     }
    #     Class Program{
    #         main(){
    #             Var a: Float;
    #             a = 1.0 + normal1.sub1(1,1);
    #         }
    #     }
    #     """
    #     expect = "Undeclared Identifier: normal1"
    #     self.assertTrue(TestChecker.test(input,expect,428))

    # def test_29(self):
    #     input = """
    #     Class normal{
    #         Val a,b: Int = 3,4;
    #         Val $c,d: Int = 4,5;
    #     }
    #     Class Program{
    #         main(){
    #             Var a: Boolean;
    #             Var res: Float;
    #             res = 1.0 + normal.a;
    #         }
    #     }
    #     """
    #     expect = "Illegal Member Access: FieldAccess(Id(normal),Id(a))"
    #     self.assertTrue(TestChecker.test(input,expect,429))

    # def test_30(self):
    #     input = """
    #     Class normal{
    #         Val a,$b: Int = 3,4;
    #         Val c,d: Int = 4,5;
    #         main(){
    #             a= a+$b+c;
    #         }
    #     }
    #     Class Program{
    #         main(){
    #             Var res: Float;
    #             res = 1.0 + normal::$b;
    #         }
    #     }
    #     """
    #     expect = "[]"
    #     self.assertTrue(TestChecker.test(input,expect,430))

    # def test_31(self):
    #     input = """
    #     Class normal{
    #         Val a,b,$b: Int = 3,4,5;
    #         Val c,d: Int = 4,5;
    #         main(){
    #             a= a+$b+c;
    #         }
    #     }
    #     Class Program{
    #         main(){
    #             Var res: Float;
    #             res = normal::$b;
    #             res = 1.0 + normal.b;
    #         }
    #     }
    #     """
    #     expect = "Illegal Member Access: FieldAccess(Id(normal),Id(b))"
    #     self.assertTrue(TestChecker.test(input,expect,431))

    # def test_32(self):
    #     input = """
    #     Class Program{
    #         main(){
    #             Var a: Array[Int,5] = Array(1,2,3,4,5);                
    #         }
    #     }
    #     """
    #     expect = "[]"
    #     self.assertTrue(TestChecker.test(input,expect,432))

    # def test_33(self):
    #     input = """
    #     Class Program{
    #         main(){
    #             Var a: Array[Int,5] = Array(1,2,True,4,5);                
    #         }
    #     }
    #     """
    #     expect = "Illegal Array Literal: [IntLit(1),IntLit(2),BooleanLit(True),IntLit(4),IntLit(5)]"
    #     self.assertTrue(TestChecker.test(input,expect,433))
    
    # def test_33(self):
    #     input = """
    #     Class Program{
    #         main(){
    #             Var a: Array[Int,5] = Array(1,2,3,4,5);
    #             a[1][2][3] = 2;                
    #         }
    #     }
    #     """
    #     expect = "[]"
    #     self.assertTrue(TestChecker.test(input,expect,433))

    # def test_34(self):
    #     input = """
    #     Class Program{
    #         main(){
    #             Var a: Array[Int,5] = Array(1,2,3,4,5);
    #             a[1][2][3.0] = 2;                
    #         }
    #     }
    #     """
    #     expect = "Type Mismatch In Expression: ArrayCell(Id(a),[IntLit(1),IntLit(2),FloatLit(3.0)])"
    #     self.assertTrue(TestChecker.test(input,expect,434))

    def test_35(self):
        input = """
        Class Program{
            main(){
                Var a: Array[Int,5] = Array(1,2,3,4,5);
                Var b: Array[Int,4] = Array(1,2,3,4);
                a = b;                
            }
        }
        """
        expect = "Type Mismatch In Statement: AssignStmt(ArrayCell(Id(a),[IntLit(1),IntLit(2),IntLit(3)]),FloatLit(2.0))"
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
        }
        Class Program{
            main(){
                Var a: A = New A(1,2);
            }
        }
        """
        expect = "Type Mismatch In Expression: NewExpr(Id(A),[IntLit(1),IntLit(2)])"
        self.assertTrue(TestChecker.test(input,expect,438))