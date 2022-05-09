grammar D96;
//1953028

@lexer::header {
from lexererr import *
}

options {
	language = Python3;
}


INT: 'Int';
FLOAT: 'Float';
STRING: 'String';
BOOLEAN: 'Boolean';
ARRAY: 'Array';
VOID: 'Void';
BREAK:'Break';
CONTINUE: 'Continue';
IF: 'If';
ELSEIF: 'Elseif'; 
ELSE: 'Else';
FOREACH: 'Foreach';
TRUE: 'True';
FALSE: 'False';
IN: 'In';
RETURN: 'Return';
NULL: 'Null';
CLASS: 'Class';
VAL: 'Val';
VAR: 'Var';
SELF: 'Self';
CONSTRUCTOR: 'Constructor';
DESTRUCTOR: 'Destructor';
NEW: 'New';
BY: 'By';


ADD: '+' ;
SUB: '-' ;
MUL: '*' ;
DIV: '/' ;
PERCENT: '%';
NOT: '!';
AND: '&&';
OR: '||' ;
EQUALOP: '==';
EQUAL: '=';
NOT_EQUALOP: '!=';
LESS_THAN: '<';
LESS_OR_EQUAL_THAN: '<=';
GREATER_THAN: '>';
GREATER_OR_EQUAL_THAN: '>=';
ATTR_ACCESS_OP: '::';
STRING_CONCAT: '+.';
EQUAL_STRING_OP: '==.';

SC: ',';

DOT: '.';

LB: '(';

RB: ')';

LP: '{';

RP: '}';

LS: '[';

RS: ']';

SEMI: ';';

COLON: ':';
//////////////////////////////////////////////////////////////////
///////////////////////// MAIN PROGRAM////////////////////////////
//////////////////////////////////////////////////////////////////

program: (classDecl)+ EOF;

//Class declaration
classDecl
	: CLASS ID (COLON ID)? LP (funcDecl | constructorFunc | destructorFunc | attributeDeclStmt)* RP
	;

//programClass: CLASS 'Program' LP classStmt* mainFunction? (classStmt)*  RP;

//classStmt: funcDecl | constructorFunc | destructorFunc | attributeDeclStmt;
//mainFunction: 'main' LB RB blockStmt;

constructorFunc: CONSTRUCTOR LB listDeclArgs? RB blockStmt;
destructorFunc: DESTRUCTOR LB RB blockStmt;

//Statements

stmt: assignStmt
    | returnStmt
    | varDecl
    | valDecl
    | funcDecl
    | ifElseStmt
    | forEachStmt
    | blockStmt
    | breakStmt
    | continueStmt
    | methodInvocationStmt
	;

assignStmt: exp (EQUAL exp)+ SEMI;
methodInvocationStmt: operands DOT ID LB listExps? RB SEMI
    | operands ATTR_ACCESS_OP DOLLAR_ID LB listExps? RB SEMI;
// An assignment statement assigns a value to a left hand side 
//which can be a scalar variable, an
// index expression. An assignment takes the following form:


//callStmt: mixedId LB listExps? RB SEMI;

returnStmt: RETURN exp? SEMI;

//If else statements
ifElseStmt: IF ifBodyStmt;
ifBodyStmt: LB exp RB blockStmt elseIfBody* elseBody? ;
elseIfBody: ELSEIF LB exp RB blockStmt;
elseBody: ELSE blockStmt;

//For/In statement
forEachStmt
	: FOREACH LB mixedId IN exp '..' exp (BY exp)? RB blockStmt
	;

//Block statement
blockStmt: LP stmt* RP; 

//Continue statement
continueStmt: CONTINUE SEMI;

//Break statement
breakStmt: BREAK SEMI;


//Function declare
funcDecl: mixedId LB listDeclArgs? RB blockStmt;

// Variable and constant declaration statement should be the same as the attribute in a class.
// Variable should start with the keyword Var while constant should start with the keyword Val.
// However, the static property of attribute cannot be applied to them so its name should not
// follow the dollar identifier rule.

attributeDeclStmt: (VAL|VAR) (declareWithoutAssign| declareWithAssign) SEMI;

//Mutable (can change over time)
varDecl: VAR (declareWithoutAssign| declareWithAssign) SEMI;

//Immutable (can't change over time)
valDecl: VAL (declareWithoutAssign| declareWithAssign) SEMI;
declareWithAssign
	: mixedId COLON varType EQUAL exp
	| mixedId SC declareWithAssign SC exp
	;
//Val a,b :Int = 1,2;
declareWithoutAssign: listMixedIds COLON varType ;

//Expression
//exp : NEW ID LB listExps? RB
//    | <assoc=right> (NOT | SUB) exp
//    | exp ( DIV | MUL | PERCENT ) exp
//    | exp ( ADD | SUB | OR | AND) exp
//    | operands ( EQUALOP | NOT_EQUALOP | GREATER_THAN | LESS_THAN | GREATER_OR_EQUAL_THAN | LESS_OR_EQUAL_THAN) operands
//    | operands ( STRING_CONCAT | EQUAL_STRING_OP ) operands
//    | operands
//	;



//fieldAccess: operands1 (DOT ID)+
//    | ID ( ATTR_ACCESS_OP DOLLAR_ID)+
//    ;
//
//methodInvocation: operands2 (DOT  ID LB listExps? RB)+
//    | ID (ATTR_ACCESS_OP DOLLAR_ID LB listExps? RB)+;

exp : exp1 (STRING_CONCAT | EQUAL_STRING_OP) exp1 | exp1;
exp1: exp1 ( OR | AND ) exp2 | exp2;
exp2: exp2 ( EQUALOP | NOT_EQUALOP | GREATER_THAN | LESS_THAN | GREATER_OR_EQUAL_THAN | LESS_OR_EQUAL_THAN ) exp3 | exp3;
exp3: exp3 ( ADD | SUB ) exp4 | exp4;
exp4: exp4 ( DIV | MUL | PERCENT) exp5
    | exp5;
exp5:  <assoc=right> (NOT | SUB) exp5 | exp6;
exp6: exp6 postfixArrayExp | operands;

postfixArrayExp: (LS exp RS)+ ;

operands:  operands DOT ID (LB listExps? RB)?| operands1;
operands1:  operands1 ATTR_ACCESS_OP DOLLAR_ID (LB listExps? RB)?| operands2;
operands2:  <assoc=right> NEW ID LB listExps? RB | operands3;
operands3: operands3 postfixArrayExp | operands4;
operands4: mixedId |operands5;
operands5: LB exp RB | operands6;
operands6: literal;


///List of expression
listExps: exp (SC exp)* ;

//listExp1s: exp1 (SC exp1)* ;

listIds: ID (SC ID)* ;

//list_dollar_id: DOLLAR_ID (SC DOLLAR_ID)* ;

mixedId: ID| DOLLAR_ID;
listMixedIds: mixedId (SC mixedId)*;

listDeclArgs: listIds COLON varType (SEMI listIds COLON varType)*;


//3.2
// comment_block: COMMENT_BLOCK ;
COMMENT_BLOCK: ([#][#] .*? ([#][#])) ->skip;

//3.7 Data types
varType
	: INT
	| FLOAT
	| STRING
	| BOOLEAN
	| arrayType
	| ID
	| VOID
	;
//Array[Int,5]
arrayType: ARRAY LS varType SC intLit RS;
// {y=str(self.text)
// size_num=y.split(',')[1].split(']')[0]
// if size_num=='0':
// 	raise ErrorToken(self.text)
// };

literal
	: intLit | FLOATLIT | booleanLit | STRINGLIT
	| indexedArray | multiDimensionArray
	| NULL
	| SELF
	;

// 3.3
intLit
 	: (INT_DEC
	| INT_OCT
	| INT_HEX
	| INT_BIN
	 )
	;
INT_OCT: [0][0-7_]+{self.text = self.text.replace("_", "")};
INT_HEX: ('0x'|'0X') [0-9A-F_]+{self.text = self.text.replace("_", "")};
INT_BIN: ('0b'|'0B') [0-1_]+{self.text = self.text.replace("_", "")};
INT_DEC: ( [1-9][0-9_]*| '0'){self.text = self.text.replace("_", "")};
FLOATLIT
	:(INT_DEC? DOT [0-9]* EXPONENT? // 1.5(e-4)
	| INT_DEC EXPONENT // 12e-5
	){self.text = self.text.replace("_", "")}
	;

fragment EXPONENT: [eE] SIGN? INT_DEC ;
fragment DIGIT: [0-9] ;
fragment SIGN: ADD | SUB ;


booleanLit: TRUE | FALSE;

indexedArray
	: ARRAY LB listExps? RB
	;

multiDimensionArray
	: ARRAY LB (indexedArray SC)* indexedArray RB
	;

ID: [a-zA-Z_][a-zA-Z0-9_]* ;
DOLLAR_ID: '$' [a-zA-Z0-9_]+;
WS: [ \t\r\n]+ -> skip; // skip spaces, tabs, newlines

fragment STR_CHAR: [\b\t\f\r\na-zA-Z0-9,-.():<>?_=+!@#$%^&*/|;' ] | [']["] | '\\ ';
// fragment STR_CHAR: ~["\\] | [\b\t\f\r\n];
fragment ESC_ILLEGAL: '\\' [a-zA-Z"'\\] ;
///still in progress'
STRINGLIT: '"' STR_CHAR* '"'
	{
		y = str(self.text)
		if y.find('\'') != -1:
			pos = y.find('\'')
			if y[pos+1] != "\"":
				raise ErrorToken('\'')
		self.text = y[1:-1]
	}
	;
UNCLOSE_STRING: ["] STR_CHAR* ('\\n' | EOF)
{
	y = str(self.text)
	raise UncloseString(y[1:])
}
;
ILLEGAL_ESCAPE: ["] STR_CHAR* ESC_ILLEGAL
{
	y = str(self.text)
	raise IllegalEscape(y[1:])
}
;
ERROR_CHAR: .{raise ErrorToken(self.text)};

